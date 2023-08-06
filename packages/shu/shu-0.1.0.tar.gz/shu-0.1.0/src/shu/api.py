import logging
import os

from flask import Blueprint, url_for
from flask_restplus import Api, Resource, apidoc, Namespace
from flask_restplus.api import SwaggerView

log = logging.getLogger(__name__)


def create_api(prefix, **extra):
    # pylint: disable=unused-variable
    """Create an API with info and health endpoints.

    :param name: The name of the application; used in the generated frontend,
        and the URL prefix.
    :param config: The application configuration.

    :returns: An instance of :class:`~apian.api.CustomAPI`.
    """
    blueprint = Blueprint(prefix, __name__)
    api = CustomAPI(blueprint, title="api", prefix=prefix, doc=prefix + "/", **extra)

    ns = Namespace("Generic")

    @api.route("/health")
    class Health(Resource):
        def get(self):
            # pylint: disable=no-self-use
            """Check the health of the service"""
            return {"status": "ok"}

    return api


def create_swagger():
    swagger = apidoc.Apidoc(
        "restplus_custom_doc",
        __name__,
        template_folder="templates",
        static_folder=os.path.dirname(apidoc.__file__) + "/static",
        static_url_path="/swagger",
    )

    @swagger.add_app_template_global
    def swagger_static(filename):
        # pylint: disable=unused-variable
        return url_for("restplus_custom_doc.static", filename=filename)

    return swagger


class CustomAPI(Api):
    """
    Hack to serve swagger.json from the /api prefix.  This is a requirement for
    serving swagger-ui from behind a path-routing load balancer without
    additional proxies.
    """

    def _register_specs(self, app_or_blueprint):
        if self._add_specs:
            endpoint = str("specs")
            self._register_view(
                app_or_blueprint,
                SwaggerView,
                self.default_namespace,
                "{}/swagger.json".format(self.prefix),
                endpoint=endpoint,
                resource_class_args=(self,),
            )
            self.endpoints.add(endpoint)

    @property
    def specs_url(self):
        """Swagger URI protocol-relative."""
        return url_for(self.endpoint("specs"), _external=True, _scheme="")
