from dataclasses import dataclass
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from wsgiref.simple_server import make_server


@dataclass
class Drink:
    name: str

    def __json__(self, request):
        return {"name": self.name}


@view_config(route_name="drinks", renderer="json", request_method="GET", openapi=True)
def list(request) -> type:
    sake = Drink(name="sake")
    return [sake]


if __name__ == "__main__":
    with Configurator() as config:
        config.include("pyramid_openapi3")
        config.pyramid_openapi3_spec("openapi.yaml", route="/api/v1/openapi.yaml")
        config.pyramid_openapi3_add_explorer(route="/api/v1/")
        config.add_route("drinks", "/api/v1/drinks/")
        config.scan()
        app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 8080, app)
    server.serve_forever()
