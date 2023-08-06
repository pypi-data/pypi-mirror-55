from os import walk, chdir, path, remove
from unidecode import unidecode
# pip install unidecode
from os.path import isfile, basename, isdir, join
import shutil
import re


def basename(input):
    return re.sub('(@2x|@3x)', '', input)


def standardize(input):
    input = unidecode(input)
    (name, extenstion) = path.splitext(input)

    if "_1x" in name:
        name = name.replace("_1x", "")
    if "_2x" in name:
        name = name.replace("_2x", "@2x")
    if "_3x" in name:
        name = name.replace("_3x", "@3x")
    _name = re.sub('(-|\.|\s)', '_', name).lower()
    return "%s%s" % (_name, extenstion)

# unaccented


def renameAllFolderAndFile(root_path):
    for (dirpath, dirnames, filenames) in walk(root_path):
        if dirpath != root_path:
            continue
        for dirname in dirnames:
            full_folder = join(dirpath, dirname)
            if isdir(full_folder):
                rename_folder = join(dirpath, standardize(dirname))
                rename(full_folder, rename_folder)
    for (dirpath, dirnames, filenames) in walk(root_path):
        for filename in filenames:
            full_file = join(dirpath, filename)
            if not isfile(full_file):
                continue
            if filename.endswith('jpg') or filename.endswith('png'):
                rename_file = path.join(dirpath, standardize(filename))
                rename(full_file, rename_file)


def rename(old_path, new_path):
    if old_path != new_path:
        print('%s rename to %s' % (old_path, new_path))
        shutil.move(old_path, new_path)


def renameToRemoveResolutionSuffix(path):
    print('renameResourceServer: remove resolution suffix')
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            full_file = join(dirpath, filename)
            if not isfile(full_file):
                continue
            newName = re.sub("@2x|@3x(?=\.)", "", filename)
            if newName != filename:
                shutil.move(full_file, join(dirpath, newName))
