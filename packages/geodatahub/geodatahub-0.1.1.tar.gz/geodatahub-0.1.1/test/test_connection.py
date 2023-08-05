#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import re

import pytest
from geojson import Point, GeometryCollection

import geodatahub

BASEURL = "https://cq6nowxuf4.execute-api.eu-west-1.amazonaws.com/dev/"

@pytest.fixture(scope="class")
def get_auth(request):
    auth = geodatahub.auth.GeodatahubAuth()
    auth.refresh_token = os.environ["REFRESH_TOKEN"]
    auth.refresh_auth()
    request.cls.access_token = auth.id_token

@pytest.fixture(scope="class")
def load_test_datasets(request):
    with open("test/fixtures/geodata_testdata.json", "r") as f:
        test_data = json.load(f)
    request.cls.test_data = test_data

    
@pytest.mark.usefixtures("get_auth")
class ConnectionTests(unittest.TestCase):

    test_uuids = []
    def test_init(self):
        c1 = geodatahub.Connection(token = 'asdf',
                                   backend_url = 'https://api.geodatahub.dk')

    def test_ping(self):
        c1 = geodatahub.Connection(token = self.access_token,
                                   backend_url = BASEURL+"notexist")
        assert c1.ping() is False

        c1 = geodatahub.Connection(token = self.access_token,
                                   backend_url = BASEURL)
        assert c1.ping() is True

    @pytest.mark.usefixtures("load_test_datasets")
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_upload_dataset(self):
        c1 = geodatahub.Connection(token = self.access_token,
                                   backend_url = BASEURL)

        test_table = [
            {
                "name": "All Null values",
                "dataset": geodatahub.models.Dataset(datatype = None,
                                                     description = None,
                                                     result = None,
                                                     distribution_info = None,
                                                     projected_geometry = None),
                "status_code": 400,
                "json_key" : "Error",
                "json_value": "type property not defined"
            },
#            {
##                "name": "All but one as non-null values",
##                "dataset": geodatahub.models.Dataset(datatype = "Borehole",
##                                                     description = "My borehole information",
##                                                     result = "Not a dict",
##                                                     distribution_info = "{}",
##                                                     projected_geometry = GeometryCollection()),
##                "status_code": 200,
##                "json_key" : "id",
##                "json_value": "uuid"
#            }
        ]

        for test in test_table:
            r = c1._call_endpoint("POST", "datasets", test["dataset"].toJSON())
            assert r.status_code == test["status_code"]
            assert test["json_key"] in r.json()

            if test["json_value"] == "uuid":
                m = re.match("(\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12})", r.json()[test["json_key"]])
                assert m is not None

                if m is not None:
                    d = c1.getDataset(m.group(0))
            else:
                assert test["json_value"] in r.json()[test["json_key"]]

if __name__ == '__main__':
    unittest.main()
