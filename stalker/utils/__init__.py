# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of oyProjectManager and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


import os
import re
import itertools
import shutil
import glob

def all_equal(elements):
    """return True if all the elements are equal, otherwise False.
    """
    first_element = elements[0]
    
    for other_element in elements[1:]:
        if other_element != first_element: return False
    
    return True

def common_prefix(*sequences):
    """return a list of common elements at the start of all sequences, then a
    list of lists that are the unique tails of each sequence.
    """
    
    # if there are no sequences at all, we're done
    if not sequences: return[], []
    # loop in parallel on the sequences
    common = []
    for elements in itertools.izip(*sequences):
        # unless all elements are equal, bail out of the loop
        if not all_equal(elements): break
        
        # got one more common element, append it and keep looping
        common.append(elements[0])
    
    # return the common prefix and unique tails
    return common, [sequence[len(common):] for sequence in sequences]

def relpath(p1, p2, sep=os.path.sep, pardir=os.path.pardir):
    """return a relative path from p1 equivalent to path p2.
    
    In particular:
    
        the empty string, if p1 == p2;
        p2, if p1 and p2 have no common prefix.
    
    """
    # replace any trailing slashes at the end
    p1 = re.sub(r"[/]+$", "" , p1)
    p1 = re.sub(r"[\\]+$", "",  p1)
    
    common, (u1, u2) = common_prefix(p1.split(sep), p2.split(sep))
    if not common:
        return p2 # leave path absolute if nothing at all in common
    
    return sep.join([pardir]*len(u1) + u2 )

def abspath(p1, p2):
    """Converts the p2 to abspath by joining it with p1
    
    The output is always normalized, so for windows all the path separators
    will be backslashes where on other systems it will be forward slashes. 
    """

    if not os.path.isabs(p2):
        return os.path.normpath(os.path.join(p1, p2))
    
    return p2

def createFolder(folderPath):
    """utility method that creates a folder if it doesn't exists
    """
    exists = os.path.exists(folderPath)
    if not exists:
        os.makedirs(folderPath)
    return exists

def mkdir(path):
    """Creates a directory in the given path
    """
    try:
        os.makedirs(path)
    except OSError:
        pass

def unique(s):
    """ Return a list of elements in s in arbitrary order, but without
    duplicates.
    """
    # Try using a set first, because it's the fastest and will usually work
    try:
        return list(set(s))
    except TypeError:
        pass # Move on to the next method
    
    # Since you can't hash all elements, try sorting, to bring equal items
    # together and then weed them out in a single pass
    t = list(s)
    try:
        t.sort()
    except TypeError:
        del t # Move on to the next method
    else:
        # the sort worked, so we are fine
        # do weeding
        return [x for i, x in enumerate(t) if not i or x != t[i-1]]
    # Brute force is all that's left
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u

def uncompress_range(_range):
    """a shotRange is a string that contains numeric data with "," and "-"
    characters
    
    1-4 expands to 1,2,3,4
    10-5 expands to 5,6,7,8,9,10
    1,4-7 expands to 1,4,5,6,7
    1,4-7,11-4 expands to 1,4,5,6,7,8,9,10,11
    """
    shotList = [] * 0
    
    assert(isinstance(_range, (str, unicode) ) )
    
    # first split for ","
    groups = _range.split(",")
    
    for group in groups:
        # try to split for "-"
        ranges = group.split("-")
        
        if len(ranges) > 1:
            if ranges[0] != '' and ranges[1] != '':
                minRange = min( int(ranges[0]), int(ranges[1]))
                maxRange = max( int(ranges[0]), int(ranges[1]))
                
                for number in range(minRange, maxRange+1):
                    if number not in shotList:
                        shotList.append( number )
        else:
            number = int(ranges[0])
            if number not in shotList:
                shotList.append(number)
    
    shotList.sort()
    
    return shotList

def matchRange(_range):
    """validates the range string
    """
    assert(isinstance(_range, (str, unicode)))
    
    pattern = re.compile('[0-9\-,]+')
    matchObj = re.match( pattern, _range )
    
    if matchObj:
        _range = matchObj.group()
    else:
        _range = ''
    
    return _range

def multiple_replace( text, adict ):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def fixWindowsPath(path):
    """replaces / with \ for windows
    """
    return unicode(path).replace(u'/',u'\\')

def findFiles(pattern, search_path, pathsep=os.pathsep):
    return glob.glob(os.path.join(search_path, pattern))

def getChildFolders(path, return_full_path=False):
    """returns the child folders for the given path
    """
    childFolders = os.listdir( path )
    childFolders = filter( os.path.isdir, map( os.path.join, [path] * len(childFolders), childFolders ) )
    
    if return_full_path:
        return childFolders
    else:
        return map( os.path.basename, childFolders )

def getChildFiles(path, return_full_path=False):
    """returns the child files for the given path
    """
    childFiles = os.listdir( path )
    childFiles = filter( os.path.isfile, map( os.path.join, [path] * len(childFiles), childFiles ) )
    
    if return_full_path:
        return childFiles
    else:
        return map( os.path.basename, childFiles )

def backupFile(full_path, maximum_backupCount=None):
    """backups a file by copying it and then renaming it by adding .#.bak
    to the end of the file name
    
    so a file called myText.txt will be backed up as myText.txt.1.bak
    if there is a file with that name than it will increase the backup number
    """
    
    # check if the file exists
    exists = os.path.exists(full_path)
    
    if not exists:
        # just return without doing anything
        return
    
    # get the base name of the file
    baseName = os.path.basename(full_path)
    
    # start the backup number from 1
    backup_no = 1
    backup_extension = '.bak'
    backup_file_full_path = ''
    
    # try to find maximum backup number
    # get the files
    backup_no = getMaximumBackupNumber(full_path) + 1
    
    # now try to get the maximum backup number
    while True:
        
        backup_file_full_path = full_path + '.' + str(backup_no) + backup_extension
        
        if os.path.exists( full_path + '.' + str(backup_no) + backup_extension ):
            backup_no += 1
        else:
            break
    
    # now copy the file with the new name
    shutil.copy( full_path, backup_file_full_path )
    
    if maximum_backupCount is not None:
        maintainMaximumBackupCount( full_path, maximum_backupCount )

def getBackupFiles(full_path):
    """returns the backup files of the given file, returns None if couldn't
    find any
    """
    # for a file lets say .settings.xml the backup file should be names as
    # .settings.xml.1.bak
    # so our search pattern should be
    # .settings.xml.*.bak
    
    backUpExtension = '.bak'
    pattern = full_path + '.*' + backUpExtension
    
    return sort_strings_with_embedded_numbers( glob.glob(pattern) )

def getBackupNumber(full_path):
    """returns the backup number of the file
    """
    
    backupExtension = '.bak'
    # remove the backupExtension
    # and split the remaining
    # and use the last one as the backupVersion
    
    backupNumber = 0
    
    try:
        backupNumber = int(full_path[0:-len(backupExtension)].split('.')[-1])
    except (IndexError, ValueError):
        backupNumber = 0
    
    return backupNumber

def getMaximumBackupNumber(full_path):
    """returns the maximum backup number of the file
    """
    
    backupFiles = getBackupFiles(full_path)
    maximumBackupNumber = 0
    
    if len(backupFiles):
        maximumBackupNumber = getBackupNumber(backupFiles[-1])
    
    return maximumBackupNumber

def maintainMaximumBackupCount(full_path, maximum_backup_count):
    """keeps maximum of given number of backups for the given file
    """
    
    if maximum_backup_count is None:
        return
    
    # get the backup files
    backupFiles = getBackupFiles(full_path)
    
    if len(backupFiles) > maximum_backup_count:
        # delete the older backups
        for backupFile in backupFiles[:-maximum_backup_count]:
            os.remove( backupFile )

def embedded_numbers(s):
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(str(s))
    pieces[1::2] = map(int, pieces[1::2])
    return pieces

def sort_strings_with_embedded_numbers(alist):
    """sorts a string with embedded numbers
    """
    return sorted(alist, key=embedded_numbers)

def padNumber(number, pad):
    """pads a number with zeros
    """
    return ("%0" + str(pad) + "d") % number

def open_browser_in_location(path):
    """Opens the os native browser at the given path
    
    :param path: The path that the browser should be opened at.
    """
    import os
    import subprocess
    import platform
    
    command = []
    
    platform_info = platform.platform()
    
    if platform_info.startswith('Linux'):
        command = 'nautilus ' + path
    elif platform_info.startswith('Windows'):
        command = 'explorer ' + path.replace('/', '\\')
    elif platform_info.startswith('Darwin'):
        command = 'open -a /System/Library/CoreServices/Finder.app ' + path
    
    if os.path.exists(path):
        subprocess.call(command, shell=True)
    else:
        raise IOError("%s doesn't exists!" % path)

