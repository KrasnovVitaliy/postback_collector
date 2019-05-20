from aiohttp import web
import logging
import db
from tasks import process_conversion
from config import Config

logger = logging.getLogger(__name__)
config = Config()

PROCESSING_SOURCE = 'wproszaim'
PROCESSING_AFF_SUB1 = 'gAds'
PROCESSING_STATUS = 'approved'


class ConfigsView(web.View):
    async def get(self):
        return web.json_response(config.dict())


class AddConversionView(web.View):
    async def get(self):
        logger.debug("Receive new postback request")
        params = self.request.rel_url.query
        logger.debug('Received params: {}'.format(params))

        conversion = db.Conversions()

        for key in ['conversion_id', 'created', 'status', 'payout', 'payout_type',
                    'referrer', 'user_agent', 'offer_id', 'offer_name', 'source', 'aff_sub1', 'aff_sub2',
                    'aff_sub3', 'aff_sub4', 'browser_device', 'transaction_id']:
            logger.debug("Process key: {}".format(key))
            if key in params:
                logger.debug("Param: {}: {}".format(key, params[key]))
                setattr(conversion, key, params[key])
            else:
                logger.debug("Key {} not found".format(key))

        db.session.add(conversion)
        db.session.commit()

        logger.debug("Are fields source aff_sub1 status present and have correct valuese")

        if conversion.source != PROCESSING_SOURCE:
            logger.debug("Conversion source is {} process only {}".format(conversion.source, PROCESSING_SOURCE))
            logger.debug("Skip processing")
            conversion.error = 'incorrect source'
            db.session.commit()
            return web.HTTPOk()

        if conversion.aff_sub1 != PROCESSING_AFF_SUB1:
            logger.debug("Conversion aff_sub1 is {} process only {}".format(conversion.aff_sub1, PROCESSING_AFF_SUB1))
            logger.debug("Skip processing")
            conversion.error = 'incorrect aff_sub1'
            db.session.commit()
            return web.HTTPOk()

        if conversion.status != PROCESSING_STATUS:
            logger.debug("Conversion status is {} process only {}".format(conversion.status, PROCESSING_STATUS))
            logger.debug("Skip processing")
            conversion.error = 'incorrect status'
            db.session.commit()
            return web.HTTPOk()

        process_conversion.delay(conversion.id)
        return web.HTTPOk()


class ConversionsView(web.View):
    async def get(self):
        logger.debug("Receive conversions list get request")
        params = self.request.rel_url.query
        logger.debug('Received params: {}'.format(params))

        if 'limit' in params:
            conversions = db.session.query(db.Conversions).order_by(db.Conversions.id.desc()).limit(params['limit'])
        else:
            conversions = db.session.query(db.Conversions).order_by(db.Conversions.id.desc()).all()
        rsp = [obj.to_json() for obj in conversions]

        logger.debug('Get request processed')
        return web.json_response(rsp)
#
#
# class ConversionsProcessingView(web.View):
#     async def get(self):
#         logger.debug("Receive conversions list get request")
#         params = self.request.rel_url.query
#         logger.debug('Received params: {}'.format(params))
#
#         if 'limit' in params:
#             conversions_processing = db.session.query(db.ConversionsProcessing).order_by(
#                 db.Conversions.id.desc()).limit(params['limit'])
#         else:
#             conversions_processing = db.session.query(db.ConversionsProcessing).order_by(db.Conversions.id.desc()).all()
#
#         rsp = [obj.to_json() for obj in conversions_processing]
#
#         logger.debug('Get request processed')
#         return web.json_response(rsp)
