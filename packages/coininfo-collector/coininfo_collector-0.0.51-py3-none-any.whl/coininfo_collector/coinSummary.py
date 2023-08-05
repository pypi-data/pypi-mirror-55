# -*- coding: utf-8 -*-
# coinSummary

'''
코인의 대략적인 정보를 관리합니다.

관리요소
 - gecko_id
 - symbol
 - name_en
 - name_ko
 - iamge_thumb
 - image_small
 - image_large
 - trade_url

 알정시간 마다 s3에 코인정보 스냅샷을 저장합니다.

 setCoinInfo => 코인정보 갱신.

 '''

import copy
from datetime import datetime
import enum
import logging
import os
from os.path import dirname, realpath
import requests
import threading
from time import mktime

from .db_manager import DBManager

from .s3Interface import S3Interface

log = logging.getLogger('coininfo_collector')


# GeckoStruct = {
#     coin_id = ''
#     gecko_id = 0
#     symbol = ''
#     name_en = ''
#     name_ko = ''
#     image_thumb = ''
#     image_small = ''
#     image_large = ''
# }

class MarketNoTag(enum.Enum):
    _global = 0
    binance = 1
    upbit = 2
    bithumb = 3

class PriceTupleTag(enum.Enum):
    price = 0
    created_ts = 1


class CoinSummaryBaseClass:
	pass

class CoinSummarySingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(CoinSummarySingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class CoinSummary(CoinSummaryBaseClass, metaclass=CoinSummarySingleton):
    def __init__(self):
        self._coinDict = dict()
        self._lock = threading.Lock()
        self._tickCnt = 0
        

    def initCoinSummary(self, dbConnString, connPool=None):
        self._dbm = DBManager(dbConnString, connPool=connPool)
        self._loadCoins()
        
        

    def _loadCoins(self):
        rows = self._dbm.selectGeckoCoinList()

        loaded_coin_ids = list()

        for row in rows:
            obj = {
                'coin_id' : row['coin_id'],
                'gecko_id' : int(row['gecko_id']),
                'symbol' : row['symbol'],
                'name_en' : row['name_en'],
                'name_ko' : row['name_ko'],
                'image_thumb' : row['image_thumb'],
                'image_small' : row['image_small'],
                'image_large' : row['image_large'],
                'trade_url' : row['trade_url'],

            }
            self._coinDict[int(obj['gecko_id'])] = obj

            loaded_coin_ids.append(row['coin_id'])

        log.debug('loaded coins:{}'.format(loaded_coin_ids))


    def getLoadedCoinsDump(self):
        return self._coinDict
        
    
    def tick(self):
        self._tickCnt += 1

        if (self._tickCnt % 1800) == 0:
            S3Interface().addJob({
                'jobName':'snapCoin',
                'data':{
                    'data':copy.deepcopy(self._coinDict),
                    'last_updated':int(mktime(datetime.utcnow().timetuple())),
                },
                'bucketName':'com.bitk.snap',
                'outputPrefix':'coin-summary/{}'.format(os.environ.get('runMode')),
            })


    def getCoinInfoByCoinId(self, coin_id):
        with self._lock:
            for k, obj in self._coinDict.items():
                if obj['coin_id'] == coin_id:
                    return obj

        return None


    def setCoinInfo(self, data):
        data['symbol'] = data['symbol'].upper()

        with self._lock:
            if data['gecko_id'] not in self._coinDict:
                self._coinDict[int(data['gecko_id'])] = data

                self._dbm.insertGeckoCoin(data)
                log.debug('inserted coin. coinID:{}'.format(data['coin_id']))
            else:
                dataOld = self._coinDict[int(data['gecko_id'])]
                update = False

                def diff(fieldName):
                    nonlocal update
                    nonlocal dataOld

                    if data[fieldName] != dataOld[fieldName]:
                        update = True
                        dataOld['coin_id'] = data['coin_id']

                diff('coin_id')
                diff('symbol')
                diff('name_en')
                diff('name_ko')
                diff('image_thumb')
                diff('image_small')
                diff('image_large')
                diff('trade_url')

                if update:
                    self._coinDict[int(data['gecko_id'])] = dataOld

                    self._dbm.updateGeckoCoin(dataOld)
                    log.debug('updated coin. coinID:{}'.format(data['coin_id']))


if __name__ == '__main__':
    import os
    appRoot = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    os.chdir(appRoot)

    # setup logging
    import utail_base
    utail_base.setup_logging(default_level=logging.DEBUG)
    utail_base.setup_logging_root(loggingLv=logging.DEBUG, filePath='/tmp/testLog.log')

    from time import sleep


    S3Interface().S3InterfaceInit(
        ACCESS_KEY=os.environ.get('aws_access_key_id'),
        SECRET_KEY=os.environ.get('aws_secret_access_key'),
    )
   
    cs = CoinSummary()
    cs.initCoinSummary(
        os.environ.get('dbConnString'),
    )
    cs._tickCnt = 1800 - 1

    while True:
        sleep(100)

    print('end')

