import azure.functions as func
import logging
from functions.request_generator import req_gen_blueprint

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(req_gen_blueprint.bp)