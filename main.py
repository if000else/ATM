import sys,os,time
from conf import config
from modules import store
from modules import functions
from modules import creditcard
from modules import api_func
from modules import log
from modules import store
from modules.display import *

auth_tool = dict(name =None, auth = False,admin = None,data = None) #check login
def auth_user(fun):
    '''
    decorator
    :return:
    '''
    def wrapper(*args,**kwargs):
        if auth_tool["auth"]:
            fun(*args,**kwargs)
        else:
            functions.colordisplay("Acess is denied!","red")
    return wrapper

def auth_admin(fun):
    def wrapper(*args,**kwargs):
        if auth_tool["admin"]:
            fun(*args,**kwargs)
        else:
            functions.colordisplay("Acess is denied!", "red")
    return wrapper
@auth_admin
def freeze(car_number):
    data = api_func.db_hander("select","card_info")
    flag = data[car_number]["freeze"]
    data[car_number]["freeze"] = not flag # convert freeze status
    print("freeze successful!")
    api_func.db_hander("modify","card_info",data)
@auth_admin
def create_card(card_info):
    pass
@auth_admin
def mag_credit(car_number):
    data = api_func.db_hander("select", "card_info")
    credit_input = input("\033[1;33;1m Input amount>>:\033[0m")
    data[car_number]["credit"] = credit_input  # modify freeze flag
    print("modify credit successful!")
    api_func.db_hander("modify", "card_info", data)
@auth_admin
def mag_change(car_number):
    data = api_func.db_hander("select", "card_info")
    change_input = input("\033[1;33;1m Input amount>>:\033[0m")
    data[car_number]["change"] = change_input  # modify freeze flag
    print("modify change successful!")
    api_func.db_hander("modify", "card_info", data)

def store_payment(order_num,money,username):
    '''
    This is pay api for store.According order number and order price to pay,
    return True if success,else return False.
    :param order_num:
    :param money:
    :param username:
    :return:
    '''
    card_number = creditcard.find_user(username)# find card num by username
    print("card num:",card_number)
    data = api_func.db_hander("select", "card_info")
    if data[card_number]["freeze"]:
        functions.colordisplay("this card is frozen! payment is denied!","red")
    else:
        user_card = data[card_number]  # get user card info
        pay_psd = input("\033[1;33;1m Input pay password:\033[0m")
        count = 0
        if pay_psd == user_card["pay_password"]:
            if user_card["change"] < money:
                functions.colordisplay("Your balance is not enough!","red")
            else:
                data[card_number]["change"] -= money
                api_func.db_hander("modify","card_info",data)#write in file
                log.logger("transaction").info("Pay successfully!")
                return True
        else:
            functions.colordisplay("Sorry,pay password is incorrect!!!","red")
            count += 1
            if count >= 3:
                data[card_number]["freeze"] = True#freeze card
                print("User %s is frozen!"%username)
                api_func.db_hander("modify", "card_info", data)  # write in file
    return False




def card_center(login_data):
    '''

    :param user_data:
    :return:
    '''
    if login_data["auth"]: # user is login
            flag_card = True
            while flag_card:
                card_number = creditcard.find_user(login_data["name"])
                if not card_number:# user does not bind credit card
                    functions.colordisplay("can not find user in db","red")
                    flag_card = False
                else:
                    all_cards = api_func.db_hander("select", "card_info")
                    current_card = all_cards[card_number]  # get current user info
                    functions.colordisplay(menu_credit,"yellow")
                    menu_choice = functions.inpmsg("Input >>:", ('1', '2', '3', '4', '5', '6', '7', '8', '9', 'b')).strip()
                    if menu_choice == '1':#User Info
                        print("Current user: [%s]"%login_data["name"])
                    elif menu_choice == '2':#Card Info
                        print("Your card number: [%s]"%card_number)
                        detail = functions.inpmsg("[m] to display more...")
                        if detail == "m":
                            print("Detail info: %s"%current_card)
                    elif menu_choice == '3':# Repay
                        creditcard.repay(current_card)
                    elif menu_choice == '4':#Withdraw
                        creditcard.withdraw(current_card)
                    elif menu_choice == '5':#Transfer
                        creditcard.transfer(current_card)
                    elif menu_choice == '6':#Freeze
                        freeze(current_card["card_number"])
                    elif menu_choice == '7':#See my Bill
                        api_func.see_bill(auth_tool["name"])
                    elif menu_choice == '8':#Manage credit
                        mag_credit(current_card["card_number"])
                    elif menu_choice == '9':#Manage change
                        mag_change(current_card["card_number"])
                    else : # menu_choice == 'b'---Back
                        flag_card = False


    else:
        functions.colordisplay("Sorry,you need to login first!", "red")


def main():
    flag_menu = True # end program
    while flag_menu:
        if auth_tool["auth"]: # already authorized
            functions.colordisplay(menu_logout,"yellow")
        else: # login is required
            functions.colordisplay(menu_login, "yellow")
        menu_choice = functions.inpmsg("Input >>:", ('1', '2', '3', '4')).strip()
        if menu_choice == '1':
            if auth_tool["auth"]: # user want to logoff
                auth_tool["auth"] = False
                log.logger("access").info("User %s  logoff!" % auth_tool["name"])
            else: # user want to login
                login_data = functions.login()
                if login_data:
                    auth_tool["data"] = login_data
                    auth_tool["name"] = login_data["username"]
                    auth_tool["auth"] = True
                    auth_tool["admin"] = login_data["admin"]
        elif menu_choice == '2':  # Credit Card Center
            card_center(auth_tool)
        elif menu_choice == '3':  # Store
            if auth_tool["auth"]:
                store.shopping(auth_tool)
            else:
                functions.colordisplay("please login first!","red")
        elif menu_choice == '4':  # Exit
            print("Bye...")
            flag_menu = False
        else:
            print("Invalid input!")

    ###########
    # rewrite userdata
if __name__ == "__main__":
    main()
