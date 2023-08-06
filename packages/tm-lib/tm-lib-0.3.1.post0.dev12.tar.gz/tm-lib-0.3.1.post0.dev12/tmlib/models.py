from typing import Tuple, List

from datetime import datetime

from mongoengine import Document, EmbeddedDocument, connect, fields, queryset_manager

from tmlib.eiutils import validate_datetime
from tmlib.settings import Settings


class ToDict:
    def to_dict(self) -> dict:
        """
        Make this class JSON convertible
        :return: dict without '_id'
        """
        p = self.to_mongo()
        p.pop('_id', None)
        return p


class Checkin(EmbeddedDocument, ToDict):
    symbol = fields.StringField()
    broker = fields.StringField()
    last_checkin = fields.DateTimeField()
    computer_name = fields.StringField(default=None)
    minion_version = fields.StringField(default=None)
    minion_edition = fields.StringField(default=None)
    current_lots = fields.FloatField(default=None)
    live_trading_status = fields.StringField(default=None)
    terminal_path = fields.StringField(default=None)


class Registration(EmbeddedDocument, ToDict):
    account_number = fields.IntField()
    broker = fields.StringField()
    rego_key = fields.StringField()
    checkins = fields.EmbeddedDocumentListField(Checkin)
    maximum_lots = fields.DecimalField()
    is_demo_account = fields.BooleanField(default=False)


class License(EmbeddedDocument, ToDict):
    minion_name = fields.StringField()
    wp_membership_id = fields.IntField()
    minion_license = fields.StringField()
    support_expires = fields.StringField()
    account_registrations = fields.EmbeddedDocumentListField(Registration)


class Customer(Document, ToDict):
    login = fields.EmailField()
    given_name = fields.StringField()
    surname = fields.StringField()
    licenses = fields.EmbeddedDocumentListField(License)

    meta = {
        'collection': 'customers',
        'indexes':
            [{
                'fields': ['login'],
                'unique': True
            }]
    }

    def __str__(self):
        return "Customer <%s>" % self.login

    def get_license(self, minion_name):
        for licence in self.licenses:
            if licence.minion_name == minion_name:
                return licence


    def get_account_registration(self, *, minion_name: str,
                                 account_number: int, broker_name: str) -> Registration:
        """
        Get account registration by minion name and account_number
        :param minion_name:
        :param account_number:
        :param broker_name:
        :return: Optional[Registration]
        """
        try:
            license: License = next(
                l for l in self.licenses if l.minion_name == minion_name
            )
            account_registration: Registration = next(
                ac for ac in license.account_registrations
                if ac.account_number == account_number and ac.broker == broker_name)
            return account_registration
        except (StopIteration, AttributeError) as err:
            raise Customer.DoesNotExist(str(err))


class Parameter(Document, ToDict):
    note_to_me = fields.StringField()
    minion_name = fields.StringField()
    broker_name = fields.ListField()
    edition = fields.ListField()
    version = fields.StringField()
    filedata = fields.StringField()

    @classmethod
    def get_or_create(cls, minion_name: str, version: str, edition: List[str]) -> Tuple['Parameter', bool]:
        try:
            p: Parameter = cls.objects.get(minion_name=minion_name, version=version, edition=edition)
            created = False
        except cls.DoesNotExist:
            p: Parameter = cls(minion_name=minion_name, version=version, edition=edition)
            created = True
        return p, created

    meta = {
        'collection': 'parameters',
        'indexes':
            [{
                'fields': ['minion_name', 'version', 'edition'],
            }]
    }


class TradeLog(Document, ToDict):
    account = fields.IntField()
    account_balance = fields.FloatField()
    close_notes = fields.StringField()
    magic_number = fields.IntField()
    minion_name = fields.StringField()
    order_close_price = fields.FloatField()
    order_close_time = fields.DateTimeField()  # MT4 time string (YYYY.DD.MM HH.MM)
    order_comment = fields.StringField()
    order_direction = fields.IntField()
    order_open_price = fields.FloatField()
    order_open_time = fields.DateTimeField()  # MT4 time string (YYYY.DD.MM HH.MM)
    order_place_time = fields.DateTimeField()  # MT4 time string (YYYY.DD.MM HH.MM)
    order_profit = fields.FloatField()
    order_profit_r = fields.FloatField()
    order_qty = fields.FloatField()
    order_type = fields.StringField()
    parameters = fields.StringField()
    period = fields.IntField()
    symbol = fields.StringField()
    ticket = fields.IntField()
    computer_name = fields.StringField(default=None)
    order_commission = fields.FloatField(default=None)
    order_swap = fields.FloatField(default=None)
    open_notes = fields.StringField(default=None)

    def to_mongo(self) -> dict:
        """
        Convert datetime to string
        """
        tl = super().to_mongo()
        for f in ("order_close_time", "order_open_time", "order_place_time"):
            try:
                tl[f] = datetime.strftime(tl[f], '%Y.%m.%d %H.%M')
            except Exception:
                # null value
                tl[f] = None
        return tl

    @queryset_manager
    def objects_without_id(doc_cls, queryset):
        return queryset.order_by('id').exclude('id')

    meta = {
        'collection': 'tradelogs',
        'indexes':
            [
                {
                    'fields': ['ticket'],
                },
                {
                    'fields': ['ticket', 'account'],
                    'unique': True
                }
            ]
    }


class Minion(Document, ToDict):
    name = fields.StringField(required=True)
    last_version_expert = fields.StringField(required=True)
    last_version_parameters = fields.StringField(required=True)
    note_to_me = fields.StringField()

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.exclude('note_to_me')

    @classmethod
    def get_or_create(cls, minion_name: str, version: str) -> Tuple['Parameter', bool]:
        try:
            p: Parameter = cls.objects.get(minion_name=minion_name, version=version)
            created = False
        except cls.DoesNotExist:
            p: Parameter = cls(minion_name=minion_name, version=version)
            created = True
        return p, created

    meta = {
        'collection': 'minions',
        'indexes':
            [{
                'fields': ['name'],
                'unique': True
            }]
    }

class WPJWT(Document):
    created_at = fields.DateTimeField(default=datetime.utcnow)
    token = fields.StringField(default="")
    username = fields.StringField()
    meta = {
        "collection": "wp_jwt",
        'indexes':
            [{
                'fields': ['username'],
                'unique': True
            }]
    }


connect('trading_minions', host=Settings.MONGO_URI)
