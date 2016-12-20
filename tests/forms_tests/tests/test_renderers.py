import os
import unittest

from django.forms.renderers import (
    BaseTemplateRenderer, DjangoTemplateRenderer, Jinja2TemplateRenderer,
    ProjectTemplateRenderer,
)
from django.test import SimpleTestCase
from django.utils._os import upath

try:
    import jinja2
except ImportError:
    jinja2 = None


class SharedTests(object):
    expected_widget_dir = 'templates'

    def test_installed_apps_template_found(self):
        """Can find a custom template in INSTALLED_APPS."""
        renderer = self.renderer()
        # Found because forms_tests is .
        tpl = renderer.get_template('forms_tests/custom_widget.html')
        expected_path = os.path.abspath(
            os.path.join(
                upath(os.path.dirname(__file__)),
                '..',
                self.expected_widget_dir + '/forms_tests/custom_widget.html',
            )
        )
        self.assertEqual(tpl.origin.name, expected_path)


class BaseTemplateRendererTests(SimpleTestCase):

    def test_get_renderer(self):
        with self.assertRaisesMessage(NotImplementedError, 'subclasses must implement get_template()'):
            BaseTemplateRenderer().get_template('')


class DjangoTemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = DjangoTemplateRenderer


@unittest.skipIf(jinja2 is None, 'jinja2 required')
class Jinja2TemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = Jinja2TemplateRenderer
    expected_widget_dir = 'jinja2'


class ProjectTemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = ProjectTemplateRenderer
