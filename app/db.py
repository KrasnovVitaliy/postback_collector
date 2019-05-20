import datetime
from config import Config
from sqlalchemy import create_engine, Column, DateTime, Integer, String, func, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

config = Config()

Base = declarative_base()

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(config.DB_URI))
session = scoped_session(Session)


class Conversions(Base):
    __tablename__ = 'conversions'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    conversion_id = Column(String(50))
    created = Column(String(50))
    status = Column(String(50))
    payout = Column(String(50))
    payout_type = Column(String(50))
    referrer = Column(String(50))
    user_agent = Column(String(50))
    offer_id = Column(String(50))
    offer_name = Column(String(50))
    source = Column(String(50))
    aff_sub1 = Column(String(50))
    aff_sub2 = Column(String(50))
    aff_sub3 = Column(String(50))
    aff_sub4 = Column(String(50))
    browser_device = Column(String(50))
    transaction_id = Column(String(50))
    is_processed = Column(Boolean())
    error = Column(String(50))

    def __init__(self,
                 conversion_id='', created='', status='', payout='', payout_type='', referrer='',
                 user_agent='', offer_id='', offer_name='', source='', aff_sub1='', aff_sub2='',
                 aff_sub3='', aff_sub4='', browser_device='', transaction_id='', is_processed=False, error=''):
        self.conversion_id = conversion_id
        self.created = created
        self.status = status
        self.payout = payout
        self.payout_type = payout_type
        self.referrer = referrer
        self.user_agent = user_agent
        self.offer_id = offer_id
        self.offer_name = offer_name
        self.source = source
        self.aff_sub1 = aff_sub1
        self.aff_sub2 = aff_sub2
        self.aff_sub3 = aff_sub3
        self.aff_sub4 = aff_sub4
        self.browser_device = browser_device
        self.transaction_id = transaction_id
        self.is_processed = is_processed
        self.error = error

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'conversion_id', 'created', 'status', 'payout', 'payout_type',
                        'referrer', 'user_agent', 'offer_id', 'offer_name', 'source', 'aff_sub1', 'aff_sub2',
                        'aff_sub3', 'aff_sub4', 'browser_device', 'transaction_id', 'is_processed', 'error']
        return self.serialize(to_serialize)


class ConversionsProcessing(Base):
    __tablename__ = 'conversions_processing'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    eventTime = Column(String(50))
    conversions_id = Column(Integer, ForeignKey("conversions.id"))
    status = Column(String(20))

    def __init__(self, eventTime='', conversions_id='', status=''):
        self.eventTime = eventTime
        self.conversions_id = conversions_id
        self.status = status

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'eventTime', 'conversions_id', 'status']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(config.DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# creates database
if __name__ == "__main__":
    prepare_db()
