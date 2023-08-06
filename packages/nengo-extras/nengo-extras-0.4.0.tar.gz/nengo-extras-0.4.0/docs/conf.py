# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set
# to its containing dir.

import sys

try:
    import nengo_extras
    import guzzle_sphinx_theme
except ImportError:
    print("To build the documentation, nengo_extras and guzzle_sphinx_theme "
          "must be installed in the current environment. Please install these "
          "and their requirements first. A virtualenv is recommended!")
    sys.exit(1)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'guzzle_sphinx_theme',
    'numpydoc',
    'nbsphinx',
    'nbsphinx_link',
]

default_role = 'py:obj'

# -- sphinx.ext.autodoc
autoclass_content = 'both'  # class and __init__ docstrings are concatenated
autodoc_default_flags = ['members']
autodoc_member_order = 'bysource'  # default is alphabetical

# -- sphinx.ext.intersphinx
intersphinx_mapping = {
    'nengo': ('https://www.nengo.ai/nengo/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
}

# -- sphinx.ext.todo
todo_include_todos = True

# -- numpydoc
numpydoc_show_class_members = False

# -- nbsphinx
nbsphinx_timeout = -1

# -- sphinx
nitpicky = True
exclude_patterns = ['_build']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'

# Need to include https Mathjax path for sphinx < v1.3
mathjax_path = ("https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.3/"
                "config/TeX-AMS-MML_HTMLorMML.js")

project = u'Nengo Extras'
authors = u'Applied Brain Research'
copyright = nengo_extras.__copyright__
version = '.'.join(nengo_extras.__version__.split('.')[:2])
release = nengo_extras.__version__  # Full version, with tags
pygments_style = 'default'

# -- Options for HTML output --------------------------------------------------

pygments_style = "sphinx"
templates_path = ["_templates"]
html_static_path = ["_static"]

html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = "guzzle_sphinx_theme"

html_theme_options = {
    "project_nav_name": "Nengo extras %s" % (version,),
    "base_url": "https://www.nengo.ai/nengo-extras",
}

html_title = "Nengo extras {0} docs".format(release)
htmlhelp_basename = 'Nengo extras'
html_last_updated_fmt = ''  # Suppress 'Last updated on:' timestamp
html_show_sphinx = False

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '11pt',
    # 'preamble': '',
}

latex_documents = [
    # (source start file, target, title, author, documentclass [howto/manual])
    ('index', 'nengo_extras.tex', html_title, authors, 'manual'),
]

# -- Options for manual page output -------------------------------------------

man_pages = [
    # (source start file, name, description, authors, manual section).
    ('index', 'nengo_extras', html_title, [authors], 1)
]

# -- Options for Texinfo output -----------------------------------------------

texinfo_documents = [
    # (source start file, target, title, author, dir menu entry,
    #  description, category)
    ('index', 'nengo_extras', html_title, authors, 'Nengo',
     'Lesser used features for Nengo', 'Miscellaneous'),
]
