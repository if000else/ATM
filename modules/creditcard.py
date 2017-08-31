from modules import api_func
from modules import functions
from conf import config
from modules import log
def find_user(username):
    '''
    find where the user has credit card ,return the  card number,else return None
    :param username:
    :return:
    '''
    userdata = api_func.db_hander("select","card_info")
    for items in userdata.values():
        if username == items["username"]:
            return items["card_number"]
    else:
        return None



def repay(card_info):
    '''
    call when user need to repay
    :param card_info:
    :return:
    '''
    if  card_info["freeze"]:# card is freeze
        functions.colordisplay("your card is frozen!Please refreeze first!", "red")
        return None
    card_number = card_info["card_number"]
    repay_change = card_info["credit"] - card_info["change"]
    if repay_change > 0:
        functions.colordisplay("You need to repay:%s yuan"%repay_change,"red")
    try:
        change = card_info["change"]
        print("Your change:%s yuan"%change)
        print("Your credit:%s yuan"%card_info["credit"])
        amount = input("\033[1;33;1m Input amount:>>\033[0m")
        interest = config.TransType["repay"]
        print("current interest:%s%%"%interest)
        new_change = calculate(amount, change, 'plus', interest)
        pay_auth = input("\033[1;33;1m Input pay password:>>\033[0m")
        if pay_auth == card_info["pay_password"]:
            data = api_func.db_hander("select","card_info")
            data[card_number]["change"] = new_change
            api_func.db_hander("modify", "card_info",data)# write in file
            print("new change:",new_change)
            log.set_log("transaction",20,"User %s repay successfully!"%card_info["username"])
        else:
            functions.colordisplay("Repay failed because of incorrect pay password!", "red")
            log.set_log("transaction",20,"User %s failed to repay,because of incorrect password" %card_info["username"])
    except Exception as e:
        log.set_log("errror",40,"User %s repay with error \n %s" %(card_info["username"],e))

def withdraw(card_info):
    '''
    call when user need to withdraw
    :param card_info: dic type
    :return:
    '''
    if  card_info["freeze"]:# card is freeze
        functions.colordisplay("your card is frozen!Please refreeze first!", "red")
        return None
    card_number = card_info["card_number"]
    try:
        change = card_info["change"]
        print("Your change:%s yuan"%change)
        amount = input("\033[1;33;1m Input amount:>>\033[0m")
        interest = config.TransType["withdraw"]
        print("Service fee %s%%:"%interest)
        new_change = calculate(amount, change, 'minus', interest)
        pay_auth = input("\033[1;33;1m Input pay password:>>\033[0m")
        if pay_auth == card_info["pay_password"]:
            data = api_func.db_hander("select", "card_info")
            data[card_number]["change"] = new_change
            api_func.db_hander("modify", "card_info", data)  # write in file
            print("Your new change:%s yuan"%new_change)
        else:
            functions.colordisplay("Repay failed because of incorrect pay password!", "red")
            log.set_log("transaction",20,"User %s withdraw failed,wrong pay password!"%card_info["username"])

    except Exception as e:
        functions.colordisplay(e, "red")
        log.set_log("error",40,"User %s withdraw failed, error!",card_info["username"])
def transfer(card_info):
    '''
    call when user need to transfer
    :param card_info: dic type
    :return: None
    '''
    if  card_info["freeze"]:# card is freeze
        functions.colordisplay("your card is frozen!Please refreeze first!","red")
    try:
        cur_card_number = card_info["card_number"]
        all_card_info = api_func.db_hander("select","card_info")
        print("current all cards: ")
        for key in all_card_info.keys():
            print(key)
        print("Your card num is:%s" %card_info["card_number"])
        change = card_info["change"]
        print("change:", change)
        trans_num = input("\033[1;33;1m Input card number you want to transfer:>>\033[0m")
        if trans_num in all_card_info.keys():
            amount = input("\033[1;33;1m Input amount:>>\033[0m")
            interest = config.TransType["transfer"]
            new_change = calculate(amount, change, 'minus', interest)
            pay_auth = input("\033[1;33;1m Input pay password:>>\033[0m")
            if pay_auth == card_info["pay_password"]:
                if trans_num in all_card_info.keys():
                    all_card_info[cur_card_number]["change"] -= new_change
                    all_card_info[trans_num]["change"] += float(change)  # receive account no interest
                    api_func.db_hander("modify", "card_info", all_card_info)  # Write in file
                    print("Your change remain:%s yuan"%all_card_info[cur_card_number]["change"])
                    log.set_log("transaction",20,"User %s transfer successfully!"%card_info["username"])

                else:
                    functions.colordisplay("Can not find the card number!","red")
            else:
                functions.colordisplay("Pay password is incorrect!","red")
                log.set_log("transaction",20,"User %s transfer failed,wrong pay_password!"%card_info["username"])
        else:
            functions.colordisplay("card does not exist!","red")

    except Exception as e:
        functions.colordisplay(e, "red")
        log.set_log("error",40,"User %s transfer failed, error!"%card_info["username"])
    return None
def calculate(amount,change,type,interest):
    '''
    calculate all kinds of transactions in detail
    :param amount:
    :param change:
    :param type:
    :param interest:
    :return: float change
    '''
    amount = float(amount)
    change = float(change)
    interest = float(interest)
    if type == 'plus':#plus
        change = amount + change*(1 - interest)

    elif type == 'minus':#minus
        change = change - amount - interest * amount
    else:
        functions.colordisplay("type error!","red")
        return None
    return change


