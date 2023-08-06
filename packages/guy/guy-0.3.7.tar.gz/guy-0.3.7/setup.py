# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['guy']
install_requires = \
['tornado>=6.0,<7.0']

setup_kwargs = {
    'name': 'guy',
    'version': '0.3.7',
    'description': 'A simple module for making HTML GUI applications with python3',
    'long_description': '**GUY** is like [wuy](https://github.com/manatlan/wuy)\n\n(just started the [documentation](https://manatlan.github.io/guy/) !!)\n\nIt\'s the new name, but it is the same thing ... but:\n\n* more robust (complete rewriting from scratch, without design flaws)\n* works on Android (with kivy/buildozer)\n\nYou can build a "py3/html" app which will work on **windows**, on **mac**, on **linux** or on **android** (it should be easy to port to iOS too) ! and can act as classic **web server** (can serve to multiple clients/browsers)\n\nHere is the same simple **guy**\'s app :\n<p align="center">\n    <table>\n        <tr>\n            <td valign="top">\n                On Ubuntu<br>\n<img src="https://github.com/manatlan/guy/blob/master/wiki/shot_ubuntu.png" width="300" border="1" style="border:1px solid black"/>             </td>\n            <td valign="top">\n                On Android9<br>\n    <img src="https://github.com/manatlan/guy/blob/master/wiki/shot_android9.png" width="300" border="1" style="border:1px solid black"/>                \n           </td>\n        </tr>\n    </table>\n\n</p>\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'url': 'https://github.com/manatlan/guy',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
