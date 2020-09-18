from flask_testing import TestCase
from flask import current_app, url_for
#Se importa la aplicacion de Flask
from main import app

class MainTest(TestCase):
    # Se implementa el metodo create_app que vive en la clase TestCase y tiene que regresar una aplicacion de Flask
    def create_app(self):
        app.config['TESTING'] = True # Se configura la aplicacion para testing
        app.config['WTF_CSRF_ENABLED'] = False # Se indica que no se va a utilizar el CSRF( Cross-site request forgery o falsificación de petición en sitios cruzados) de las formas porque en este caso no existe una sesion activa del usuario
        
        return app

    # El primer Test es para probar que la app de Flask existe
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    # El segundo Test es para probar que la app se encuentra en modo Testing
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    # El tercer Test es para probar que index redirige a hello
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('hello'))

    # El cuarto Test es para probar que al hacer un GET de hello el servidor esta enviando una respuesta 200 o una respuesta OK
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))

        self.assert200(response)

    # El quinto Test es para probar que al hacer un POST en hello el servidor traiga el error 405
    def test_hello_post(self):

        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    # El sexto Test es para probar que el Blueprint esta creado y registrado
    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    # El septimo Test es para probar que en la ruta auth existe login y al hacer GET el servidor envia una respuesta 200
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    
    # El octavo Test es para probar que el login esta rendereando correctamente
    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))

        self.assertTemplateUsed('login.html')


    # El noveno Test es para probar que al hacer POST en login redirige a index
    def test_auth_login_post(self):

        fake_form = {
        'username': 'fake',
        'password': 'fake-password'
        }

        response = self.client.post(url_for('auth.login'), data= fake_form)
        self.assertRedirects(response, url_for('index'))