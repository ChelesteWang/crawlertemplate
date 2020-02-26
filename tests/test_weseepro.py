from tests.model import TestCase
from crawler.weseepro import weseepro_start as weseepro_crawler
from etl.weseepro import weseepro_start as weseepro_etl


class WeSeeProTestCase(TestCase):
    def crawler(self):
        return weseepro_crawler(self.task_id, self.task_info, self.logger, self.msg)

    def wash(self):
        return weseepro_etl(self.task_id, self.task_info, self.logger, self.msg)


if __name__ == "__main__":
    task_info = {
        "crawler_info": {
            "start_page": 1,
            "end_page": 1,
            "base_dir": "/dockerdata",
        },
        "etl_info": {
            "base_dir": "/dockerdata",
        }
    }
    WeSeeProTestCase(task_info).run()