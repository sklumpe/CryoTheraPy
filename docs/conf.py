# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cryotheraPy'
copyright = '2023, Florian Beck'
author = 'Florian Beck'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


import os,sys

todo_include_todos = True
sys.path.insert(0,os.path.abspath("../src"))
extensions = ['sphinx_rtd_theme','sphinx.ext.todo','sphinx.ext.viewcode','sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme ='bizstyle'
html_static_path = ['_static']
