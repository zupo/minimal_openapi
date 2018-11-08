from dataclasses import dataclass
from openapi_core.schema.exceptions import OpenAPIMappingError
from pyramid.config import Configurator
from pyramid.httpexceptions import exception_response
from pyramid.response import Response
from pyramid.view import view_config
from wsgiref.simple_server import make_server


@dataclass
class Drink:
    name: str

    def __json__(self, request):
        return {"name": self.name}


# fmt: off
DRINKS = [
    Drink(name="water"),
]
# fmt: on


@view_config(route_name="drinks", renderer="json", request_method="GET", openapi=True)
def list(request):
    return DRINKS


@view_config(route_name="drinks", renderer="json", request_method="POST", openapi=True)
def create(request):
    drink = Drink(name=request.openapi_validated.body.name)
    DRINKS.append(drink)
    return drink


if __name__ == "__main__":
    with Configurator() as config:
        config.include("pyramid_openapi3")
        config.pyramid_openapi3_spec("openapi.yaml", route="/api/v1/openapi.yaml")
        config.pyramid_openapi3_validation_error_view("openapi_validation_error")
        config.pyramid_openapi3_add_explorer(route="/api/v1/")
        config.add_route("drinks", "/api/v1/drinks/")
        config.scan()
        app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 8080, app)
    server.serve_forever()


def extract_error(err):
    import pdb

    pdb.set_trace()
    if isinstance(getattr(err, "original_exception", None), OpenAPIMappingError):
        return extract_error(err.original_exception)
    return err.msg


@view_config(name="openapi_validation_error")
def openapi_validation_error(context, request):
    errors = [str(err) for err in request.openapi_validated.errors]
    return exception_response(400, json_body=errors)
