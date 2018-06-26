import json
import yaml
import os
import logging
import Tlock
import time
import shutil
import re
def file_init():
    PathSetLock=True
    paths={}
    while PathSetLock:
        servername=input("请输入服务器名字(输入Q完成路径设置)：")
        if(servername=='Q'):
            break
        serverpath=input("请输入文件路径：")
        paths[servername]=serverpath
    interval=input("时间间隔单位(分钟)：")
    backups=input("是否备份？(输入1为是，输入0为否)：")
    if backups==0:
        backups=0
    else:
        backups=1
    config_data={}
    config_data["paths"]=paths
    config_data["interval"]=interval
    config_data["backups"]=backups
    with open("config.json","w") as f:
        json.dump(config_data,f,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False)
def backup(config_data):
    current_time=time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    if not os.path.exists('./backups/'+current_time):
        os.mkdir('./backups/'+current_time)
    for path in config_data['paths'].keys():
        if not os.path.isfile(config_data['paths'][path]):
            logging.warning("文件"+config_data['paths'][path]+"不存在！")
        else:
            shutil.copyfile(config_data['paths'][path],'./backups/'+current_time+'/'+path+'.yml')      #复制文件
            logging.info("正在备份文件："+config_data['paths'][path])
def check_merge(config_data,permissions_is_merged):
    if config_data['backups']==1:
        backup(config_data)
    lock=True
    while(lock):
        try:
            yaml_permissions_data={}
            for (servername,path) in config_data['paths'].items():
                with open(path,"r") as f:
                    yaml_permissions_data[servername]=yaml.load(f)
                    logging.info("已载入"+servername+"的数据。")
            lock=False
        except IOError:
            print("打开文件错误，请重新进行设置")
            file_init()
            with open("config.json","r") as f:
                config_data=json.load(f)
    players_in_every_server_set={}
    players_in_all_server_set=set()
    for (servername,yaml_data) in yaml_permissions_data.items():
        players_in_every_server_set[servername]=set(yaml_permissions_data[servername]["users"].keys())
        players_in_all_server_set=players_in_every_server_set[servername]|players_in_all_server_set
    for player in players_in_all_server_set:
        #print(players_in_all_server_set)
        print(player)
        if re.match(r'^\w{8}\-\w{4}\-\w{4}\-\w{4}\-\w{12}',player):
            pass
        else:
            logging.warning("UUID错误："+player+",跳过该玩家！")
            continue
        permissions_in_every_server={}
        isExist_in_servers={}
        logging.info("检查玩家(UUID)："+player)
        for (servername,players_set_in_this_server) in players_in_every_server_set.items():
            if player in players_set_in_this_server:
                isExist_in_servers[servername]=True
                logging.info("此玩家存在于:"+servername+"游戏ID："+yaml_permissions_data[servername]["users"][player]['lastname'])
                permissions_in_every_server[servername]=set(yaml_permissions_data[servername]["users"][player]["permissions"])
            else:
                isExist_in_servers[servername]=False
                logging.info("此UUID在"+servername+"不存在")
        orset=set()
        andset=set()
        firstLOCK=0
        for servername in permissions_in_every_server:
            if isExist_in_servers[servername]:
                orset=orset|permissions_in_every_server[servername]
                if firstLOCK==0:
                    andset=orset
                    firstLOCK=1
                '''print(andset)
                print('&')
                print(permissions_in_every_server[servername])'''
                andset=andset&permissions_in_every_server[servername]
        '''print("orset")
        print(orset)
        print("andset")
        print(andset)'''
        different_permissions=orset-andset
        logging.info("DIFF权限集：")
        logging.info(different_permissions)
        for p in different_permissions:
            lock=False
            for ap in permissions_is_merged:
                if ap in p:
                    lock=True
            if lock:
                logging.info('权限'+p+'符合要求'+'进行合并，UUID存在的服务器：')
                for servername in isExist_in_servers:
                    if isExist_in_servers[servername]:
                        logging.info(servername)
                        permissions_in_every_server[servername].add(p)
        for servername in isExist_in_servers:
            if isExist_in_servers[servername]:
                yaml_permissions_data[servername]["users"][player]['permissions']=list(permissions_in_every_server[servername])
        logger.info("*****************************************************")
    for servername in config_data['paths'].keys():
        with open(config_data['paths'][servername],'w+') as f:
            yaml.dump(yaml_permissions_data[servername],f,default_flow_style=False,allow_unicode=True)
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
logfilename='logs.log'
logfilepath='./logs/'
if not os.path.exists(logfilepath):
    os.mkdir(logfilepath)
if not os.path.isfile(logfilepath+logfilename):
    first_f=open(logfilepath+logfilename,'w')
    first_f.writelines("************************BEGIN************************")
    first_f.close()
fh=logging.FileHandler(logfilepath+logfilename,mode='a')
fh.setLevel(logging.DEBUG)
ch=logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)