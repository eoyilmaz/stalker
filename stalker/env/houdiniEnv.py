# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of oyProjectManager and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import os
import hou
import re
from oyProjectManager import utils
from oyProjectManager.models.asset import Asset
from oyProjectManager.models.entity import EnvironmentBase
from oyProjectManager.models.project import Project
from oyProjectManager.models.repository import Repository
from oyProjectManager.models.sequence import Sequence
from oyProjectManager.models.version import Version

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Houdini(EnvironmentBase):
    """the houdini environment class
    """

    name = 'Houdini'
    
    def save_as(self, version):
        """the save action for houdini environment
        """
        
        if not version:
            return
        
        # set the extension to hip
        assert isinstance(version, Version)
        version.extension = 'hip'
        
        # create the folder if it doesn't exists
        try:
            os.makedirs(
                os.path.dirname(
                    version.full_path
                )
            )
        except OSError:
            # dirs exist
            pass
        
        # houdini uses / instead of \ under windows
        # lets fix it
        
        # *************************************************************
        # trying to set the render file name while the file has not been
        # saved before creates an error
        # so save the file two times if it is not saved before
        
        ## check if the HIP environment variable has some data
        #if os.environ["HIP"] == os.environ["HOME"]:
        # save the file to create a meaningful HIP variable
        hou.hipFile.save(file_name=str(version.full_path))
        
        # set the environment variables
        self.set_environment_variables(version)
        
        # set the render file name
        self.set_render_filename(version)
        
        # houdini accepts only strings as file name, no unicode support as I
        # see
        hou.hipFile.save(file_name=str(version.full_path))
        
        # set the environment variables
        self.set_environment_variables(version)
        
        return True
    
    def open_(self, version, force=False):
        """the open action for houdini environment
        """
        if not version:
            return
        
        if hou.hipFile.hasUnsavedChanges() and not force:
            raise RuntimeError
        
        hou.hipFile.load(
            file_name=str(version.full_path),
            suppress_save_prompt=True
        )
        
        # set the environment variables
        self.set_environment_variables(version)
        
        return True, []

    def post_open(self, version):
        """just skip it
        """
        return
    
    def import_(self, version):
        """the import action for houdini environment
        """
        hou.hipFile.merge(str(version.fullPath))
        return True

    def get_current_version(self):
        """Returns the currently opened Version instance
        """
        version = None
        full_path = hou.hipFile.name()
        if full_path != 'untitled.hip':
            version = self.get_version_from_full_path(full_path)
        return version

    def get_version_from_recent_files(self):
        """returns the version from the recent files
        """
        version = None
        recent_files = self.get_recent_file_list()
        for i in range(len(recent_files)-1,0,-1):
            version = self.get_version_from_full_path(recent_files[i])
            if version:
                break
        return version
    
    def get_last_version(self):
        """gets the file name from houdini environment
        """

        version = self.get_current_version()

        if version is None:
            # read the recent file list
            version = self.get_version_from_recent_files()

        #if version is None:
        #    # get the latest possible version instance by using the project path

        return version
    
    def set_environment_variables(self, version):
        """sets the environment variables according to the given Version
        instance
        """

        if not version:
            return
        
        # set the $JOB variable to the parent of version.full_path
        logger.debug('version: %s' % version)
        logger.debug('version.path: %s' % version.path)
        logger.debug('version.filename: %s' % version.filename)
        logger.debug('version.full_path: %s' % version.full_path)
        logger.debug('version.full_path (calculated): %s' %
                     os.path.join(
                         version.path,
                         version.filename
                         ).replace("\\", "/")
        )
        job = os.path.dirname(str(version.full_path))
        
        logger.debug('job: %s' % job)
        
        # update the environment variables
        #os.environ.update({"JOB": job})
        os.environ["JOB"] = job
        
        # also set it using hscript, hou is a little bit problematic
        hou.hscript("set -g JOB = '" + job + "'")
        try:
            hou.allowEnvironmentVariableToOverwriteVariable("JOB", True)
        except AttributeError:
            # should be Houdini 12
            hou.allowEnvironmentToOverwriteVariable('JOB', True)
    
    def get_recent_file_list(self):
        """returns the recent HIP files list from the houdini
        """
        # use a FileHistory object
        fHist = FileHistory()
        
        # get the hip files list
        return fHist.get_recent_files('HIP')
    
    def get_frame_range(self):
        """returns the frame range of the
        """
        # use the hscript commands to get the frame range
        timeInfo = hou.hscript('tset')[0].split('\n')
        
        pattern = r'[-0-9\.]+'
        
        start_frame = int(
            hou.timeToFrame(
                float(re.search(pattern, timeInfo[2]).group(0))
            )
        )
        duration = int(re.search(pattern, timeInfo[0]).group(0))
        end_frame = start_frame + duration - 1
        
        return start_frame, end_frame
    
    def set_frame_range(self, start_frame=1, end_frame=100, adjust_frame_range=False):
        """sets the frame range
        """
        # --------------------------------------------
        # set the timeline
        current_frame = hou.frame()
        if current_frame < start_frame:
            hou.setFrame(start_frame)
        elif current_frame > end_frame:
            hou.setFrame(end_frame)
        
        # for now use hscript, the python version is not implemented yet
        hou.hscript(
            'tset `('+ str(start_frame) +'-1)/$FPS` `'+ str(end_frame)+'/$FPS`'
        )
        
        # --------------------------------------------
        # Set the render nodes frame ranges if any
        # get the out nodes
        output_nodes = self.get_output_nodes()
        
        for output_node in output_nodes:
            output_node.setParms(
                    {'trange':0,'f1':start_frame,'f2':end_frame,'f3':1}
            )
    
    def get_output_nodes(self):
        """returns the rop nodes in the scene
        """
        ropContext = hou.node('/out')
        
        # get the children
        outNodes = ropContext.children()
        
        exclude_node_types = [
            hou.nodeType(hou.nodeTypeCategories()["Driver"], "wedge")
        ]
        
        # remove nodes in type in exclude_node_types list
        new_out_nodes = [node for node in outNodes
                         if node.type() not in exclude_node_types]
        
        return new_out_nodes
    
    def get_fps(self):
        """returns the current fps
        """
        return int(hou.fps())
    
    def set_render_filename(self, version):
        """sets the render file name
        """
        render_output_folder = version.output_path
        base_name = version.base_name
        take_name = version.take_name
        version_string = 'v%03d' % version.version_number
        user_initials = version.created_by.initials
        
        output_filename = os.path.join(
            render_output_folder, "`$OS`",
            base_name + "_" + take_name + "_`$OS`_" +
            version_string + "_" + user_initials + ".$F4.exr"
        )
        
        output_filename = output_filename.replace('\\','/')
        
        # compute a $JOB relative file path
        # which is much safer if the file is going to be render in multiple OSes
        # $HIP = the current asset path
        # $JOB = the current sequence path
        #hip = self._asset.path
        #hip = hou.getenv("HIP")
        job = hou.getenv("JOB")
        # eliminate environment vars
        while "$" in job:
            job = os.path.expandvars(job)
        
        job_relative_output_file_path = "$JOB/" + utils.relpath(
            job, output_filename, "/", ".."
        )
        
        output_nodes = self.get_output_nodes()
        for output_node in output_nodes:
            # get only the ifd nodes for now
            if output_node.type().name() == 'ifd':
                # set the file name
                try:
                    output_node.setParms(
                        {'vm_picture': str(job_relative_output_file_path)}
                    )
                except hou.PermissionError:
                    # node is locked
                    pass
                
                # set the compression to zips (zip, single scanline)
                output_node.setParms({"vm_image_exr_compression": "zips"})
                
                # also create the folders
                output_file_full_path = output_node.evalParm('vm_picture')
                output_file_path = os.path.dirname(output_file_full_path)
                
                flat_output_file_path = output_file_path
                while "$" in flat_output_file_path:
                    flat_output_file_path = os.path.expandvars(
                        flat_output_file_path
                    )
                
                try:
                    os.makedirs(flat_output_file_path)
                except OSError:
                    # dirs exists
                    pass
    
    def set_fps(self, fps=25):
        """sets the time unit of the environment
        """
        if fps <= 0:
            return
        
        # keep the current start and end time of the time range
        start_frame, end_frame = self.get_frame_range()
        hou.setFps(fps)
        
        self.set_frame_range(start_frame, end_frame)
    
    def replace_paths(self):
        """replaces all the paths in all the path related nodes
        """
        # get all the nodes and their childs and
        # try to get string and file path parameters
        # and replace them if they contain absolute paths
        pass

class FileHistory(object):
    """A Houdini recent file history parser
    
    Holds the data in a dictionary, where the keys are the file types and the
    values are string list of recent file paths of that type
    """
    
    def __init__(self):
        self._history_file_name = 'file.history'
        self._history_file_path = ''
        
        if os.name == 'nt':
            # under windows the HIH is useless
            # interpret the HIH from POSE environment variable
            self._history_file_path = os.path.dirname( os.getenv('POSE') )
        else:
            self._history_file_path = os.getenv('HIH')
        
        self._history_file_full_path = os.path.join(
            self._history_file_path,
            self._history_file_name
        )
        
        self._buffer =  []
        
        self._history = dict()
        
        self._read()
        self._parse()
    
    def _read(self):
        """reads the history file to a buffer
        """
        try:
            history_file = open( self._history_file_full_path )
        except IOError:
            self._buffer = []
            return
        
        self._buffer = history_file.readlines()
        
        # strip all the lines
        self._buffer = [ line.strip() for line in self._buffer ]
        
        history_file.close()
    
    def _parse(self):
        """parses the data in self._buffer
        """
        self._history = dict()
        buffer_list = self._buffer
        key_name = ''
        path_list = []
        len_buffer = len(buffer_list)
        
        for i in range(len_buffer):
            # try to find a '{'
            if buffer_list[i] == '{':
                # create a key with the previous line
                key_name = buffer_list[i-1]
                path_list = []
                
                # starting from the next line
                for j in range(i+1, len_buffer):
                    
                    # add all the lines to the path_list until you find a '}'
                    current_element = buffer_list[j]
                    if  current_element != '}':
                        path_list.append(current_element)
                    else:
                        # set i to j+1 and let it continue
                        i = j + 1
                        break
                # append the key and data to the dictionary
                self._history[key_name] = path_list
    
    def get_recent_files(self, type_name=''):
        """returns the file list of the given file type
        """
        if type_name == '' or type_name is None:
            return []
        else:
            return self._history.get(type_name, [])
