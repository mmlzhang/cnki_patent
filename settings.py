
import os


PROJECT_NAME_CN = "中国专利网数据抓取"
PROJECT_NAME_EN = "patent_spider"

# 调试模式
DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 请求下载延迟
DOWNLOAD_DELAY = 1

# 布隆过滤器哈希文件位置
BLOOM_FILE_PATH = os.path.join(BASE_DIR, ".bloom_filter")

# 日志文件位置
LOG_DIR = os.path.join(BASE_DIR, "log")

# 数据存储目录
FILE_SAVE_PATH = os.path.join(BASE_DIR, "patent_data")

# chrome driver path
DRIVER_PATH = os.path.join(BASE_DIR, "utils/chromedriver")

# 钉钉
DING_TALK_URL = "https://oapi.dingtalk.com/robot/send?" \
                "access_token=ecc00ea08d61e9a49cf45e7a60edc76625ec4a1f85dd826725d78204969050c3"

# IP 代理
proxies = {
    # 'http': 'http:192.168.145.38:43128',
    # 'https': 'http://192.168.145.38:43128'
}
