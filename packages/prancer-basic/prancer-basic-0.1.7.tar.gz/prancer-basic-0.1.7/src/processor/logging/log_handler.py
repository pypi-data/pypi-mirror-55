"""Helper functions to setup logging for the framework."""
import datetime
import logging
from logging.handlers import RotatingFileHandler
import datetime
import time
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from processor.helper.config.config_utils import framework_dir,\
    get_config_data, framework_config, TESTS, NODB, config_value


FWLOGGER = None
FWLOGFILENAME = None
MONGOLOGGER = None
DBLOGGER = None
dbhandler = None



class MongoDBHandler(logging.Handler):
    """Customized logging handler that puts logs to the database, pymongo required
    """
    def __init__(self, dburl, dbname):
        global DBLOGGER
        logging.Handler.__init__(self)
        try:
            # dbconnection = MongoClient(port=27017, serverSelectionTimeoutMS=3000)
            dbconnection =  MongoClient(host=dburl, serverSelectionTimeoutMS=3000)
            _ = dbconnection.list_database_names()
            if dbname:
                db = dbconnection[dbname]
            else:
                db = dbconnection['test']
            # collection = 'logs_%s' % datetime.datetime.now().strftime('%Y%M%d%H%M%S')
            if db:
                self.db = db
                self.set_log_collection()
            else:
                self.collection = None
                self.coll_name = ''
                # coll = db[collection]
                # self.db = db
                # self.collection = coll
                # # DBLOGGER = '%s:%s' % (dbname, collection)
                # DBLOGGER = collection
        except ServerSelectionTimeoutError as ex:
            self.collection = None

    def set_log_collection(self):
        global DBLOGGER
        coll_name = 'logs_%s' % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        coll = self.db[coll_name]
        self.collection = coll
        DBLOGGER = coll_name
        self.coll_name = coll_name

    def get_log_collection(self):
        return self.coll_name

    def reset_log_collection(self):
        self.collection = None
        self.coll_name = ''

    def emit(self, record):
        """Add record to the database"""
        # format the log message so it can be put to db (escape quotes)
        self.log_msg = self.format(record)
        db_record = {
            "timestamp": int(time.time() * 1000),
            "level": record.levelname,
            "module": record.module,
            "line": record.lineno,
            "asctime": record.asctime,
            "msg": self.log_msg
        }

        try:
            if self.collection:
                self.collection.insert(db_record, check_keys=False)
        except Exception as e:
            print('CRITICAL Logger DB ERROR: Logging to database not possible!')



def logging_fw(fwconfigfile):
    """Framework file logging"""
    global FWLOGFILENAME, dbhandler
    fwlogfile = '%Y%m%d-%H%M%S'
    if not fwconfigfile:
        fwconfigfile = framework_config()
    fw_cfg = get_config_data(fwconfigfile)
    log_config = {
        "level": logging.INFO,
        "propagate": True,
        "size": 10,
        "backups": 10,
        "db": None
    }
    if fw_cfg and 'LOGGING' in fw_cfg:
        fwconf = fw_cfg['LOGGING']
        log_config['level'] = logging.getLevelName(fwconf['level']) \
            if 'level' in fwconf and fwconf['level'] else logging.INFO
        log_config['size'] = fwconf.getint('size') if 'size' in fwconf else 10
        log_config['backups'] = fwconf.getint('backups') if 'backups' in fwconf else 10
        log_config['propagate'] = fwconf.getboolean('propagate') if 'propagate' in fwconf \
            else True
        log_config['db'] = fwconf['dbname'] if 'dbname' in fwconf else None
        log_config['dburl'] = fw_cfg['MONGODB']['dburl'] if 'dbname' in fwconf else None
    level = os.getenv('LOGLEVEL', None)
    loglevel = level if level and level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] \
        else log_config['level']
    logformat = '%(asctime)s(%(module)s:%(lineno)4d) - %(message)s'
    logging.basicConfig(level=loglevel, format=logformat)
    logger = logging.getLogger(__name__)
    logger.propagate = log_config['propagate']
    # logpath = '%s/log/' % get_logdir(fw_cfg)
    _, logpath = get_logdir(fw_cfg)
    FWLOGFILENAME = '%s/%s.log' % (logpath, datetime.datetime.today().strftime(fwlogfile))
    handler = RotatingFileHandler(
        FWLOGFILENAME,
        maxBytes=1024 * 1024 * log_config['size'],
        backupCount=log_config['backups']
    )
    handler.setFormatter(logging.Formatter(logformat))
    handler.setLevel(log_config['level'])
    logger.addHandler(handler)
    unittest = os.getenv('UNITTEST', "false")
    nodb = config_value(TESTS, NODB, False)
    if log_config['db'] and unittest != "true" and not nodb:
        dblogformat = '%(asctime)s-%(message)s'
        dbhandler = MongoDBHandler(log_config['dburl'], log_config['db'])
        dbhandler.setFormatter(logging.Formatter(dblogformat))
        dbhandler.setLevel(loglevel)
        logger.addHandler(dbhandler)
    return logger


def getlogger(fw_cfg=None):
    """Get the logger for the framework."""
    global FWLOGGER
    if FWLOGGER:
        return FWLOGGER
    FWLOGGER = logging_fw(fw_cfg)
    return FWLOGGER

def get_logdir(fw_cfg):
    log_writeable = True
    if not fw_cfg:
        cfgini = framework_config()
        fw_cfg = get_config_data(cfgini)
    logdir = '%s' % framework_dir()
    if fw_cfg and 'LOGGING' in fw_cfg:
        fwconf = fw_cfg['LOGGING']
        if 'logFolder' in fwconf and fwconf['logFolder'] and os.path.isdir(logdir):
            logdir = '%s/%s' % (logdir, fwconf['logFolder'])
            try:
                if not os.path.exists(logdir):
                    os.makedirs(logdir)
            except:
                log_writeable = False
    try:
        if log_writeable:
            from pathlib import Path
            testfile = '%s/%d' % (logdir, int(time.time()))
            Path(testfile).touch()
            if os.path.exists(testfile):
                os.remove(testfile)
            else:
                log_writeable = False
    except:
        log_writeable = False
    return log_writeable, logdir

def get_dblogger():
    return DBLOGGER

def get_dblog_handler():
    return dbhandler

