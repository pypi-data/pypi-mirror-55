# -*- coding: utf-8 -*-
"""Allow default templates and configuration files redefinition locally"""
from os import path

from sphinx_paw.constants import NOTSET

DEFAULT_PATH = path.join(path.dirname(__file__), 'defaults')


def rewritable_file_path(app, filename, local_path=NOTSET, default_path=NOTSET):
    """Get filepath in documentation src or default in sphinx_paw"""
    src_dir = app.srcdir
    if local_path:
        found_path = path.join(src_dir, local_path, filename)
    else:
        found_path = path.join(src_dir, filename)

    if path.exists(found_path):
        return found_path

    if default_path is NOTSET:
        default_path = DEFAULT_PATH
    elif default_path is None:
        raise FileNotFoundError(f"Local file {found_path} not found")

    return path.join(default_path, filename)


def rewritable_file_content(app, filename):
    """Get rewritable file content"""
    file_path = rewritable_file_path(app, filename, DEFAULT_PATH)
    with open(file_path, 'rb') as content_fh:
        content = content_fh.read().decode()
        return content
