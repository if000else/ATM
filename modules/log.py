
import logging,os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PathOfLog = os.path.join(path,"log")
def set_log(type,level,message):
    '''
    print log to file with parameters
    :param type: "acccess","transaction"...
    :param level: 10-50
    :param message:
    :return:
    '''
    file_name = "%s/%s.log"%(PathOfLog,type)
    logging.basicConfig(filename=file_name,format="%(asctime)s [%(levelname)s]>>:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",level=20)
    if level == 10:
        logging.debug(message)
    elif level == 20:
        logging.info(message)
    elif level == 30:
        logging.warning(message)
    elif level == 40:
        logging.error(message)
    elif level == 50:
        logging.critical(message)
# use:
# set_log("access","info","hi")

# LogOfLevel = 20 # INFO
#  PathOfLog = os.path.join(path,"log")
#
# LogOfTypes = {
#     'transaction': 'transactions.log',
#     'access': 'access.log',
#     'error':'error.log'
# }
# LogOfLevels = {
#     10 :"debug",
#     20 :"info",
#     30 :"warning",
#     40 :"error",
#     50 :"critical",
#
# }





# def logger(log_type):
#     '''
#     :param log_type: access or transaction or others
#     :return: obj or logger
#     '''
#     #create logger
#     logger = logging.getLogger(log_type)
#     logger.setLevel(config.LogOfLevel)
#
#
#     # create console handler and set level to debug
#     ch = logging.StreamHandler()
#     ch.setLevel(config.LogOfLevel)
#
#     # create file handler and set level to warning
#     log_file = "%s/%s" %(PathOfLog, config.LogOfTypes[log_type])
#     fh = logging.FileHandler(log_file)
#     fh.setLevel(config.LogOfLevel)
#     # create formatter
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
#     # add formatter to ch and fh
#     ch.setFormatter(formatter)
#     fh.setFormatter(formatter)
#
#     # add ch and fh to logger
#     logger.addHandler(ch)
#     logger.addHandler(fh)
#
#     return logger
# Access = logger("access")
# Transaction = logger("transaction")
# Error = logger("error")





