from flask import request, abort, g
import jwt
import inspect

from .FlaskJwtRouter import FlaskJwtRouter


class JwtRoutes(FlaskJwtRouter):
    white_list_routes = []
    _api_name = None  # JWT_ROUTER_API_NAME
    """
        :example
            white_list_routes = [
                ("GET", "/users"),
                ("POST", f"api/v1/complaints"),
                ("PUT", f"api/v1/visitor_emails"),
                ("DELETE", f"api/v1/spam"),
            ]
    """
    def __init__(self, app=None, **kwargs):
        super().__init__(app, **kwargs)

        self.auth_model = FlaskJwtRouter.set_entity_model(kwargs)
        self.white_list_routes = getattr(self.config, "WHITE_LIST_ROUTES", [])
        if self.app is not None:
            self._init_app()

    def _init_app(self):
        """
        :return: None
        """
        # Initiate middleware
        self.app.before_request(self._before_middleware)

    def _prefix_api_name(self, w_routes=[]):
        """
        If the config has JWT_ROUTER_API_NAME defined then
        update each white listed route with an api name
        :example: "/user" -> "/api/v1/user"
        :param w_routes:
        :return List[str]:
        """
        api_name = self.config.get("JWT_ROUTER_API_NAME")
        if not api_name:
            return w_routes
        # Prepend the api name to the white listed route
        named_white_routes = []
        for route_name in w_routes:
            verb, path = route_name
            named_white_routes.append((verb, f"{api_name}{path}"))
        return named_white_routes

    def _allow_public_routes(self, white_routes):
        """
        Create a list of tuples ie [("POST", "/users")] as public routes.
        Returns False if current route and verb are white listed.
        :param flask_request:
        :param white_routes: List[Tuple]:
        :returns bool:
        """
        method = request.method
        path = request.path
        white_routes = self._prefix_api_name(white_routes)
        for white_route in white_routes:
            if method == white_route[0] and path == white_route[1]:
                return False
        return True

    def _before_middleware(self):
        """
            TODO exception from jwt
            - Checks the headers contain a Bearer string OR params.
            - Checks to see that the route is white listed.
        :return: Callable or None
        """
        if self._allow_public_routes(self.config["WHITE_LIST_ROUTES"]):
            try:
                if request.args.get("auth"):
                    token = request.args.get("auth")
                else:
                    bearer = request.headers.get("Authorization")
                    token = bearer.split("Bearer ")[1]
            except Exception as err:
                print("here----->", self.config)
                self.logger.error(err)
                return abort(401)

            try:
                decoded_token = jwt.decode(token, self.get_secret_key(), algorithms="HS256")
            except Exception as err:
                self.logger.error(err)
                return abort(401)

            if self.auth_model is not None:
                try:
                    g.entity = self._update_model_entity(decoded_token)
                except Exception as err:
                    self.logger.error(err)
                    return abort(401)

    def _get_user_from_auth_model(self, entity_id):
        """
        :param entity_id:
        :return: Any - TODO correct return type
        """
        result = self.auth_model.query.filter_by(**{f"{self.get_entity_key()}": entity_id}).one()
        return result

    def _update_model_entity(self, token):
        """
        :param token:
        :return: user Dict[str, Any] or None - TODO correct type
        """
        self._set_auth_model()
        result = self.auth_model.f_j_r_get_entity(token[f"{self.get_entity_key()}"])
        return result

    def _set_auth_model(self):
        """
        :return: None
        """
        methods = inspect.getmembers(self.auth_model, predicate=inspect.ismethod)
        for m in methods:
            if m == "f_j_r_get_entity":
                raise ValueError("Please change the name of your Entity get method.")
        setattr(self.auth_model, "f_j_r_get_entity", self._get_user_from_auth_model)
