#coding: utf-8
import logging
from multiprocessing import Process
import requests
import traceback
from time import sleep
from utils import ua
import time
import random
import datetime
import json
import os


def async_wrapper(func):
    def wrapper(*args, **kwargs):
        logging.info("%s is running" % func.__name__)
        p = Process(target=func, args=args, kwargs=kwargs)
        p.start()
    return wrapper


def request_http(url, data=None, method='GET', ua_type='Desktop', header=None,
                 http_proxy=None, https_proxy=None, request_retry_times=5,
                 request_time_out=120, request_break_time=5,
                 return_type=None, request_type=None, is_verify=False, check_status_code=True):
    """
    通用http请求函数
    :param url: 请求地址
    :param data: GET 请求参数 POST 请求body
    :param method: GET POST
    :param ua_type: Desktop, Mobile, None则没有
    :param header: 如果有，则为header
    :param http_proxy: 如果有，则为proxy_dict = {
            "http": "http://username:password@hogehoge.proxy.jp:8080/",
            "https": "http://username:password@hogehoge.proxy.jp:8080/"
         }
    :param https_proxy: 同上
    :param request_retry_times: 失败重试次数
    :param request_time_out: 请求等待时间
    :param request_break_time: 请求间隔时间
    :param return_type: json, text, None则返回res对象
    :param request_type: None则正常，json则为json请求
    :param is_verify: verify=False，减少不必要的请求验证
    :param check_status_code: check_status_code=True,验证请求状态码
    :return:
    """
    request_dict = dict()
    # 1. 填装header
    if header:
        request_dict['headers'] = header
    else:
        if ua_type == 'Desktop':
            request_dict['headers'] = ua.get_header_with_desktop_rnd_ua()
        elif ua_type == 'Mobile':
            request_dict['headers'] = ua.get_header_with_rnd_ua()
        else:
            # 不需要头
            pass
    # 2. 设置代理
    if http_proxy or https_proxy:
        proxy_dict = dict()
        if http_proxy:
            proxy_dict.setdefault('http', http_proxy)
        if https_proxy:
            proxy_dict.setdefault('https', https_proxy)
        request_dict['proxies'] = proxy_dict
    # 3. 填装请求报文
    if method == 'POST':
        if request_type is None:
            # 正常的form-data
            if data:
                request_dict['data'] = data
        elif request_type == 'json':
            # json请求
            if data:
                request_dict['json'] = data
    elif method == 'GET':
        # 都是params
        if data:
            request_dict['params'] = data
    elif method == 'PUT':
        if data:
            request_dict['data'] = data
    elif method == 'PATCH' or method == 'DELETE':
        # 都是 params
        if data:
            request_dict['data'] = data
    if not is_verify:
        request_dict['verify'] = False
    request_dict['timeout'] = request_time_out
    # 4. 进入发送请求的逻辑
    try_times = 0
    while try_times <= request_retry_times:
        try:
            res = requests.request(method, url, **request_dict)
            if check_status_code and res.status_code >= 400:
                print("%d failed %s" % (res.status_code, res.text))
                assert False
            # 返回
            if not return_type:
                return res
            if return_type == 'text':
                return res.text
            elif return_type == 'json':
                return res.json()
            return res
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            try_times += 1
            print("sleep %d seconds and try %s again" % (request_break_time, url))
            sleep(request_break_time)
            continue
    raise Exception("%s %s request failed" % (url, method))


def download_url(src_url, dst_url, http_proxy=None, https_proxy=None, cache=True):
    """
    下载指定的url到本地的指定位置。
    :param src_url: 源url。
    :param dst_url: 目标url。
    :param http_proxy:
    :param https_proxy:
    :return:
    """
    if cache:
        if os.path.exists(dst_url): return
    proxies = {"http": http_proxy, "https": https_proxy}
    r = request_http(src_url, http_proxy=http_proxy, https_proxy=https_proxy, request_retry_times=2,
                     request_break_time=1)
    with open(dst_url, 'wb') as f:
        f.write(r.content)


def nullable_visit(obj, attr, attr_type='attr', para=None, index=None, default=None):
    """
    判断obj是否为None，不为None时执行相应的操作。
    :param attr: 需要执行的函数名，或需要访问的字段名
    :param attr_type: 为'attr'时，表示执行的操作是访问指定的字段；为'func'时，表示调用指定的函数。
    :param para: 调用函数时的参数。
    :param index: 访问字段时，若字段值是一个列表，则返回其中的指定元素。
    :param default: 默认值。
    """
    if obj is None:
        return default
    try:
        if attr_type == 'attr':
            if index is None:
                return getattr(obj, attr, default)
            lst = getattr(obj, attr, None)
            if lst is not None:
                if len(lst) >= index + 1:
                    return getattr(obj, attr, None)[index]
            return default
        if attr_type == 'func':
            f = getattr(obj, attr)
            return f(para)
        return default
    except Exception as ex:
        return default


def current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def logger_generate(msg, origin_name='origin_name', app_name='app_name', log_level='DEBUG'):
    # [DEBUG][2019-12-09 11:20:29] from=cralwer_meta|method=|to=
    current_time = current_time_str()
    return "[{}][{}][{}][{}] {}".format(
        log_level, current_time, app_name, origin_name, str(msg)
    )


def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())+''.join([str(random.randint(1,10)) for i in range(5)])


def load_json_from_file(file_path, encoding='utf-8'):
    with open(file_path, "r", encoding=encoding) as f:
        return json.loads(f.read())


def json_to_file(file_path, data, encoding='utf-8'):
    with open(file_path, "w", encoding=encoding) as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    print(tid_maker())