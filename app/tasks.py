from celery import Celery
import logging
from config import Config
import db
import gads_client

config = Config()
logger = logging.getLogger(__name__)

app = Celery('conversion_processing_tasks', broker=config.CELERY_BROKER_URL)


@app.task
def process_conversion(record_id):
    logger.debug("Process conversion with id: {}".format(record_id))
    conversion = db.session.query(db.Conversions).filter(
        db.Conversions.id == record_id).first()

    conversion_processing_obj = db.ConversionsProcessing(
        eventTime=conversion.created,
        conversions_id=conversion.id
    )
    db.session.add(conversion_processing_obj)
    db.session.commit()

    status_code, rsp_text = gads_client.send_event_attribution(
        aff_sub2=conversion.aff_sub2,
        aff_sub3=conversion.aff_sub3,
        aff_sub4=conversion.aff_sub4,
        transaction_id=conversion.transaction_id,
        source=conversion.source,
        referrer=conversion.referrer,
        offer_id=conversion.offer_id, offer_name=conversion.offer_name,
        payout=conversion.payout,
        conversion_id=conversion.conversion_id, created=conversion.created, payout_type=conversion.payout_type,
        browser_device=conversion.browser_device
    )

    logger.debug("Ret code: {} data: {}".format(status_code, rsp_text ))
    conversion.is_processed = True
    if status_code == 200:
        logger.info('Conversion {} processed successfully'.format(conversion.id))
        conversion_processing_obj.status = 'ok'
    else:
        conversion_processing_obj.status = 'error'
        logger.error('Error in conversion {} processing: {}'.format(conversion.id, rsp_text))
    db.session.commit()
