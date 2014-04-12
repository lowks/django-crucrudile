from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.db import models

from django_crucrudile.models.mixins import (
    AutoPatternsMixin,
    make_model_mixin,
    make_model_mixins
)

from tests.views import (
    AutoPatternsMixinTestView,
    MakeModelMixinTestView,
    MakeModelMixinWithoutViewMixinTestView,
    MakeModelMixinsFirstTestView,
    MakeModelMixinsSecondTestView,
    MakeModelMixinsThirdTestView
)

class AutoPatternsMixinTestCase(TestCase):
    class AutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
        @classmethod
        def get_views(cls):
            views = super(
                AutoPatternsMixinTestCase.AutoPatternsMixinTestModel,
                cls
            ).get_views()
            views.append(AutoPatternsMixinTestView)
            return views
    class NoViewsAutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
        pass

    model_class = AutoPatternsMixinTestModel
    no_views_model_class = NoViewsAutoPatternsMixinTestModel

    def test_get_model_name(self):
        self.assertEqual(
            self.model_class.get_model_name(),
            "autopatternsmixintestmodel"
        )

    def test_get_url_namespaces(self):
        # default namespaces is application name (here, 'tests')
        #TODO: Fix test (try with no_content_types=True)
        self.assertEqual(
            self.model_class.get_url_namespaces(),
            ['tests',]
        )

    def test_get_url_name(self):
        # we use the same fake view as ModelActionMixinTestCase
        self.assertEqual(
            self.model_class.get_url_name(AutoPatternsMixinTestView),
            "tests:autopatternsmixintestmodel-auto-patterns-mixin-test"
        )

    def test_get_views(self):
        # by default get_views returns an empty list
        self.assertEqual(
            self.model_class.get_views(),
            [AutoPatternsMixinTestView, ]
        )
        self.assertEqual(
            self.no_views_model_class.get_views(),
            []
        )

    def test_get_args_by_view(self):
        # by defaults args are an empty directory, and when view is
        # not in get_views(), ImproperlyConfigured shall be raised
        try:
            self.no_views_model_class.get_args_by_view(AutoPatternsMixinTestView)
        except ImproperlyConfigured:
            raised = True
        else:
            raised = False
        finally:
            self.assertTrue(raised)

        self.assertEqual(
            self.model_class.get_args_by_view(
                AutoPatternsMixinTestView
            ),
            {}
        )

class MakeModelMixinTestCase(TestCase):
    _key_test_func = lambda arg: arg.test_callable_key
    _value_test_func = lambda arg: arg.test_callable_value
    _value_test_class_func = classmethod(_value_test_func)

    view_class = MakeModelMixinTestView
    url_func_name = 'get_make_model_mixin_test_url'
    url_func_return_value = 'tests:makemodelmixintestmodel-make-model-mixin-test'

    # data to test make_model_mixin (with extra_args argument) with
    extra_args = {'test_key' : 'test_value',
                  'test_callable_key' : _value_test_func}
    extra_args_called = {'test_key' : 'test_value',
                         'test_callable_key' : 'model_test_callable_value'}

    extra_funcs = {'test_key' : _value_test_class_func,
                   lambda arg: 'test_callable_key' : _value_test_class_func}
    extra_funcs_called = {'test_key' : 'test_value',
                          'test_callable_key' : 'model_test_callable_value'}

    def setUp(self):
        class MakeModelMixinTestModel(
                make_model_mixin(
                    self.view_class,
                ),
                models.Model):
            pass
        self.model_class = MakeModelMixinTestModel

        class ExtraArgsMakeModelMixinTestModel(
                make_model_mixin(
                    self.view_class,
                    extra_args=self.extra_args
                ),
                models.Model):
            test_callable_value = 'model_test_callable_value'
        self.extra_args_model_class = ExtraArgsMakeModelMixinTestModel

        class ExtraFuncsMakeModelMixinTestModel(
                make_model_mixin(
                    type(self.view_class.__name__,
                         (self.view_class,),
                         {'test_callable_key' : 'view_test_callable_value'}),
                    extra_funcs=self.extra_funcs
                ),
                models.Model):
            test_callable_value = 'model_test_callable_value'
        self.extra_funcs_model_class = ExtraFuncsMakeModelMixinTestModel

    def test_make_model_mixin(self):
        self.assertEqual(
            self.model_class.get_views(),
            [self.view_class, ]
        )
        self.assertEqual(
            self.model_class.get_args_by_view(
                self.view_class
            ),
            {}
        )
        self.assertTrue(
            hasattr(self.model_class,
                    self.url_func_name)
        )
        self.assertEqual(
            getattr(self.model_class,
                    self.url_func_name,
                    lambda: None)(),
            self.url_func_return_value
        )

    def test_make_model_mixin_extra_args(self):
        self.assertEqual(
            self.extra_args_model_class.get_args_by_view(
                self.view_class
            ),
            self.extra_args_called
        )

    def test_make_model_mixin_extra_funcs(self):
        for func in self.extra_funcs_called:
            self.assertTrue(hasattr(self.extra_funcs_model_class, func))
            self.assertEqual(
                getattr(self.extra_funcs_model_class,
                        func,
                        lambda arg: None)(),
                'model_test_callable_value')

class MakeModelMixinWithoutViewMixinTestCase(MakeModelMixinTestCase):
    view_class = MakeModelMixinWithoutViewMixinTestView
    url_func_name = 'get_make_model_mixin_without_view_mixin_test_url'
    url_func_return_value = 'tests:makemodelmixinwithoutviewmixintestmodel-make-model-mixin-without-view-mixin-test'

    def setUp(self):
        class MakeModelMixinWithoutViewMixinTestModel(
                make_model_mixin(
                    self.view_class,
                ),
                models.Model):
            pass
        self.model_class = MakeModelMixinWithoutViewMixinTestModel

        class ExtraArgsMakeModelMixinWithoutViewMixinTestModel(
                make_model_mixin(
                    self.view_class,
                    extra_args=self.extra_args
                ),
                models.Model):
            test_callable_value = 'model_test_callable_value'
        self.extra_args_model_class = ExtraArgsMakeModelMixinWithoutViewMixinTestModel

        class ExtraFuncsMakeModelMixinWithoutViewMixinTestModel(
                make_model_mixin(
                    type(self.view_class.__name__,
                         (self.view_class,),
                         {'test_callable_key' : 'view_test_callable_value'}),
                    extra_funcs=self.extra_funcs
                ),
                models.Model):
            test_callable_value = 'model_test_callable_value'
        self.extra_funcs_model_class = ExtraFuncsMakeModelMixinWithoutViewMixinTestModel

class MakeModelMixinsTestCase(TestCase):
    views = [MakeModelMixinsFirstTestView,
             MakeModelMixinsSecondTestView,
             MakeModelMixinsThirdTestView]

    def check_views_in_mixins(self, mixins):
        for index, mixin in enumerate(mixins):
            self.assertEqual(
                mixin.get_views(),
                [self.views[index]]
            )

    def test_make_model_mixins_1tuple(self):
        self.check_views_in_mixins(
            make_model_mixins(
                [(view,) for view in self.views]
            )
        )

    def test_make_model_mixins_2tuple(self):
        self.check_views_in_mixins(
            make_model_mixins(
                [(view,) for view in self.views]
            )
        )

    def test_make_model_mixins_3tuple(self):
        self.check_views_in_mixins(
            make_model_mixins(
                [(view,) for view in self.views]
            )
        )
