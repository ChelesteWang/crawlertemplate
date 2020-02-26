from utils.common import request_http, tid_maker, json_to_file
from bs4 import BeautifulSoup

# import multiprocessing
import os
import traceback
import json
import time

dir_name = "weseepro"

base_url = "https://www.weseepro.com/api/v1/message/messages/v1/getCacheRankingList?day=1"
steam_url = "https://www.weseepro.com/api/v1/message/stream/v3/procedure/spam?pageNumber=1&pageSize=30&end_uuid=&isWeb=1"
article_detail_url = "https://www.weseepro.com/api/v1/message/stream/spam1/{}?dataType={}&page_size=10&end_uuid=&uuid={}"


def weseepro_start(task_id, task_info, logger, msg):
    detail_data = task_info['detail'] if 'detail' in task_info else dict()
    config = task_info['crawler_info']
    base_dir = config['base_dir']
    os.makedirs(base_dir, exist_ok=True)
    unique_code = tid_maker()
    download_path = os.path.join(base_dir, dir_name, unique_code)
    os.makedirs(download_path, exist_ok=True)
    detail_data['version'] = unique_code
    msg.append(
        logger.info(
            "weseepro download_path[{}]  task_id[{}]".format(
                # pool_size,
                download_path, task_id
            )
        )
    )
    response = request_http(base_url, data=None, method='GET', ua_type='Desktop', header=None,
                        http_proxy=None, https_proxy=None, request_retry_times=3,
                        request_time_out=20, request_break_time=5,
                        return_type='json', request_type=None, is_verify=False, check_status_code=True)
    list_path = os.path.join(download_path, "daily.json")
    json_to_file(list_path, response)
    count = 0
    detail_data['list_path'] = list_path
    detail_data['article'] = dict()
    for cell in response['data']:
        index = cell['uuid']
        atype = cell['type']
        count += 1
        article_url = article_detail_url.format(index, atype, index)
        detail = request_http(article_url, data=None, method='GET', ua_type='Desktop', header=None,
                        http_proxy=None, https_proxy=None, request_retry_times=3,
                        request_time_out=20, request_break_time=5,
                        return_type='json', request_type=None, is_verify=False, check_status_code=True)
        cell_path = os.path.join(download_path, index+".json")
        detail_data['article'][index] = cell_path
        json_to_file(cell_path, detail)
    msg.append(
        logger.info("list end len[{}]".format(count))
    )
    msg.append(logger.info(
        "weseepro finish task_id[{}]".format(task_id)
    ))
    return detail_data


class Logger(object):
    pass

def log_test(x):
    print(x)
    return x


if __name__ == "__main__":
    start = time.time()
    print("start")
    task_info = {
        "detail": dict(),
        "crawler_info": {
            "start_page": 1,
            "end_page": 1,
            "base_dir": "/dockerdata",
        }
    }
    task_id = "local_test"
    logger = Logger()
    for level in [
        "INFO", "DEBUG", "ERROR", "WARNING", "DANGER"
    ]:
        setattr(logger, level.lower(), log_test)
    msg = list()
    detail = weseepro_start(task_id, task_info, logger, msg)
    with open("detail.json", "w") as f:
        f.write(json.dumps(detail))
    with open("log.txt", "w") as f:
        for line in msg:
            f.write(line + "\n")
    print("end")
    print("cost %.3f" % (time.time() - start))