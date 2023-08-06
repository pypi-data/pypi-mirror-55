import os
from os.path import join, exists, isfile
import shutil
from pick import pick
from zalopaysupport.common import yes_no, choose_environment, dynamic_copytree
from zalopaysupport.rename import renameToRemoveResolutionSuffix, renameAllFolderAndFile
from zalopaysupport.resource import clone_folder_structure, svn_copy_resource, svn_map_images


def cloneResource(src_path, target_path):
    resource1x = join(target_path, '1x')
    resource2x = join(target_path, '2x')
    resource3x = join(target_path, '3x')
    if exists(target_path):
        shutil.rmtree(target_path)
    os.makedirs(resource1x)
    os.makedirs(resource2x)
    os.makedirs(resource3x)

    clone_folder_structure(src_path, resource1x)
    clone_folder_structure(src_path, resource2x)
    clone_folder_structure(src_path, resource3x)
    images_dict = svn_map_images(src_path)
    svn_copy_resource(src_path, resource1x, images_dict, 1)
    svn_copy_resource(src_path, resource2x, images_dict, 2)
    svn_copy_resource(src_path, resource3x, images_dict, 3)
    renameToRemoveResolutionSuffix(target_path)
    return (resource1x, resource2x, resource3x)


def prepareImageResourceBeforeUpload(source, target):
    if yes_no("Rename input [Y/n]: "):
        renameAllFolderAndFile(source)
    (resource1x, resource2x, resource3x) = cloneResource(source, target)


def uploadImagesToZPSVN(source, subPathOnSVN):
    svnPath = os.environ.get('ZALOPAY_SVN')
    if not svnPath:
        print("DO NOT FOUND ZALOPAY_SVN ENVIRONMENT")
        return

    title = 'Please choose environment (press SPACE to mark, ENTER to continue): '
    options = ['sandbox', 'staging']
    envs = pick(options, title, multi_select=True, min_selection_count=1)
    for env, index in envs:
        envPath = join(svnPath, env)
        if not exists(envPath):
            print("DO NOT FOUND FOLDER: %s " % (envPath))
            continue
        targetPath = join(envPath, subPathOnSVN)
        if exists(targetPath):
            if yes_no('folder `%s` exists on svn, you want to remove it [Y/n]: ' % (subPathOnSVN)):
                shutil.rmtree(targetPath)
        dynamic_copytree(source, targetPath)
