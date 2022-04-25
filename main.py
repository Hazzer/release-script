#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import shutil
import subprocess
import argparse

import xml.etree.ElementTree as ET

default_dir_list = ["About", "Assemblies", "Defs", "Patches", "Languages", "Textures", "LoadFolders.xml",
                    "changelog.txt"]


def get_mod_name(path):
    joined_path = os.path.join(path, "About", "About.xml")
    if os.path.exists(joined_path):
        mod_about = ET.parse(joined_path).getroot()
        return mod_about.find("name").text
    else:
        print("Not mod directory")


def get_special_dirs(path):
    joined_path = os.path.join(path, "LoadFolders.xml")
    additional_dirs = []
    if os.path.exists(joined_path):
        load_folder = ET.parse(joined_path).getroot()
        for child in load_folder:
            for li in child:
                if li.text != '/':
                    additional_dirs.append(li.text)
    print(f'Dirs from LoadFolders.xml: {additional_dirs}')
    return additional_dirs


def make_release(start_dir, target_dir, release, zip_tool):
    mod_name = get_mod_name(start_dir)
    if mod_name and os.path.exists(target_dir):
        print(f'Coping mod {mod_name} to mod local directory')
        local_directory = os.path.join(target_dir, mod_name.replace(" ", ""))
        if os.path.exists(local_directory):
            shutil.rmtree(local_directory)
            os.makedirs(local_directory)

        all_files_to_copy = default_dir_list + get_special_dirs(start_dir)
        print("=======================Data copy===============================")
        for file in all_files_to_copy:
            path_to_copy = os.path.join(start_dir, file)
            if os.path.exists(path_to_copy):
                target = os.path.join(local_directory, file)
                print(f'Copy {path_to_copy} to {target}')
                if os.path.isdir(path_to_copy):
                    shutil.copytree(path_to_copy, target)
                else:
                    shutil.copyfile(path_to_copy, target)

        release_path = os.path.join(os.path.expanduser("~"), "Desktop", mod_name.replace(" ", "") + ".zip")
        if os.path.exists(release_path):
            print(f"Removing old release {release_path}")
            os.remove(release_path)
        if release:
            system = subprocess.Popen([zip_tool, "a", "-r", release_path, os.path.join(local_directory, "*")])
            system.communicate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy and release script')
    parser.add_argument('-start_dir', dest='start_dir', type=str, help='Mod source code directory')
    parser.add_argument('-target_dir', dest='target_dir', type=str, help='Steam mod local directory')
    parser.add_argument('-zip_tool', dest='zip_tool', type=str, help='7zip exe to create pack')
    parser.add_argument('-r', dest='release', type=bool, help='Create zip file', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    make_release(args.start_dir, args.target_dir, args.release, args.zip_tool)
