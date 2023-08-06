#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Required for aws signature
import hmac
import datetime
import hashlib
import logging as lg

import requests
import json
from .models import Dataset
from .auth import GeodatahubAuth

# Setup logging module
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.INFO)
LOG = lg.getLogger("geodatahub.Connection")


class Connection(object):

    def __init__(self,
                 token=None,
                 api_key=None,
                 backend_url='https://api.geodatahub.dk'):
        """Set up connection properties to GeoDataHub backend.

        Parameters
        ----------
        token: str, Optional
          Token used to provide user authentication against backend
        api_key: str, Optional
          An API key supplied by the backend
        backend_url: str, Optional
          URL to GeoDataHub backend
        """

        # Setup authentization header
        self._auth_headers = {}
        self._auth = GeodatahubAuth()

        if token is not None:
            self.set_token(token)

        if api_key is not None:
            self._auth_headers["x-api-key"] = api_key

        self._backend_url = backend_url
        self._host = "execute-api.amazonaws.com"
        self._region = "eu-west-1"
        self._service = "execute-api"

    def set_token(self, token):
        """Set the authentication token

        All communication with the backend needs to
        authenticate the user.

        Parameters
        ------------
        token : string
          Authentication token from the authentication module
        """
        self._auth_headers["Authorization"] = token

    def _call_endpoint(self, method, path, payload = None):
        """Call the API with a specific payload

        Parameters
        -----------
        method: str
          HTTP type of operations (GET, POST)
        path: str
          API endpoint to call (/datasets)
        payload: dict, Optional
          Parameters for the endpont

        Returns
        ---------
        response: dict
          JSON reponse from the API
        """
        
#        header = self._sign_with_sig4(method, path)
        header = self._auth_headers
        endpoint = self._backend_url + path

        if method == "POST":
            if payload is not None:
                resp = requests.post(endpoint,
                                     headers=header,
                                     json=payload)
            else:
                resp = requests.post(endpoint, headers=header)
        else:
            resp = requests.get(endpoint, headers=header)

        if resp.status_code == 401:
            # Token expired
            self._auth.refresh_auth()

            # Call API again with new tokens
            return self._call_endpoint(method, path, payload)

        return resp

    def ping(self):
        """Test connection to API

        This method calls the /ping endpoint. If
        the connection was successful True is returned
        otherwise the error message is written to the log
        and False is returned.

        Returns
        ------------
        response: bool
          If the connection was successful
        """
        r = self._call_endpoint("GET", "ping")

        if r.status_code != 200:
            try:
                LOG.error('GET to ' + self._backend_url +
                          '/ping was not successfull ' +
                          '(HTTP status code: ' + str(r.status_code) +
                          '\n\nServer response:\n' + json.dumps(r.json()))
            except:
                LOG.error('GET to ' + self._backend_url +
                          '/ping was not successfull ' +
                          '(HTTP status code: ' + str(r.status_code) +
                          '\n\nUnable to decode response!\n')
            return False

        return True

    def uploadDataset(self, dataset):
        """Upload metadata dataset via the API

        This method send the dataset encoded as JSON
        to the /datasets endpoint. If successful the
        newly created unique ID is returned by the API.

        Parameters
        ------------
        dataset: geodatahub.Dataset
          Dataset object to upload

        Returns
        ----------
        dataset_id: str
          The dataset UUIDv4 from the API
        """
        r = self._call_endpoint("POST", "datasets", payload=dataset.toJSON())

        if r.status_code != 200:
            try:
                raise Exception('POST to ' + self._backend_url +
                                '/datasets was not successfull ' +
                                '(HTTP status code: ' + str(r.status_code) +
                                ')\n\nTried to send:\n' +
                                json.dumps(dataset.toJSON()) +
                                '\n\nServer response:\n' + json.dumps(r.json()))
            except:
                raise Exception('POST to ' + self._backend_url +
                                '/datasets was not successfull ' +
                                '(HTTP status code: ' + str(r.status_code) +
                                ')\n\nTried to send:\n' +
                                json.dumps(dataset.toJSON()) +
                                '\n\nServer response:\n' + r.text)


        return r.json()['id']

    def getDataset(self, uuid):
        """Returns datasets from the GeoDataHub backend by the unique id.

        Parameters
        -----------
        uuid: str
          Unique ID in UUIDv4 format

        Returns
        --------
        dataset: geodatahub.Dataset
          Dataset with matching UUID
        """

        r = self._call_endpoint("GET", 'datasets/%s' % uuid)

        if r.status_code != 200:
            raise Exception('GET to ' + self._backend_url +
                            '/dataset/%s was not successfull ' % uuid +
                            '(HTTP status code: ' + str(r.status_code) +
                            '\n\nServer response:\n' + json.dumps(r.json()))


        try:
            dataset = Dataset(**r.json())
        except TypeError:
            LOG.error("Unable to decode response %s" % r.json())
            raise
        return dataset

    def searchDataset(self, query = ""):
        """Returns datasets from the GeoDataHub backend by search parameters

        Parameters
        ------------
        query: str
          Search string

        Returns
        --------
        datasets: list of geodatahub.Dataset
          Dataset(s) that matches the search
        """

        r = self._call_endpoint("GET", 'datasets?q=%s' % query)

        if r.status_code != 200:
            raise Exception('GET to ' + self._backend_url +
                            '/dataset/%s was not successfull ' % uuid +
                            '(HTTP status code: ' + str(r.status_code) +
                            '\n\nServer response:\n' + json.dumps(r.json()))


        datasets = []
        try:
            for dset in r.json():
                datasets.append(Dataset(**dset))
        except TypeError:
            LOG.error("Unable to decode response %s" % r.json())
            raise

        return datasets
