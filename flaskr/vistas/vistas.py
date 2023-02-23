from flask_restful import Resource
from ..modelos import db, Cancion, Album, Usuario, CancionSchema, AlbumSchema, UsuarioSchema
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from datetime import datetime
from ..tareas import registar_log

cancion_schema = CancionSchema()
album_shema = AlbumSchema()
usuario_shema = UsuarioSchema()


class VistaCanciones(Resource):
    def get(self):
        return [cancion_schema.dump(c) for c in Cancion.query.all()]

    @jwt_required()
    def post(self):
        nueva_cancion = Cancion(
            titulo=request.json['titulo'],
            minutos=request.json['minutos'],
            segundos=request.json['segundos'],
            interprete=request.json['interprete']
        )
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)


class VistaCancion(Resource):

    @jwt_required()
    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    @jwt_required()
    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get('titulo', cancion.titulo)
        cancion.minutos = request.json.get('minutos', cancion.minutos)
        cancion.segundos = request.json.get('segundos', cancion.segundos)
        cancion.interprete = request.json.get('interprete', cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    @jwt_required()
    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '', 200


class VistaAlbumsUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_shema.dump(a) for a in usuario.albumes]

    @jwt_required()
    def post(self, id_usuario):
        new_album = Album(
            titulo=request.json['titulo'],
            anio=request.json['anio'],
            descripcion=request.json['descripcion'],
            medio=request.json['medio']
        )
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(new_album)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return 'El usuario ya tiene un album con el mismo nombre', 409

        return album_shema.dump(new_album)


class VistaAlbum(Resource):
    @jwt_required()
    def get(self, id_album):
        return album_shema.dump(Album.query.get_or_404(id_album))

    @jwt_required()
    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get('titulo', album.titulo)
        album.anio = request.json.get('anio', album.anio)
        album.descripcion = request.json.get('descripcion', album.descripcion)
        album.medio = request.json.get('medio', album.medio)
        db.session.commit()
        return album_shema.dump(album)

    @jwt_required()
    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '', 200


class VistaCancionesAlbum(Resource):
    def post(self, id_album):
        album = Album.query.get_or_404(id_album)

        if "id_cancion" in request.json.keys():
            new_cancion = Cancion.query.get(request.json["id_cancion"])
            if new_cancion is not None:
                album.canciones.append(new_cancion)
                db.session.commit()
            else:
                return 'Canción errónea', 404
        else:
            new_cancion = Cancion(
                titulo=request.json['titulo'],
                minutos=request.json['minutos'],
                segundos=request.json['segundos'],
                interprete=request.json['interprete']
            )
            album.canciones.append(new_cancion)
        db.session.commit()
        return cancion_schema.dump(new_cancion)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]


class VistaSignIn(Resource):

    def post(self):
        new_usuario = Usuario(
            nombre=request.json["nombre"],
            contrasena=request.json["contrasena"]
        )
        access_token = create_access_token(identity=request.json['nombre'])
        db.session.add(new_usuario)
        db.session.commit()
        return {'mensaje': 'Usuario creado correctamente', 'accessToken': access_token}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get('contrasena', usuario.contrasena)
        db.session.commit()
        return usuario_shema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):
    def post(self):
        u_nombre = request.json["nombre"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(
            nombre=u_nombre, contrasena=u_contrasena).all()
        if usuario:
            registar_log.delay(u_nombre, datetime.utcnow())
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Usuario no encontrado'}, 401
