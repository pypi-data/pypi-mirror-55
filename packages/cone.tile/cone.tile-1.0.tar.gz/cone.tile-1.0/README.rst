Tiles for use in pyramid framework
==================================

This package provides rendering snippets of markup organized as tiles for the
pyramid framework.

A tile is a piece of web application, i.e. a form, a navigation, etc.

Splitting your application in such small and logic application parts makes it
easy to re-use this application, simplifies application AJAXification and
the use of same application parts in different manners.

.. image:: https://img.shields.io/pypi/v/cone.tile.svg
    :target: https://pypi.python.org/pypi/cone.tile
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/cone.tile.svg
    :target: https://pypi.python.org/pypi/cone.tile
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/bluedynamics/cone.tile.svg?branch=master
    :target: https://travis-ci.org/bluedynamics/cone.tile

.. image:: https://coveralls.io/repos/github/bluedynamics/cone.tile/badge.svg?branch=master
    :target: https://coveralls.io/github/bluedynamics/cone.tile?branch=master


Usage
=====


Register tiles
--------------

A tile is registered similar to a pyramid view. Registration is done with the
the ``cone.tile.tile`` decorator on classes.

.. code-block:: python

    from cone.tile import tile
    from cone.tile import Tile

    @tile(
        name='b_tile',
        path='package:browser/templates/b_tile.pt',
        permission='view',
        strict=False)
    class BTile(Tile):
        pass

There also exists a ``cone.tile.register_tile`` function. It should not be used
directly any more. ``tile`` decorator attaches this function to venusian for
deferred tile registration.

.. code-block:: python

    from cone.tile import register_tile

    register_tile(
        name='a_tile',
        path='package:browser/templates/a_tile.pt',
        permission='view')

``tile`` decorator accepts the following arguments:

**name**
    Identifier of the tile (for later lookup).

**path**
    Either relative path to the template or absolute path or path prefixed
    by the absolute package name delimeted by ':'. If ``path`` is used
    ``attribute`` is ignored.

**attribute**
    Attribute on the given _class to be used to render the tile. Defaults to
    ``render``.

**interface**
    Interface or class of the pyramid model the tile is registered for.

**class_**
    Class to be used to render the tile. usally ``cone.tile.Tile`` or a
    subclass of. Promises to implement ``cone.tile.ITile``. When the ``tile``
    decorator is used, the decorated class is expected as tile implementation.

**permission**
    Enables security checking for this tile. Defaults to ``view``. If set to
    ``None`` security checks are disabled.

**strict**
    Wether to raise ``Forbidden`` or not if rendering is not permitted.
    Defaults to ``True``. If set to ``False`` the exception is consumed and an
    empty unicode string is returned.

Tiles can be overwritten later while application initialization by just
registering it again. This is useful for application theming and customization.


Rendering tiles
---------------

Tile rendering with the ``render_tile`` function

.. code-block:: python

    from cone.tile import render_tile
    rendered = render_tile(model, request, name)

Inside templates which are bound to the tile, more tiles can be rendered on
current model and request via ``tile``

.. code-block:: html

    <tal:sometile replace="structure tile('tilename')" />


The Tile
--------

A tile is similar to what's known in the zope world as content provider.

Before rendering of the tile is done, the ``prepare`` function is called which
can be used to load data or whatever.

Further, the ``show`` flag is considered (which might have been set in the
``prepare`` function) and rendering is skipped if it evaluates to ``False``.


More on rendering
-----------------

There are helper functions for rendering which pass the tile renderer to
templates for invoking child tiles and consider redirections.

The tile class provides a redirect function, which expects either a string
containing a URL or a ``webob.exc.HTTPFound`` instance. This causes rendering
of remaining tiles to be skipped and ``request.environ['redirect']`` to be set.

**cone.tile.render_template**
    Render template. Passes tile renderer to template. Considers redirection.
    Returns empty string if redirection found.

**cone.tile.render_template_to_response**
    Render template to response. Passes tile renderer to template. Considers
    redirection. Returns HTTPFound instance if redirection found, otherwise
    rendered response.

**cone.tile.render_to_response**
    Renders some result to the response considering redirection. Returns
    HTTPFound instance if redirection found, otherwise rendered response.


Contributors
============

- Robert Niederreiter <rnix [at] squarewave [dot] at>

- Jens Klein <jens [at] bluedynamics [dot] com>

- Attila Olah
