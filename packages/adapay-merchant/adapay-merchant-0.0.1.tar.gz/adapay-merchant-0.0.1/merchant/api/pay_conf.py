import merchant
from merchant.api import urls
from merchant.api.api_request import ApiRequest


class MerchantPayConf(object):
    @classmethod
    def create(cls, **kwargs):
        """
        商户入驻
        """
        url = merchant.base_url + urls.pay_conf_create
        return ApiRequest.post(url, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
         商户入驻查询
        """
        url = merchant.base_url + urls.pay_conf_query
        return ApiRequest.get(url, kwargs)

    @classmethod
    def modify(cls, **kwargs):
        """
         商户入驻修改
        """
        url = merchant.base_url + urls.pay_conf_modify
        return ApiRequest.post(url, kwargs)


