import logging
import os


username = ''
password = ''
code_province = ''
code_city = ''
location = ''
# vaccine = ''
jingdu = ''
weidu = ''
send_type = ''
send_parameter = ''
niuma=''
logger_level = os.getenv('jksb_logger_level')
jksb_timer =  os.getenv('jksb_timer')  # '[[0,35,10],[6,6,10]]'
zhb_parameter = os.getenv('jksb_zhb_parameter')
# baidu_API_Key =  "vN7WwZMuo5MhfX2uMSdcHqEC" # os.getenv("jksb_baidu_API_Key")  #
# baidu_Secret_Key = "kgR463xXGDLEOpK51apyG5bQjQsGDUpZ" # os.getenv("jksb_baidu_Secret_Key") #

# 检查参数是否都有值
if username is None:
    raise Exception("参数jksb_username无值")
if password is None:
    raise Exception("参数jksb_password无值")
if code_province is None:
    raise Exception("参数jksb_code_province无值")
if code_city is None:
    raise Exception("参数jksb_code_city无值")
if location is None:
    raise Exception("参数jksb_location无值")
if jingdu is None:
    raise Exception("参数jksb_jingdu无值")
if weidu is None:
    raise Exception("参数jksb_weidu无值")
if send_type is None:
    raise Exception("参数jksb_send_type无值")
if send_parameter is None:
    raise Exception("参数jksb_send_parameter无值")

# 设置日志等级
if logger_level == 'DEBUG':
    logger_level = logging.DEBUG
elif logger_level == 'WARNING':
    logger_level = logging.WARNING
elif logger_level == 'ERROR':
    logger_level = logging.ERROR
elif logger_level == 'INFO':
    logger_level = logging.CRITICAL
else:
    logger_level = logging.INFO


url_login = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
}

if __name__ == '__main__':
    tt = eval('[[6,6,9],[6,6,9]]')
    print(type(tt))
    for i,t in enumerate(tt):
        print(t[1])
