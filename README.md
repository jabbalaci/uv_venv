# uv_venv

With [uv](https://docs.astral.sh/uv/), create the `.venv` folder in `~/.virtualenvs` and put a symlink on it in your project folder.

## Description

The command `uv venv` creates `.venv/` in the project folder.

This script creates the virt. env. in a separate folder (`~/.virtualenvs`),
and in the project folder it creates a symbolic link called `.venv` that points
on the virt. env. located in `~/.virtualenvs`.

## Rationale

[Poetry](https://python-poetry.org/) works like this by default. With this
script I can make `uv` behave similarly to Poetry.

I prefer storing my projects in Dropbox. Since a `.venv/` folder can grow really huge, it makes no sense
to store these folders in Dropbox. I prefer putting
them in a separate folder, outside of Dropbox.

## Usage

Create the folder `~/.virtualenvs`. Virt. environments
will be created there.

Put a symbolic link or an alias on this script and
name it `uv_venv`. Then:

```shell
$ uv init
$ uv_venv
```
