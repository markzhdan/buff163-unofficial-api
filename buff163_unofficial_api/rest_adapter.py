import requests
import requests.packages
from typing import Dict
import logging
from json.decoder import JSONDecodeError
from buff163_unofficial_api.exceptions import Buff163Exception
from buff163_unofficial_api.models import Result


class RestAdapter:
    def __init__(
        self,
        hostname: str = "buff.163.com/api",
        session_cookie: str = "",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ) -> None:
        """Constructor for RestAdapter

        Args:
            hostname (str): Api url. Defaults to "buff.163.com/api".
            session_cookie (str, optional): Used for authentication. Defaults to "".
            ssl_verify (bool, optional): Set to false if having SSL/TLS cert validation issues. Defaults to True.
            logger (logging.Logger, optional): App logger. Defaults to None.
        """
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"https://{hostname}"
        self._session_cookie = session_cookie
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        """Private method for api requests (GET, POST, DELETE, etc.)

        Args:
            http_method (str): GET, POST, DELETE, etc.
            endpoint (str): URL endpoint
            ep_params (Dict, optional): Endpoint parameters. Defaults to None.
            data (Dict, optional): Data to pass to Buff163API. Defaults to None.

        Raises:
            Buff163Exception: Requests fail
            Buff163Exception: Bad JSON
            Buff163Exception: Error response code

        Returns:
            Result: status_code, message, data
        """
        full_url = self.url + endpoint
        headers = {"Cookie": self._session_cookie}

        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )
        # Performing an HTTP request and logging its details; exceptions are logged and a custom exception is raised.
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=data,
            )

        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise Buff163Exception("Request failed") from e

        # Convert JSON response to a Python object; raise and log a custom exception for JSON parsing errors
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise Buff163Exception("Bad JSON in response") from e

        # Check code is valid and data is produced
        is_login_error = data_out["code"] != "OK"
        if is_login_error:
            log_line = log_line_post.format(False, 401, "Login Required")
            self._logger.error(msg=log_line)
            raise Buff163Exception("Login is required")

        # Check response status code for success (200-299) and log accordingly.
        is_success = 299 >= response.status_code >= 200
        # log_line = log_line_post.format(
        #     is_success, response.status_code, response.reason
        # )
        if is_success:
            self._logger.debug(msg="log_line")
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise Buff163Exception(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """Sends a GET request to a specified API endpoint.

        Args:
            endpoint (str): The endpoint for the GET request.
            ep_params (Dict, optional): Parameters to include in request. Defaults to None.

        Returns:
            Result: status_code, message, data
        """
        return self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """Sends a POST request to a specified API endpoint.

        Args:
            endpoint (str): The endpoint for the POST request.
            ep_params (Dict, optional): Parameters to include in the request. Defaults to None.
            data (Dict, optional): Data passed in the request. Defaults to None.

        Returns:
            Result: status_code, message, data
        """
        return self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )

    def delete(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        """Sends a DELETE request to a specified API endpoint.

        Args:
            endpoint (str): The endpoint for the POST request.
            ep_params (Dict, optional): Parameters to include in the request. Defaults to None.
            data (Dict, optional): Data passed in the request. Defaults to None.

        Returns:
            Result: status_code, message, data
        """
        return self._do(
            http_method="DELETE", endpoint=endpoint, ep_params=ep_params, data=data
        )

    def fetch_data(self, url: str) -> bytes:
        """Private method for fetching data from url.

        Args:
            url (str): Url of fetch request.

        Raises:
            Buff163Exception: Request failure.
            Buff163Exception: Status code not valid.

        Returns:
            bytes: Data in bytes (mainly for images).
        """
        http_method = "GET"
        try:
            log_line = f"method={http_method}, url={url}"
            self._logger.debug(msg=log_line)
            response = requests.request(
                method=http_method, url=url, verify=self._ssl_verify
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise Buff163Exception(str(e)) from e

        # If status_code in 200-299 range, return byte stream, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)
        if not is_success:
            raise Buff163Exception(response.reason)
        return response.content
