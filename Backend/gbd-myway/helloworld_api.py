import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


package = 'Hello'


class Moment(messages.Message):
    name = messages.StringField(1)
    lat = messages.StringField(2)
    lon = messages.StringField(3)
    desc = messages.StringField(4)
    url = messages.StringField(5)

class Route(messages.Message):
    moments = messages.MessageField(Moment, 1, repeated=True)


STORED_MOMENTS = Route(moments=[
    Moment(name = "Aeropuerto BsAs", lat="-34.822491", lon="-58.5349216", desc="LLegando a Argentina =D"),
    Moment(name = "Belushi Bar", lat="-34.5865761", lon="-58.4332076", desc="Que excelente lugar, chicas hermosas!"),
    Moment(name = "Esquina Libertad", lat="-34.7003212", lon="-58.6834717", desc="Increible las cosas que te encuentras por aca"),
    Moment(name = "Obelisco", lat="-34.6037019", lon="-58.381873", desc="Plaza de la republica!"),
    Moment(name = "Parque de la cuidad", lat="-34.6732276", lon="-58.4501549", desc="La torre espacial esta DE MIEDO"),
])


@endpoints.api(name='mywayapi', version='v1')
class MyWayApi(remote.Service):
    """MyWay API v1."""
    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Route,
                      path='route/{id}', http_method='GET',
                      name='moments.listMoments')
    def greetings_list(self, unused_request):
        try:
            return STORED_MOMENTS
        except(IndexError, TypeError):
            raise endpoints.NotFoundException('Route %s not found.' %
                                                (request.id,))

    

    @endpoints.method(ID_RESOURCE, Moment,
                      path='moment/{id}', http_method='GET',
                      name='moments.getMoment')
    def greeting_get(self, request):
        try:
            return STORED_MOMENTS.moments[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Share %s not found.' %
                                              (request.id,))

APPLICATION = endpoints.api_server([MyWayApi])