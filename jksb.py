import json
import os
import re

import requests
import logging

from time import sleep
import parameter
from parameter import *
import utils

logging.basicConfig(level=logger_level, format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger('jksb')

def run():
    # 输出参数状态
    logger.info("脚本启动成功！请验证你的信息：")
    logger.info("学号：" + parameter.username)
    logger.info("密码：" + parameter.password)
    logger.info("省份编号：" + parameter.code_province)
    logger.info("城市编号：" + parameter.code_city)
    logger.info("详细位置：" + parameter.location)
    logger.info("经度：" + parameter.jingdu)
    logger.info("纬度：" + parameter.weidu)
    logger.info("通知方法：" + parameter.send_type)
    logger.info("通知参数：" + parameter.send_parameter)

    # 打卡进程
    try:
        logger.info("正在检查是否已经打卡...")
        response_data = utils.get_signin_status()
        if response_data[0] is True and logger_level is not logging.DEBUG:
            logger.info("今日已成功打卡！")
        else:
            # ----------------------------登录后的首个页面----------------------------
            logger.info("今日尚未打卡！")
            logger.info("开始今日打卡进程...")
            did = re.search('(?<=did" value=")[0-9a-zA-Z]*(?=")', response_data[1]).group()
            door = re.search('(?<=door" value=")[0-9a-zA-Z]*(?=")', response_data[1]).group()
            sid1 = re.findall('(?<=sid" value=")[0-9a-zA-Z]*(?=")', response_data[1])[0]
            sid2 = re.findall('(?<=sid" value=")[0-9a-zA-Z]*(?=")', response_data[1])[1]
            men6 = re.search('(?<=men6" value=")[0-9a-zA-Z]*(?=")', response_data[1]).group()
            ptopid = re.search('(?<=ptopid" value=")[0-9a-zA-Z]*(?=")', response_data[1]).group()

            logger.debug("jksb页面中did参数值为："+did)
            logger.debug("jksb页面中door参数值为："+door)
            logger.debug("jksb页面中sid1参数值为："+sid1)
            logger.debug("jksb页面中men6参数值为："+men6)
            logger.debug("jksb页面中ptopid参数值为："+ptopid)
            logger.debug("jksb页面中sid2参数值为："+sid2)

            data_jksb_info = {
                'did': did,
                'door': door,
                'sid': [sid1, sid2],
                'men6': men6,
                'ptopid': ptopid,
            }
            url_jksb_info = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
            sleep(3)
            logger.info("正在获取打卡页面表单数据...")
            response_data = utils.http.request(method='POST', url=url_jksb_info, body=utils.urlencode(data_jksb_info), headers=header)
            logger.info("成功获取打卡页面表单数据！")
            # ----------------------------提交信息页面----------------------------
            sheng6 = re.search('(?<=sheng6" value=")[0-9a-zA-Z]*(?=")', response_data.data.decode())
            shi6 = re.search('(?<=shi6" value=")[0-9a-zA-Z]*(?=")', response_data.data.decode())
            fun3 = re.search('(?<=fun3" value=")[0-9a-zA-Z]*(?=")', response_data.data.decode())
            ptopid = re.search('(?<=ptopid" value=")[0-9a-zA-Z]*(?=")', response_data.data.decode())
            sid = re.search('(?<=sid" value=")[0-9a-zA-Z]*(?=")', response_data.data.decode())

            data_jksb = {
                'myvs_1': '否',  # 1. 您今天是否有发热症状?
                'myvs_2': '否',  # 2. 您今天是否有咳嗽症状?
                'myvs_3': '否',  # 3. 您今天是否有乏力或轻微乏力症状?
                'myvs_4': '否',  # 4. 您今天是否有鼻塞、流涕、咽痛或腹泻等症状?
                'myvs_5': '否',  # 5. 您今天是否被所在地医疗机构确定为确诊病例?
                'myvs_7': '否',  # 6. 您是否被所在地政府确定为密切接触者?
                'myvs_8': '否',  # 7. 您是否被所在地政府确定为次密切?
                'myvs_11': '否',  # 9. 您今天是否被所在地医疗机构进行院内隔离观察治疗?
                'myvs_12': '否',  # 10. 您今天是否被要求在政府集中隔离点进行隔离观察?
                'myvs_13': '否',  # 11. 您今日是否被所在地政府有关部门或医院要求居家隔离观察?
                'myvs_15': '否',  # 12. 共同居住人是否有确诊病例?
                'myvs_13a': parameter.code_province,  # **************当前实际所在省份（河南为41）
                'myvs_13b': parameter.code_city,  # **************当前实际所在地（请在平台自行查阅地点代码）
                'myvs_13c': parameter.location,  # **************当前所在详细地址（自行填写）
                'myvs_24': '否',  # 15. 您是否为当日返郑人员?
                'memo22': '成功获取',  # 地理位置（此项无需更改）
                'did': '2',
                'door': '',
                'day6': '',
                'men6': 'a',
                'sheng6': sheng6.group() if sheng6 else None,  # 此项从上方返回中找值
                'shi6': shi6.group() if shi6 else None,  # 此项从上方返回中找值
                'fun3': fun3.group() if fun3 else None,  # 此项从上方返回中找值
                'jingdu': jingdu,  # **************此项填所在地经度
                'weidu': weidu,  # **************此项填所在地纬度
                'ptopid': ptopid.group() if ptopid else None,
                'sid': sid.group() if sid else None,
            }
            url_jksb = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
            logger.debug("打卡信息："+str(data_jksb))
            sleep(3)
            logger.info("正在提交打卡信息...")
            response_data = utils.http.request(method='POST', url=url_jksb, body=utils.urlencode(data_jksb), headers=header)
            logger.info("提交打卡信息成功！")
            # ----------------------------结果返回页面----------------------------
            logger.info("正在查询打卡结果...")

            sleep(3)

            if ('同学'.__eq__(re.search('同学', response_data.data.decode()).group())) is True:
                logger.info("打卡成功！")
                sleep(60)
            else:
                utils.send_message("亲："+str(parameter.niuma)+" 打卡失败~手动手动~快快快~")
                logger.error("打卡失败！")

    except Exception as err:
        logger.error("程序运行异常！错误信息："+str(err))

def init():
    # json配置
    # 数据路径
    path = "./config.json"
    # 读取文件数据
    with open(path, "r", encoding='utf-8') as f:
        row_data = json.load(f)

    # 对单个用户进行循环
    now_user = 0
    user_total = len(row_data['data'])
    logger.info("===============总用户数===============：{}".format(user_total))
    # 读取每一条json数据
    for d in row_data['data']:
        if now_user >= 8:
            now_user = 0
            sleep(1200)
        now_user += 1
        # 获取需要的各个参数
        parameter.username = d['username']
        parameter.password = d['password']
        parameter.code_province = d['code_province']
        parameter.code_city = d['code_city']
        parameter.location = d['location']
        parameter.jingdu = d['jingdu']
        parameter.weidu = d['weidu']
        parameter.send_type = d['send_type']
        parameter.send_parameter = d['send_parameter']
        parameter.niuma = d['niuma']
        # 打卡
        run()

if __name__ == '__main__':
    init()
