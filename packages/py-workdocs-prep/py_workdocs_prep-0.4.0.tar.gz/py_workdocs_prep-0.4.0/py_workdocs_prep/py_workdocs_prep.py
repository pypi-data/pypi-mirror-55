import os
import re
import shutil
from datetime import datetime
import argparse
import tarfile
import gzip
import traceback
from py_workdocs_prep import LogWrapper


L = LogWrapper()
VALID_NAME_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890-_.'
FULL_LENGTH_WARNING_THRESHOLD = 244

test_mode = False

directories_to_delete_if_found = [
    '.git',
    'venv*',
    'node_modules'
]

ignore_names_exact = [
    'Microsoft User Data',
    'Outlook files',
    'Thumbs.db',
    'Thumbnails',
]

warnings = list()

data = dict()
data['all_original_files'] = list()
data['all_original_dirs_only'] = list()
data['processing'] = dict()
data['processing']['directories_deleted'] = list()
data['processing']['files_deleted'] = list()
data['processing']['renamed_files'] = list()
data['processing']['renamed_directories'] = list()


def set_test_mode():
    '''Only used for unit testing
    '''
    global test_mode
    test_mode = True


def is_directory_to_be_deleted(current_directory_name: str, directories_to_delete_if_found: list=directories_to_delete_if_found)->bool:
    last_part = current_directory_name.split(os.sep)[-1]
    must_delete = False
    try:
        for term in directories_to_delete_if_found:
            if re.search(term, current_directory_name, re.IGNORECASE) is not None:
                must_delete = True
        if re.search('.tmp$', current_directory_name):
            must_delete = True
        if re.search('^\\.', last_part) is not None or re.search('\\.$', last_part):
            must_delete = True
        if must_delete is True:
            try:
                shutil.rmtree(current_directory_name)
                if test_mode:
                    data['processing']['directories_deleted'].append(current_directory_name)
                L.info(message='deleted directory "{}"'.format(current_directory_name))
            except:
                L.warning(message='Error while deleting directory "{}"'.format(current_directory_name))
            return True
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return False


def is_file_starting_or_ending_with_tilde(current_file_with_full_path: str)->bool:
    file_name = current_file_with_full_path.split(os.sep)[-1]
    must_delete = False
    try:
        if re.search('^~', file_name) is not None or re.search('~$', file_name) is not None:
            must_delete = True
        if re.search('.tmp$', current_file_with_full_path):
            must_delete = True
        if re.search('^\\.', file_name) is not None or re.search('\\.$', file_name):
            must_delete = True
        if must_delete is True:
            try:
                os.unlink(current_file_with_full_path)
                if test_mode:
                    data['processing']['files_deleted'].append(current_file_with_full_path)
                L.info(message='deleted file "{}"'.format(current_file_with_full_path))
            except:
                L.warning(message='Error while deleting file "{}"'.format(current_file_with_full_path))
            return True
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return False


def file_rename(current_file_with_full_path: str)->str:
    try:
        file_name = current_file_with_full_path.split(os.sep)[-1]
        path_name = ''
        if os.sep == '/':
            path_name = '/'.join(current_file_with_full_path.split(os.sep)[:-1]) 
        else:
            path_name = '\\'.join(current_file_with_full_path.split(os.sep)[:-1]) 
        final_file_name = ''
        for char in file_name:
            if char not in VALID_NAME_CHARS:
                final_file_name = '{}{}'.format(final_file_name, '_')
            else:
                final_file_name = '{}{}'.format(final_file_name, char)
        target_file = '{}{}{}'.format(path_name, os.sep, final_file_name)
        if file_name != final_file_name:
            pattern = re.compile('__*')
            final_file_name = pattern.sub('_', final_file_name)
            target_file = '{}{}{}'.format(path_name, os.sep, final_file_name)
            try:
                shutil.move(current_file_with_full_path, target_file)
                if test_mode:
                    data['processing']['renamed_files'].append(
                        (
                            current_file_with_full_path,
                            target_file,
                        )
                    )
                L.info(message='renamed file "{}" to "{}"'.format(current_file_with_full_path, target_file))
            except:
                L.warning(message='Error while moving file "{}"'.format(current_file_with_full_path))
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
        target_file = current_file_with_full_path
    return target_file


def directory_rename(current_directory_name: str)->str:
    try:
        dir_name = current_directory_name.split(os.sep)[-1]
        path_name = ''
        if os.sep == '/':
            path_name = '/'.join(current_directory_name.split(os.sep)[:-1]) 
        else:
            path_name = '\\'.join(current_directory_name.split(os.sep)[:-1]) 
        final_dir_name = ''

        for char in dir_name:
            if char not in VALID_NAME_CHARS:
                final_dir_name = '{}{}'.format(final_dir_name, '_')
            else:
                final_dir_name = '{}{}'.format(final_dir_name, char)
        target_dir = '{}{}{}'.format(path_name, os.sep, final_dir_name)
        if dir_name != final_dir_name:
            pattern = re.compile('__*')
            final_dir_name = pattern.sub('_', final_dir_name)
            target_dir = '{}{}{}'.format(path_name, os.sep, final_dir_name)
            try:
                shutil.move(current_directory_name, target_dir)
                if test_mode:
                    data['processing']['renamed_directories'].append(
                        (
                            current_directory_name,
                            target_dir,
                        )
                    )
                L.info(message='renamed directory "{}" to "{}"'.format(current_directory_name, target_dir))
            except:
                L.warning(message='Error while moving directory "{}"'.format(current_directory_name))
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
        target_dir = current_directory_name
    return target_dir


def recurse_dir(root_dir: str, directories_to_delete_if_found: list=directories_to_delete_if_found):
    '''
    Note: Initial pattern from https://www.devdungeon.com/content/walk-directory-python was adopted in the final product.
    '''
    try:
        root_dir = os.path.abspath(root_dir)
        for item in os.listdir(root_dir):
            item_full_path = os.path.join(root_dir, item)
            if item in ignore_names_exact:
                L.warning(message='ignoring based on configuration: "{}"'.format(item_full_path))
            else:
                if os.path.isdir(item_full_path):
                    if is_directory_to_be_deleted(item_full_path, directories_to_delete_if_found=directories_to_delete_if_found) is False:
                        item_full_path = directory_rename(current_directory_name=item_full_path)
                        if test_mode:
                            data['all_original_dirs_only'].append(item_full_path)
                        L.info(message='original directory: "{}" '.format(item_full_path))
                        recurse_dir(item_full_path, directories_to_delete_if_found=directories_to_delete_if_found)
                else:
                    keep_file = 0
                    if is_file_starting_or_ending_with_tilde(current_file_with_full_path=item_full_path) is False:
                        keep_file += 1
                    if keep_file > 0:
                        final_file_name_and_full_path = file_rename(current_file_with_full_path=item_full_path)
                        if test_mode:
                            data['all_original_files'].append(final_file_name_and_full_path)
                        L.info(message='original file: "{}" '.format(final_file_name_and_full_path))
                    else:
                        L.warning(message='File "{}" was marked to be deleted'.format(item_full_path))
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))


def archive_recurse_dir(directory: str, tar_handler: object):
    try:
        directory = os.path.abspath(directory)
        for item in os.listdir(directory):
            item_full_path = os.path.join(directory, item)
            if os.path.isdir(item_full_path):
                archive_recurse_dir(directory=item_full_path, tar_handler=tar_handler)
            else:
                try:
                    tar_handler.add(item_full_path)
                    L.info(message='Archived "{}"'.format(item_full_path))
                except:
                    L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))


def backup_files(root_dir: str)->str:
    try:
        backup_file = '{}{}backup_py_workdocs_prep_{}.tar'.format(
            os.getcwd(),
            os.sep,
            int(datetime.utcnow().timestamp())
        )
        print('Backing up to archive "{}"'.format(backup_file))
        tar = tarfile.open(backup_file, 'w')
        archive_recurse_dir(directory=root_dir, tar_handler=tar)
        tar.close()
        backup_file_gz = '{}.gz'.format(backup_file)
        with open(backup_file, 'rb') as f_in:
            with gzip.open(backup_file_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.unlink(backup_file)
        print('Backup complete')
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
        backup_file_gz = ''
    return backup_file_gz


def parse_command_line_args(root_dir: str):
    try:
        parser = argparse.ArgumentParser(description='Prepare a directory for migration to AWS WorkDocs')
        parser.add_argument(
            '-b', '--backup',
            action='store_true',
            help='Backup the files in the selected directory first. Files will be added to a tar archive and which will then be gzipped'
        )
        args = parser.parse_args()
        if args.backup is True:
            backup_files(root_dir=root_dir)
    except:
        L.error(message='EXCEPTION: {}'.format(traceback.format_exc()))


def start(start=os.getcwd()):
    print('Starting in "{}"'.format(start))
    parse_command_line_args(root_dir=start)
    recurse_dir(root_dir=start)


if __name__ == "__main__":
    start(start=os.getcwd())

# EOF
