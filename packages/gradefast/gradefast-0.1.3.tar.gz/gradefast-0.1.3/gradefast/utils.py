"""
Utility classes and methods for developer in a hurry
"""
import os
import re
import sys
import json
import copy
import time
import zipfile
import logging
import datetime
import threading
import traceback
from pathlib import Path
from urllib.parse import urlparse

import requests
from halo import Halo

from gradefast import logconfig
from gradefast.exceptions import *

logger = logconfig.configure_and_get_logger(__name__, logging.DEBUG)

def setup_logger(name, log_file, level=logging.INFO):
    '''Function setup as many loggers as you want'''

    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# TODO (manjrekarom):
# 1. Retry feature not implemented
class Downloader:
    """
    A utility that downloads items given in :class:`~gradefast.submission.SubmissionGroup`
    from web to disk
    
    Parameters
    ----------
    cookie: str
        HTTP session cookie to get authorized to the web portal

    storage_location: str
        Location to store downloaded files. A folder is created inside of it
        for each team_id. Default is './'

    extract: bool
        Whether to extract zip items after downloading. Default is False

    keep_original: bool
        Deletes zip files after unzip successful. Default is True

    retry: bool
        Retry download if it fails. Default is True

    retry_times: int
        Retry retry_times until the file is downloaded. Default is 2 i.e. 2 times

    .. todo:

        Keep or delete files after deletion and retry on fail is not yet implemented

    Attributes
    ----------
    cookie: str

    storage_location: str
    
    extract: bool
    
    keep_original: bool
    
    retry: bool
    
    retry_times: int

    """
    def __init__(self, cookie, types=['zip', 'png'], storage_location = './', extract=False, 
    keep_original=True, retry=True, retry_times=2):
        self.cookie = cookie
        self.types = types
        self.storage_location = storage_location
        self.extract = extract
        self.keep_original = keep_original
        self.retry = retry
        self.retry_times = retry_times

    @staticmethod
    def get_extension(url):
        """
        Find extension of a file from its download url

        Parameters
        ----------
        url: str
            Download url of a file

        Returns
        -------
        str
            Extension of the downloadable file
        """
        o = urlparse(url)
        pattern = re.compile("\.([\w_]*)$")
        matches = pattern.search(o.path)
        if matches != None:
            return matches[1]

    @staticmethod
    def get_extension_from_header(response):
        """
        Returns extension of file being downloaded from its response headers

        Check content-disposition header to find filename and extracts extension
        from it

        Parameters
        ----------
        response: `requests.response`

        Returns
        -------
        str
            Extension of file being downloaded
        """
        try:
            content_disposition_header = response.headers['content-disposition']
        except KeyError as e:
            raise Exception('There is no content disposition header to fetch downloaded\'s file extension')
        content_disposition_list = content_disposition_header.split(';')
        pattern = re.compile("filename=(.*)$")
        for item in content_disposition_list:
            matches = pattern.search(item)
            if matches != None:
                return Path(matches[1]).suffix[1:]

    @staticmethod
    def parent_folder_name(task_name, theme_name):
        """
        Builds name of the parent folder inside storage_location where all files
        will be downloaded.

        New task downloads get saved inside a newly created folder named with timestamp. 

        Parameters
        ----------
        task_name: str
        
        theme_name: str

        Returns
        -------
        str

        """
        directory_name = "{}_{}_{}".format(task_name, theme_name, 
        datetime.datetime.now().strftime("%Y_%m_%d-%H_%M"))
        return directory_name

    @staticmethod
    def create_storage_directory(dir_path):
        """
        Create storage location directory if it doesnt exist

        Parameters
        ----------
        dir_path: str

        Returns
        -------
        bool
            If true then directory is successfully created
        """
        if not os.path.isdir(dir_path):
            # file permission
            os.makedirs(dir_path, 0o755)
        return True

    @staticmethod
    def create_team_folder(team_id, dir_path):
        """
        Create folder for each team by naming it with team_id

        Parameters
        ----------
        team_id: int

        dir_path: str
            Directory inside which to create the team folder

        Returns
        -------
        str
            Returns path of team folder which was successfully created
        """
        if type(team_id) == int:
            team_id = str(team_id)

        team_folder_path = os.path.join(dir_path, team_id)
        if not os.path.isdir(team_folder_path):
            os.makedirs(team_folder_path, 0o755)

        return os.path.abspath(team_folder_path)


    @staticmethod
    def download_summary(downloaded_submission_group, file_path=''):
        pass

    @staticmethod
    def download_file_item(cookie, submission, file_item_name, download_directory, file_name=''):
        """
        Downloads and saves file

        Initiates a network request to download and save file following the naming
        convention. The information about file url is picked up from a 
        :class:`~gradefast.submission.Submission`

        Parameters
        ----------
        url: str
            Url of the file to download

        cookie: str
            HTTP session cookie to authenticate to the web page

        file_name: str
            Name of file item being downloaded. The information is also present in 
            :class:`~gradefast.submission.Submission`

        submission: :class:`~gradefast.submission.Submission`

        storage_location: str

        Returns
        -------
        str
            Full path of the downloaded file
        """
        team_id = submission.team_id
        if type(team_id) == int:
            team_id_str = str(team_id)
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
        if 'name' in cookie.keys() and 'value' in cookie.keys():
            cookie = {cookie['name']: cookie['value']}
        
        # download file
        response = requests.get(submission.items[file_item_name]['url'], 
        allow_redirects=True, cookies=cookie)
        logger.debug(f"Attempting download for file with url:"  \
            f"{submission.items[file_item_name]['url']}")
        
        # get extension of the final url obtained after redirection
        file_extension = Downloader.get_extension(response.url)
        if file_extension == None:
            file_extension = Downloader.get_extension_from_header(response)
        if file_extension == None:
            raise Exception("Cannot identify extension of the file, does the url"   \
            "not have extension? Check content-disposition for filename=<xyz>.<extension>")
        
        # name downloaded file according to convention
        if file_name == '':
            file_name = "{}_{}.{}".format(team_id_str, file_item_name, file_extension)
        download_file_path = os.path.abspath(os.path.join(download_directory, file_name))

        with open(download_file_path, 'wb') as file:
            file.write(response.content)
            
        return download_file_path

    @staticmethod
    def extract_if_zip(team_id, zip_item_name, final_submission_group):
        zip_path = final_submission_group[team_id].items[zip_item_name]['path']
        if Path(zip_path).suffix != '.zip':
            return False, final_submission_group
        # unzip and store it
        unzip_path = Extracter.get_default_unzip_path(zip_path)
        did_extract = Extracter.extract_file(zip_path, unzip_path)
        logger.debug(f'Extracting file_item {zip_path}')
        if not did_extract:
            raise Exception(f"Error unzipping {zip_path} of team {team_id}")
        # mark the zips extracted property true
        final_submission_group[int(team_id)].items[zip_item_name]['extracted'] = True
        unzip_item_name = zip_item_name + "_unzipped"
        final_submission_group[int(team_id)].items[unzip_item_name] = {}
        final_submission_group[int(team_id)].items[unzip_item_name]['path'] = unzip_path
        return True, final_submission_group

    # TODO: Maintain a list of downloaded and not downloaded files 
    def download(self, submission_group):
        """
        Downloads submission_group files to disk

        Parameters
        ----------
        submissions: :class:`~gradefast.submission.SubmissionGroup`
        
        Returns
        -------
        final_submissions: :class:`~gradefast.submission.SubmissionGroup`
            :class:`~gradefast.submission.SubmissionGroup` with files successfully
            downloaded set to ``True``
        dir_path: str
            path
        """
        # copy submissions
        final_submission_group = copy.deepcopy(submission_group)

        # First make a parent folder
        parent_folder_name = Downloader.parent_folder_name(submission_group.task_name, 
        submission_group.theme_name)
        
        # path of download directory
        download_directory = os.path.join(self.storage_location, parent_folder_name)
        # create download directory
        if not Downloader.create_storage_directory(download_directory):
            raise Exception('Cannot create storage/download directory')
        self.storage_location = download_directory

        # Setting up download success and failure loggers
        self.logger1 = setup_logger('download_success', os.path.join(self.storage_location,
        'download_success.log'), level = logging.INFO)
        self.logger2 = setup_logger('download_failed', os.path.join(self.storage_location,
        'download_failed.log'), level = logging.INFO)

        cookie = self.cookie
        if 'name' in self.cookie.keys() and 'value' in self.cookie.keys():
            cookie = {self.cookie['name']: self.cookie['value']}
            
        print('Downloading {} files ...'.format(len(submission_group)))
        # spinner = Spinner()
        spinner = Halo(spinner='dots')

        for submission in submission_group:
            try:
                team_id = submission.team_id
                team_directory = Downloader.create_team_folder(team_id, download_directory)
                
                for file_item_name, meta in submission.items.items():
                    if file_item_name not in self.types:
                        continue

                    spinner.start(text='Downloading file_item "{}" for team_id: {}'\
                        .format(file_item_name, str(team_id)))

                    # only download files indicated with types
                    # download and save file
                    downloaded_file_path = Downloader.download_file_item(cookie, submission, file_item_name,
                    team_directory)

                    if downloaded_file_path == None:
                        raise Exception(f"Failed to download file {file_item_name}:{meta['url']} to path"   \
                            f"{downloaded_file_path} for team {submission.team_id}")
                    
                    # add more meta information in newly created final submissions object
                    final_submission_group[str(team_id)].items[file_item_name]['downloaded'] = True            
                    final_submission_group[str(team_id)].items[file_item_name]['path'] = downloaded_file_path

                    self.logger1.info(str(submission.team_id) + ' ' + file_item_name + ' successfully downloaded.')
                    # extract and return new submission group
                    if self.extract == True:
                        _, final_submission_group = Downloader.extract_if_zip(submission.team_id, file_item_name,
                    final_submission_group)
                    
                    # spinner success tick
                    spinner.succeed()
            except Exception as e:
                spinner.fail('Failed to download.')
                logger.exception(f"Exception when attempting download on {meta['url']}" \
                    f"{submission.team_id}")
                self.logger2.exception("{}'s {} failed to download.".format(str(submission.team_id), file_item_name))
                sys.stdout.write('\bFailed.. Trying next file\n')
        
        spinner.stop()
        # write a json to create a submissions object from
        # utils.Persist.to_json(submissions, save_location=path)
        return final_submission_group, download_directory

class Extracter:
    """
    A utility that extracts standalone zips or zip items from 
    :class:`~gradefast.submission.SubmissionGroup` from web to disk
    
    Parameters
    ----------
    cookie: str
        HTTP session cookie to get access to the portal

    storage_location: str
        Location to store downloaded files. A folder is created for each id

    extract: bool
        Extracts zip files

    keep_original: bool
        Deletes zip files after unzip successful

    retry: bool
        Retry download if it fails

    retry_times: int
        Retry retry_times until the file is downloaded

    .. todo:

        Keep or delete files after deletion and retry on fail is not yet implemented

    Attributes
    ----------
    cookie: str
    storage_location: str
    extract: bool
    keep_original: bool
    retry: bool
    retry_times: int
    """
    
    @staticmethod
    def extract_summary(extracted_submission_group, file_path=''):
        pass

    @staticmethod
    def get_default_unzip_path(zip_path):
        """
        Returns default name of a zip item from it's path

        An extracted zip item is named as <team-id>_<file_item_name>_unzippped

        Parameters
        ----------
        zip_path: str

        Returns
        -------
        str

        """
        if Path(zip_path).suffix != '.zip':
            raise Exception('Enter a valid zip path')
        file_name, file_extension = os.path.splitext(os.path.basename(zip_path))
        unzip_name = file_name + '_unzipped'
        unzip_path = os.path.join(os.path.dirname(zip_path), unzip_name)
        return os.path.abspath(unzip_path)

    @staticmethod
    def extract_file(zip_path, extract_path):
        """
        Extracts a single zip and the contents are extracted at extract_path

        Inside extract path directory the contents inside the zip are stored.

        Parameters
        ----------
        zip_path: str
            Path to zip file

        extract_path: str
            Full path of directory to unzip the archive at

        Returns
        -------
        bool
            If zip was extracted to the location
        """
        try:
            zip_ref = zipfile.ZipFile(zip_path, 'r')
            # if extract_path == '' or extract_path == None:
            #     extract_path = Extract.default_unzip_name(zip_path)
            zip_ref.extractall(extract_path)
            zip_ref.close()
        except Exception as e:
            logger.exception(f'Exception when attempting to unzip {zip_path} to {extract_path}')
            return False
        return True
    
    @staticmethod
    def extract(submission_group):
        """
        Extracts all zip items found in :class:`~gradefast.submission.SubmissionGroup`
        and stores them in the specific team folder.

        Parameters
        ----------
        submission_group: :class:`~gradefast.submission.SubmissionGroup`

        Returns
        -------
        bool
        """
        new_submission_group = copy.deepcopy(submission_group)
        # extracted = {}
        for submission in submission_group:
            team_id = submission.team_id
            for file_item_name, meta_info_dict in submission.items.items():
                file_path = meta_info_dict['path']
                if Path(file_path).suffix != '.zip':
                    continue
                # path to unzipped folder
                try:
                    extract_path = Extracter.get_default_unzip_path(file_path)
                    if not Extracter.extract_file(file_path, extract_path):
                        continue
                    # write zip to extracted
                    new_submission_group[team_id].items[file_item_name]['extracted'] = True
                    # make entry for extracted folder
                    new_submission_group[team_id].items[file_item_name + '_unzipped'] = {'path': extract_path}
                except Exception as e:
                    logger.exception(f'Exception when attempting to extract submission {submission}' \
                        f'and "file_name" {file_item_name} meta {meta_info_dict}')
            # extracted[submission.team_id] = False
        return new_submission_group

def subtract_dict(A, B):
    a_copy = A.copy()
    b_copy = B.copy()
    all(map(a_copy.pop, b_copy))
    return a_copy
    
def is_string_number(name):
    # check if the name of the folder is a number
    try:
        int(name)
        return True
    except ValueError:
        return False 

def object_equality(obj1, obj2, ignore_attrs=[]):
    # this method doesnt not consider private fields and functions
    # when evaluating equals    
    if not isinstance(obj2, type(obj1)):
        return False
    list_of_attrs = dir(obj1) + dir(obj2)
    try:
        for attr in list_of_attrs:
            if attr in ignore_attrs:
                continue
            if not attr.startswith("_") and not callable(getattr(obj1, attr)):
                if getattr(obj1, attr) != getattr(obj2, attr):
                    return False
    except AttributeError as e:
        logger.exception('Some member fields are not present in either objects',
        stack_info=True)
        return False
    return True

def combine_list_elements(*items):
    """
    Combines items into a single list of items

    Items can contain a single item of any type or a list of items. If combined 
    list evaluates to a single item, only an item is returned else a list of items
    is returned.

    Returns
    -------
    list
        Combined list of items 
    """
    combined_list = []
    for item in items:
        logger.debug(item)
        if item == None or (type(item) == str and item.strip() == ''):
            continue
        if type(item) == list:
            combined_list += item
        elif type(item) == str:
            combined_list.append(item)
    
    logger.debug(f"Output of combining {items} is {combined_list}")
    if len(combined_list) == 1:
        return combined_list[0]

    return combined_list
