# -*- coding: utf-8 -*-

import sys, os

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
master_doc = 'index'
autoclass_content = 'both'

project = u'Moodstocks API client'
copyright = u'2013, Moodstocks SAS'

html_theme = "default"
html_theme_options = {
  "nosidebar": "true",
}
html_domain_indices = False
html_use_index = False

sys.path.insert(0, os.path.abspath('src'))
