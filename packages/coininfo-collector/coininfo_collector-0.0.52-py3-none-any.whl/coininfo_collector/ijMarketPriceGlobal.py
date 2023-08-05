# -*- coding: utf-8 -*-
# ijMarketPriceGlobal
import logging
import os
import requests
import ujson
from .coinSummaryCache import CoinSummaryCache as CSC
from .web_requests_async import async_post, async_put


log = logging.getLogger('coininfo_collector')

class IJMarketPriceGlobal:
    reportURL_exchange_coins = ''
    reportURL_sparkline = ''
    requestURL_getCoinInfo = ''

    def __init__(self, *args, **kwargs):
        pass
    

    @staticmethod
    def setURL(
        urlExchangeCoins,
        urlSparklinePrefix,
        requestGetCoinInfoURL,
    ):
        IJMarketPriceGlobal.reportURL_exchange_coins = urlExchangeCoins
        IJMarketPriceGlobal.reportURL_sparkline = urlSparklinePrefix + '/updateSparkline'
        IJMarketPriceGlobal.requestURL_getCoinInfo = requestGetCoinInfoURL


    @staticmethod
    async def getCoinInfo(coinId):
        try:
            respJson = await async_post(
                log,
                IJMarketPriceGlobal.requestURL_getCoinInfo,
                data={
                    'coin_id':coinId,
                },
                retJson=True
            )
            if respJson is None:
                log.error('failed getCoinInfo. url:{}'.format(
                    IJMarketPriceGlobal.requestURL_getCoinInfo
                ))
                return None

        except Exception as inst:
            log.error('exception in getCoinPriceGlobal-getCoinInfo. msg:{}'.format(inst.args))
            return None

        return respJson

    @staticmethod
    async def reportCoinPriceGlobal(jobName, data):

        geckoIdList = list()

        async def makeOutput(order, collectGeckoId=False, cutVolume=0):

            log.debug('coinPriceGlobal. order:{} cutVolume:{}'.format(order, cutVolume))
            
            output = {}
            output['market_name'] = '_global'
            output['data'] = list()
            output['order'] = order
            rank = 0

            for coin in data[:]:
                
                if cutVolume > 0:
                    if cutVolume > coin['total_volume']:
                        data.remove(coin)
                        continue

                coinObjWrap = await IJMarketPriceGlobal.getCoinInfo(coin['id'])
                if coinObjWrap is None or coinObjWrap['coinObj'] is None:
                    log.error('none of coininfo. coindID:{}'.format(coin['id']))
                    continue

                coinObj = coinObjWrap['coinObj']

                

                output['data'].append(
                    {
                        'rank':rank,
                        'id':coinObj['coin_id'],
                        'name_en':coinObj['name_en'],
                        'name_ko':coinObj['name_ko'],
                        'current_price':float(coin['current_price']),
                        'price_change_percentage_24h':float(coin['price_change_percentage_24h']),
                        'symbol':coinObj['symbol'],
                        'total_volume':float(coin['total_volume']),
                        'img_num': int(coinObj['gecko_id']),
                        'trade_url': coinObj['trade_url'],
                        'image_thumb' : coinObj['image_thumb'],
                        'image_small' : coinObj['image_small'],
                        'image_large' : coinObj['image_large'],
                    }
                )

                # for sparkline
                if collectGeckoId:
                    geckoIdList.append(int(coinObj['gecko_id']))

                rank += 1
                if rank >= 10:
                    break

            return output

        async def reportFunc(url, output):
            resp = await async_put(log, url, data=output)
            if resp is None:
                log.error('failed reportCoinPriceGlobal. url:{}'.format(url))
            else:
                log.debug('reported reportCoinPriceGlobal')
                log.debug('testDump:{}'.format(ujson.dumps(output, ensure_ascii=False)))


        await reportFunc(
            IJMarketPriceGlobal.reportURL_exchange_coins,
            await makeOutput(
                'volume_desc',
                True,
            )
        )

        # data 를 가격변동순으로 정렬
        def getKey(coinEntity):
            if 'price_change_percentage_24h' not in coinEntity:
                return 0.0

            if coinEntity['price_change_percentage_24h'] is None:
                return 0.0

            return float(abs(float(coinEntity['price_change_percentage_24h'])))

        data = sorted(
            data,
            key=getKey,
            reverse=True
        )
        await reportFunc(
            IJMarketPriceGlobal.reportURL_exchange_coins + '_order_price_change24h',
            await makeOutput(
                'order_price_change_percentage_24h_desc',
                False,
                int(os.environ.get('GLOBAL_PRICE_CUT_VOLUME_USD', 0)),
            )
        )

        # update Sparkline
        await IJMarketPriceGlobal.reportSparkline(geckoIdList)

    
    @staticmethod
    async def reportSparkline(geckoIdList):
        try:
            # report to scheduler
            resp = await async_post(
                log,
                IJMarketPriceGlobal.reportURL_sparkline,
                data={
                    'geckoIdList':geckoIdList,
                }
            )
            if resp is None:
                log.error('failed report. url:{}'.format(
                    IJMarketPriceGlobal.reportURL_sparkline,
                ))
        except Exception as inst:
            log.error('exception in reportSparkline. url:{} msg:{}'.format(
                IJMarketPriceGlobal.reportURL_sparkline,
                inst.args
            ))
        



    @staticmethod
    async def _report_retry(retyCnt, name, url, output):
        for i in range(retyCnt):
            resp = await async_put(
                log,
                url,
                data=output
            )
            if resp is None:
                log.error('failed {}'.format(name))
            else:
                log.debug('reported {}. url:{}'.format(name, url))