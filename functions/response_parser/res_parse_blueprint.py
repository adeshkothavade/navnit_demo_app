import azure.functions as func
import logging
import json
from . import response_parser
from abc import ABC, abstractmethod


bp = func.Blueprint()

class get_Response(ABC):
    @abstractmethod
    def get_service_provider(self,data):
        pass



class icici_response(get_Response):
    def get_service_provider(self,data):
        mapping_file = 'mappings/icici_mapping.json'
        spec_file='specifications/icici_to_standard_spec.json'
        return response_parser.get_data(mapping_file, spec_file,data)
    
class hdfc_response(get_Response):
    def get_service_provider(self,data):
        mapping_file = 'mappings/hdfc_mapping.json'
        spec_file='specifications/hdfc_to_standard_spec.json'
        return response_parser.get_data(mapping_file, spec_file,data)

# mapping providers to their classes
def get_json_data(provider_name,data):
    provider_mapping = {
        "ICICI":icici_response,
        "HDFC":hdfc_response
    }

    provider_class = provider_mapping.get(provider_name)
    if provider_class:
        response = provider_class()
        return response.get_service_provider(data)
    else:
        raise ValueError("Not a valid Provider Name!")

@bp.route(route="parseResponse")
def parse_response(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    provider_name = req_body.get("Supplier_Name")
    if not provider_name:
        return func.HttpResponse("Please provide a valid Provider Name.")
    
    parsed_json_data = get_json_data(provider_name,req_body)

    return func.HttpResponse(
        json.dumps(parsed_json_data),
        status_code=200

    )
        
    

    