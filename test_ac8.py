import os
import unittest
from flask import template_rendered
from server import app


class AbstractViewCase(object):

    templates = []
    _defaultLinks = [
        '/',
        '/entrar/',
        '/contato/',
        '/sobre-a-impacta/',
        '/inscrever/'
    ]

    longMessage = False

    def _registrar_template(self, app, template, context):
        if len(self.templates) > 0:
            self.templates = []
        self.templates.append((template, context))

    def _links(self):
        return []

    def setUp(self):
        template_rendered.connect(self._registrar_template)
        self.template_str = open(
            os.path.join(
                os.path.dirname(__file__),
                'templates/'+self._template)
            ).read()
        self.client = app.test_client()
        self.response = self.client.get(self._url)
        self.conteudo = self.response.data.decode('UTF-8')

    def tearDown(self):
        template_rendered.disconnect(self._registrar_template)

    def test_ok(self):
        self.assertEqual(
            200,
            self.response.status_code,
            msg="Caminho {} não respondeu com 200".format(self._url)
        )

    def test_links_pagina(self):
        links = self._defaultLinks + self._links()
        for link in links:
            self.assertIn(
                link,
                self.conteudo,
                msg="Link de endereço {} não encontrado!".format(link)
            )

    def test_template_base(self):
        self.assertIn(
            'base.html',
            self.template_str,
            msg="Não foi encontrado o base.html no template {}".format(
                self._template
            )
        )

    def test_template_usado(self):
        templates = []
        for template, context in self.templates:
            templates.append(template)
            if getattr(template, 'name') == self._template:
                return True
        raise AssertionError(
            'Template {} não foi usado. Templates utilizados: {}'.format(
                self._template,
                templates
            )
        )


class TestHomeView(AbstractViewCase, unittest.TestCase):

    _url = '/'
    _template = 'index.html'


class TestContatoView(AbstractViewCase, unittest.TestCase):

    _url = '/contato/'
    _template = 'contato.html'


class TestEntrarView(AbstractViewCase, unittest.TestCase):

    _url = '/entrar/'
    _template = 'entrar.html'

    def _links(self):
        return [
            '/esqueci-a-senha/'
        ]


class TestEsqueciView(AbstractViewCase, unittest.TestCase):

    _url = '/esqueci-a-senha/'
    _template = 'esqueci.html'


class TestInscricaoView(AbstractViewCase, unittest.TestCase):

    _url = '/inscrever/'
    _template = 'inscrever.html'


class TestRedefinirView(AbstractViewCase, unittest.TestCase):

    _url = '/redefinir-a-senha/'
    _template = 'recuperar.html'


class TestSobreView(AbstractViewCase, unittest.TestCase):

    _url = '/sobre-a-impacta/'
    _template = 'sobre.html'


class TestAgradecimentoView(AbstractViewCase, unittest.TestCase):

    _url = '/agradecimento/'
    _template = 'agradecimento.html'
