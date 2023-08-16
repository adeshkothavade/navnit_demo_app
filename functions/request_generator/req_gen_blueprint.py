import azure.functions as func
import logging
import json
from . import hdfc_generator

bp = func.Blueprint()

@bp.route(route="generateRequest")
def generate_request(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Starting generate_request")

    req_body = req.get_json()
    provider_name = req_body.get("provider_name")
    generated_request_body = {}
    if provider_name == "HDFC":
        generated_request_body = hdfc_generator.generate_request()

    logging.info("generate_request successfully completed")
    return func.HttpResponse(
        json.dumps(generated_request_body),
        status_code = 200
        )