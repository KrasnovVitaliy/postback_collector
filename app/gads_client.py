import requests
from random import randint
from urllib.parse import urlencode
from config import Config
import logging

logger = logging.getLogger(__name__)
config = Config()

GADS_ENDPOINT = 'https://www.google-analytics.com/collect'
DEFAULT_TID = 'UA-136208181-2'
DEFAULT_T = 'transaction'
RANDOM_RANGE = 999999


def create_event(cid, ds, dr, cn, gclid, ti, ta, tr, cd1, cd2, cd3, cd4, tid=DEFAULT_TID, t=DEFAULT_T, v=1):
    data = {
        'v': v,
        'tid': tid,
        'cid': cid,
        't': t,
        'ds': ds,
        'dr': dr,
        'cn': cn,
        'gclid': gclid,
        'ti': ti,
        'ta': ta,
        'tr': tr,
        'cd1': cd1,
        'cd2': cd2,
        'cd3': cd3,
        'cd4': cd4,
    }
    encoded_data = urlencode(data)
    encoded_data += "&z={}".format(randint(0, RANDOM_RANGE))
    return encoded_data


def send_event_attribution(aff_sub2, aff_sub3, aff_sub4, transaction_id, source, referrer, offer_id, offer_name,
                           payout, conversion_id, created, payout_type, browser_device):
    data = create_event(cid=aff_sub3, ds=source, dr=referrer, cn=aff_sub2, gclid=aff_sub4, ti=transaction_id,
                        ta="{}/{}".format(offer_id, offer_name), tr=payout, cd1=conversion_id,
                        cd2=created, cd3=payout_type, cd4=browser_device)
    logger.debug("Generated event data: {}".format(data))

    rsp = requests.post(GADS_ENDPOINT, data=data)
    logger.debug("GAps status code: {} response: {}".format(rsp.status_code, rsp.text))

    if rsp.status_code != 200:
        logger.error("Could not to send appsflyer event: {}".format(rsp.text))
        return rsp.status_code, rsp.text

    return rsp.status_code, rsp.text


def main():
    print(send_event_attribution(aff_sub2='aff_sub2', aff_sub3='aff_sub3', aff_sub4='aff_sub4',
                                 transaction_id='transaction_id', source='source', referrer='referrer',
                                 offer_id='offer_id', offer_name='offer_name', payout='payout',
                                 conversion_id='conversion_id', created='created', payout_type='payout_type',
                                 browser_device='browser_device'))


if __name__ == "__main__":
    main()
