# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of oyProjectManager and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import os
import platform

import jinja2

import nuke
from oyProjectManager import utils
from oyProjectManager.models.entity import EnvironmentBase


class Nuke(EnvironmentBase):
    """the nuke environment class
    """
    
    name = "Nuke"
    
    def __init__(self, version=None, name='', extensions=None):
        """nuke specific init
        """
#        # call the supers __init__
#        super(Nuke, self).__init__(asset, name, extensions)
        
        # and add you own modifications to __init__
        # get the root node
        self._root = self.get_root_node()
        
        self._main_output_node_name = "MAIN_OUTPUT"
    
    
    def get_root_node(self):
        """returns the root node of the current nuke session
        """
        return nuke.toNode("root")
    
    def save_as(self, version):
        """"the save action for nuke environment
        
        uses Nukes own python binding
        """
        
        # set the extension to '.nk'
        version.extension = '.nk'
        
        # set project_directory
        self.project_directory = os.path.dirname(version.path)
        
        # create the main write node
        self.create_main_write_node(version)
        
        # replace read and write node paths
        self.replace_external_paths()
        
        # create the path before saving
        try:
            os.makedirs(version.path)
        except OSError:
            # path already exists OSError
            pass

        # set frame range
        if version.type.type_for == 'Shot':
            self.set_frame_range(
                version.version_of.start_frame,
                version.version_of.end_frame
            )
        
        nuke.scriptSaveAs(version.full_path)
        
        return True
    
    def export_as(self, version):
        """the export action for nuke environment
        """
        # set the extension to '.nk'
        version.extension = '.nk'
        nuke.nodeCopy(version.fullPath)
        return True
    
    def open_(self, version, force=False):
        """the open action for nuke environment
        """
        nuke.scriptOpen(version.full_path)
        
        # set the project_directory
        self.project_directory = os.path.dirname(version.path)
        
        # TODO: file paths in different OS'es should be replaced with the current one
        # Check if the file paths are starting with a string matching one of the
        # OS'es project_directory path and replace them with a relative one
        # matching the current OS 
        
        # replace paths
        self.replace_external_paths()
        
        # return True to specify everything was ok and an empty list
        # for the versions those needs to be updated
        return True, []

    def post_open(self, version):
        """the post open action for the nuke environment
        """
        pass
    
    def import_(self, version):
        """the import action for nuke environment
        """
        nuke.nodePaste(version.full_path)
        return True

    def get_current_version(self):
        """Finds the Version instance from the current open file.
        
        If it can't find any then returns None.
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        full_path = self._root.knob('name').value()
        return self.get_version_from_full_path(full_path)
    
    def get_version_from_recent_files(self):
        """It will try to create a
        :class:`~oyProjectManager.models.version.Version` instance by looking at
        the recent files list.
        
        It will return None if it can not find one.
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        # use the last file from the recent file list
        i = 1
        while True:
            try:
                full_path = nuke.recentFile(i)
            except RuntimeError:
                # no recent file anymore just return None
                return None
            i += 1
            
            version = self.get_version_from_full_path(full_path)
            if version is not None:
                return version
    
    def get_version_from_project_dir(self):
        """Tries to find a Version from the current project directory
        
        :return: :class:`~oyProjectManager.models.version.Version`
        """
        versions = self.get_versions_from_path(self.project_directory)
        version = None
        
        if versions:
            version = versions[0]
        
        return version
    
    def get_last_version(self):
        """gets the file name from nuke
        """
        version = self.get_current_version()
        
        # read the recent file list
        if version is None:
            version = self.get_version_from_recent_files()

        # get the latest possible Version instance by using the workspace path
        if version is None:
            version = self.get_version_from_project_dir()

        return version
    
    def get_frame_range(self):
        """returns the current frame range
        """
        #self._root = self.get_root_node()
        startFrame = int(self._root.knob('first_frame').value())
        endFrame = int(self._root.knob('last_frame').value())
        return startFrame, endFrame
    
    def set_frame_range(self, start_frame=1, end_frame=100,
                        adjust_frame_range=False):
        """sets the start and end frame range
        """
        self._root.knob('first_frame').setValue(start_frame)
        self._root.knob('last_frame').setValue(end_frame)
    
    def set_fps(self, fps=25):
        """sets the current fps
        """
        self._root.knob('fps').setValue(fps)
    
    def get_fps(self):
        """returns the current fps
        """
        return int(self._root.knob('fps').getValue())
    
    def get_main_write_nodes(self):
        """Returns the main write node in the scene or None.
        """
        # list all the write nodes in the current file
	all_main_write_nodes = []
        for write_node in nuke.allNodes("Write"):
            if write_node.name().startswith(self._main_output_node_name):
                all_main_write_nodes.append(write_node)
        
        return all_main_write_nodes
    
    def create_main_write_node(self, version):
        """creates the default write node if there is no one created before.
        """
        
        # list all the write nodes in the current file
        main_write_nodes = self.get_main_write_nodes()

        # check if there is a write node or not
        if not len(main_write_nodes):
            # create one with correct output path
            main_write_node = nuke.nodes.Write()
            main_write_node.setName(self._main_output_node_name)
            main_write_nodes.append(main_write_node)
        
	for main_write_node in main_write_nodes:
            # set the output path
            output_file_name = ""
            
            if version.type.type_for == "Shot":
                output_file_name = version.project.code + "_"
                #output_file_name += version.version_of.sequence.code + "_"
            
            # get the output format
            output_format_enum = \
                main_write_node.knob('file_type').value().strip()
            if output_format_enum == '':
                # set it to png by default
                output_format_enum = 'png'
                main_write_node.knob('file_type').setValue(output_format_enum)
            elif output_format_enum == 'ffmpeg':
                output_format_enum = 'mov'

            output_file_name += \
                version.base_name + "_" + \
                version.take_name + "_" + \
                version.type.code + "_" + \
                "v%03d" % version.version_number
            
            if output_format_enum != 'mov':
              output_file_name += ".####." + output_format_enum
            else:
              output_file_name += '.' + output_format_enum
            
            # check if it is a stereo comp
            # if it is enable separate view rendering
            
            # set the output path
            output_file_full_path = os.path.join(
                version.output_path,
                output_format_enum,
                output_file_name
            ).replace("\\", "/")
            
            # create the path
            try:
                os.makedirs(os.path.dirname(output_file_full_path))
            except OSError:
                # path already exists
                pass

            # set the output file path
            main_write_node.knob("file").setValue(output_file_full_path)
    
    def replace_external_paths(self, mode=0):
        """replaces file paths with environment variable scripts
        """
        
        # TODO: replace file paths if project_directory changes
        # check if the project_directory is still the same
        # if it is do the regular replacement
        # but if it is not then expand all the paths to absolute paths
        
        # convert the given path to tcl environment script
        def repPath(path):
            return utils.relpath(self.project_directory, path, "/", "..")
        
        # get all read nodes
        allNodes = nuke.allNodes()
        
        readNodes = [node for node in allNodes if node.Class() == "Read"]
        writeNodes = [node for node in allNodes if node.Class() == "Write"]
        readGeoNodes = [node for node in allNodes if node.Class() == "ReadGeo"]
        readGeo2Nodes = [node for node in allNodes if node.Class() == "ReadGeo2"]
        writeGeoNodes = [node for node in allNodes if node.Class() == "WriteGeo"]
        
        def nodeRep(nodes):
            """helper function to replace path values
            """
            [node["file"].setValue(
                repPath(
                    os.path.expandvars(
                        os.path.expanduser(
                            node["file"].getValue()
                        )
                    ).replace('\\', '/')
                )
            ) for node in nodes]
        
        nodeRep(readNodes)
        nodeRep(writeNodes)
        nodeRep(readGeoNodes)
        nodeRep(readGeo2Nodes)
        nodeRep(writeGeoNodes)
    
    @property
    def project_directory(self):
        """The project directory.
        
        Set it to the project root, and set all your paths relative to this
        directory.
        """
        
        root = self.get_root_node()
        
        # TODO: root node gets lost, fix it
        # there is a bug in Nuke, the root node get lost time to time find 
        # the source and fix it.
#        if root is None:
#            # there is a bug about Nuke,
#            # sometimes it losses the root node, while it shouldn't
#            # I can't find the source
#            # so instead of using the root node,
#            # just return the os.path.dirname(version.path)
#            
#            return os.path.dirname(self.version.path)
        
        return root["project_directory"].getValue()
    
    @project_directory.setter
    def project_directory(self, project_directory_in):
        
        project_directory_in = project_directory_in.replace("\\", "/")
        
        root = self.get_root_node()
        root["project_directory"].setValue(project_directory_in)
    
    def create_slate_info(self):
        """Returns info about the current shot which will contribute to the
        shot slate
        
        :return: string
        """
        
        version = self.get_current_version()
        shot = version.version_of
        
        # create a jinja2 template
        template = jinja2.Template("""Show: {{shot.project.name}}
Shot: {{shot.number}}
Frame Range: {{shot.start_frame}}-{{shot.end_frame}}
Handles: +{{shot.handle_at_start}}, -{{shot.handle_at_end}}
Artist: {{version.created_by.name}}
Version: v{{'%03d'|format(version.version_number)}}
Status: WIP
        """)
        
        template_vars = {
            "shot": shot,
            "version": version
        }
        
        return template.render(**template_vars)
