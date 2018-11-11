# An example RESTful API app showcasing the power of pyramid_openapi3

This repository showcase how to use the [pyramid_openapi3]() Pyramid add-on for building robust RESTful APIs. With only a few lines of code you get automatic validation of requests and responses against an OpenAPI v3 schema and Swagger "try-it-out" documentation for your API.

## How to run

```bash
$ pipenv install
$ pipenv run python run.py
$ open http://localhost:8080/api/v1/
```

Then use the Swagger interface to discover the API and the `Try it out` button to run through a few request/response scenarios.

For example:
* Get all TODO items using the GET request.
* Adding a new TODO item using the POST request.
* Getting a 400 BadRequest response for an empty POST request
* Getting a 400 BadRequest response for a POST request when `title` is too long (over 40 characters).
* Getting a 400 BadRequest response for a POST request when there is an additional field:

    ```json
    {"title": "walk the dog", "foo": "bar"}s
    ```

## Further read

* More information about the library providing the integration between OpenAPI specs and Pyramid, more advanced features and design defence, is available in the [niteoweb/pyramid_openapi3](https://github.com/niteoweb/pyramid_openapi3) repository.

* More validators for fields are listed in the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#properties) document. You can use Regex as well.

* If you like the scaffolding of this project (pipenv, Makefile, etc.) you might also want to check out the [niteoweb/makefiles](https://github.com/niteoweb/makefiles) repository.

* For an idea of a fully-fledged production OpenApi specification, check out [WooCart's spec](https://app.woocart.com/api/v1/openapi.yaml).
