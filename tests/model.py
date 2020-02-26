import uuid
import json
import traceback

class Logger(object):
    pass


def log_test(x):
    print(x)
    return x


class TestCase(object):
    def __init__(self, config_json, log_path="log.txt", detail_path="detail.json"):
        logger = Logger()
        for level in [
            "INFO", "DEBUG", "ERROR", "WARNING", "DANGER"
        ]:
            setattr(logger, level.lower(), log_test)
        self.logger = logger
        # 设置测试日志
        self.task_id = str(uuid.uuid1())
        self.task_info = config_json
        self.msg = list()
        self.log_path = log_path
        self.detail_path = detail_path

    def run(self):
        is_success = True
        try:
            detail = self.crawler()
            self.task_info['detail'] = detail
            detail = self.wash()
            print("测试完成")
            print(self.task_info["detail"]["version"])
        except:
            print(traceback.format_exc())
            is_success = False
        finally:
            with open(self.log_path, "w") as f:
                for line in self.msg:
                    f.write(line + "\n")
            with open(self.detail_path, "w") as f:
                f.write(json.dumps(self.task_info))
        print("test end")
        return is_success

    # override these function
    def crawler(self):
        # TODO: 爬虫测试函数
        print("test crawler")
        return dict()

    # override these function
    def wash(self):
        print("test wash")
        # TODO: etl测试函数
        return dict()


