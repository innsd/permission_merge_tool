######################################################################################
#The tool which is used to merge permission of minecraft game plugin GroupManner     #
#author:insnd                                                                        #
#e-mail:innsd@qq.com                                                                 #
#The poor poor poor program haven't Exception handing,so,emmmmm......                #
#Please use std data                                                                 #
#ONLY RUN ON LINUX!                                                                  #
######################################################################################
import yaml
import os
import json
import schedule
import time
import threading
import Tlock
from funclib import *
logger.info('----------------------程序启动----------------------')
try:
    with open("config.json","r") as f:
        config_data=json.load(f)
    logging.info("1服路径："+config_data['path1'])
    logging.info("2服路径："+config_data['path2'])
    logging.info("3服路径："+config_data['path3'])
    logging.info("间隔时间："+str(config_data['interval']))
    logging.info("是否备份："+str(config_data['backups']))
    logger.info("*****************************************************")
#        print(config_data)
except FileNotFoundError:
    print("第一次使用本程序？请完成以下初始化设置：")
    file_init()
except PermissionError:
    print("文件权限错误，请联系系统管理员检查文件权限！")
    exit()
with open("permissions.json","r") as f_p:
    permissions_is_merged=json.load(f_p)
schedule.every(config_data["interval"]).minutes.do(check_merge,config_data,permissions_is_merged)
c=threading.Thread(target=console,name='console thread')
c.start()
while True:
    if Tlock.Tlock:
        logging.info("baybay~")
        c.join()
        exit()
    schedule.run_pending()
    time.sleep(1)
def stop():
    global Tlock
    Tlock=True