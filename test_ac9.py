import io
import unittest

from flask import message_flashed
from urllib.parse import urlparse
from unittest.mock import patch
from server import app


class AbstractTest(object):

    flashed_messages = []

    def _add_flash_message(self, app, message, category):
        self.flashed_messages.append((message, category))

    def setUp(self):
        message_flashed.connect(self._add_flash_message)
        self.client = app.test_client()

    def tearDown(self):
        message_flashed.disconnect(self._add_flash_message)

    def post(self, url, dados):
        return self.client.post(
            url,
            data=dados,
            follow_redirects=False
        )

    def assertMensagemPassada(self, mensagem):
        for _message, _category in self.flashed_messages:
            if _message == mensagem:
                return True

        raise AssertionError(
            "Mensagem '{}' não foi passada na requisição".format(mensagem)
        )

    def assertRedirecionou(self, resposta, url):
        if resposta.status_code != 302:
            raise AssertionError(
                '''
                Era esperado um redirecionamento (302), mas o status foi {}
                '''.format(
                    resposta.status_code
                )
            )
        location = urlparse(resposta.location).path
        if location != url:
            raise AssertionError(
                '''
                Deveria redirecionar para {} mas foi para {}
                '''.format(
                    url,
                    location
                )
            )
        return True

    def assertNaoRedirecionou(self, resposta):
        if resposta.status_code != 200:
            raise AssertionError(
                '''
                Era esperado um status ok (200), mas o status foi {}
                '''.format(
                    resposta.status_code
                )
            )


class TestEntrarForm(AbstractTest, unittest.TestCase):
    def test_post_correto(self):
        resposta = self.post(
            '/entrar/',
            dict(
                usuario='usuario',
                senha='teste123*'
            )
        )
        self.assertRedirecionou(resposta, '/')

    def test_post_sem_usuario(self):
        resposta = self.post(
            '/entrar/',
            dict(
                usuario='',
                senha='teste123*'
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Usuário é obrigatório!')

    def test_post_sem_senha(self):
        resposta = self.post(
            '/entrar/',
            dict(
                usuario='usuario',
                senha=''
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Senha é obrigatória!')

    def test_post_senha_incorreta(self):
        resposta = self.post(
            '/entrar/',
            dict(
                usuario='usuario',
                senha='teste1'
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Usuário e/ou senha incorretos!')


class TestEsqueciForm(AbstractTest, unittest.TestCase):

    def test_post_correto(self):
        resposta = self.post(
            '/esqueci-a-senha/',
            dict(email='teste@email.com')
        )
        self.assertRedirecionou(resposta, '/redefinir-a-senha/')

    def test_post_incorreto(self):
        resposta = self.client.post(
            "/esqueci-a-senha/",
            data=dict(email=""),
            follow_redirects=False
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('E-mail é obrigatório!')


class TestRecuperarForm(AbstractTest, unittest.TestCase):

    def test_post_correto(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='teste123*',
                senha2='teste123*'
            ))
        self.assertRedirecionou(resposta, '/')

    def test_post_sem_senha(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='',
                senha2='teste123*'
            ))
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Senha é obrigatória!')

    def test_post_sem_senha2(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='teste123*',
                senha2=''
            ))
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Confirmação de senha é obrigatória!')

    def test_post_senhas_diferentes(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='teste123*',
                senha2='teste1234'
            ))
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Senha e confirmação não estão iguais!')

    def test_post_senha_sem_numero(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='teste*',
                senha2='teste*'
            ))
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Senha deve ter ao menos um número!')

    def test_post_senha_sem_alfanumerico(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='teste123',
                senha2='teste123'
            ))
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada(
            'Senha deve ter ao menos um caracter alfanumérico!'
        )

    def test_post_senha_pequena(self):
        resposta = self.post(
            '/redefinir-a-senha/',
            dict(
                senha='t12*',
                senha2='t12*'
            ))
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Senha deve ter ao menos 5 caracteres!')


class TestContatoForm(AbstractTest, unittest.TestCase):

    def test_post_correto(self):
        with patch('sys.stdout', io.StringIO()) as fake_out:
            resposta = self.post(
                '/contato/',
                dict(
                    nome='Professor Yuri',
                    email='teste@email.com',
                    assunto='B',
                    mensagem='Olá formulário de contato'
                )
            )
            self.assertRedirecionou(resposta, '/agradecimento/')
            self.assertIn(
                'Envio de e-mail de Contato:',
                fake_out.getvalue()
            )
            self.assertIn(
                '===========================',
                fake_out.getvalue()
            )
            self.assertIn(
                'Nome: Professor Yuri',
                fake_out.getvalue()
            )
            self.assertIn(
                'E-mail: teste@email.com',
                fake_out.getvalue()
            )
            self.assertIn(
                'Assunto: Bug',
                fake_out.getvalue()
            )
            self.assertIn(
                'Como Conheceu: Nenhum informado.',
                fake_out.getvalue()
            )
            self.assertIn(
                'Olá formulário de contato',
                fake_out.getvalue()
            )
            self.assertIn(
                'Mensagem:',
                fake_out.getvalue()
            )
            self.assertIn(
                '+++++++++++++++++++++++++++',
                fake_out.getvalue()
            )

    def test_post_sem_nome(self):
        resposta = self.post(
            '/contato/',
            dict(
                nome='',
                email='teste@email.com',
                assunto='B',
                mensagem='Olá formulário de contato'
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Nome completo é obrigatório!')

    def test_post_sem_email(self):
        resposta = self.post(
            '/contato/',
            dict(
                nome='Professor Yuri',
                email='',
                assunto='B',
                mensagem='Olá formulário de contato'
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('E-mail é obrigatório!')

    def test_post_sem_assunto(self):
        resposta = self.post(
            '/contato/',
            dict(
                nome='Professor Yuri',
                email='teste@email.com',
                assunto='',
                mensagem='Olá formulário de contato'
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Assunto é obrigatório!')

    def test_post_sem_mensagem(self):
        resposta = self.post(
            '/contato/',
            dict(
                nome='Professor Yuri',
                email='teste@email.com',
                assunto='B',
                mensagem=''
            )
        )
        self.assertNaoRedirecionou(resposta)
        self.assertMensagemPassada('Mensagem é obrigatória!')
