import json,os,sys
from modules import api_func
from modules import creditcard
from modules import log
print(sys.path)
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PathOfDatabase = os.path.join(path,"database")
def colordisplay(string,arg):
    '''
    :param string: print strings with colors
    :param arg: red,green...
    :return:
    '''
    if arg == 'red':
     print("\033[1;31;1m%s\033[0m"%string)#红色
    elif arg == 'green':
     print("\033[1;32;1m%s\033[0m"%string)#绿色
    elif arg == 'yellow':
     print("\033[1;33;1m%s\033[0m"%string)#黄色
    elif arg == 'blue':
     print("\033[1;34;1m%s\033[0m"%string)#蓝色
    elif arg == 'purple':
     print("\033[1;34;1m%s\033[0m"%string)#紫色
    else:
     print("\033[1;30;1m%s\033[0m" %string)#白色


def login():
    '''
    call while login
    :return: info of user, dic;else return None
    '''
    count = [0,""]
    while True:
        all_userdata = api_func.db_hander("select", "user_info")  # get user_info
        print("All users:")##########
        for item in all_userdata.keys():############
            print(item)##########
        username = input("\033[1;33;1mPlease input username:\033[0m")
        username = username.strip()
        log.set_log("access",20,"User %s attempts to login!"%username)
        if username in all_userdata.keys():
            userdata = all_userdata[username] # get specific user
            psd = input("\033[1;33;1mPlease input password:\033[0m")
            psd = psd.strip()
            if psd == userdata["password"]:
                if userdata["locked"]:#locked
                    print("\033[1;31;1m User has been locked!!\033[0m")
                else:
                    log.set_log("access",20,"User %s  login successfully!" % username)
                    print("\033[1;33;1m Login accept!\033[0m")
                    return userdata
            else: #password is incorrect
                colordisplay("password is incorrect!","red")
                log.set_log("access",20,"User %s failed to login!" % username)
                if count[1] == username:# tha same user
                    count[0] += 1
                    if count[0] >= 3:#more than 3 times
                        colordisplay("User %s is locked because of attempting too many times!","red")
                        api_func.db_hander("modify","user_info",all_userdata)# write in file
                        log.set_log("access",20,"User %s is locked because of attempting too many times!" % username)
                else:# another user
                    count[1] = username
                    count[0] += 1

        elif username == "b": # back
            break
        else:
            print("\033[1;31;1m Can not find such user!!!\033[0m")
    return None

def db_handler(data,filename):
    '''
    update data timely
    :param data: type of dic
    :param filename: filename
    :return: data
    '''
    path = "%s/%s.txt"%(PathOfDatabase,filename)
    if filename == "user_info":
        with open(path, "w") as f:
            json.dump(data,f)
    elif filename == "card_info":
        with open(path, "w") as f:
            json.dump(data, f)
    return data

def inpmsg(message, limit_value=tuple()):
    '''
    inspect input message is valid or not
    :param message:sting type  to display
    :param limit_value:
    :return:
    '''
    is_null_flag = True
    while is_null_flag:
        input_value = input(message).strip().lower()
        if not input_value:
            colordisplay("Input is empty!", "red")
            continue
        elif len(limit_value) > 0:
            if input_value not in limit_value:
                colordisplay("Input is invalid,please retry!","red")
                continue
            else:
                is_null_flag = False
        else:
            is_null_flag = False
            continue
    return input_value