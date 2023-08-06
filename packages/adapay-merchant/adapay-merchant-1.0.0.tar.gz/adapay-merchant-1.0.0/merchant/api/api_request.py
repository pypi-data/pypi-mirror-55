"""
2019.8.1 create by jun.hu
默认请求对象
"""
import json
import requests
import merchant
from merchant import log_error
from merchant.utils.common_utils import pop_empty_value, get_plain_text
from merchant.utils.log_util import log_info
from merchant.utils.pycrypt_utils import rsa_sign, rsa_design


class ApiRequest:

    @staticmethod
    def post(url, request_params, request_file=None):
        return ApiRequest._request(url, 'post', request_params, request_file)

    @staticmethod
    def get(url, request_params):
        return ApiRequest._request(url, 'get', request_params)

    @staticmethod
    def _build_request_info(url, method, params, files):
        """
        根据请求方式构造请求头和请求参数
        :return: header 请求头 params 请求参数
        """
        header = {'authorization': merchant.api_key,
                  "sdk_version": 'python_v' + merchant.__version__,
                  'signature': ''}

        params = pop_empty_value(params)

        plain_text = url

        if params:
            if 'post' == method and not files:
                plain_text = plain_text + json.dumps(params)
            else:
                plain_text = plain_text + get_plain_text(params)

        if not merchant.private_key:
            raise RuntimeError('privite_key is none')

        flag, cipher_text = rsa_sign(merchant.private_key, plain_text, 'utf-8')

        if not flag:
            log_error('request to {}, sign error {} '.format(url, cipher_text))

        header.update({'signature': cipher_text})
        log_info('request to {}, param is {}, \nhead is {}'.format(url, params, header))

        return header, params

    @staticmethod
    def _request(url, method, params=None, files=None):
        """
        执行请求
        :param url: 请求地址
        :param method: 请求方法类型
        :param params: 请求参数
        :param files: 上传的文件
        :return: 网路请求返回的数据
        """
        header, params = ApiRequest._build_request_info(url, method, params, files)

        http_method = getattr(requests, method or 'post')

        if files:
            resp = http_method(url, data=params, files=files, timeout=merchant.connect_timeout, headers=header)

        elif method == 'post':
            resp = http_method(url, json=params, files=files, timeout=merchant.connect_timeout, headers=header)

        else:
            resp = http_method(url, params, timeout=merchant.connect_timeout, headers=header)

        log_info('request to {}, resp is {}'.format(url, resp.text))

        return ApiRequest._build_return_data(resp)

    @staticmethod
    def _build_return_data(resp):

        try:
            resp_json = json.loads(resp.text)
        except Exception as e:
            log_error('adapay resp_code is ' + str(resp.status_code))
            log_error(str(e))
            return resp.text

        data = resp_json.get('data', '')
        resp_sign = resp_json.get('signature', '')

        if not resp_sign:
            return resp_json

        if not merchant.public_key:
            raise RuntimeError('public_key is none')

        flag, info = rsa_design(resp_sign, data, merchant.public_key)

        if not flag:
            log_error('check signature error !'.format(info))
            raise RuntimeError(info)

        return json.loads(data)
