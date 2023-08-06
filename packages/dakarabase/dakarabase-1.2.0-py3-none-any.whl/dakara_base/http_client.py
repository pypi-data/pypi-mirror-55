"""HTTP client helper module

This module provides the HTTP client class `HTTPClient`, built on the requests
library. The class is designed to be used with an API which communicates with
JSON messages.  It is pretty straightforward to use:

>>> config = {
...     "url": "http://www.example.com",
...     "login": "login here",
...     "password": "password here",
... }
>>> client = HTTPClient(config, endpoint_prefix="api/")
>>> client.authenticate()
>>> data = client.get("library/songs/")
>>> client.post("library/songs", json={"title": "some title"})
"""


import logging

from furl import furl
import requests

from dakara_base.exceptions import DakaraError
from dakara_base.utils import truncate_message, create_url


logger = logging.getLogger(__name__)


def authenticated(fun):
    """Decorator that ensures the token is set

    It makes sure that the given function is called only if authenticated. If
    not authenticated, calling the function will raise a `NotAuthenticatedError`.

    Args:
        fun (function): function to decorate.

    Returns:
        function: decorated function.
    """

    def call(self, *args, **kwargs):
        if self.token is None:
            raise NotAuthenticatedError("No connection established")

        return fun(self, *args, **kwargs)

    return call


class HTTPClient:
    """HTTP client designed to work with an API

    The API must use JSON for message content.

    The client uses a token credential policy only and authenticates with a
    traditional login/password mechanism.

    Attributes:
        mute_raise (bool): if true, no exception will be raised when performing
            connections with the server (but authentication), only logged.
        server_url (str): URL of the server.
        token (str): value of the token. The token is set when successfuly
            calling `authenticate`.
        login (str): login used for authentication.
        password (str): password used for authentication.

    Args:
        config (dict): config of the server.
        endpoint_prefix (str): prefix of the endpoint, added to the URL.
        mute_raise (bool): if true, no exception will be raised when performing
            connections with the server (but authentication), only logged.

    Raises:
        ParameterError: if critical parameters cannot be found in the
            configuration.
    """

    def __init__(self, config, endpoint_prefix="", mute_raise=False):
        self.mute_raise = mute_raise

        try:
            # url
            self.server_url = create_url(**config, path=endpoint_prefix)

            # authentication
            self.token = None
            self.login = config["login"]
            self.password = config["password"]

        except KeyError as error:
            raise ParameterError(
                "Missing parameter in server config: {}".format(error)
            ) from error

    def send_request_raw(
        self,
        method,
        endpoint,
        *args,
        message_on_error="",
        function_on_error=None,
        **kwargs
    ):
        """Generic method to send requests to the server

        It takes care of errors and raises exceptions.

        Args:
            method (str): name of the HTTP method to use.
            endpoint (str): endpoint to send the request to. Will be added to
                the end of the server URL.
            message_on_error (str): message to display in logs in case of
                error. It should describe what the request was about.
            function_on_error (function): fuction called if the request is not
                successful, it will receive the response and must return an
                exception that will be raised. If not provided, a basic error
                management is done.
            Extra arguments are passed to requests' get/post/put/patch/delete
                methods.

        Returns:
            requests.models.Response: response object.

        Raises:
            MethodError: if the method is not supported.
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        # handle method function
        if not hasattr(requests, method):
            raise MethodError("Method {} not supported".format(method))

        send_method = getattr(requests, method)

        # handle message on error
        if not message_on_error:
            message_on_error = "Unable to request the server"

        # forge URL
        url = furl(self.server_url).add(path=endpoint).url
        logger.debug("Sending %s request to %s", method.upper(), url)

        try:
            # send request to the server
            response = send_method(url, *args, **kwargs)

        except requests.exceptions.RequestException as error:
            # handle connection error
            logger.error("%s, communication error", message_on_error)
            raise ResponseRequestError(
                "Error when communicating with the server: {}".format(error)
            ) from error

        # return here if the request was made without error
        if response.ok:
            return response

        # otherwise call custom error management function
        if function_on_error:
            raise function_on_error(response)

        # otherwise manage error generically
        logger.error(message_on_error)
        logger.debug(
            "Error %i: %s", response.status_code, truncate_message(response.text)
        )

        raise ResponseInvalidError(
            "Error {} when communicationg with the server: {}".format(
                response.status_code, response.text
            )
        )

    @authenticated
    def send_request(self, *args, **kwargs):
        """Generic method to send requests to the server when connected

        It adds token header for authentication and takes care of errors.
        If `mute_raise` is set, no exceptions are raised in case of error when
        communicating with the server.

        Args:
            See `send_request_raw`.

        Returns:
            requests.models.Response: response object. None if an error occurs
            when communicating with the server and `mute_raise` is set.

        Raises:
            MethodError: if the method is not supported.
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        try:
            # make the request
            return self.send_request_raw(
                *args, headers=self.get_token_header(), **kwargs
            )

        # manage request error
        except ResponseError:
            if self.mute_raise:
                return None

            raise

    def get(self, *args, **kwargs):
        """Generic method to get data on server

        Args:
            endpoint (str): endpoint to send the request to. Will be added to
                the end of the server URL.
            message_on_error (str): message to display in logs in case of
                error. It should describe what the request was about.
            function_on_error (function): fuction called if the request is not
                successful, it will receive the response and must return an
                exception that will be raised. If not provided, a basic error
                management is done.
            Extra arguments are passed to requests' get method.

        Returns:
            dict: response object from the server.

        Raises:
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        return self.get_json_from_response(self.send_request("get", *args, **kwargs))

    def post(self, *args, **kwargs):
        """Generic method to post data on server

        Args:
            endpoint (str): endpoint to send the request to. Will be added to
                the end of the server URL.
            message_on_error (str): message to display in logs in case of
                error. It should describe what the request was about.
            function_on_error (function): fuction called if the request is not
                successful, it will receive the response and must return an
                exception that will be raised. If not provided, a basic error
                management is done.
            Extra arguments are passed to requests' post method.


        Returns:
            dict: response object from the server.

        Raises:
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        return self.get_json_from_response(self.send_request("post", *args, **kwargs))

    def put(self, *args, **kwargs):
        """Generic method to put data on server

        Args:
            endpoint (str): endpoint to send the request to. Will be added to
                the end of the server URL.
            message_on_error (str): message to display in logs in case of
                error. It should describe what the request was about.
            function_on_error (function): fuction called if the request is not
                successful, it will receive the response and must return an
                exception that will be raised. If not provided, a basic error
                management is done.
            Extra arguments are passed to requests' put method.

        Returns:
            dict: response object from the server.

        Raises:
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        return self.get_json_from_response(self.send_request("put", *args, **kwargs))

    def patch(self, *args, **kwargs):
        """Generic method to patch data on server

        Args:
            endpoint (str): endpoint to send the request to. Will be added to
                the end of the server URL.
            message_on_error (str): message to display in logs in case of
                error. It should describe what the request was about.
            function_on_error (function): fuction called if the request is not
                successful, it will receive the response and must return an
                exception that will be raised. If not provided, a basic error
                management is done.
            Extra arguments are passed to requests' patch method.

        Returns:
            dict: response object from the server.

        Raises:
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        return self.get_json_from_response(self.send_request("patch", *args, **kwargs))

    def delete(self, *args, **kwargs):
        """Generic method to patch data on server

        Args:
            endpoint (str): endpoint to send the request to. Will be added to
                the end of the server URL.
            message_on_error (str): message to display in logs in case of
                error. It should describe what the request was about.
            function_on_error (function): fuction called if the request is not
                successful, it will receive the response and must return an
                exception that will be raised. If not provided, a basic error
                management is done.
            Extra arguments are passed to requests' delete method.

        Returns:
            dict: response object from the server.

        Raises:
            ResponseRequestError: for any error when communicating with the server.
            ResponseInvalidError: if the response has an error code different
                to 2**.
        """
        return self.get_json_from_response(self.send_request("delete", *args, **kwargs))

    def authenticate(self):
        """Authenticate with the server

        The authentication process relies on login/password which gives an
        authentication token. This token is stored in the instance.

        Raises:
            See `send_request_raw`.
            AuthenticationError: if the connection is denied or if any onther
                error occurs.
        """
        data = {"username": self.login, "password": self.password}

        def on_error(response):
            # manage failed connection response
            if response.status_code == 400:
                return AuthenticationError(
                    "Login to server failed, check the config file"
                )

            # manage any other error
            return AuthenticationError(
                "Unable to authenticate to the server, error {code}: {message}".format(
                    code=response.status_code, message=truncate_message(response.text)
                )
            )

        # connect to the server with login/password
        logger.debug("Authenticate to the server")
        response = self.send_request_raw(
            "post",
            "token-auth/",
            message_on_error="Unable to authenticate to the server",
            function_on_error=on_error,
            json=data,
        )

        # store token
        self.token = response.json().get("token")
        logger.info("Login to server successful")
        logger.debug("Token: %s", self.token)

    @authenticated
    def get_token_header(self):
        """Get the connection token as it should appear in the header

        Can be called only after a successful authentication.

        Returns:
            dict: formatted token.
        """
        return {"Authorization": "Token " + self.token}

    @staticmethod
    def get_json_from_response(response):
        """Parse the response of a request if possible

        Args:
            response (requests.models.Response): response of a request.

        Returns:
            dict: parsed response. None if no response was given or response
            has no content.
        """
        if response and response.text:
            return response.json()

        return None


class ResponseError(DakaraError):
    """Generic error when communicating with the server
    """


class ResponseRequestError(ResponseError):
    """Error when sending request to the server
    """


class ResponseInvalidError(ResponseError):
    """Error with the request sent to the server
    """


class AuthenticationError(ResponseInvalidError):
    """Error raised when authentication fails
    """


class ParameterError(DakaraError, ValueError):
    """Error raised when server parameters are unproperly set
    """


class MethodError(DakaraError, ValueError):
    """Error raised when using an unsupported method
    """


class NotAuthenticatedError(DakaraError):
    """Error raised when authentication is missing
    """
