from modules import display
from modules import functions
from modules import creditcard
from conf import config
from modules import api_func
# import main.store_payment
import os,sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.join(path)
sys.path.append(path)
import main

def shopping(autu_tool):
    '''
    This is a life store.You can buy something special according to your need.And you can add things
    to your shop car,then pay with your credit card.
    :param autu_tool: login check
    :return: None
    '''
    shop_car = {}
    shop_flag = True
    while shop_flag:
        functions.colordisplay(display.shop_list,"yellow")
        choice = functions.inpmsg("Input:",('1001','1002','1003','1004','1005',
                                                 '1006','1007','1008','1009','ok','pay','b'))
        select = config.ShopLists.keys()
        single = {"number":None,"price":None,"amount":0}
        if choice in select:
            if choice in shop_car.keys():#already select
                shop_car[choice]["amount"] += 1
            else:
                single["number"] = choice
                single["price"] = config.ShopLists[choice]["price"]
                single["amount"] = 1
                new_dic = {single["number"]:single}
                shop_car.update(new_dic)
                print("Added to shop car...")
        elif choice == 'ok':
            print("You have choose:")
            print("number price amount")
            for items in shop_car.values():
                print(items["number"],' ',items["price"],' ',items["amount"])
        elif choice == 'pay':
            if not shop_car: # shop_car is empty!!!
               functions.colordisplay("You didn't add any goods!",'red')
            else:
                print("Generating bill...")
                total = shop_car_dc(shop_car)#get total price
                print("Generating order...")
                order_num = api_func.gene_order(total,shop_car,autu_tool["name"])
                print("Skipping to payment...")
                pay_flay = main.store_payment(order_num,total,autu_tool["name"])# call payment
                if  pay_flay:# pay success
                    shop_car.clear()# clear shop car
                else:
                    print("Pay failed,please check!")
        else:
            print("User %s leave store..."%autu_tool["name"])
            shop_flag = False
    return None
def shop_car_dc(shop_car):
    '''
    display all item of shop_car in detail and calculate total price
    :param shop_car:
    :return:total_price float
    '''
    line = 1
    print(display.shop_car)
    total_price = 0
    for i in shop_car.values():
        price = float(i["price"])
        amount = float(i["amount"])
        total_price = total_price +  price * amount
        print("{line}.   {num}  {price} {amount}".format(
            line = str(line),num = i["number"],price = i["price"], amount = i["amount"]
        ) )
        line += 1
    print("sum =",total_price)

    return total_price
