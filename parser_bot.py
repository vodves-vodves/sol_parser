import requests
import time
import cloudscraper
from json import dumps

url1 = 'https://api-mainnet.magiceden.io/popular_collections'
url2 = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery'
url3 = 'https://api-mainnet.magiceden.io/all_collections_with_escrow_data'
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': True
    }
)


def all_coll():
    params_all_coll = {
        'edge_cache': 'true'
    }
    all_coll = scraper.get(f'{url3}', params=params_all_coll)
    stat_code = all_coll.status_code
    all_coll = all_coll.json()
    all_coll_list = []
    if stat_code == 200 and all_coll['collections'] != []:
        for i in all_coll['collections']:
            all_coll_list.append(i['symbol'])
    else:
        all_coll_list.append('Что-то пошло не так!')
    return all_coll_list


def popular_coll(day):
    params_pop_coll = {
        'more': 'true',
        'timeRange': f'{day}d',
        'edge_cache': 'true'
    }
    pop_coll = scraper.get(f'{url1}', params=params_pop_coll)
    stat_code = pop_coll.status_code
    pop_coll = pop_coll.json()
    pop_coll_list = ''
    number = 1
    if stat_code == 200 and pop_coll['collections'] != []:
        for i in pop_coll['collections']:
            pop_coll_list += f'{number}) {i["name"]} - https://www.magiceden.io/marketplace/{i["symbol"]} \n\n'
            number += 1
    else:
        pop_coll_list += 'Что-то пошло не так!'
    return pop_coll_list


def floor_price_coll(coll):
    params = dumps({
        "$match": {"collectionSymbol": coll}, "$sort": {"takerAmount": 1}, "$skip": 0, "$limit": 15
    })
    one_coll = scraper.get(f'{url2}', params={'q':params})
    stat_code = one_coll.status_code
    one_coll = one_coll.json()
    all_collection_floor = ''
    if stat_code == 200 and one_coll['results'] != []:
        for i in one_coll['results']:
            all_collection_floor += f'{i["title"]} - {i["price"]} $SOL \nhttps://www.magiceden.io/item-details/{i["mintAddress"]}\n\n'

    else:
        all_collection_floor += 'Коллекция не существует или ошибка в названии!'
    return all_collection_floor


if __name__ == "__main__":
    print(popular_coll('30'))
    #print(all_coll())
    #print(floor_price_coll('degods'))

