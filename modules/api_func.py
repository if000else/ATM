import os,sys,json
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PathOfDatabase = os.path.join(path,"database")
PathOfReport = os.path.join("report")

def db_hander(actions,filename,dic_data = None):
    '''
    api for file read and write
    :param actions: select or modify
    :param filename: name of file so than write in
    :param kwargs: type of dic ,data is used to write in
    :return: None or data
    '''
    file_path = "%s/%s.txt"%(PathOfDatabase,filename)
    if os.path.isfile(file_path):
        if actions == "select":
            with open(file_path,'r') as f:
                data = json.load(f)
                # print("\033[1;33;1mImport successful!\033[0m")
                return data
        elif actions == "modify":
            with open(file_path, "w") as f:
                json.dump(dic_data,f)
                print("\033[1;34;1m Transaction is accept!\033[0m")
        else:
            print("\033[1;31;1mActions is invalid!\033[0m")
    else:
        print("\033[1;31;1mFile does not exist!\033[0m")
    return None

# def consume_record(username,order_number = None):
#     '''
#     when import order num,write in file ,otherwise  display user bill info only
#     :param username:
#     :param order_number:
#     :return:
#     '''
#     path = "%s/%sBill.txt"%(PathOfReport,username)
#     if order_number:#import order info
#         if os.path.isfile(path):
#             with open(path,'a+') as f:
#                 f.write(order_number+' '+username)#order + name
#                 print("record successful!")
#         else:
#             with open(path,'w') as f:
#                 f.write(order_number + ' ' + username)  # order + name
#                 print("record successful!")
#     else:# display bill info
#         with open(path,'r') as f:
#             for line in f:
#                 print(line)



def gene_order(price,shop_car,username,save=False):
    '''
    generate order_num and save to file according save flag
    :param price: total price of order,float
    :param shop_car: dic
    :param username:
    :param save: true or false
    :return:
    '''
    import time
    price = str(price)
    timestring = time.strftime("%Y%m%d%H%M%S")
    time_create = time.strftime("%Y-%m-%d %H:%M:%S")
    string = '60088'
    order_num = string+timestring
    path = "%s/order.txt" % PathOfReport
    with open(path, 'a') as f:  # time + order num + price + username
        f.write(time_create + ' ' + order_num + ' ' + price + ' ' + username + '\n')
        f.write("Details:\n")
        for item in shop_car.values():
            f.write(item["number"] + '--' + str(item["price"]) + '--' + str(item["amount"]) + '\n')
    # path_user = "%s/%sBill.txt" % (PathOfReport, username)
    # with open(path_user, 'a+') as f1:
    #     f1.write(time_create + ' ' + order_num + ' ' + username + price + 'yuan\n')
    #     print("Order have write in  user file!")
    return order_num
def user_bill(ordernum,username):
    '''
    find user order info with order num in order.txt
    :param ordernum:
    :return:
    '''
    import re
    order_path = "%s/order.txt" % PathOfReport
    user_path = "%s/%sBill.txt" % (PathOfReport, username)
    with open(order_path,'r') as f1,open(user_path,'a+') as f2:
        for line in f1:
            find = re.search(ordernum,line)
            if find:
                f2.write(line)


def see_bill(username):
    '''
    display user bill
    :param username:
    :return: None
    '''
    path = "%s/%sBill.txt"%(PathOfReport,username)
    with open(path,'r') as f:
        for line in f:
            if not line:
                print("No item to display!")
                break
            else:
                print(line)
    return None