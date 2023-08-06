from pyramid_chameleon.zpt import ZPTTemplateRenderer
from pyramid.config.views import preserve_view_attrs
from pyramid.httpexceptions import HTTPForbidden
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.interfaces import IAuthorizationPolicy
from pyramid.interfaces import IDebugLogger
from pyramid.interfaces import IRequest
from pyramid.interfaces import IResponseFactory
from pyramid.interfaces import ISecuredView
from pyramid.interfaces import IViewClassifier
from pyramid.path import caller_package
from pyramid.renderers import RendererHelper
from pyramid_chameleon.renderer import template_renderer_factory
from pyramid.threadlocal import get_current_registry
try:  # pragma: no coverage
    from urllib import quote
except ImportError:  # pragma: no coverage
    from urllib.parse import quote
from webob import Response
from webob.exc import HTTPFound
from zope.component import ComponentLookupError
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer
try:  # pragma: no coverage
    import html
except ImportError:  # pragma: no coverage
    import cgi as html
import os
import sys
import traceback
import venusian


IS_PY2 = sys.version_info[0] < 3


class ITile(Interface):
    """Renders some HTML snippet.
    """
    name = Attribute(u"The name under which this tile is registered.")
    show = Attribute(u"Flag wether to render the tile.")

    def __call__(model, request):
        """Renders the tile.

        It's intended to work this way: First it calls its own prepare method,
        then it checks its own show attribute. If this returns True it renders
        the template in the context of the ITile implementing class instance.
        """

    def prepare():
        """Prepares the tile.

        I.e. fetch data to display ...
        """


def _update_kw(**kw):
    if not ('request' in kw and 'model' in kw):
        raise ValueError('Expected kwargs missing: model, request.')
    kw.update({'tile': TileRenderer(kw['model'], kw['request'])})
    return kw


def _redirect(kw):
    if kw['request'].environ.get('redirect'):
        return True
    return False


def render_template(path, **kw):
    """Render template considering redirect flag.
    """
    kw = _update_kw(**kw)
    if _redirect(kw):
        return u''
    if not (':' in path or os.path.isabs(path)):
        raise ValueError('Relative path not supported: {}'.format(path))
    info = RendererHelper(name=path, registry=kw['request'].registry)
    renderer = template_renderer_factory(info, ZPTTemplateRenderer)
    try:
        return renderer(kw, {})
    except Exception:
        etype, value, tb = sys.exc_info()
        msg = 'Error while rendering tile template.\n{}'.format(
            ''.join(traceback.format_exception(etype, value, tb))
        )
        logger = kw['request'].registry.getUtility(IDebugLogger)
        logger.debug(msg)
        raise


def render_template_to_response(path, **kw):
    """Render template to response considering redirect flag.
    """
    kw = _update_kw(**kw)
    kw['request'].environ['redirect'] = None
    info = RendererHelper(name=path, registry=kw['request'].registry)
    renderer = template_renderer_factory(info, ZPTTemplateRenderer)
    result = renderer(kw, {})
    if _redirect(kw):
        redirect = kw['request'].environ['redirect']
        if isinstance(redirect, HTTPFound):
            return redirect
        return HTTPFound(location=redirect)
    response_factory = kw['request'].registry.queryUtility(
        IResponseFactory,
        default=Response)
    return response_factory(result)


def render_to_response(request, result):
    """Render result to response considering redirect flag.
    """
    if _redirect(kw={'request': request}):
        redirect = request.environ['redirect']
        if isinstance(redirect, HTTPFound):
            return redirect
        return HTTPFound(location=redirect)
    response_factory = request.registry.queryUtility(
        IResponseFactory,
        default=Response)
    return response_factory(result)


def render_tile(model, request, name, catch_errors=True):
    """Render a tile.

    Intended usage is in application code.

    ``model``
        application model aka context

    ``request``
        the current request

    ``name``
        name of the requested tile

    ``catch_errors``
        if set to False, ComponentLookupError will be propagated, otherwise it
        will be catched and the error message will be returned as the result
    """
    if not catch_errors:
        return request.registry.getMultiAdapter(
            (model, request),
            ITile,
            name=name)
    try:
        return request.registry.getMultiAdapter(
            (model, request),
            ITile,
            name=name)
    except ComponentLookupError as e:
        # XXX: ComponentLookupError appears even if another error causes tile
        #      __call__ to fail.
        settings = request.registry.settings
        if settings.get('debug_authorization', False):
            msg = u"Error in rendering_tile: {}".format(str(e))
            logger = request.registry.getUtility(IDebugLogger)
            logger.debug(msg)
        err_msg = str(e).decode('utf-8') if IS_PY2 else str(e)
        return u"Tile with name '{}' not found:<br /><pre>{}</pre>".format(
            name, html.escape(err_msg))


class TileRenderer(object):
    """Render a tile.

    Intended usage is as instance in template code.
    """

    def __init__(self, model, request):
        self.model = model
        self.request = request

    def __call__(self, name):
        return render_tile(self.model, self.request, name)


@implementer(ITile)
class Tile(object):
    """Tile class.
    """

    name = None
    """Name of this tile as string.
    """

    path = None
    """Path to template related to this tile as string. Expected in the form
    ``packagename:template.pt``.
    """

    attribute = 'render'
    """Name of function used to render this tile if no path set. Defaults to
    ``render``
    """

    def __init__(self, path=None, attribute=None, name=None):
        """Construct tile.

        @param path: Path to template as string.
        @param attribute: Name of function used to render this tile if no path
        set. Defaults to ``render``.
        @param name: Name of this tile as string.
        """
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if attribute is not None:
            self.attribute = attribute

    def __call__(self, model, request):
        """Render tile.

        * Calls ``prepare`` function
        * Check ``show`` flag and returns empty string if ``True``
        * Check template ``path`` and renders template with tile as context
          if set
        * Looks up function on self by ``attribute`` name and use it for tile
          rendering if no template path set.
        * Check whether redirection has been triggered some when while
          processing and return empty string if so, otherwide return rendered
          result.

        @param model: tile related model
        @param request: pyramid request
        @return string: rendered result
        """
        self.model = model
        self.request = request
        self.prepare()
        if not self.show:
            return u''
        if self.path:
            result = render_template(
                self.path,
                request=request,
                model=model,
                context=self)
        else:
            renderer = getattr(self, self.attribute)
            result = renderer()
        if request.environ.get('redirect'):
            return u''
        return result

    @property
    def show(self):
        """Flag whether this tile should be displayed. Defaults to ``True``
        """
        return True

    def prepare(self):
        """Function which can be used for preparation if desired before
        rendering this tile. Does nothing by default.
        """
        pass

    def render(self):
        """Default rendering function for this tile if no template path set.
        """
        raise NotImplementedError('Base Tile does not implement ``render``')

    def redirect(self, redirect):
        """Given param is either a string containing a URL or a HTTPFound
        instance.

        Why do we need a redirect in a tile?

        A tile is not always rendered to the response, form tiles i.e.
        might perform redirection.
        """
        self.request.environ['redirect'] = redirect

    @property
    def nodeurl(self):
        """XXX: move out from here
        """
        # XXX: see cone.app.browser.utils, not imported in order not to
        # depend on it, as this is supposed to move anyway
        rp = [p for p in self.model.path if p is not None]
        # XXX: replacing with '__s_l_a_s_h__' is a total hack, will be removed
        #      once cone.ugm is ported, which depends on this foo
        rp = [quote(p.replace('/', '__s_l_a_s_h__')) for p in rp]
        return '/'.join([self.request.application_url] + rp)


def _secure_tile(tile, permission, authn_policy, authz_policy, strict):
    """wraps tile and does security checks.
    """
    wrapped_tile = tile
    if authn_policy and authz_policy and (permission is not None):
        def _permitted(context, request):
            principals = authn_policy.effective_principals(request)
            return authz_policy.permits(context, principals, permission)

        def _secured_tile(context, request):
            result = _permitted(context, request)
            if result:
                return tile(context, request)
            msg = getattr(
                request,
                'authdebug_message',
                'Unauthorized: tile {} failed permission check'.format(tile)
            )
            if strict:
                raise HTTPForbidden(msg, result=result)
            settings = request.registry.settings
            if settings.get('debug_authorization', False):
                logger = request.registry.getUtility(IDebugLogger)
                logger.debug(msg)
            return u''
        _secured_tile.__call_permissive__ = tile
        _secured_tile.__permitted__ = _permitted
        _secured_tile.__permission__ = permission
        wrapped_tile = _secured_tile
    preserve_view_attrs(tile, wrapped_tile)
    return wrapped_tile


# Registration
def register_tile(name=None, path=None, attribute=None, interface=Interface,
                  class_=Tile, permission='view', strict=True, _level=2):
    """Registers a tile.

    ``name``
        Identifier of the tile (for later lookup). If name is None, it is
        taken from given tile class_. If name still None, an exception
        is raised.

    ``path``
        Either relative path to the template or absolute path or path prefixed
        by the absolute package name delimeted by ':'. If ``path`` is used
        ``attribute`` is ignored.

    ``attribute``
        Function name on the given class_ to be used to render the tile.

    ``interface``
        Interface or Class of the pyramid model the tile is registered for.

    ``class_``
        Class which implements ``cone.tile.ITile``. Normally ``cone.tile.Tile``
        or subclass of it.

    ``permission``
        Enables security checking for this tile. Defaults to ``view``. If set to
        ``None`` security checks are disabled.

    ``strict``
        Wether to raise ``Forbidden`` or not. Defaults to ``True``. If set to
        ``False`` the exception is consumed and an empty unicode string is
        returned.

    ``_level``
        is a bit special to make doctests pass the magic path-detection.
        you must never touch it in application code.
    """
    if name is None:
        name = class_.name
    if name is None:
        raise ValueError((
            'Tile ``name`` must be either given at registration time '
            'or set on given tile class: {}'
        ).format(str(class_)))
    if path and not (':' in path or os.path.isabs(path)):
        path = '{}:{}'.format(caller_package(_level).__name__, path)
    tile = class_(path=path, attribute=attribute, name=name)
    registry = get_current_registry()
    registered = registry.adapters.registered
    unregister = registry.adapters.unregister
    logger = registry.getUtility(IDebugLogger)
    if permission is not None:
        authn_policy = registry.queryUtility(IAuthenticationPolicy)
        authz_policy = registry.queryUtility(IAuthorizationPolicy)
        tile = _secure_tile(
            tile,
            permission,
            authn_policy,
            authz_policy,
            strict)
        exists = registered(
            (IViewClassifier, IRequest, interface),
            ISecuredView,
            name=name)
        if exists:
            msg = u"Unregister secured view for '{}' with name '{}'".format(
                str(interface), name)
            logger.debug(msg)
            unregister(
                (IViewClassifier, IRequest, interface),
                ISecuredView,
                name=name)
        registry.registerAdapter(
            tile,
            (IViewClassifier, IRequest, interface),
            ISecuredView,
            name)
    exists = registered((interface, IRequest), ITile, name=name)
    if exists:
        msg = u"Unregister tile for '{}' with name '{}'".format(
            str(interface), name)
        logger.debug(msg)
        unregister((interface, IRequest), ITile, name=name)
    registry.registerAdapter(
        tile,
        [interface, IRequest],
        ITile,
        name,
        event=False)


class tile(object):
    """Decorator to register classes and functions as tiles.
    """
    venusian = venusian  # for testing injection

    def __init__(self, name=None, path=None, attribute=None,
                 interface=Interface, permission='view',
                 strict=True, _level=2):
        """See ``register_tile`` for details on the other parameters.
        """
        self.name = name
        if path and not (':' in path or os.path.isabs(path)):
            path = '{}:{}'.format(caller_package(_level).__name__, path)
        self.path = path
        self.attribute = attribute
        self.interface = interface
        self.permission = permission
        self.strict = strict

    def __call__(self, ob):
        kw = dict(
            name=self.name,
            path=self.path,
            attribute=self.attribute,
            interface=self.interface,
            class_=ob,
            permission=self.permission,
            strict=self.strict
        )

        def callback(context, name, ob):
            register_tile(**kw)
        self.venusian.attach(ob, callback, category='pyramid', depth=1)
        return ob
