import json
import yaml
import os
import logging
def file_init():
    path1=input("请输入第一个服务器的权限文件路径：")
    path2=input("请输入第二个服务器的权限文件路径：")
    path3=input("请输入第三个服务器的权限文件路径：")
    interval=input("时间间隔单位(分钟)：")
    backups=input("是否备份？(输入1为是，输入0为否)：")
    config_data={}
    config_data["path1"]=path1
    config_data["path2"]=path2
    config_data["path3"]=path3
    config_data["interval"]=interval
    config_data["backups"]=backups
    with open("config.json","w") as f:
        json.dump(config_data,f,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False)
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logfile='./logs/logs.log'
fh=logging.FileHandler(logfile,mode='a')
fh.setLevel(logging.DEBUG)
ch=logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)