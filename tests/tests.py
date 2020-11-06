import unittest
import random
from unittest import mock

from werkzeug.datastructures import MultiDict

from form import IMCForm
from main import imc_calc, app


class IIMCFormulaCalcCase(unittest.TestCase):

    def test_imc_abaixo_do_peso(self):
        peso = random.uniform(50, 55)
        altura = random.uniform(1.85, 2)
        imc = imc_calc(peso, altura)
        self.assertLess(imc, 17.0)

    def test_imc_peso_normal(self):
        peso = random.uniform(66, 72.5)
        altura = random.uniform(1.7, 1.75)
        imc = imc_calc(peso, altura)
        self.assertGreaterEqual(imc, 18.5)
        self.assertLess(imc, 25.0)

    def test_imc_obesidade(self):
        peso = random.uniform(120, 150)
        altura = random.uniform(1.5, 1.7)
        imc = imc_calc(peso, altura)
        self.assertGreaterEqual(imc, 40.0)


class TestRotasCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @mock.patch("main.IMCForm")
    @mock.patch("main.redirect")
    def test_imc_validate_campo_incorreto(self, mock_redirect, MockICMForm):
        error_message = "DEU RUIM"
        mock_redirect.return_value = error_message
        form = MockICMForm()

        form.validate_on_submit.return_value = False

        resp = self.app.post('/imc', data=dict(altura=12, peso="fdsafs"))
        self.assertEqual(error_message, resp.data.decode('utf-8'))


class TestIMCFormCase(unittest.TestCase):

    altura_random = random.uniform(0.5, 2.3)
    peso_random = random.uniform(40, 150)

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False

    def test_atributo_em_string(self):
        with app.test_request_context():
            form = IMCForm(MultiDict([('altura', self.altura_random), ('peso', "fsda"), ('submit', True)]))
            self.assertFalse(form.validate())

    def test_valores_minimos(self):
        with app.test_request_context():
            form = IMCForm(MultiDict([('altura', 0.1), ('peso', self.peso_random), ('submit', True)]))
            self.assertFalse(form.validate())

            form = IMCForm(MultiDict([('altura', -1), ('peso', self.peso_random), ('submit', True)]))
            self.assertFalse(form.validate())

            form = IMCForm(MultiDict([('altura', 0.5), ('peso', self.peso_random), ('submit', True)]))
            self.assertTrue(form.validate())

            form = IMCForm(MultiDict([('altura', self.altura_random), ('peso', -1), ('submit', True)]))
            self.assertFalse(form.validate())

    def test_atributos_validos(self):
        with app.test_request_context():
            form = IMCForm(MultiDict([('altura', self.altura_random), ('peso', self.peso_random), ('submit', True)]))
            self.assertTrue(form.validate())
