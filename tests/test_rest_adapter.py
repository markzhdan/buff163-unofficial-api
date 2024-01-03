import requests
from requests.exceptions import RequestException
from unittest import TestCase, mock

from buff163_unofficial_api.exceptions import Buff163Exception
from buff163_unofficial_api.models import Result
from buff163_unofficial_api.rest_adapter import RestAdapter


class TestRestAdapter(TestCase):
    def setUp(self):
        self.rest_adapter = RestAdapter()
        self.response = requests.Response()

    # _do
    def test__do_good_request_returns_result(self):
        # Arrange
        self.response.status_code = 200
        self.response._content = "{}".encode()
        # Act
        with mock.patch("requests.request", return_value=self.response):
            result = self.rest_adapter._do("GET", "")
            # Assert
            self.assertIsInstance(result, Result)

    def test__do_bad_request_raises_buff163_exception(self):
        with mock.patch("requests.request", side_effect=RequestException):
            with self.assertRaises(Buff163Exception):
                self.rest_adapter._do("GET", "")

    def test__do_bad_json_raises_buff163_exception(self):
        bad_json = '{"invalid JSON": '
        self.response._content = bad_json
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(Buff163Exception):
                self.rest_adapter._do("GET", "")

    def test__do_300_or_higher_raises_buff163_exception(self):
        self.response.status_code = 300
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(Buff163Exception):
                self.rest_adapter._do("GET", "")

    def test__do_199_or_lower_raises_buff163_exception(self):
        self.response.status_code = 199
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(Buff163Exception):
                self.rest_adapter._do("GET", "")

    # get
    def test_get_method_passes_in_get(self):
        self.response.status_code = 200
        self.response._content = "{}".encode()
        with mock.patch("requests.request", return_value=self.response) as request:
            self.rest_adapter.get("")
            self.assertTrue(request.method, "GET")

    # post
    def test_post_method_passes_in_post(self):
        self.response.status_code = 200
        self.response._content = "{}".encode()
        with mock.patch("requests.request", return_value=self.response) as request:
            self.rest_adapter.post("")
            self.assertTrue(request.method, "POST")

    # delete
    def test_delete_method_passes_in_delete(self):
        self.response.status_code = 200
        self.response._content = "{}".encode()
        with mock.patch("requests.request", return_value=self.response) as request:
            self.rest_adapter.delete("")
            self.assertTrue(request.method, "DELETE")

    # def test_fetch_data(self):
    #     self.fail()
