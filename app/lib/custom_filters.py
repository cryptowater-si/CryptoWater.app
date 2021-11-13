import arrow


class CustomTemplateFilters(object):
    def __init__(self, app):
        "Add filters to app"
        data = CustomTemplateFilters.filters()
        for jin_filter in data.keys():
            app.jinja_env.filters[jin_filter] = data[jin_filter]

    @staticmethod
    def filters():
        desc = {
            "Timestamp": CustomTemplateFilters.TimestampToLocal,
            "TimestampDateTime": CustomTemplateFilters.TimestampToDateTime,
            "Crypto": CustomTemplateFilters.CurencyCrypto,
            "Logo": CustomTemplateFilters.CoinLogo,
        }
        return desc

    @staticmethod
    def TimestampToLocal(value):
        try:
            local = arrow.Arrow.utcfromtimestamp(value)
            return local.humanize()
        except Exception:
            return value

    @staticmethod
    def TimestampToDateTime(value):
        try:
            local = arrow.Arrow.utcfromtimestamp(value)
            return local.format("YYYY-MM-DD HH:mm")
        except Exception:
            return value

    @staticmethod
    def CurencyCrypto(value):
        """crypto"""
        try:
            if type(value) == int or type(value) == float:
                return "{:.8f}".format(round(value, 8))
        except Exception:
            pass
        return value

    @staticmethod
    def CoinLogo(value):
        d = {
            "LANA": "/static/pic/LanaCoin_logo_v3.png",
            "TAJ": "/static/pic/tajcoin.png",
            "ARCO": "/static/pic/AquariusCoin ArcoV2.png",
        }
        if value in d.keys():
            return d[value]
