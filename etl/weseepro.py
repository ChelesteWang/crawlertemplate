from utils.common import request_http, tid_maker, load_json_from_file, current_time_str
import os
import json
import time

dir_name = "weseepro"


def get_name(item):
    # article_data['ground_message']
    if 'author' in item:
        return item['author'] if item['author'] else "无"
    if 'nick_name' in item:
        return item['nick_name'] if item['nick_name'] else "无"
    return "未知"


def weseepro_start(task_id, task_info, logger, msg):
    detail_data = task_info['detail'] if 'detail' in task_info else dict()
    config = task_info['etl_info']
    base_dir = config['base_dir']
    os.makedirs(base_dir, exist_ok=True)
    unique_code = detail_data['version']
    detail_data['wash_result'] = list()
    output_path = os.path.join(base_dir, dir_name, unique_code + "_wash")
    os.makedirs(output_path, exist_ok=True)
    msg.append(
        logger.info(
            "weseepro output_path[{}]  task_id[{}]".format(
                # pool_size,
                output_path, task_id
            )
        )
    )
    list_path = detail_data['list_path']
    list_data = load_json_from_file(list_path)
    article_dict = detail_data['article']
    for i, item in enumerate(list_data['data']):
        index = item['uuid']
        article_path = article_dict[index]
        article_data = load_json_from_file(article_path)
        article_data = article_data['data']
        res = dict()
        res['index'] = index
        res['rank'] = 100 - i
        # print(article_data['ground_message'])
        res['author'] = get_name(article_data['ground_message'])
        res['title'] = article_data['ground_message']['content']
        res['description'] = article_data['ground_message']['summary'] if 'summary' in article_data['ground_message'] else "无"
        res['publish_time'] = article_data['ground_message']['public_time'] if 'public_time ' in article_data['ground_message'] else current_time_str()
        res['url'] = article_data['ground_message']['url']
        res['path'] = article_path
        detail_data['wash_result'].append(res)
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
        "detail": {
            "version": "2020012322384589759962122",
            "list_path": "/dockerdata/weseepro/2020012322384589759962122/daily.json",
            "article": {"eb9bc085ca5543dabb7ad4297eb1ead3": "/dockerdata/weseepro/2020012322384589759962122/eb9bc085ca5543dabb7ad4297eb1ead3.json", "42ee871b10de475986ae1b3125a013d9": "/dockerdata/weseepro/2020012322384589759962122/42ee871b10de475986ae1b3125a013d9.json", "f55baf03ed5f4ce4be2fa2eee64369ec": "/dockerdata/weseepro/2020012322384589759962122/f55baf03ed5f4ce4be2fa2eee64369ec.json", "65e426ebea034ab3a4244fdfdae4e2bd": "/dockerdata/weseepro/2020012322384589759962122/65e426ebea034ab3a4244fdfdae4e2bd.json", "5204565b9f22463ca8e932d772f07103": "/dockerdata/weseepro/2020012322384589759962122/5204565b9f22463ca8e932d772f07103.json", "8cb8cb5242a94550bd36dfd6849ad69d": "/dockerdata/weseepro/2020012322384589759962122/8cb8cb5242a94550bd36dfd6849ad69d.json", "0356228e2b6c4c77b3544b78cf360951": "/dockerdata/weseepro/2020012322384589759962122/0356228e2b6c4c77b3544b78cf360951.json", "c1b861fd57a94728b8cb323d72360d87": "/dockerdata/weseepro/2020012322384589759962122/c1b861fd57a94728b8cb323d72360d87.json", "e85538d261074225a9d4ff263538ff88": "/dockerdata/weseepro/2020012322384589759962122/e85538d261074225a9d4ff263538ff88.json", "944ea7dc1e1d4626a38cfcd8e1b491c7": "/dockerdata/weseepro/2020012322384589759962122/944ea7dc1e1d4626a38cfcd8e1b491c7.json", "ca172e772fcd48019dd5d37723268eaa": "/dockerdata/weseepro/2020012322384589759962122/ca172e772fcd48019dd5d37723268eaa.json", "ebd1d98203ba453a870da0bc45a603b6": "/dockerdata/weseepro/2020012322384589759962122/ebd1d98203ba453a870da0bc45a603b6.json", "badf203d684d4086b02947b29fa5b76f": "/dockerdata/weseepro/2020012322384589759962122/badf203d684d4086b02947b29fa5b76f.json", "83c7429cd0d34c6e886601a18d76b8b0": "/dockerdata/weseepro/2020012322384589759962122/83c7429cd0d34c6e886601a18d76b8b0.json", "262fb0894fda4f37b884aadffc996ff2": "/dockerdata/weseepro/2020012322384589759962122/262fb0894fda4f37b884aadffc996ff2.json", "29db9f4bc4b2458b83833404b3892b7b": "/dockerdata/weseepro/2020012322384589759962122/29db9f4bc4b2458b83833404b3892b7b.json", "5eca95ed942644649b54b0ce51b23a18": "/dockerdata/weseepro/2020012322384589759962122/5eca95ed942644649b54b0ce51b23a18.json", "168f10b7f26b4a9f95b1090c7a414b78": "/dockerdata/weseepro/2020012322384589759962122/168f10b7f26b4a9f95b1090c7a414b78.json", "ebde8138d51948c7afc28c5b10c289c4": "/dockerdata/weseepro/2020012322384589759962122/ebde8138d51948c7afc28c5b10c289c4.json", "baf90cdf821f4101bd8ad59297b8d8fb": "/dockerdata/weseepro/2020012322384589759962122/baf90cdf821f4101bd8ad59297b8d8fb.json", "af876d3235fe42cf8c7e9f612335c266": "/dockerdata/weseepro/2020012322384589759962122/af876d3235fe42cf8c7e9f612335c266.json", "c2f6e7d8050f4b289684876b30eceee3": "/dockerdata/weseepro/2020012322384589759962122/c2f6e7d8050f4b289684876b30eceee3.json", "64b8f84899584657bf541b6843b94ef9": "/dockerdata/weseepro/2020012322384589759962122/64b8f84899584657bf541b6843b94ef9.json", "b3d2dbde59084ccbb32851394e6e45b5": "/dockerdata/weseepro/2020012322384589759962122/b3d2dbde59084ccbb32851394e6e45b5.json", "b2d295dc410a45b48f984bc511b16369": "/dockerdata/weseepro/2020012322384589759962122/b2d295dc410a45b48f984bc511b16369.json"}},
        "etl_info": {
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


