text_selector
===============================

A Custom Jupyter Widget for selecting part of text and assingning it one of tags.

Usage:
------

An example of use case can be found in [example.ipynb](https://github.com/randomunrandom/text_selector/blob/master/example.ipynb)
Note^ if you have less than 10 tags you don't need to pass colors, otherwise you have too.

Installation
------------

For a development installation (requires npm) run in terminal:

    $ git clone https://github.com/randomunrandom/text_selector.git
    $ cd text_selector
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix text_selector
    $ jupyter nbextension enable --py --sys-prefix text_selector

Docker
------

To create and start docker container run:

    $ git clone https://github.com/randomunrandom/text_selector.git
    $ cd text_selector
    $ docker build -t text_selector .
    $ docker run -p 8888:8888 -it --rm --name text_selector text_selector

if port 8888 is occupied change ${port} to any available port

    $ docker run -p ${port}:8888 -it --rm --name text_selector text_selector
