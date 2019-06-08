from aiohttp import web
import logging
import db
from tasks import process_conversion
from config import Config

logger = logging.getLogger(__name__)
config = Config()

PROCESSING_SOURCE = 'wproszaim'
PROCESSING_AFF_SUB1 = 'gAds'
PROCESSING_STATUSES = ['approved']  # , 'pending'


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

        logger.debug("Are fields source aff_sub1 status present and have correct values")

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

        if conversion.status not in PROCESSING_STATUSES:
            logger.debug("Conversion status is {} process only {}".format(conversion.status, PROCESSING_STATUSES))
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

        filters = {}
        for key in params:
            filters[key] = params[key]

        limit_count = -1
        if 'limit' in params:
            del filters['limit']
            limit_count = params['limit']

        sort_direction = db.Conversions.id.desc()
        if 'sort' in params:
            del filters['sort']
            if params['sort'] == 'asc':
                sort_direction = db.Conversions.id.asc()

        conversions = db.session.query(db.Conversions).filter_by(**filters).order_by(sort_direction).limit(
            limit_count).all()
        rsp = [obj.to_json() for obj in conversions]
        return web.json_response(rsp)


class ConversionsProcessingView(web.View):
    async def get(self):
        logger.debug("Receive conversions processing list get request")
        params = self.request.rel_url.query
        logger.debug('Received params: {}'.format(params))

        filters = {}
        for key in params:
            filters[key] = params[key]

        limit_count = -1
        if 'limit' in params:
            del filters['limit']
            limit_count = params['limit']

        sort_direction = db.ConversionsProcessing.id.desc()
        if 'sort' in params:
            del filters['sort']
            if params['sort'] == 'asc':
                sort_direction = db.ConversionsProcessing.id.asc()

        conversions_processing = db.session.query(db.ConversionsProcessing).filter_by(**filters).order_by(
            sort_direction).limit(
            limit_count).all()
        rsp = [obj.to_json() for obj in conversions_processing]
        for i in rsp:
            i['conversions_link'] = "http://{}:{}/conversions?id={}".format(
                config.PUBLIC_HOST, config.PORT, i['conversions_id'])
        return web.json_response(rsp)
