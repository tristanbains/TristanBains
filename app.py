from flask import Flask, render_template, make_response, request, render_template_string,redirect,url_for,jsonify #, Markup
from markupsafe import Markup 
from flask_flatpages import FlatPages, pygmented_markdown
from flask_frozen import Freezer
from flask_minify import minify 
import markdown
from yaml import safe_load


import pandas as pd
from datetime import date, timedelta, datetime
import subprocess
import numpy as np
import sys, os, re, shutil, glob
import copy
from urllib.parse import urljoin

# ----- SETTINGS -----

lang = 'EN'

data_theme = 'emerald'

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'



# ----- HELP FUNCTIONS -----


# prerendering function so that html in md files is recognized:
def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    prerendered_body = markdown.markdown(prerendered_body, extensions=['fenced_code','toc', 'attr_list','tables'])
    # prerendered_body = html_edit_svgs(prerendered_body)
    # prerendered_body = html_add_code_classes(prerendered_body)
    return pygmented_markdown(prerendered_body)


# ----- DATA -----



dict_website = {
    'NL':{
        'url':'https://www.tristanbains.nl',
        'google_analytics_id':None,
        },
    'EN':{
        'url':'https://www.tristanbains.com',
        'google_analytics_id':None,
    }
}

lang_other = 'EN' if lang=='NL' else 'NL'

# dict_website_lang = dict_website[lang]


# ----- FLASK -----


app = Flask(__name__)
app.config['FLATPAGES_HTML_RENDERER'] = prerender_jinja
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True

# initializing minify for html, js and cssless 
minify(app=app, html=True, js=True, cssless=True)


@app.context_processor
def dict_all():
    return dict(
        lang = lang,
        lang_other = lang_other,
        dict_website = dict_website
    )


# ----- ROUTES -----


@app.route('/')
def index():
    url_other = urljoin(dict_website[lang_other]['url'],request.path)
    return render_template(
        'index.html',
        url_other=url_other)


@app.route("/<path:path>/")
def page(path):
    path_lang = os.path.join(lang,path)
    page = pages.get_or_404(path_lang)
    url_other = urljoin(dict_website[lang_other]['url'],request.path)
    # url_other = dict_website[lang_other]['url']+request.path
    return render_template(
        'page.html',
        page=page,
        url_other=url_other
    )


# ----- BUILD -----


if __name__ =='__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.config['FREEZER_DESTINATION'] = 'build_'+lang
        app.config['DEBUG'] = True
        freezer.freeze()
        print(f"Building {app.config['FREEZER_DESTINATION']} for TristanBains")

        # folder_build = app.config['FREEZER_DESTINATION']
        # create_sitemap_xml(base_url=base_url,folder_build=folder_build)
        # create_robots_txt(base_url=base_url,folder_build=folder_build)
    else:
        # app.run(port=5000)
        app.run(host='0.0.0.0',debug=True,port=5000)