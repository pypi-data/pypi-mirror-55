# -*- coding: utf-8 -*-
# SSFixedJob
import logging
import requests
import ujson

import os
from time import time

# from .priceInExchange import PriceInExchange
#from .marketPairs import MarketPairs
from .coinSummaryCache import CoinSummaryCache
from .priceInExchangeCache import PriceInExchangeCache
from .sparklineWriter import SparklineWriter
from .web_requests_async import async_put, async_post


log = logging.getLogger('coininfo_collector')

class SSFixedJobs:
    reportURL_coins = ''
    reportURL_coinMarketPrice = ''
    reportURL_coins_markets = ''
    reportURL_global = ''
    reportURL_market_chart = ''
    reportURL_exchange_coins_ex = ''

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def setReportURL(
        url_data_svc
    ):
        SSFixedJobs.reportURL_coins = url_data_svc + '/coin/set'
        SSFixedJobs.reportURL_coinMarketPrice = url_data_svc + '/exchange/coins'
        SSFixedJobs.reportURL_coins_markets = url_data_svc + '/coin/markets'
        SSFixedJobs.reportURL_global = url_data_svc + '/coin/stats/global_gecko'
        SSFixedJobs.reportURL_market_chart = url_data_svc + '/coin/market/chart'
        SSFixedJobs.reportURL_exchange_coins_ex = url_data_svc + '/exchange/coins_ex'
        

    @staticmethod
    async def recvResponseAsync(jobName, output, id):
        if jobName == 'coins':
            await SSFixedJobs.reportCoins(output['data'])
            await SSFixedJobs.updateCoins(output['data'])
        elif jobName == 'coins_markets':
            await SSFixedJobs.reportCoinsMarket(output['data'])
        elif jobName == 'global':
            await SSFixedJobs.reportGlobal(output['data'])
            await SSFixedJobs.sendToTelegramSvc(
                os.environ['TELEGRAMSVC_ENDPOINT'] + '/primary_global',
                output['data']
            )
        elif jobName == 'market_chart':
            await SSFixedJobs.reportMarketChart(output['data'])
        elif jobName == 'ticker':
            if 'TICKER_USE' in os.environ:
                await SSFixedJobs.reportTicker(id, output)
        elif jobName == 'coinPriceMarket':
            await SSFixedJobs.reportCoinPriceMarket(output, id)

            if id == 'upbit':
                def findBitcoinPrice(output):
                    for ent in output['data']:
                        if ent['id'] != 'bitcoin':
                            continue
                        return ent['current_price']
                    return 0

                bitcoinPrice = findBitcoinPrice(output) 
                if 0 != bitcoinPrice:
                    await SSFixedJobs.sendToTelegramSvc(
                        os.environ['TELEGRAMSVC_ENDPOINT'] + '/coin_price_update',
                        {
                            'data':{
                                'exchange_id':'upbit',
                                'coin_id':'bitcoin',
                                'price':bitcoinPrice,
                            }
                        },
                    )


    @staticmethod
    async def sendToTelegramSvc(sendUrl, data):
        try:
            if 'TELEGRAMSVC_USE' not in os.environ:
                return

            if 'TELEGRAM_SVC_API_KEY' in os.environ:
                data['TELEGRAM_SVC_API_KEY'] = os.environ['TELEGRAM_SVC_API_KEY']

            resp = await async_put(
                log,
                sendUrl,
                data=data
            )
            if resp is not None:
                log.debug('send telegramsvc doc')
            else:
                log.error('failed send to TELEGRAMSVC_ENDPOINT. url:{}'.format(
                    sendUrl,
                ))
        except Exception as inst:
            print('exception in post to telegram-svc. url:{}'.format(
                sendUrl,
            ))


    @staticmethod
    async def reportCoins(data):
        try:
            resp = await async_put(
                log,
                SSFixedJobs.reportURL_coins,
                data=data
            )
            if resp is not None:
                log.debug('reported coins. url:{} coinId: {}'.format(
                    SSFixedJobs.reportURL_coins,
                    data['id']
                ))
            else:
                log.error('report failed coins. coinId:{} url:{}'.format(
                    data['id'],
                    SSFixedJobs.reportURL_coins,
                ))
        except Exception as inst:
            log.error('exception in reportCoins. msg:{}'.format(inst.args))

    @staticmethod
    async def reportCoinsMarket(data):
        perPage = 250

        marketsCnt = len(data)
        
        curIdx = 0
        curPage = 0

        while True:
            isLagePage = True if (curIdx+perPage) >= marketsCnt else False
            objectData = {"data":data[curIdx:curIdx+perPage], "page":curPage, "lastPage":isLagePage}

            resp = await async_put(
                log,
                SSFixedJobs.reportURL_coins_markets,
                data=objectData
            )
            if resp is not None:
                log.debug('reported reportCoinsMarket. curIDX:{} curPage:{}'.format(curIdx, curPage))
                break
            else:
                log.error('failed reportCoinsMarket. url:{}'.format(
                    SSFixedJobs.reportURL_coins_markets,
                ))

            if isLagePage is True:
                break

            curIdx = curIdx + perPage
            curPage = curPage + 1


    @staticmethod
    async def reportTicker(exchangeId, output):
        tickers = output['tickers']
        if 0 >= len(tickers):
            log.error('reportTicker(). empty tickers')
            return True

        try:
            resp = await async_put(
                log,
                SSFixedJobs.reportURL_exchange_coins_ex,
                data={
                    'name':exchangeId,
                    'tickers':tickers,
                    'mts':int(round(time() * 1000))
                }
            )
            if resp is not None:
                log.debug('reported tickers. exchange:{}'.format(exchangeId))
            else:
                log.error('failed reportTicker. url:{}'.format(
                    SSFixedJobs.reportURL_exchange_coins_ex,
                ))
        except Exception as inst:
            log.error('exception reportTicker. url:{} msg:{}'.format(
                SSFixedJobs.reportURL_exchange_coins_ex, inst.args
            ))

        
        # cpu 부하가 많아서 pair 정보는 업데이트는 보류..
        # SSFixedJobs.reportPairs()


    # @staticmethod
    # def reportPairs(exchange_id, tickers):
    #     #exchange_id = tickers[0]['market']['identifier']
    #     pairSet = set()

    #     for ticker in tickers:
    #         pairSet.add(
    #             ticker['base'] + '|' + ticker['target']
    #         )

    #     pairs = list(pairSet)
    #     pairs.sort(reverse=False)

    #     # pair update.
    #     MarketPairs().setMarketPairs(exchange_id, pairs)
    #     return True

    
    @staticmethod
    async def reportGlobal(data):
        data['mts'] = int(round(time() * 1000))

        resp = await async_put(
            log,
            SSFixedJobs.reportURL_global,
            data=data
        )
        if resp is not None:
            log.debug('reported reportGlobal.')
        else:
            log.error('failed reportGlobal. url:{}'.format(
                SSFixedJobs.reportURL_global,
            ))


    @staticmethod
    async def reportMarketChart(data):
        resp = await async_put(
            log,
            SSFixedJobs.reportURL_market_chart,
            data=data
        )
        if resp is not None:
            log.debug('reported reportMarketChart.')
        else:
            log.error('failed reportMarketChart. url:{}'.format(
                SSFixedJobs.reportURL_market_chart,
            ))


    @staticmethod
    async def updateCoins(data):
        # 게코넘버
        gecko_num = 0
        try:
            thumbURL = data['image']['thumb']
            idxStart = thumbURL.find('images/') + 7
            endIDX = thumbURL.find('/', idxStart)
            gecko_num = int(thumbURL[idxStart:endIDX])
        except Exception as inst:
            log.error('updateCoins failed get geckoNumber. id:{} msg:{} thumbURL:{}'.format(
                data['id'],
                inst.args,
                thumbURL,
                ))
            return

        trade_url = ''
        # for ticker in data['tickers']:
        #     if 'trade_url' not in ticker:
        #         continue

        #     if ticker['trade_url'] == None:
        #         continue

        #     trade_url = ticker['trade_url']
        #     break

            
        image_thumb = ''
        image_small = ''
        image_large = ''
        try:
            image_thumb = data['image']['thumb']
            image_small = data['image']['small']
            image_large = data['image']['large']
        except Exception as inst:
            log.error('updateCoins no field. error:{}'.format(inst.args))
            return

        try:
            await SSFixedJobs.setCoinInfo(
                {
                    'data':{
                        'coin_id' : data['id'],
                        'gecko_id' : int(gecko_num),
                        'symbol' : data['symbol'],
                        'name_en' : data['localization']['en'],
                        'name_ko' : data['localization']['ko'],
                        'image_thumb' : image_thumb,
                        'image_small' : image_small,
                        'image_large' : image_large,
                        'trade_url' : trade_url,
                    }
                }
            )
        except Exception as inst:
            log.error('failed updateCoins setCoinInfo. error:{}'.format(inst.args))

    @staticmethod
    async def setCoinInfo(data):
        resp = await async_post(
            log,
            'http://' + os.environ['schudulerURLPrefix'] + '/set_coin_info',
            data=data
        )
        if resp is not None:
            log.debug('post setCoinInfo()')
        else:
            log.error('failed setCoinInfo. url:{}'.format(
                'http://' + os.environ['schudulerURLPrefix'] + '/set_coin_info',
            ))


    @staticmethod
    async def reportCoinPriceMarket(output, marketId):
        # 모든 ticker 정보의 거래량 합산
        addedInfoMap = dict()
        exchangeList = list()
        volumeDic = dict()

        priceMap = await PriceInExchangeCache().getPrice1dayMarket(marketId)
        if priceMap is None:
            log.error('none of price1dMarket. marketId:{}'.format(marketId))
            return None


        def getPriceChange(price1d, current_price):
            if price1d is None:
                return 0.0
            if price1d == 0:
                return 0.0
            return ((current_price / price1d) - 1.0) * 100.0

        for ticker in output['tickers']:
            #print(ujson.dumps(ticker))
            if 'coin_id' not in ticker:
                log.debug('no coinid. content:{}'.format(ujson.dumps(ticker)))
                continue

            currentPrice = float(ticker['converted_last']['usd'])
            currentVolume = float(ticker['volume'])
            
            if str(ticker['coin_id']) not in addedInfoMap:
                sigPrice = currentPrice
                maxVolume = currentVolume

                addedInfoMap[str(ticker['coin_id'])] = (
                    sigPrice,       # 대표 가격.
                    ticker['trade_url'],
                    maxVolume,      # 최대 거래량.
                )

                price1d = PriceInExchangeCache().getPrice1dayByMarketData(priceMap, ticker['coin_id'])
                volumeDic[str(ticker['coin_id'])] = {
                    'vol':currentPrice * currentVolume,
                    'price1d':price1d,
                    'price_change':getPriceChange(price1d, currentPrice)
                }

            else:
                prevValues = addedInfoMap[str(ticker['coin_id'])]

                if currentVolume > prevValues[2]:
                    sigPrice = currentPrice
                    maxVolume = currentVolume

                    addedInfoMap[str(ticker['coin_id'])] = (
                        sigPrice,       # 대표 가격
                        ticker['trade_url'],
                        maxVolume,      # 최대 거래량
                    )

                volumeDic[str(ticker['coin_id'])]['vol'] += currentPrice * currentVolume

        for coin_id, value_pair in volumeDic.items():
            exchangeList.append(
                [
                    value_pair['vol'], 
                    coin_id,
                    value_pair['price1d'], 
                    value_pair['price_change'], 
                ]
            )


        # 보관하던 tickers 삭제
        del output['tickers']

        geckoIdList = list()

        async def makeOutput(order, collectGeckoId=False):
            
            output['data'] = list()
            output['order'] = order

            coinObjList = list()

            for coin in exchangeList:
                coinObj = await CoinSummaryCache().getCoinInfoByCoinId(coin[1])
                if coinObj is None:
                    log.error('none of coininfo. coin:{}'.format(coin[1]))
                else:
                    coinObjList.append((coin, coinObj))

                if 10 <= len(coinObjList):
                    break

            if 10 > len(coinObjList):
                log.error('다음 페이지를 읽어들여서 합산해야 함.')

            # 보고용 자료 생성
            for rank, coinPair in enumerate(coinObjList):
                coin = coinPair[0]
                coinObj = coinPair[1]
                current_price = float(addedInfoMap[coin[1]][0])

                output['data'].append( 
                    {
                        'rank':rank,
                        'id':coinObj['coin_id'],
                        'name_en':coinObj['name_en'],
                        'name_ko':coinObj['name_ko'],
                        'current_price':current_price,
                        'price_change_percentage_24h':coin[3],
                        'symbol':coinObj['symbol'],
                        'total_volume':coin[0],
                        'img_num': int(coinObj['gecko_id']),
                        'trade_url': addedInfoMap[coin[1]][1],
                        'image_thumb' : coinObj['image_thumb'],
                        'image_small' : coinObj['image_small'],
                        'image_large' : coinObj['image_large'],
                    }
                )

                if collectGeckoId:
                    nonlocal geckoIdList
                    geckoIdList.append(int(coinObj['gecko_id']))

            return output

        
        async def reportFunc(url, output):
            resp = await async_put(log, url, data=output)
            if resp is None:
                log.error('failed CoinPriceMarket. url:{}'.format(url))
            else:
                log.debug('reported CoinPriceMarket')
                log.debug('reported CoinPriceMarket contents:{}'.format(
                    ujson.dumps(output, ensure_ascii=False)
                ))


        #exchangeList.sort(reverse=True)
        # 볼륨정렬
        exchangeList.sort(key=lambda element : element[0], reverse=True)

        await reportFunc(
            SSFixedJobs.reportURL_coinMarketPrice,
            await makeOutput('volume_desc', True)
        )

        # 가격변동정렬
        def getKey(coinPair):
            if coinPair[3] is None:
                return 0.0
            return float(abs(float(coinPair[3])))

        exchangeList.sort(key=getKey, reverse=True)

        await reportFunc(
            SSFixedJobs.reportURL_coinMarketPrice + '_order_price_change24h',
            await makeOutput('order_price_change_percentage_24h_desc', False)
        )

        # 거래소-코인 가격정보 저장
        await PriceInExchangeCache().saveCoinPrice(marketId, addedInfoMap)

        # update Sparkline
        if 'sparklineWriter' in os.environ and os.environ['sparklineWriter'] == 'no':
            pass
        else:
            SparklineWriter().updateSparkline(geckoIdList)

        return True
        