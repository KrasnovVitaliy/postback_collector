import pytest
import requests
import json

POSTBACK_HOST = "127.0.0.1"
POSTBACK_PORT = 7000


class TestSimple(object):
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_new_conversion(self):
        params = {
            'conversion_id': 'conversion_id',
            'created': 'created',
            'status': 'approved',
            'payout': 'payout',
            'payout_type': 'payout_type',
            'referrer': 'referrer',
            'user_agent': 'user_agent',
            'offer_id': 'offer_id',
            'offer_name': 'offer_name',
            'source': 'wproszaim',
            'aff_sub1': 'gAds',
            'aff_sub2': 'aff_sub2',
            'aff_sub3': 'aff_sub3',
            'aff_sub4': 'aff_sub4',
            'browser_device': 'browser_device',
            'transaction_id': 'transaction_id',
        }
        rsp = requests.get("http://{}:{}".format(POSTBACK_HOST, POSTBACK_PORT), params=params)
        assert rsp.status_code == 200, "Response status code must be 200 in all cases"

    def test_incorrect_source(self):
        params = {
            'conversion_id': 'conversion_id',
            'created': 'created',
            'status': 'approved',
            'payout': 'payout',
            'payout_type': 'payout_type',
            'referrer': 'referrer',
            'user_agent': 'user_agent',
            'offer_id': 'offer_id',
            'offer_name': 'offer_name',
            'source': 'incorrect',
            'aff_sub1': 'gAds',
            'aff_sub2': 'aff_sub2',
            'aff_sub3': 'aff_sub3',
            'aff_sub4': 'aff_sub4',
            'browser_device': 'browser_device',
            'transaction_id': 'transaction_id',
        }
        rsp = requests.get("http://{}:{}".format(POSTBACK_HOST, POSTBACK_PORT), params=params)
        assert rsp.status_code == 200, "Response status code must be 200 in all cases"
