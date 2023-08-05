from .connect import connection
from .Errors import *


class Weaviate:

    # New weaviate client
    def __init__(self, url, auth_client_secret=""):
        # TODO check if url is right form
        self.connection = connection.Connection(url=url, auth_client_secret=auth_client_secret)


    # Takes a dict describing the thing and adds it to weaviate
    # The thing is associated with the class given in class_name
    # If an uuid is given the thing will be created under this uuid
    def create_thing(self, thing, class_name, uuid=None):

        weaviate_obj = {
            "class": class_name,
            "schema": thing
        }
        if uuid is not None:
            weaviate_obj["id"] = uuid

        try:
            response = self.connection.run_rest("/things", connection.REST_METHOD_POST, weaviate_obj)
        except ConnectionError as conn_err:
            print("Connection error, thing was not added to weaviate: " + str(conn_err))
            raise ConnectionError


        if response.status_code != 200: #TODO catch all status codes
            try:
                if 'already exists' in response.json()['error'][0]['message']:
                    raise ThingAlreadyExistsException
            except KeyError:
                pass
            except Exception as e:
                print('Unexepected exception: ' + str(e))
                raise Exception

            print("WARNING: STATUS CODE WAS NOT 200 but " + str(response.status_code) + " with: " + str(
                response.json()))

            raise UnexpectedStatusCodeException

    # Add a property reference to a thing
    # thing_uuid the thing that should have the reference as part of its properties
    # the name of the property within the thing
    # The beacon dict takes the form: [{
    #                     "beacon": "weaviate://localhost/things/uuid",
    #                     ...
    #                 }]
    def add_property_reference_to_thing(self, thing_uuid, property_name, property_beacons):
        path = "/things/" + thing_uuid + "/references/" + property_name
        try:
            response = self.connection.run_rest(path, property_beacons, connection.REST_METHOD_POST)
        except ConnectionError as conn_err:
            print("Connection error, reference was not added to weaviate: " + str(conn_err))
            raise ConnectionError

        if response.status_code == 200:
            return
        elif response.status_code == 401:
            raise UnauthorizedRequest401Exception
        elif response.status_code == 403:
            raise ForbiddenRequest403Exception
        elif response.status_code == 422:
            raise SemanticError422Exception
        elif response.status_code == 500:
            raise ServerError500Exception(response.json())
        else:
            raise UnexpectedStatusCodeException