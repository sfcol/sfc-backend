'''
Module providing access to the Box API
'''

import openapi_client
import requests
import logging

from openapi_client.rest import ApiException
from uuid import uuid4

from ..transferobjects.lockerdata import LockerAddress, LockerTransferObject, LockerContact, GpsCoordinates, LockerCompartmentSpecification, LockerCompartmentInventory
from ..transferobjects.shipment import CreateShipmentData, Shipment
from .errors import ShipmentCreationFailedException

logger = logging.getLogger(__name__)

class BoxApiClientService:
    '''
    Class encapsulating access to the Box API
    '''

    TOKEN_ENDPOINT = "https://auth.demo.box.deutschebahn.com/auth/realms/demo-box/protocol/openid-connect/token"
    CLIENT_ID = "d955dfb0-2097-468e-a3d7-116fe2870f3f"
    CLIENT_SECRET = "9dd8c4c5-dee9-469e-81d9-1433377f8fa0"


    # Our own affiliate ID (generated)
    _api_token = None

    # Configure OAuth2 access token for authorization: DEMO_Environment
    configuration = openapi_client.Configuration(
        host="https://api.demo.box.deutschebahn.com/v1"
    ) 

    @staticmethod
    def _get_access_token(token_endpoint, client_id, client_secret):
        """
        Get OAUTH client_credentials flow token
        :param token_endpoint:
        :param client_id:
        :param client_secret:
        :return:
        """
        r = requests.post(token_endpoint,
                        data=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}',
                        headers={"Content-Type": "application/x-www-form-urlencoded"})
        if r.status_code != 200:
            raise Exception("Unable to get token!")
        
        return r.json().get("access_token")

    @staticmethod
    def _map_shipment_create_data(shipment_data: CreateShipmentData):
        '''
        Map the data for a new shipment
        '''
        locker_delivery_order_request= {
                "affiliateReferenceId": str(uuid4()),
                "lockerLocationId": shipment_data.starting_locker_id,
                "shipped_item": {
                    "shippedItemType": "PACKAGED",
                    "forAccessibility": False,
                    "weight": 100,
                    "length": 200,
                    "height": 200,
                    "depth": 200,
                    "labelId": shipment_data.shipped_item.labelId
                },
                "courier": "DEMO",
                "deliveryMode": "NOT_GUARANTEED",
                "transactionType": "STANDARD_ORDER"
            }
    
        return locker_delivery_order_request

    @staticmethod
    def _map_create_response(response):
        '''
        Map the received response to our strutures
        '''
        shipment_response = Shipment()

        shipment_response.shipment_id = response.transaction_id
        shipment_response.shipment_status = response.transaction_state

        return shipment_response

    @staticmethod
    def create_shipment(shipment_data: CreateShipmentData):
        '''
        Create a shipment
        '''
        if BoxApiClientService._api_token is None:
            BoxApiClientService._api_token = BoxApiClientService._get_access_token(BoxApiClientService.TOKEN_ENDPOINT, BoxApiClientService.CLIENT_ID, BoxApiClientService.CLIENT_SECRET)
            BoxApiClientService.configuration.access_token = BoxApiClientService._api_token

        with openapi_client.ApiClient(BoxApiClientService.configuration) as api_client:
            api_instance = openapi_client.BoxAPIApi(api_client)

            shipment_request_data = BoxApiClientService._map_shipment_create_data(shipment_data)

            try:
                response = api_instance.start_new_order(locker_delivery_order_request=shipment_request_data)
                shipment_response = BoxApiClientService._map_create_response(response)
                return shipment_response
            except ApiException as apiError:
                logger.error("Failed to call API", exc_info=apiError)
                raise ShipmentCreationFailedException("API reported error during shipment creation")

    @staticmethod
    def get_locations_from_api():
        if BoxApiClientService._api_token is None:
            BoxApiClientService._api_token = BoxApiClientService._get_access_token(BoxApiClientService.TOKEN_ENDPOINT, BoxApiClientService.CLIENT_ID, BoxApiClientService.CLIENT_SECRET)
            BoxApiClientService.configuration.access_token = BoxApiClientService._api_token

        with openapi_client.ApiClient(BoxApiClientService.configuration) as api_client:
            api_instance = openapi_client.BoxAPIApi(api_client)
            locations = api_instance.get_all_locker_locations()

            mapped_results = [BoxApiClientService.map_location_results(result) for result in locations.results]

            return mapped_results

    @staticmethod
    def find_locker_from_api(latitude, longitude, radius):
        if BoxApiClientService._api_token is None:
            BoxApiClientService._api_token = BoxApiClientService._get_access_token(BoxApiClientService.TOKEN_ENDPOINT, BoxApiClientService.CLIENT_ID, BoxApiClientService.CLIENT_SECRET)
            BoxApiClientService.configuration.access_token = BoxApiClientService._api_token

        with openapi_client.ApiClient(BoxApiClientService.configuration) as api_client:
            api_instance = openapi_client.BoxAPIApi(api_client)
            locations = api_instance.get_locker_locations_nearby_geoposition(latitude, longitude, radius=radius)

            mapped_results = [BoxApiClientService.map_location_results(result) for result in locations]

            return mapped_results
    
    @staticmethod
    def find_locker_services_from_api(location_id):
        if BoxApiClientService._api_token is None:
            BoxApiClientService._api_token = BoxApiClientService._get_access_token(BoxApiClientService.TOKEN_ENDPOINT,
                                                                                BoxApiClientService.CLIENT_ID,
                                                                                BoxApiClientService.CLIENT_SECRET)
            BoxApiClientService.configuration.access_token = BoxApiClientService._api_token
        with openapi_client.ApiClient(BoxApiClientService.configuration) as api_client:
            api_instance = openapi_client.BoxAPIApi(api_client)
            services = api_instance.get_locker_location_available_services(location_id=location_id)
            # mapped_results = [BoxApiClientService.map_location_results(result) for result in locations]
            return services

    @staticmethod
    def map_location_results(result):
        '''
        Map from API output to our models
        '''
        lockerObject = LockerTransferObject()
        lockerObject.location_id = result.location_id
        lockerObject.description = result.description
        services = BoxApiClientService.find_locker_services_from_api(lockerObject.location_id)
        # parse contact
        locker_contact = LockerContact()
        locker_contact.email_address = services.contact_email_address
        locker_contact.phone = services.contact_phone_number
        lockerObject.contact = locker_contact
        locker_address = LockerAddress()
        locker_address.publicName = services.public_locker_name
        lockerObject.address = locker_address
        lockerObject.is_public = services.is_public
        compartment_list = []
        for compartments in services.supported_compartments:
            inventory = LockerCompartmentInventory()
            spec = LockerCompartmentSpecification()
            spec.max_weigth = compartments.max_weight
            spec.length = compartments.dimension.length
            spec.height = compartments.dimension.height
            spec.depth = compartments.dimension.depth
            spec.size_type = compartments.dimension.description
            inventory.compartment_specification = spec
            inventory.quantityTotal = compartments.quantity_total
            inventory.quantityAvailable = compartments.quantity_accessible
            compartment_list.append(inventory)
        lockerObject.compartments = compartment_list
        coordinates = GpsCoordinates()
        coordinates.latitude = result.latitude
        coordinates.longitude = result.longitude
        coordinates.altitude = result.altitude
        coordinates.accuracy = result.accuracy
        lockerObject.geolocation = coordinates
        return lockerObject
