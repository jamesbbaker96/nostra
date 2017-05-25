import datetime as dt
import urllib, json

from nostra.extensions import db
from nostra.models.relationships import tags_posts
from nostra.database import (
    Column,
    Model,
    SurrogatePK,
)


class IS(SurrogatePK, Model):

    __tablename__ = 'IS'

    primarysymbol = db.Column(db.Text)
    slug = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts_br', lazy='dynamic'))

    def __init__(self, primarysymbol, **kwargs):
        db.Model.__init__(self, primarysymbol=primarysymbol, **kwargs)

class BS(SurrogatePK, Model):

    __tablename__ = 'BS'

    primarysymbol = db.Column(db.Text)
    year = db.Column(db.Integer)
    BSarray = db.Column(db.Array)

    """CommitmentsContingencies = db.Column(db.Long)
    DeferredCharges = db.Column(db.Long)
    DeferredIncomeTaxesCurrent = db.Column(db.Long)
    DeferredIncomeTaxesLongterm = db.Column(db.Long)
    AccountsPayableandAccruedExpenses = db.Column(db.Long)
    AccruedInterest = db.Column(db.Long)
    AdditionalPaidinCapital = db.Column(db.Long)
    AdditionalPaidinCapitalPreferredStock = db.Column(db.Long)
    CashandCashEquivalents = db.Column(db.Long)
    CashCashEquivalentsandShorttermInvestments = db.Column(db.Long)
    IntangibleAssets = db.Column(db.Long)
    InventoriesNet = db.Column(db.Long)
    LongtermDeferredIncomeTaxLiabilities = db.Column(db.Long)
    LongtermDeferredLiabilityCharges = db.Column(db.Long)
    LongtermInvestments = db.Column(db.Long)
    MinorityInterest = db.Column(db.Long)
    OtherAccumulatedComprehensiveIncome = db.Column(db.Long)
    OtherAssets = db.Column(db.Long)
    OtherCurrentAssets = db.Column(db.Long)
    OtherCurrentLiabilities = db.Column(db.Long)
    OtherInvestments = db.Column(db.Long)
    OtherLiabilities = db.Column(db.Long)
    PartnersCapital = db.Column(db.Long)
    PensionPostretirementObligation = db.Column(db.Long)
    PreferredStock = db.Column(db.Long)
    PrepaidExpenses = db.Column(db.Long)
    PropertyPlantEquipmentNet = db.Column(db.Long)
    RestrictedCash = db.Column(db.Long)
    RetainedEarnings = db.Column(db.Long)
    TemporaryEquity = db.Column(db.Long)
    TotalAssets = db.Column(db.Long)
    TotalCurrentAssets = db.Column(db.Long)
    TotalCurrentLiabilities = db.Column(db.Long)
    TotalLiabilities = db.Column(db.Long)
    TotalLongtermDebt = db.Column(db.Long)
    TotalReceivablesNet = db.Column(db.Long)
    TotalShorttermDebt = db.Column(db.Long)
    TotalStockholdersEquity = db.Column(db.Long)
    TreasuryStock = db.Column(db.Long)"""


    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)


    def __init__(self, primarysymbol, **kwargs):
        db.Model.__init__(self, primarysymbol=primarysymbol, **kwargs)

    def parse(primarysymbol)
        url = 'http://edgaronline.api.mashery.com/v1/corefinancials?primarysymbols='+primarysymbol+'&conceptgroups=BalanceSheetConsolidated&appkey=anapqb65c25p9pr9twjapaj3' # define XML location
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for x in range(0, 3)
            for y in range(0, 30)
                data['result']['rowset'][x]['groups'][0]['rowset'][0]['value']


class CFS(SurrogatePK, Model):

    __tablename__ = 'CFS'

    primarysymbol = db.Column(db.Text)
    slug = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts_br', lazy='dynamic'))

    def __init__(self, primarysymbol, **kwargs):
        db.Model.__init__(self, primarysymbol=primarysymbol, **kwargs)
