import os
import sys

from fastapi import FastAPI
from funtime import Store


from app.models.price import (
    BatchBarEpisode, SingleBarEpisode, 
    GetBarEpisode, GetBarEpisodeMulti,
    GetBarEpisodeMultiBefore, GetBarEpisodeBefore
)

mhost = os.getenv('MONGO_HOST', "localhost")
store = Store(mhost).create_lib('global').get_store()['global']

priceapi = FastAPI(openapi_prefix="/price")

@priceapi.post("/set_single")
async def SavePrice(set_single: SingleBarEpisode):
    """ 
        Given:

            1. episode: A string that highlights the current price
            2. is_live: A Boolean that highlights if we're adding pricing for real life
            3. single: A nested dictionary that has coin information that we're trying to save 
                1. coinname: a string that has the
                2. bar - A dictionary that pushes the key data
                    1. time
                    2. close
                    3. high
                    4. low
                    5. _open
                    6. volume
        
        * Save the bar in a temporary MongoDB database
        * If it's live, we ignore the episode id
    """
    coin = set_single.single.coinname
    bar = dict(set_single.single.bar)
    bar['type'] = "price_info" 
    bar['symbol'] = coin
    bar['timestamp'] = set_single.single.bar.time
    message = f"We've saved the coin: {coin}"
    if set_single.is_live:
        store.store(bar)
        return {"message": message, "success": True, "data": bar}    
    
    bar["episode"] = set_single.episode
    store.store(bar)
    return {"message": message, "success": True, "data": bar}


@priceapi.post("/get_single")
async def GetPrices(get_single: GetBarEpisode):
    """ 
        Given:

            1. Episode - An episode id from which you're getting the bar. This is ignored if live
            2. Coin Name - The pair balance
            3. Is Live - A boolean set to determine if we're getting the latest bar pricing
    
        * We ignore the episode if it's live 
        * This gets the latest bar. It should be used to get the correct information.
    """

    coin = get_single.coinname
    episode = get_single.episode
    message = f"Get latest bar for {coin}"

    if get_single.is_live:
        last = list(store.query_latest({
                "type": "price_info", 
                "episode": {'$exists': False}, 
                "symbol": coin
            })
        )

        if len(last) == 0:
            message = f"Prices for the coin: {coin} does not exist"
            return {
                "message": message,
                "last": [],
                "success": False
            }
        

        return {
            "message": message, 
            "last": last[0]
        }
    else:
        
        last = list(store.query_latest({
                "type": "price_info", 
                "episode": episode, 
                "symbol": coin
            })
        )

        if len(last) == 0:
            message = f"Prices for the coin: {coin} does not exist"
            return {
                "message": message,
                "last": [],
                "success": False
            }

        return {
            "message": message, 
            "last": last[0],
            "success": True
        }

@priceapi.post("/get_single_before")
async def GetPrices(get_single: GetBarEpisodeBefore):
    """ 
        Given:

            1. Episode - An episode id from which you're getting the bar. This is ignored if live
            2. Coin Name - The pair balance
            3. Is Live - A boolean set to determine if we're getting the latest bar pricing
    
        * We ignore the episode if it's live 
        * This gets the latest bar. It should be used to get the correct information.
    """

    coin = get_single.coinname
    episode = get_single.episode
    message = f"Get latest bar for {coin}"
        
    last = list(store.query_latest({
            "type": "price_info", 
            "episode": episode, 
            "symbol": coin,
            "since":get_single.timestamp
        })
    )

    if len(last) == 0:
        message = f"Prices for the coin: {coin} does not exist"
        return {
            "message": message,
            "last": [],
            "success": False
        }

    return {
        "message": message, 
        "last": last[0],
        "success": True
    }


@priceapi.post("/get_multi")
async def GetPricesMulti(get_multi: GetBarEpisodeMulti):
    """ 
        Given:

            1. Episode - An episode id from which you're getting the bar. This is ignored if live
            2. Coin Name - The pair balance
            3. Is Live - A boolean set to determine if we're getting the latest bar pricing
            4. Limit - The limit for

        * We ignore the episode if it's live 
    """

    coin = get_multi.coinname
    episode = get_multi.episode
    message = f"Get latest bar for {coin}"

    if get_multi.is_live:
        last = list(store.query_latest({
                "type": "price_info", 
                "episode": {'$exists': False}, 
                "symbol": coin
            })
        )

        if len(last) == 0:
            message = f"Prices for the coin: {coin} does not exist"
            return {
                "message": message,
                "last": [],
                "success": False
            }
        

        return {
            "message": message, 
            "last": last
        }
    else:
        
        last = list(store.query_latest({
                "type": "price_info", 
                "episode": episode, 
                "symbol": coin
            })
        )

        if len(last) == 0:
            message = f"Prices for the coin: {coin} does not exist"
            return {
                "message": message,
                "last": [],
                "success": False
            }

        return {
            "message": message, 
            "last": last,
            "success": True
        }

@priceapi.post("/get_multi_before")
async def GetPricesBefore(get_multi: GetBarEpisodeMultiBefore):
    """ 
        Given:

            1. Episode - An episode id from which you're getting the bar. This is ignored if live
            2. Coin Name - The pair balance
            3. Is Live - A boolean set to determine if we're getting the latest bar pricing
            4. Limit - The limit for

        * We ignore the episode if it's live 
    """

    coin = get_multi.coinname
    episode = get_multi.episode
    message = f"Get latest bar for {coin}"
        
    last = list(store.query_latest({
            "type": "price_info", 
            "episode": episode, 
            "symbol": coin,
            "since":get_multi.timestamp
        })
    )

    if len(last) == 0:
        message = f"Prices for the coin: {coin} does not exist"
        return {
            "message": message,
            "last": [],
            "success": False
        }

    return {
        "message": message, 
        "last": last,
        "success": True
    }


@priceapi.post("/set_multi")
async def SetPricesMulti(set_multi: BatchBarEpisode):
    """ 
        Given:

            1. A UserID
            2. An Exchange
            3. A Dict Explaining if this is a live, or backtest
    
        * Get the trades for a user. 
        * Use to determine if the trades are open or closed.
    """
    message = "Get trades for a certain user"
    
    
    coin = set_multi.multi.coinname
    episode = set_multi.episode
    bars = list(set_multi.multi.bars)
    message = f"We've saved the coin: {coin}"
    if set_multi.is_live:
        bar_list = []
        for bar in bars:
            bar = dict(bar)
            bar['type'] = "price_info" 
            bar['symbol'] = coin
            bar['timestamp'] = bar['time']
            bar_list.append(bar)
        
        store.bulk_upsert(bar_list)
        return {"message": message, "success": True, "data": bar_list}    
    else:
        bar_list = []
        for bar in bars:
            bar = dict(bar)
            bar['type'] = "price_info" 
            bar['symbol'] = coin
            bar['episode'] = episode
            bar['timestamp'] = bar['time']
            bar_list.append(bar)
        store.bulk_upsert(bar_list)
        return {"message": message, "success": True, "data": bar_list}