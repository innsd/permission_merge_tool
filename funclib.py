import json
import yaml
import os
import logging
import Tlock
import time
import shutil
def file_init():
    path1=input("请输入第一个服务器的权限文件路径：")
    path2=input("请输入第二个服务器的权限文件路径：")
    path3=input("请输入第三个服务器的权限文件路径：")
    interval=input("时间间隔单位(分钟)：")
    backups=input("是否备份？(输入1为是，输入0为否)：")
    if backups==0:
        backups=0
    else:
        backups=1
    config_data={}
    config_data["path1"]=path1
    config_data["path2"]=path2
    config_data["path3"]=path3
    config_data["interval"]=interval
    config_data["backups"]=backups
    with open("config.json","w") as f:
        json.dump(config_data,f,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False)
def backup(config_data):
    paths={'path1':config_data["path1"],'path2':config_data['path2'],'path3':config_data['path3']}
    current_time=time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    if not os.path.exists('./backups/'+current_time):
        os.mkdir('./backups/'+current_time)
    for path in paths.keys():
        if not os.path.isfile(paths[path]):
            logging.warning("文件"+paths[path]+"不存在！")
        else:
            shutil.copyfile(paths[path],'./backups/'+current_time+'/'+path+'.yml')      #复制文件
            logging.info("正在备份文件："+paths[path])
def check_merge(config_data,permissions_is_merged):
    if config_data['backups']==1:
        backup(config_data)
    lock=True
    while(lock):
        try:
            with open(config_data["path1"],"r") as f1:
                permission1=yaml.load(f1)
            with open(config_data["path2"],"r") as f2:
                permission2=yaml.load(f2)
            with open(config_data["path3"],"r") as f3:
                permission3=yaml.load(f3)
            lock=False
        except IOError:
            print("打开文件错误，请重新进行设置")
            file_init()
            with open("config.json","r") as f:
                config_data=json.load(f)
    players_in_f1=set(permission1["users"].keys())
    players_in_f2=set(permission2["users"].keys())
    players_in_f3=set(permission3["users"].keys())
    players=players_in_f1|players_in_f2|players_in_f3
    for player in players:
        permissions_in_1=set()
        permissions_in_2=set()
        permissions_in_3=set()
        exist_in_1=False
        exist_in_2=False
        exist_in_3=False
        logger.info("检查玩家(UUID)："+player)
        if player in players_in_f1:
            exist_in_1=True
            permissions_in_1=set(permission1["users"][player]["permissions"])
            logger.info("此玩家在1服:"+permission1["users"][player]['lastname'])
        if player in players_in_f2:
            exist_in_2=True
            permissions_in_2=set(permission2["users"][player]["permissions"])
            logger.info("此玩家在2服:"+permission2["users"][player]['lastname'])
        if player in players_in_f3:
            exist_in_3=True
            permissions_in_3=set(permission3["users"][player]["permissions"])
            logger.info("此玩家在3服:"+permission3["users"][player]['lastname'])
        if not (exist_in_1 and exist_in_2 and exist_in_3):
            logger.info("此玩家不在所有服务器中存在，跳过")
            logger.info("*****************************************************")
            continue
        logger.info("玩家："+permission1["users"][player]['lastname']+"- - -")
        different_permissions=(permissions_in_1|permissions_in_2|permissions_in_3)-(permissions_in_1&permissions_in_2&permissions_in_3)
        logger.info("DIFF权限集：")
        logger.info(different_permissions)
        for p in different_permissions:
            lock=False
            for ap in permissions_is_merged:
                if ap in p:
                    lock=True
            if lock:
                logger.info("玩家："+permission1["users"][player]['lastname']+"的权限:"+p+"符合要求，进行合并")
                permissions_in_1.add(p)
                permissions_in_2.add(p)
                permissions_in_3.add(p)
                permission1["users"][player]['permissions']=list(permissions_in_1)
                permission2["users"][player]['permissions']=list(permissions_in_2)
                permission3["users"][player]['permissions']=list(permissions_in_3)
        logger.info("*****************************************************")
    lock=True
    while(lock):
        try:
            with open(config_data["path1"],"w+") as f1:
                yaml.dump(permission1,f1,default_flow_style=False,allow_unicode=True)
            with open(config_data["path2"],"w+") as f2:
                yaml.dump(permission2,f2,default_flow_style=False,allow_unicode=True)
            with open(config_data["path3"],"w+") as f3:
                yaml.dump(permission3,f3,default_flow_style=False,allow_unicode=True)
            lock=False
        except IOError:
            print("打开文件错误，请重新进行设置")
            file_init()
            with open("config.json","r") as f:
                config_data=json.load(f)
def console():
    loop_lock=True
    while loop_lock:
        command=input()
        if command=='stop':
            Tlock.LockToTrue()
            exit(0)
        elif command=='help':
            print('暂时没有写好，并且不打算写帮助了')
        elif command=='backup':
            pass
        elif command=='gc':
            pass
        else:
            print('未知命令，输入help查看帮助。')
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