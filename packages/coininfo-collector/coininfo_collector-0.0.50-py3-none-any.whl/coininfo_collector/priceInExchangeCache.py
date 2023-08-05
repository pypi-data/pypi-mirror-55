# -*- coding: utf-8 -*-
# priceInExchangeCache
import os
import logging
from .web_requests_async import async_post

log = logging.getLogger('coininfo_collector')

import enum
class PriceTupleTag(enum.Enum):
    price = 0
    created_ts = 1

class PriceInExchangeCacheBaseClass:
	pass

class PriceInExchangeCacheSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(PriceInExchangeCacheSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class PriceInExchangeCache(PriceInExchangeCacheBaseClass, metaclass=PriceInExchangeCacheSingleton):
    def __init__(self):
        pass

    async def getPrice1day(self, market_id, coin_id):
        resp = await async_post(
            log,
            'http://' + os.environ['schudulerURLPrefix'] + '/get_price_1day',
            data={
                'market_id':market_id,
                'coin_id':coin_id
            },
            retJson=True
        )
        if resp is not None:
            log.debug('post getPrice1day()')
        else:
            log.error('failed getPrice1day. url:{}'.format(
                'http://' + os.environ['schudulerURLPrefix'] + '/get_price_1day',
            ))
        
        return resp

    async def getPrice1dayMarket(self, market_id):
        resp = await async_post(
            log,
            'http://' + os.environ['schudulerURLPrefix'] + '/get_price_1day_market',
            data={
                'market_id':market_id,
            },
            retJson=True
        )
        if resp is not None:
            log.debug('post getPrice1dayMarket()')
            return resp['market_price']
        else:
            log.error('failed getPrice1dayMarket. url:{}'.format(
                'http://' + os.environ['schudulerURLPrefix'] + '/get_price_1day_market',
            ))
            return None

    @staticmethod
    def getPrice1dayByMarketData(priceMap, coinId):
        for k, v in priceMap.items():
            if k == coinId:
                return v[0][PriceTupleTag.price.value]
        return None


    async def saveCoinPrice(self, market_id, addedInfoMap):
        resp = await async_post(
            log,
            'http://' + os.environ['schudulerURLPrefix'] + '/save_coin_price',
            data={
                'market_id':market_id,
                'addedInfoMap':addedInfoMap
            },
            retJson=True
        )
        if resp is not None:
            log.debug('post saveCoinPrice()')
        else:
            log.error('failed saveCoinPrice. url:{}'.format(
                'http://' + os.environ['schudulerURLPrefix'] + '/save_coin_price',
            ))
        
        return resp



if __name__ == '__main__':
    from time import sleep

    while True:
        sleep(100)

    print('end')

