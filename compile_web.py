# -*- coding: utf-8 -*-
'''Compile professional homepage

This script compiles the CS20 homepage.
It uses Jinja2 templates. There is a general template in /templates
The individual files are made with template inheritance in the /pagesrc directory.
For each template in "pagesrc", the script looks for a python module of the
same name in "pagepy" and calles it's "data" method.
That method is expected to return a dictionary, which is then passed to the jinja2
template to fill in values.
Not all pages require input data, thus if no matching module is found, no data is passed to
jinja.

The navigation bar is defined in templates/basic.html and it is assumed that
the number of files in /src matches what is defined in basic.html.

This script needs to be executed in the exact directory where it is now,
because it uses relative input paths.

'''
from __future__ import print_function

import argparse
from glob import glob
import os
import shutil
import importlib

from jinja2 import Environment, FileSystemLoader, select_autoescape


parser = argparse.ArgumentParser(description='Generate webpages for CS20. We want to generate statics pages for simplicity, but might read in some database (e.g. the database of abstracts) when doing so.')
parser.add_argument('outpath',
                    help='base directory for output')

args = parser.parse_args()

# Generate html
env = Environment(loader=FileSystemLoader(['.']),
                  autoescape=select_autoescape(['html']))

pagelist = glob('pagesrc/*html')
''' Not foolproof!
The navigation bar is defined in templates/basic.html
and I need to sync that with the content of the src directory by hand
'''

if not os.path.exists(args.outpath):
    os.makedirs(args.outpath)

for page in pagelist:
    print("Working on {0}".format(page))
    try:
        datareader = importlib.import_module('pagepy.' + os.path.basename(page)[:-5])
        data = datareader.data()
    except ImportError:
        data = {}
    template = env.get_template(page)
    with open(os.path.join(args.outpath, os.path.basename(page)), "w") as html_out:
        html_out.write(template.render(**data))


# copy several directories verbatim
for d in ['css', 'fonts', 'images', 'js', 'icons', 'maps', 'docs']:
    outdir = os.path.join(args.outpath, d)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    filelist = glob(os.path.join(d, '*'))
    for f in filelist:
        shutil.copy(f, outdir)

# copy favicons which should live in root directory
filelist = glob(os.path.join('favicon', '*'))
for f in filelist:
    shutil.copy(f, args.outpath)

print("Done. Website is in directory: {}.".format(args.outpath))
