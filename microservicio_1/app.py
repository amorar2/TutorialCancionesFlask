from microservicio_1 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)


class ViewScore(Resource):
    def post(self, id_cancion):
        content = requests.get(
            'http://localhost:5000/cancion/{}'.format(id_cancion))
        if content.status_code != 200:
            return content.json(), content.status_code
        else:
            cancion = content.json()
            cancion['puntaje'] = request.json['puntaje']
            # args = {cancion, }
            return json.dumps(cancion)


api.add_resource(ViewScore, '/cancion/<int:id_cancion>/puntuar')
