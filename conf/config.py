import os,sys,logging

#LOG
LogOfLevel = 20 # INFO
# PathOfLog = os.path.join(path,"log")

LogOfTypes = {
    'transaction': 'transactions.log',
    'access': 'access.log',
    'error':'error.log'
}

# Transaction
TransType = {
    "repay":0,
    "pay":0,
    "withdraw":0.05,
    "transfer":0.01
}
ShopLists = {
    '1001':{"item":"Love","price":999},
    '1002':{"item":"Knowledge","price":899},
    '1003':{"item":"Health","price":1000},
    '1004':{"item":"Luck","price":666},
    '1005':{"item":"Honor","price":199},
    '1006':{"item":"Friendship","price":399},
    '1007':{"item":"Family","price":599},
    '1008':{"item":"Relationship","price":299},
    '1009':{"item":"RP","price":9},

}
