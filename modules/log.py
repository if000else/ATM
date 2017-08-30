
import logging,os
from conf import config
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PathOfLog = os.path.join(path,"log")
def logger(log_type):
    '''
    :param log_type: access or transaction or others
    :return: obj or logger
    '''
    #create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(config.LogOfLevel)


    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(config.LogOfLevel)

    # create file handler and set level to warning
    log_file = "%s/%s" %(PathOfLog, config.LogOfTypes[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(config.LogOfLevel)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
#use:
# logger.info("text")