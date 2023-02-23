from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:7002/0')

@celery_app.task()
def registar_log(usuario, fecha):
    with open('log_signin.txt', 'a+') as file:
        file.write('{} - Inicio de sesión: {}\n'.format(usuario, fecha))