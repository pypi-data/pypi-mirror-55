"""Domeneshop API client implementation."""

import json
import logging
from typing import List

import urllib3
import certifi
import base64

logger = logging.getLogger(__name__)

VALID_TYPES = [
    "A",
    "AAAA",
    "CNAME",
    "ANAME",
    "TLSA",
    "MX",
    "SRV",
    "DS",
    "CAA",
    "NS",
    "TXT",
]

COMMON_KEYS = {"host", "data", "ttl", "type"}

VALID_KEYS = {
    "MX": {"priority"},
    "SRV": {"priority", "weight", "port"},
    "TLSA": {"usage", "selector", "dtype"},
    "DS": {"tag", "alg", "digest"},
    "CAA": {"flags", "tag"},
}


class Client:
    def __init__(self, token: str, secret: str):
        """
        See the documentation at https://api.domeneshop.no/docs/ for
        help on how to acquire your API credentials.

        :param token: The API client token
        :type token: str
        :param secret: The API client secret
        :type secret: str

        """

        self._headers = {
            "Authorization": "Basic {}".format(
                base64.b64encode("{}:{}".format(token, secret).encode()).decode()
            ),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "domeneshop-python/0.4.2",
        }
        self._http = urllib3.HTTPSConnectionPool(
            "api.domeneshop.no", 443, maxsize=5, block=True, headers=self._headers, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()
        )

    # Domains

    def get_domains(self) -> List[dict]:
        """
        Retrieve a list of all domains.

        :return: A list of domain dictionaries

        """
        resp = self._request("GET", "/domains")
        domains = json.loads(resp.data.decode('utf-8'))
        return domains

    def get_domain(self, domain_id: int) -> dict:
        """
        Retrieve a domain.
        
        :param domain_id: The domain ID to retrieve

        :return: A domain dictionary
        """

        resp = self._request("GET", "/domains/{0}".format(domain_id))
        domain = json.loads(resp.data.decode('utf-8'))
        return domain

    # DNS records

    def get_records(self, domain_id: int) -> List[dict]:
        """
        Retrieve DNS records for a domain, or raises an error.
        
        :param domain_id: The domain ID to operate on

        :return: A list of record dictionaries
        """
        resp = self._request("GET", "/domains/{0}/dns".format(domain_id))
        records = json.loads(resp.data.decode('utf-8'))
        return records

    def get_record(self, domain_id: int, record_id: int) -> dict:
        """
        Retrieve a specific DNS record for a domain, or raises an error.
        
        :param domain_id: The domain ID to operate on
        :param record_id: The DNS record ID to retrieve

        :return: A record dictionary
        """
        resp = self._request("GET", "/domains/{0}/dns/{1}".format(domain_id, record_id))
        record = json.loads(resp.data.decode('utf-8'))
        return record

    def create_record(self, domain_id: int, record: int) -> int:
        """
        Create a DNS record for a domain, or raises an error. The record is validated
        primitively before being passed on to the API.
        
        :param domain_id: The domain ID to operate on
        :param record: A dict

        :return: The Record ID of the created record.

        Raises:
            TypeError: If the record appears to be invalid
        """
        _validate_record(record)
        resp = self._request("POST", "/domains/{0}/dns".format(domain_id), data=record)

        record_id = resp.headers.get("location").split("/")[-1]
        return int(record_id)

    def modify_record(self, domain_id: int, record_id: int, record: dict) -> None:
        """
        Modify a DNS record for a domain, or raises an error. The record is validated
        primitively before being passed on to the API.
        
        :param domain_id:  The domain ID to operate on
        :param record: A dict

        :return: A list of record dictionaries

        Raises:
            TypeError if the record appears to be invalid.
        """
        _validate_record(record)
        self._request(
            "PUT", "/domains/{0}/dns/{1}".format(domain_id, record_id), data=record
        )

    def delete_record(self, domain_id: int, record_id: int) -> None:
        """
        Delete a DNS record for a domain, or raises an error.
        
        :param domain_id:  The domain ID to operate on
        :param record_id: The record ID to delete
        """
        self._request("DELETE", "/domains/{0}/dns/{1}".format(domain_id, record_id))

    # Forwards

    def get_forwards(self, domain_id: int) -> List[dict]:
        """
        Retrieve forwardings for a domain, or raises an error.
        
        :param domain_id: The domain ID to operate on

        :return: A list of forwarding dictionaries
        """
        resp = self._request("GET", "/domains/{0}/forwards".format(domain_id))
        records = json.loads(resp.data.decode('utf-8'))
        return records

    def get_forward(self, domain_id: int, host: str) -> List[dict]:
        """
        Retrieve forwardings for a domain, or raises an error.
        
        :param domain_id: The domain ID to operate on

        :return: A list of forwarding dictionaries
        """
        resp = self._request("GET", "/domains/{0}/forwards/{1}".format(domain_id, host))
        records = json.loads(resp.data.decode('utf-8'))
        return records

    def create_forward(
        self, domain_id: int, host: str, target: str, frame=False
    ) -> None:
        """
        Create a forwarding for a domain, or raises an error.
        
        :param domain_id:  The domain ID to operate on
        :param host:  The host (subdomain) to modify
        :param forward: A dict

        :return: A list of record dictionaries

        """

        forward = {"frame": frame, "host": host, "url": target}

        print(forward)

        self._request(
            "POST", "/domains/{0}/forwards".format(domain_id, host), data=forward
        )

    def modify_forward(
        self, domain_id: int, host: str, target: str, frame=False
    ) -> None:
        """
        Modify a forwarding for a domain, or raises an error.
        
        :param domain_id:  The domain ID to operate on
        :param host:  The host (subdomain) to modify
        :param forward: A dict
        """

        forward = {"frame": frame, "host": host, "url": target}

        self._request(
            "PUT", "/domains/{0}/forwards/{1}".format(domain_id, host), data=forward
        )

    def delete_forward(self, domain_id: int, host: str) -> None:
        """
        Deletes a forwarding for a domain, or raises an error.
        
        :param domain_id:  The domain ID to operate on
        :param host:  The host (subdomain) to delete
        """

        self._request("DELETE", "/domains/{0}/forwards/{1}".format(domain_id, host))

    def _request(self, method="GET", endpoint="/", data=None):
        if data is not None:
            data = json.dumps(data).encode("utf-8")
        try:
            resp = self._http.request(method, "/v0" + endpoint, body=data)
            if resp.status >= 400:
                try:
                    data = json.loads(resp.data.decode('utf-8'))
                except json.JSONDecodeError:
                    data = {"error": resp.status, "help": "A server error occurred."}
                raise DomeneshopError(resp.status, data) from None
        except urllib3.exceptions.HTTPError as e:
            raise e
        else:
            return resp


class DomeneshopError(Exception):
    def __init__(self, status_code: int, error: dict):
        """
        Exception raised for API errors.

            :param status_code: The HTTP status code
            :type status_code: int
            :param error: The error returned from the API
            :type error: dict
        """
        self.status_code = status_code
        self.error_code = error.get("code")
        self.help = error.get("help")

        error_message = "{0} {1}. {2}".format(
            self.status_code, self.error_code, self.help
        )

        super().__init__(error_message)


def _validate_record(record: dict):
    record_keys = set(record.keys())
    record_type = record.get("type")

    if record_type not in VALID_TYPES:
        raise TypeError("Record has invalid type. Valid types: {0}".format(VALID_TYPES))

    required_keys = COMMON_KEYS | VALID_KEYS.get(record_type, set())

    if record_keys != required_keys:
        raise TypeError(
            "Record is missing or has invalid keys. Required keys: {0}".format(
                required_keys
            )
        )
