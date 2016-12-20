import os

from django.conf import settings
from django.template.backends.django import DjangoTemplates
from django.template.loader import get_template
from django.utils import lru_cache
from django.utils._os import upath
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

try:
    from django.template.backends.jinja2 import Jinja2
except ImportError:
    Jinja2 = None

ROOT = upath(os.path.dirname(__file__))


@lru_cache.lru_cache()
def get_default_renderer():
    renderer_class = import_string(settings.FORM_RENDERER)
    return renderer_class()


class BaseTemplateRenderer(object):
    def get_template(self, template_name):
        raise NotImplementedError('subclasses must implement get_template()')

    def render(self, template_name, context, request=None):
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()


class EngineRendererMixin(object):
    def get_template(self, template_name):
        return self.engine.get_template(template_name)

    @cached_property
    def engine(self):
        return self.backend({
            'APP_DIRS': True,
            'DIRS': [],
            'POST_APP_DIRS': [os.path.join(ROOT, self.backend.app_dirname)],
            'NAME': 'djangoforms',
            'OPTIONS': {},
        })


class DjangoTemplateRenderer(EngineRendererMixin, BaseTemplateRenderer):
    """
    Load Django templates from app directories and the built-in widget
    templates in django/forms/templates.
    """
    backend = DjangoTemplates


class Jinja2TemplateRenderer(EngineRendererMixin, BaseTemplateRenderer):
    """
    Load Jinja2 templates from app directories and the built-in widget
    templates in django/forms/jinja2.
    """
    backend = Jinja2


class ProjectTemplateRenderer(BaseTemplateRenderer):
    """
    Load templates using template.loader.get_template() which is configured
    based on settings.TEMPLATES.
    """
    def get_template(self, template_name):
        return get_template(template_name)
