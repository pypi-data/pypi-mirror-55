from decimal import Decimal


class MoneyUtils(object):

    @staticmethod
    def decimal_places(value, places=2):
        places = Decimal(10) ** -places
        value = Decimal(value).quantize(places)
        return value
