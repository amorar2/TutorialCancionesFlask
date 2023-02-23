from flaskr import create_app
from flask_restful import Api, Resource
from .modelos import db, Cancion, CancionSchema

cancion_schema = CancionSchema()

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


class ViewTablaPuntajes(Resource):
    def get(self):
        return [cancion_schema.dump(c) for c in Cancion.query.all()]

api = Api(app)
api.add_resource(ViewTablaPuntajes, '/tabla-puntajes')