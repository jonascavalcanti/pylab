import time
from typing import Any, List, Optional

import requests
from requests import Response
from requests.status_codes import codes as http_code

from .env import Env


class ClientApi:
    def __init__(self, endpoint: str, auth_header: dict):
        self.__endpoint = endpoint
        self.__auth_header = auth_header

    def get(self, path: str, params: dict = None) -> Any:
        """HTTP requets wrapper for GET verb,
          with builtin retry policy and return validation

        :param path:
            API path to call starting from SCIM endpoint root
        :param params:
            HTTP request querystring params
        """
        return self.__request_with_retries(
            http_method='GET',
            path=path,
            http_codes_expected=[http_code.ok],
            params=params)

    def post(self, path: str, data: Any) -> Optional[dict]:
        """HTTP requets wrapper for POST verb, with builtin retry policy and
            return validation

        :param path:
            API path to call starting from SCIM endpoint root
        :param data:
            HTTP request body data
        """
        return self.__request_with_retries(
            http_method='POST',
            path=path,
            http_codes_expected=[http_code.ok, http_code.created],
            data=data)

    def put(self, path: str, data: Any) -> Optional[dict]:
        """HTTP requets wrapper for PUT verb, with builtin retry policy and
        return validation

        :param path:
            API path to call starting from SCIM endpoint root
        :param data:
            HTTP request body data
        """
        return self.__request_with_retries(
            http_method='PUT',
            path=path,
            http_codes_expected=[http_code.ok],
            data=data)

    def patch(self, path: str, data: Any) -> Optional[dict]:
        """HTTP requets wrapper for PATCH verb, with builtin retry policy and
          return validation

        :param path:
            API path to call starting from SCIM endpoint root
        :param data:
            HTTP request body data
        """
        return self.__request_with_retries(
            http_method='PATCH',
            path=path,
            http_codes_expected=[
                http_code.ok,
                http_code.no_content],
            data=data)

    def delete(self, path: str) -> Optional[dict]:
        """HTTP requets wrapper for DEL verb, with builtin retry policy and
          return validation

        :param path:
            API path to call starting from SCIM endpoint root
        """
        return self.__request_with_retries(
            http_method='DELETE',
            path=path,
            http_codes_expected=[http_code.ok,
                                 http_code.no_content,
                                 http_code.not_found])

    def __request_with_retries(
            self,
            http_method: str,
            path: str,
            http_codes_expected: List[int],
            **kwargs
    ) -> Optional[dict]:
        """HTTP request wrapper with retry policy

        :param http_method:
            API path to call starting from SCIM endpoint root
        :param path:
            API path to call starting from SCIM endpoint root
        :param http_codes_expected:
            HTTP codes which shall be validated as success
        :param kwargs:
            HTTP request parameters
        """
        cur_try = 0
        while cur_try < Env.API_MAX_ATTEMPTS:
            cur_try += 1
            kwargs['headers'] = self.__auth_header
            response = requests.request(
                timeout=120,
                method=http_method,
                url=f"{self.__endpoint}{path}",
                **kwargs)

            if response.status_code == http_code.too_many_requests:
                time.sleep(Env.API_SLEEP_TIME)
                continue

            return self.get_response_data(
                http_codes_expected=http_codes_expected,
                response=response)
        return None

    @staticmethod
    def get_response_data(http_codes_expected: List[int], response: Response) -> Optional[dict]:
        """HTTP response reader wrapper,
          with builtin expected HTTP code validation

        :param http_codes_expected:
            HTTP codes which shall be validated as success
        :param response:
            HTTP full response object for validation
        """
        if response is None:
            raise requests.exceptions.HTTPError(
                        'Empty response, no http-status-code available.'
                    )

        if (not response.ok) and (
                            response.status_code not in http_codes_expected
                        ):
            raise requests.exceptions.HTTPError(
                f"[HTTP {response.status_code}/{response.reason}] "
                f"{response.text}"
                if response.text is not None else
                                'No response data is avaiable.')

        if (response.text is None) or len(response.text) == 0:
            return None

        return response.json()
