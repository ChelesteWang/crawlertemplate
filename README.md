# 爬虫sdk开发规范 V1.0

编写人：qaq

## 更新日志

2020年2月27日    创建文档

## 一、前言



## 二、作业方式

单个爬虫的产出物

* `crawler/{name}.py` ，负责html或者json数据的抓取，存储
* `etl/{name}.py` ，负责将上一步爬取的数据进行抽取和解析，并*按照数据规格* 整理成交付的json数据，存储
* `tests/test_{name}.py`，继承 `tests/model.py` 的基类TestCase并编写可执行的测试样例
* 文档，必要的内容，详见 三

比如，我需要开发 [go2au](http://www.go2au.net/house/rent/) 的爬虫，那么我会开发

* `crawler/go2au.py` 爬取链接的html数据，返回必要的数据给etl，本地存储html文件
* `etl/go2au.py` 根据 `crawler/go2au.py`  抓取的html数据，清洗，并生成清洗json，本地存储
* tests/test_go2au.py 引用  `crawler/go2au.py` 和 `etl/go2au.py` 里面的主函数，串联整个测试流程
* 文档，必要的内容，详见 三

## 三、开发注意事项【必读】

### 3.1. 开发规范

1. 发送请求函数必须使用 utils/common.py 中的 `request_http` 函数，其他的可以抽出的公用函数：

   * 如果 utils/common.py 中有，请使用 `utils/common.py` 中的函数
   * 如果 `utils/common.py` 中没有，请新增到 `utils/common.py` 中并添加注释
   * **以上会在 code review 中被审核**

2. 主函数的格式应该为

   ```python
   def {name}_start(task_id, task_info, logger, msg):
       """
       task_id: 平台生成唯一task_id号，可以忽略
       task_info: 平台传来的配置信息，其中
                  task_info['crawler_info'] 中存着爬虫的配置
                  task_info['etl_info']中存着etl的配置
       logger：日志对象，生成msg
       msg: list 回传平台的日志信息，要求开发者使用 logger.info 或者其他等级如 logger.error 添加日志，并加入list。只需要加必要的日志，日志不能太多，但是必要的日志必须添加。
       * 函数最后返回的 detail_data 将会覆盖外部的task_info['detail']，并传递到etl或者下游，变量传递请使用该变量
       """
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
       # ...
       msg.append(logger.info(
           "weseepro finish task_id[{}]".format(task_id)
       ))
       return detail_data
   ```

   3. 开发者的代码需要在python3.5+的requirements.txt环境下可以运行，**如果需要新的依赖，请提出说明**
   4. 如果需要第三方服务支持（如googlemap，ocr识别，代理池），请和qaq联系

## 3.2 配置规范

```python
config = task_info['crawler_info']
# 1. crawler 必须有能控制爬取数量的参数设计, 如start_page, end_page
start = config['start_page']
end = config['end_page']
# 2. 必须要有base_dir, 作为数据默认存储路径，并在函数中定义 dir_name={name}，拼接成 base_dir/dir_name 作为本爬虫的 存储路径
dir_name = "go2au"
base_dir = config['base_dir']
download_dir = os.path.join(base_dir, dir_name)
os.makedirs(download_dir, exist_ok=True)
# 3. 在task_info['detail']中需要生成唯一的version, 使用 utils/common.py中的 tig_maker()
unique_code = tid_maker()
detail_data['version'] = unique_code
# 4. 在 task_info['crawler_info'] 中需要设计 'slience_time' 字段，单位秒，如果该字段不存在，则爬虫不sleep，如果存在，则每爬完一页，执行一次sleep
slience_time = config['slience_time'] if 'slience_time' in config else None
```

## 3.3. 抓取规范

1. 爬取web端的数据源时，请**先检查网站的robots.txt**协议，并**尽量遵守**，需要在产出物文档中说明robots协议，如果部分爬取接口没有遵守，请**加以注释说明**

2. 爬取源存在图片时，仅需要将图片的url存储在json结果中就可以，但是要求确保url可以访问

3. 如果涉及用户敏感信息，请谨慎爬取 （以 */user/* 等常见）

4. 如果抓取内容 是 不规则的，需要将爬取策略和PM沟通，梳理方案后再开发

5. 如果抓取源有 ip 限制（比如有的网站仅国内，或者某个地区可以访问）需要给出说明





