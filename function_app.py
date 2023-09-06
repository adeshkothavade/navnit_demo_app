import azure.functions as func
import logging
from functions.response_parser import res_parse_blueprint
from functions.request_generator import req_gen_blueprint

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(res_parse_blueprint.bp)
app.register_functions(req_gen_blueprint.bp)