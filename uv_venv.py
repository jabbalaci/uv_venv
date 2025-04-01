#!/usr/bin/env python3

"""
The command "uv venv" creates `.venv/` in the project folder.

This script creates the virt. env. in a separate folder (`~/.virtualenvs`),
and in the project folder it creates a symbolic link called `.venv` that points
on the virt. env. located in `~/.virtualenvs`.

Tested under Linux only.

Author: Laszlo Szathmary (jabba.laci@gmail.com), 2024--2025
"""

import base64
import hashlib
import os
import shutil
import sys

SYNC = True

VIRTUALENVS_BASE: str = os.path.join(os.path.expanduser("~"), ".virtualenvs")
CWD: str = os.getcwd()


def generate_poetry_hash(path: str) -> str:
    """
    Using the same hashing alg. as poetry.
    """
    sha256 = hashlib.sha256(path.encode("utf-8")).digest()
    b64 = base64.urlsafe_b64encode(sha256).decode("utf-8")
    return b64[:8]


def generate_venv_name(project_path: str = CWD) -> str:
    """
    The generated name is similar to poetry's.
    """
    project_name = os.path.basename(project_path)
    path_hash = generate_poetry_hash(project_path)
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    venv_name = f"{project_name.lower()}-{path_hash}-py{python_version}"
    #
    return venv_name


def execute(cmd: str) -> None:
    print("$", cmd)
    os.system(cmd)


def delete_current_venv() -> None:
    if os.path.isdir(".venv"):
        try:
            shutil.rmtree(".venv")
            print("Successfully deleted .venv/ and all its contents")
        except OSError as e:
            print(f"Error: .venv/ : {e.strerror}")
            sys.exit(1)
    else:
        try:
            os.unlink(".venv")
            print("Successfully deleted .venv")
        except OSError as e:
            print(f"Error: .venv : {e.strerror}")
            sys.exit(1)


def check_current_state_and_reset() -> None:
    # ~/.virtualenvs must exist
    if not os.path.isdir(dname := VIRTUALENVS_BASE):
        print(f"Error: the folder {dname} doesn't exist")
        print("Tip: create it")
        sys.exit(1)
    # if ~/.virtualenvs exists:
    venv_folder_path = os.path.join(VIRTUALENVS_BASE, generate_venv_name())
    if os.path.isdir(venv_folder_path):
        print(f"Poetry-like virt. env. already exists: {venv_folder_path}")
        answer = input("Do you want to delete it [yN]? ").strip().lower()
        if answer == "y":
            try:
                shutil.rmtree(venv_folder_path)
                print(f"Successfully deleted {venv_folder_path} and all its contents")
            except OSError as e:
                print(f"Error: {venv_folder_path} : {e.strerror}")
                sys.exit(1)
        else:
            print("abort")
            sys.exit(1)
        #
    # if ~/.virtualenvs/<venv_folder> doesn't exist
    # ./.venv mustn't exist
    if os.path.exists(".venv") or os.path.islink(".venv"):
        print(".venv already exists in the current folder")
        answer = input("Do you want to delete it [yN]? ").strip().lower()
        if answer == "y":
            delete_current_venv()
        else:
            print("abort")
            sys.exit(1)
        #
    #


def main() -> None:
    # if not os.path.isfile("pyproject.toml"):
    # print("Error: this folder doesn't look like a uv-initialized project")
    # print("Tip: execute 'uv init' first")
    # sys.exit(1)

    venv_folder_path = os.path.join(VIRTUALENVS_BASE, generate_venv_name())

    check_current_state_and_reset()
    assert not os.path.exists(venv_folder_path)
    assert not os.path.exists(".venv")

    cmd = f"uv venv '{venv_folder_path}'"
    execute(cmd)
    cmd = f"ln -s '{venv_folder_path}' .venv"
    execute(cmd)
    if SYNC and os.path.isfile("pyproject.toml"):
        cmd = "uv sync"
        execute(cmd)


if __name__ == "__main__":
    main()
