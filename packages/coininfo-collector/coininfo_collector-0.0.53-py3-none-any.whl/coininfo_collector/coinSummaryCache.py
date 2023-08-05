# -*- coding: utf-8 -*-
# coinSummaryCache
import os
import logging
from .web_requests_async import async_post

log = logging.getLogger('coininfo_collector')

class CoinSummaryCacheBaseClass:
	pass

class CoinSummaryCacheSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(CoinSummaryCacheSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class CoinSummaryCache(CoinSummaryCacheBaseClass, metaclass=CoinSummaryCacheSingleton):
    def __init__(self):
        self._coinDict = dict()

    async def loadCoins(self):
        resp = await async_post(
            log,
            'http://' + os.environ['schudulerURLPrefix'] + '/load_coin_summary',
            retJson=True
        )
        if resp is not None:
            self._coinDict = resp['data']

            log.debug('post loadCoins()')
        else:
            log.error('failed loadCoins. url:{}'.format(
                'http://' + os.environ['schudulerURLPrefix'] + '/load_coin_summary',
            ))

        
    async def getCoinInfoByCoinId(self, coin_id):
        for k, obj in self._coinDict.items():
            if obj['coin_id'] == coin_id:
                return obj

        resp = await async_post(
            log,
            'http://' + os.environ['schudulerURLPrefix'] + '/get_coin_info',
            data={
                'coin_id':coin_id
            },
            retJson=True
        )
        if resp is not None:
            log.debug('post getCoinInfoByCoinId()')

            if resp['coinObj'] is not None:
                # save to cache.
                self._coinDict[int(resp['gecko_id'])] = resp['coinObj']
                return resp['coinObj']
        else:
            log.error('failed getCoinInfoByCoinId. url:{}'.format(
                'http://' + os.environ['schudulerURLPrefix'] + '/get_coin_info',
            ))

        return None



if __name__ == '__main__':
    from time import sleep

    while True:
        sleep(100)

    print('end')

