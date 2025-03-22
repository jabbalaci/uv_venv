#!/usr/bin/env python3

"""
The command "uv venv" creates .venv/ in the project folder.

This script creates the virt. env. in a separate folder (~/.virtualenvs),
and in the project folder it creates a symbolic link called .venv that points
on the virt. env. located in ~/.virtualenvs .

Tested under Linux only.

Author: Laszlo Szathmary (jabba.laci@gmail.com), 2024--2025
"""

import base64
import hashlib
import os
import sys

# DRY_RUN = True  # Don't actually execute any commands. Just print them.
DRY_RUN = False  # Execute commands.

VIRTUALENVS_BASE = os.path.join(os.path.expanduser("~"), ".virtualenvs")


def generate_poetry_hash(path):
    """
    Using the same hashing alg. as poetry.
    """
    sha256 = hashlib.sha256(path.encode("utf-8")).digest()
    b64 = base64.urlsafe_b64encode(sha256).decode("utf-8")
    return b64[:8]


def generate_venv_name(project_path):
    """
    The generated name is similar to poetry's.
    """
    project_name = os.path.basename(project_path)
    path_hash = generate_poetry_hash(project_path)
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    venv_name = f"{project_name.lower()}-{path_hash}-py{python_version}"
    #
    return venv_name


def execute(cmd):
    print("$", cmd)
    if not DRY_RUN:
        os.system(cmd)


def main():
    project_path = os.getcwd()

    venv_name = generate_venv_name(project_path)
    # print(f"Generated Poetry-like virt. env. name: {venv_name}")
    # print(venv_name)

    if not os.path.isdir(dname := VIRTUALENVS_BASE):
        print(f"Error: the folder {dname} doesn't exist")
        print("Tip: create it")
        exit(1)

    venv_folder = os.path.join(VIRTUALENVS_BASE, venv_name)
    if os.path.isdir(venv_folder):
        print(f"Poetry-like virt. env. already exists: {venv_folder}")
        print("Tip: remove it first to generate a new one")
        exit(1)
    if os.path.exists(".venv"):
        print(".venv already exists in the current folder")
        print("Tip: remove it first to generate a new one")
        exit(1)
    # print("#", venv_folder)
    cmd = f"uv venv {venv_folder}"
    execute(cmd)
    cmd = f"ln -s {venv_folder} .venv"
    execute(cmd)


if __name__ == "__main__":
    main()
