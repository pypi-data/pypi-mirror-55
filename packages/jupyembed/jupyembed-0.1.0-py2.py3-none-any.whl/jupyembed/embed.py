# -*- coding: utf-8 -*-

"""Main module."""

import nbformat
import pandas as pd
import json

def embed_data_in_notebook(notebook_path, data_files, as_version=4):
    """ Embed data provided in data field to notebook_path
    
    """
    # check if notebook exists
    try:
        nb = nbformat.read(notebook_path, as_version=as_version)
    except:
        # by default create a v4 notebook.
        # maybe change this behaviour
        nb = nbformat.v4.new_notebook()

    # check if embed_data tool is used previously
    if 'embed_data' not in nb['metadata']:
        nb['metadata']['embed_data'] = {}

    for data in data_files:
#         if data in nb['metadata']['embed_data']:
#             # check for overwrite of data
#             pass
#         else:
        nb['metadata']['embed_data'][data] = pd.read_csv(data, header=None).to_json()
#     print(nb['metadata']['embed_data'])
    nbformat.write(nb, notebook_path)


def read_embeded_data(notebook_path, data, as_version=4, dataframe=True):
    nb = nbformat.read(notebook_path, as_version=as_version)
    if dataframe: 
        return pd.read_json(nb['metadata']['embed_data'][data])
    else:
        return pd.read_json(nb['metadata']['embed_data'][data]).values

    
def embed_requirements(notebook_path, requirements, as_version=4):
    # check if notebook exists
    try:
        nb = nbformat.read(notebook_path, as_version=as_version)
    except:
        # by default create a v4 notebook.
        # maybe change this behaviour
        nb = nbformat.v4.new_notebook()

    # check if requirements already present
    if 'requirements' not in nb['metadata']:
        nb['metadata']['requirements'] = set()
    
    nb['metadata']['requirements'] = set(requirements)
    nbformat.write(nb, notebook_path)

def install_requirements(notebook_path, pip_or_conda='pip'):
    pass



