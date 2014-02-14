from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import FormView

from sortable_listview import SortableListView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin, SelectRelatedMixin

class TemplateView(AuthMixin, TemplateView):
    pass

class ListView(AuthMixin, ModelInfoMixin, SortableListView, SelectRelatedMixin):
    template_name_suffix = '_list'
    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        suffix = self.template_name_suffix

        names.append("%s/object%s.html" % (custom_app_path or self.model._meta.app_label, suffix))
        raise Exception("test")
        return names

class DetailView(AuthMixin, ModelInfoMixin, DetailView):
    template_name_suffix = '_detail'
    def get_template_names(self):
        names = super(DetailView, self).get_template_names()
        suffix = self.template_name_suffix

        names.append("%s/object%s.html" % (self.model._meta.app_label, suffix))
        return names

class FormView(AuthMixin, FormView):
    pass

class HomeView(TemplateView):
    pass
