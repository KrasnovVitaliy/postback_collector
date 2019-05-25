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

    def test_new_approved_conversion(self):
        params = {
            'conversion_id': 'conversion_id',
            'created': 'created',
            'status': 'approved',
            'payout': '50',
            'payout_type': 'payout_type',
            'referrer': 'http://example.com',
            'user_agent': 'user_agent',
            'offer_id': 'offer_id',
            'offer_name': 'offer_name',
            'source': 'wproszaim',
            'aff_sub1': 'gAds',
            'aff_sub2': '(direct)',
            'aff_sub3': '35009a79-1a05-49d7-b876-2b884d0f825b',
            'aff_sub4': 'CL6Q-OXyqKUCFcgK2goddQuoHg',
            'browser_device': 'browser_device',
            'transaction_id': 'OD564',
        }
        rsp = requests.get("http://{}:{}".format(POSTBACK_HOST, POSTBACK_PORT), params=params)
        assert rsp.status_code == 200, "Response status code must be 200 in all cases"

    def test_new_pending_conversion(self):
        params = {
            'conversion_id': 'conversion_id',
            'created': 'created',
            'status': 'pending',
            'payout': '50',
            'payout_type': 'payout_type',
            'referrer': 'http://example.com',
            'user_agent': 'user_agent',
            'offer_id': 'offer_id',
            'offer_name': 'offer_name',
            'source': 'wproszaim',
            'aff_sub1': 'gAds',
            'aff_sub2': '(direct)',
            'aff_sub3': '35009a79-1a05-49d7-b876-2b884d0f825b',
            'aff_sub4': 'CL6Q-OXyqKUCFcgK2goddQuoHg',
            'browser_device': 'browser_device',
            'transaction_id': 'OD564',
        }
        rsp = requests.get("http://{}:{}".format(POSTBACK_HOST, POSTBACK_PORT), params=params)
        assert rsp.status_code == 200, "Response status code must be 200 in all cases"

    def test_incorrect_source(self):
        params = {
            'conversion_id': 'conversion_id',
            'created': 'created',
            'status': 'approved',
            'payout': '50',
            'payout_type': 'payout_type',
            'referrer': 'http://example.com',
            'user_agent': 'user_agent',
            'offer_id': 'offer_id',
            'offer_name': 'offer_name',
            'source': 'incorrect',
            'aff_sub1': 'gAds',
            'aff_sub2': 'aff_sub2',
            'aff_sub3': '35009a79-1a05-49d7-b876-2b884d0f825b',
            'aff_sub4': 'CL6Q-OXyqKUCFcgK2goddQuoHg',
            'browser_device': 'browser_device',
            'transaction_id': 'transaction_id',
        }
        rsp = requests.get("http://{}:{}".format(POSTBACK_HOST, POSTBACK_PORT), params=params)
        assert rsp.status_code == 200, "Response status code must be 200 in all cases"
