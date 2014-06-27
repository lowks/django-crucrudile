"""A route is an implementation of the abstract class Entity that
yields URL patterns made from its attributes. In the code, this is
represented by subclassing :class:`django_crucrudile.entity.Entity`
and providing a generator in ``patterns()``, yielding URL patterns
made from the route attributes. When route classes provide
:func:`django_crucrudile.entities.Entity.patterns`, it makes them
become concrete implementations of the Entity abstract class. Route
classes themselves are abstract by nature and need a definition of the
abstract function :func:`Route.get_callback`.

This module contains two abstract route classes (they are not usable
as such, but provide the base attributes and functions for route
objects) :

 - :class:`Route` : the "main" abstract route class, provides
   :func:`Route.patterns`, yielding patterns made from the route
   metadata and using the callback returned by implementations of the
   abstract function :func:`Route.get_callback`.
 - :class:`ModelRoute` : subclasses :class:`Route`, store model from
   arguments when instantiating, and provides functions to get route
   metadata from the model

These two abstract classes are used to provide three concrete
implementations, that take specific metadata (either on initialization
or as class attribute) to be able to return URL patterns :

 - :class:`CallbackRoute` : Implements :class:`Route`, provides an
   implementation of :func:`Route.get_callback` that returns the
   callback set on the route (either in :func:`CallbackRoute.__init__`
   or as class attribute).
 - :class:`ViewRoute` : Implements :class:`Route`, provides an
   implementation of :func:`Route.get_callback` that returns the a
   callback obtaining from the view class set on the route (either in
   :func:`ViewRoute.__init__` or as class attribute).
 - :class:`ModelViewRoute` : Implements :class:`ModelRoute` using
   :class:`ViewRoute`, passes the model in the view keyword arguments,
   and can be used with Django generic views. Can also be used in a
   :class:`django_crucrudile.routers.ModelRouter` store.

"""
from abc import abstractmethod

from django.conf.urls import url

from django_crucrudile.entities import Entity


class Route(Entity):
    """Abstract class for a :class:`django_crucrudile.entity.Entity` that
    yields URL patterns.

    .. warning:: Abstract class ! Subclasses should define the
                 :func:`get_callback` function.

    The URL part and URL name must be either set on class, or given at
    :func:`__init__`.

    .. inheritance-diagram:: Route
    """
    name = None
    """
    :attribute name: URL name to use for this pattern
    :type name: str
    """
    url_part = None
    """
    :attribute url_part: URL regex to use for the pattern
    :type url_part: str
    """
    auto_url_part = True
    """
    :attribute auto_url_part: Automatically set :attr:`url_part` to
                              :attr:`name` if set in class or passed
                              as :func:`__init__` argument.
    :type auto_url_part: bool
    """

    def __init__(self,
                 name=None, url_part=None,
                 **kwargs):
        """Initialize Route, check that needed attributes/arguments are
defined.

        """
        if name is not None:
            self.name = name
        elif self.name is None:
            raise ValueError(
                "No ``name`` argument provided to __init__"
                ", and no name defined as class attribute."
                " (in {})".format(self)
            )
        if url_part is not None:
            self.url_part = url_part
        elif self.url_part is None:
            if self.auto_url_part:
                self.url_part = self.name
            else:
                raise ValueError(
                    "No ``url_part`` argument provided to __init__"
                    ", no url_part defined as class attribute."
                    " (in {}), and auto_url_part is set to False."
                    "".format(self)
                )
        super().__init__(**kwargs)

    def patterns(self, parents=None, add_redirect=None):
        """Yield patterns for URL parts in :func:`get_url_parts`, using
        callback in :func:`get_callback` and URL name from
        :func:`get_url_name`.

        :argument parents: Not used in :class:`Route`'s implementation
                           of ``patterns``.
        :type parents: list of :class:`django_crucrudile.routers.Router`
        :argument add_redirect: Not used in :class:`Route`'s implementation
                           of ``patterns``.
        :type add_redirect: bool

        """
        callback = self.get_callback()
        url_name = self.get_url_name()
        for url_part in self.get_url_parts():
            yield url(
                url_part,
                callback,
                url_name
            )

    @abstractmethod
    def get_callback(self):  # pragma: no cover
        """Return callback to use in the URL pattern

        **Abstract method !** Should be defined by subclasses,
        otherwise class instantiation will fail.

        """
        pass

    def get_url_parts(self):
        """Yield URL parts (usually for different combinations of URL
        arguments). The :class:`Route` implementation of
        :func:`patterns` will yield an URL pattern for each URL part
        returned by this iterator.

        By default, yields only :attr:`url_part`.
        """
        yield self.url_part

    def get_url_name(self):
        """Return the URL name, by default from :attr:`name`"""
        return self.name


class CallbackRoute(Route):
    """Implementation of Route that requires a callback to be set either
    on the class (:attr:`callback` attribute), or to be passed in
    :func:`__init__`.

    .. inheritance-diagram:: CallbackRoute
    """
    callback = None
    """
    :attribute callback: Callback that will be used by the URL pattern
    :type callback: callable
    """
    def __init__(self,
                 callback=None,
                 **kwargs):
        """Initialize CallbackRoute, check that callable is defined at
        class-level or passed as argument

        """
        if callback is not None:
            self.callback = callback
        elif self.callback is None:
                raise ValueError(
                    "No ``callback`` argument provided to __init__"
                    ", and no callback defined as class attribute."
                    " (in {})".format(self)
                )
        super().__init__(**kwargs)

    def get_callback(self):
        """Return :attr:`callback`"""
        return self.callback


class ViewRoute(Route):
    """Implementation of Route that requires a view class to be set either
    on the class (:attr:`view_class` attribute), or to be passed in
    :func:`__init__`.

    The view class will be used to get the callback to give to the URL
    pattern.

    .. inheritance-diagram:: ViewRoute
    """

    view_class = None
    """
    :attribute view_class: View class that will be used to get the
                           callback to pass to the URL pattern
    :type callback: :class:`django.views.generic.view`
    """
    def __init__(self,
                 view_class=None,
                 **kwargs):
        """Initialize ViewRoute, check that view_class is defined at
        class-level or passed as argument.

        """
        if view_class is not None:
            self.view_class = view_class
        elif self.view_class is None:
            raise ValueError(
                "No ``view_class`` argument provided to __init__"
                ", and no view_class defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(**kwargs)

    def get_callback(self):
        """Return callback using :func:`django.generic.views.View.as_view`,
        getting arguments from :func:`get_view_kwargs`."""
        return self.view_class.as_view(
            **self.get_view_kwargs()
        )

    def get_view_kwargs(self):
        """Return arguments to use to get the view callback."""
        return {}


class ModelRoute(Route):
    """Implementation of Route that requires a model to be set either
    on the class (:attr:`model` attribute), or to be passed in
    :func:`__init__`.

    .. warning:: Abstract class ! Subclasses should define the
                 :func:`get_callback` function.

    .. inheritance-diagram:: ModelRoute
    """
    model = None
    """
    :attribute model: Model to use on the Route
    :type model: :class:`django.db.models.Model`
    """
    def __init__(self,
                 model=None,
                 **kwargs):
        """Initialize ModelRoute, check that model is defined at class-level
        or passed as argument.

        """
        if model is not None:
            self.model = model
        elif self.model is None:
            raise ValueError(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(**kwargs)

    @property
    def model_url_name(self):
        """Return the model name to be used when building the URL name"""
        return self.model._meta.model_name

    @property
    def model_url_part(self):
        """Return the model name to be used when building the URL part"""
        return self.model_url_name

    def get_url_parts(self):
        """Yield an URL part built using :class:`ModelRoute`
        :func:`model_url_part` and :class:`Route`
        :attr:`Route.url_part`.

        """
        yield "^{}/{}$".format(self.model_url_part, self.url_part)

    def get_url_name(self):
        """Return the URL name built using :class:`ModelRoute`
        :func:`model_url_name` and :class:`Route`
        :attr:`Route.name`.

        """
        return "{}-{}".format(self.model_url_name, self.name)


class ModelViewRoute(ViewRoute, ModelRoute):
    """Combine :class:`ViewRoute` and :class:`ModelRoute` to make a view
    that can easily be used with a model and a generic view.

    Also provide :func:`make_for_view`, that helpes building
    subclasses of this class for a given view class.

    .. inheritance-diagram:: ModelViewRoute
    """
    def __init__(self, *args, **kwargs):
        # TODO: Experimental!
        super().__init__(*args, **kwargs)
        self.redirect = self.get_url_name()

    @classmethod
    def make_for_view(cls, view_class, **kwargs):
        """Return a subclass of this class, setting the ``view_class``
        argument at class-level.

        This is useful when combined with
        :func:`django_crucrudile.entity.store.EntityStore.register_class`,
        as it only accepts classes (in opposition to
        :func:`django_crucrudile.entity.store.EntityStore.register`).

        """
        view_name = view_class.__name__
        if view_name.endswith('View'):
            view_name = view_name[:-4]
        route_name = "{}Route".format(view_name)

        kwargs['view_class'] = view_class
        kwargs['name'] = view_name.lower()

        return type(
            route_name,
            (cls,),
            kwargs
        )

    def get_view_kwargs(self):
        """Make the view use :attr:`ModelRoute.model`.

        This is the effective combination of :class:`ModelRoute` and
        :class:`ViewRoute`.

        """
        return {'model': self.model}
