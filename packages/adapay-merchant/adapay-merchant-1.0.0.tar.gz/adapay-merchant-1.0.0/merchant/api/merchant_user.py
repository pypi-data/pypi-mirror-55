import merchant
from merchant.api import urls
from merchant.api.api_request import ApiRequest


class MerchantUser(object):
    @classmethod
    def create(cls, **kwargs):
        """
        商户开户进件
        """
        url = merchant.base_url + urls.merchant_user_create
        return ApiRequest.post(url, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
        查询商户开户信息
        """
        url = merchant.base_url + urls.merchant_user_query
        return ApiRequest.get(url, kwargs)


