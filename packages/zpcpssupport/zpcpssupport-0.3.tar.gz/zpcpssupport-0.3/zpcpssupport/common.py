import os
from os.path import join, isdir, isfile, exists, splitext
from pick import pick
import shutil


def yes_no(answer):
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    while True:
        choice = input(answer).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'\n")


def choose_environment():
    title = 'Please choose environment: '
    options = ['sandbox', 'staging']
    option, index = pick(options, title)
    return option


def choose_multi_environment():
    title = 'Please choose environment (press SPACE to mark, ENTER to continue): '
    options = ['sandbox', 'staging', 'production']
    selected = pick(options, title, multi_select=True, min_selection_count=1)


def dynamic_copytree(src, dst, *argv):
    # options: [0]: excteption_extension

    if not exists(dst):
        shutil.copytree(src, dst)
        return
    print("dynamic copytree with target forder exists")
    if bool(argv):
        excteption_extension = argv[0]

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for filename in files:
            x, file_extension = splitext(filename)
            if bool(excteption_extension) and file_extension in excteption_extension:
                continue
            src_file = join(src_dir, filename)
            tar_file = src_file.replace(src, dst)
            shutil.copy(src_file, tar_file)
