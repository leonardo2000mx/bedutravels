import graphene

from graphene_django.types import DjangoObjectType
from .models import User, Zona, Tour, Opinion, Salida


class UserType(DjangoObjectType):
    """ Tipo de dato para manejar el tipo User """
    class Meta:
        # Se relaciona con el origen de la data en models.User
        model = User

class ZonaType(DjangoObjectType):
    """ Tipo de dato para manejar el tipo Zona """
    class Meta:
        # Se relaciona con el origen de la data en models.Zona
        model = Zona


class Query(graphene.ObjectType):
    """ Definición de las respuestas a las consultas posibles """

    # Se definen los posibles campos en las consultas
    all_users = graphene.List(UserType)  # allUsers
    all_zonas = graphene.List(ZonaType)  # allZonas

    # Se define las respuestas para cada campo definido
    def resolve_all_users(self, info, **kwargs):
        # Responde con la lista de todos registros
        return User.objects.all()

    def resolve_all_zonas(self, info, **kwargs):
        # Responde con la lista de todos registros
        return Zona.objects.all()

# Se crea un esquema que hace uso de la clase Query


class CrearZona(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        descripcion = graphene.String()
        latitud = graphene.Decimal()
        longitud = graphene.Decimal()

    zona = graphene.Field(ZonaType)

    def mutate(self, info, nombre, descripcion=None, latitud=None,
    longitud=None):
        zona = Zona(
            
                nombre=nombre,
                descripcion=descripcion,
                latitud=latitud,
                longitud=longitud
            )
        zona.save()
        return CrearZona(zona=zona)

class EliminarZona(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try:
            zona = Zona.objects.get(pk=id)
            zona.delete()
            ok = True
        except Zona.DoesNotExist:
            ok = False

        return EliminarZona(ok=ok)  
    

class Mutaciones(graphene.ObjectType):
    crear_zona = CrearZona.Field()
    eliminar_zona = EliminarZona.Field()

schema = graphene.Schema(query=Query,mutation=Mutaciones)