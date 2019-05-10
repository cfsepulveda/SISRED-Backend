from django.test import TestCase
from .models import Version, RED, ProyectoConectate, Metadata, Perfil, Recurso, RolAsignado, Rol, ComentarioMultimedia, \
    Comentario
from django.contrib.auth.models import User
import datetime
import json
from django.forms.models import model_to_dict
from sisred_app.views.views_equipo4 import createNotification
from .models import User, Perfil, RED, Fase, ProyectoConectate, Recurso, NotificacionTipo, Rol, RolAsignado, \
    Notificacion
from django.contrib.auth.models import User
import json


# Create your tests here.
class SisredTestCase(TestCase):
    def test_find_user_by_identification_number(self):
        user_model1 = User.objects.create_user(username='test1', password='kd8wke-DE34', first_name='test1',
                                               last_name='test1', email='test1@test.com')

        profile1 = Perfil.objects.create(usuario=user_model1, numero_identificacion="1100960499", estado="1")

        response = self.client.get('/api/habilitar-usuario/' + str(profile1.numero_identificacion))
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['username'], 'test1')

    def test_update_user_state_in_sisred(self):
        user_model1 = User.objects.create_user(username='test1', password='kd8wke-DE34', first_name='test1',
                                               last_name='test1', email='test1@test.com')

        profile1 = Perfil.objects.create(usuario=user_model1, numero_identificacion="1100960499", estado="1")

        response = self.client.put('/api/habilitar-usuario/' + str(profile1.numero_identificacion))
        current_data = json.loads(response.content)
            
        self.assertEqual(current_data[0]['estado_sisred'], 1)

    def test_update_ready_state_red(self):
        red = RED.objects.create(id_conectate="S0001", nombre="null", nombre_corto="null", descripcion="1 video",
                                 fecha_inicio="2019-12-31", fecha_cierre="2019-12-31", fecha_creacion="2019-12-31",
                                 porcentaje_avance="0", tipo="Sin definir", solicitante="PR0011(Sandra)",
                                 horas_estimadas="0", horas_trabajadas="0", proyecto_conectate_id="1")

        response = self.client.put('/api/habilitar-red/' + str(red.id_conectate))
        current_data = json.loads(response.content)
        print(current_data)

        self.assertEqual(current_data[0]['listo'], True)

    def test_create_closing_comment(self):
        user = User.objects.create_user(username='admin', password='123456', email='admin@admin.com',
                                        first_name='Adriana',
                                        last_name='Vargas')
        perfil = Perfil.objects.create(id_conectate=1, usuario=user, estado=1, estado_sisred=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')

        self.red = RED.objects.create(id_conectate='1', nombre='Video', descripcion=' ',
                                      tipo='mp4', solicitante='MISO', proyecto_conectate=proyecto)

        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        com_mul = ComentarioMultimedia.objects.create(x1=1, y1=5, x2=3, y2=5)

        url = '/api/comentario-cierre/'
        response = self.client.post(url, json.dumps(
            {
                "contenido": "comentario de cierre para area 2 ---> prueba",
                "version": self.version.id,
                "comentario_multimedia": com_mul.id,
                "esCierre": "True"
            }), content_type='application/json')

        current_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_data['esCierre'], True)

