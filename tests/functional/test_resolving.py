from nose.tools import assert_equal
from django.conf.urls import url, include

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .routers import base_router
from .models import (
    DocumentModel,
    GroupModel,
    PhaseModel,
    EntityModel,
    InterfaceModel,
    CommentModel,
    TaskModel
)


MODEL_NAME_DICT = {
    u'documents': (DocumentModel,
                  GroupModel,
                  PhaseModel),
    u'entities': (EntityModel,
                 InterfaceModel),
    None: (CommentModel,
           TaskModel)
}

ACTION_NAME_DICT = {
    u'list': ListView,
    u'detail': DetailView,
    u'create': CreateView,
    u'update': UpdateView,
    u'delete': DeleteView,
}


class ResolveTestCase(object):
    router = base_router

    def setUp(self):
        self.patterns = list(self.router.patterns())
        self.url = url(
            u'^/',
            include(self.patterns),
        )

    def _test_model_view(self,
                         model_name, action_name, view_name,
                         prefix):
        if prefix:
            path = u"/{}/{}/{}".format(prefix, model_name, action_name)
        else:
            path = u"/{}/{}".format(model_name, action_name)

        match = self.url.resolve(
            path
        )

        assert_equal(
            match.func.__name__,
            view_name
        )

        assert_equal(
            match.url_name,
            u"{}-{}".format(model_name, action_name)
        )

        assert_equal(
            match.namespace,
            (prefix or u'')
        )

    def test_model_views(self):
        for prefix, models in MODEL_NAME_DICT.items():
            for model_class in models:
                model_name = model_class._meta.model_name
                for action_name, view_class in ACTION_NAME_DICT.items():
                    view_name = view_class.__name__
                    yield (
                        self._test_model_view,
                        model_name, action_name, view_name, prefix
                    )
