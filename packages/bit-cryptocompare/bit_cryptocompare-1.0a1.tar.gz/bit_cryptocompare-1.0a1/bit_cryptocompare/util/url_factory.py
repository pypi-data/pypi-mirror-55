import logging
import sys
import traceback
from enum import Enum
from functools import wraps
from typing import Any, Mapping

import requests
from requests.exceptions import HTTPError, RetryError, UnrewindableBodyError, \
    ConnectionError, Timeout, URLRequired, TooManyRedirects, ChunkedEncodingError, \
    ProxyError, SSLError, ConnectTimeout, ReadTimeout, MissingSchema, InvalidSchema, \
    InvalidURL, InvalidHeader, InvalidProxyURL, ContentDecodingError, StreamConsumedError

import bit_cryptocompare.errors as errors
from bit_cryptocompare.config import crypto_compare_config as explorer, default_config
from bit_cryptocompare.util.data import CryptoCompare

query_pattern = r'\.+'


def generate_url(named_url: str, query: Mapping = None) -> str:
    """ Generate a url fragment that can be passed to targeted API """
    if isinstance(query, Mapping):
        named_url += '?'
        query = [f'{x}={y}' for x, y in query.items() if y is not None]
        if query:
            start = query[0]
            named_url += start
            fragment = '&'.join(query[1:])
            named_url += fragment
            return named_url
        return named_url


def _generic_call(api_url, essential: Mapping = None, query: Mapping = None):
    url_key = None
    keyed_endpoints = ['EXCHANGES_WITH_ORDER_BOOK_DATA', 'ORDER_BOOK_L1_TOP',
                       'ORDER_BOOK_L2_SNAPSHOT', 'ALL_EXCHANGES_GENERAL_INFO',
                       'NEWS_ARTICLE_CATEGORIES']
    headers = {'content-type': 'application/json'}

    if isinstance(api_url, Enum):
        url_key = api_url.value
    elif isinstance(api_url, str):
        url_key = api_url.upper()

    # Prepare the header with api key
    if url_key in keyed_endpoints:
        try:
            api_key = default_config.get_by_value('user', 'api_key')
            if isinstance(api_key, str) and api_key.lower() == 'none':
                raise errors.ApiKeyError('API key not available or invalid')
            headers.update({'authorization': api_key})
        except KeyError:
            raise KeyError('API key not available or invalid')

    # Prepare the query for the endpoint
    if 'extraParams' not in query:
        extras = default_config.get_by_value(section='application', option='name')
        query['extraParams'] = extras
    if isinstance(essential, Mapping):
        query.update(essential)

    for k, v in query.items():
        if isinstance(v, bool):
            v = str(v)
            query[k] = v.lower()
        if not isinstance(v, str):
            query[k] = str(v)

    target_url = explorer.get_by_value('urls', url_key)

    # Prepare request
    server_response = requests.get(target_url, headers=headers, params=query)

    status_code = server_response.status_code
    if 200 <= status_code < 400:
        return server_response.json()
    if status_code >= 400:
        if 'auth key' in server_response.content.get('Message'):
            raise errors.ApiKeyError
        raise errors.HttpResponseError


def network_log(func):
    def _logger(e: Exception, enable_log):
        logging.basicConfig(filename=default_config.get_by_value('logging', 'log'),
                            level=logging.ERROR)
        message = str()
        _, _, exception_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(exception_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                    "File: %s; Line: %d; Function: %s; Message: %s" %
                    (trace[0], trace[1], trace[2], trace[3]))
            if enable_log:
                message += '\n'.join(stack_trace)
                logging.log(level=logging.ERROR, msg=message)
            else:
                raise e

    @wraps(func)
    def wrapper(*args, **kwargs):
        enable_log = default_config.get_by_value('logging', 'enabled')

        try:
            return func(*args, **kwargs)
        except (HTTPError, RetryError, UnrewindableBodyError, ConnectionError, Timeout,
                URLRequired, TooManyRedirects, ChunkedEncodingError) as e:
            _logger(e, enable_log)
        except (ProxyError, SSLError, ConnectTimeout) as e:
            _logger(e, enable_log)
        except ReadTimeout as e:
            _logger(e, enable_log)
        except (MissingSchema, InvalidSchema, InvalidURL, InvalidHeader) as e:
            _logger(e, enable_log)
        except InvalidProxyURL as e:
            _logger(e, enable_log)
        except (ContentDecodingError, StreamConsumedError) as e:
            _logger(e, enable_log)

    return wrapper


def single_symbol_price(fsym: str, tsyms: str, try_conversion: bool = True,
                        relaxed_validation: bool = True, exchange: str = None,
                        extras: Any = None, sign: bool = False):
    return _generic_call(
            CryptoCompare.SINGLE_SYMBOL_PRICE,
            essential={
                    'fsym': fsym,
                    'tsyms': tsyms,
            },
            query={
                    'tryConversion': try_conversion,
                    'relaxedValidation': relaxed_validation,
                    'e': exchange,
                    'extraParams': extras,
                    'sign': sign
            })


def multiple_symbols_price(fsyms: str, tsyms: str, try_conversion: bool = True,
                           relaxed_validation: bool = True, exchange: str = None,
                           extras: str = None, sign: bool = None):
    # essential parameters: fsym, tsyms
    return _generic_call(
            CryptoCompare.MULTIPLE_SYMBOLS_PRICE,
            essential={
                    'fsyms': fsyms,
                    'tsyms': tsyms,
            },
            query={
                    'tryConversion': try_conversion,
                    'relaxedValidation': relaxed_validation,
                    'e': exchange,
                    'extraParams': extras,
                    'sign': sign
            })


def multiple_symbols_full_data(fsyms: str,
                               tsyms: str, try_conversion: bool = True,
                               relaxed_validation: bool = True,
                               exchange: str = None,
                               extras: str = None, sign: bool = True):
    # essential parameters: fsym, tsyms
    return _generic_call(
            CryptoCompare.MULTIPLE_SYMBOLS_FULL_DATA,
            essential={
                    'fsyms': fsyms,
                    'tsyms': tsyms
            },
            query={
                    'tryConversion': try_conversion,
                    'relaxedValidation': relaxed_validation,
                    'e': exchange,
                    'extraParams': extras,
                    'sign': sign
            })


def generate_custom_average(fsym: str, tsym: str, exchange: str,
                            relaxed_validation: bool = False,
                            extras: str = None, sign: bool = True):
    # essential parameters: fsym, tsyms, e
    return _generic_call(
            CryptoCompare.GENERATE_CUSTOM_AVERAGE,
            essential={
                    'fsym': fsym,
                    'tsym': tsym,
                    'e': exchange
            },
            query={
                    'relaxedValidation': relaxed_validation,
                    'extraParams': extras,
                    'sign': sign
            })


def daily_pair_ohlcv(fsym: str, tsym: str, try_conversion: bool = True,
                     aggregate: str = None,
                     aggregate_predictable_time_periods: str = None):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.DAILY_PAIR_OHLCV,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'tryConversion': try_conversion,
                    'aggregate': aggregate,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods
            }
    )


def hourly_pair_ohlcv(fsym: str, tsym: str, try_conversion: bool = True,
                      aggregate: str = None,
                      aggregate_predictable_time_periods: str = None, limit: str = None,
                      tots: str = None, explain_path: str = None,
                      extras: str = None,
                      sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.HOURLY_PAIR_OHLCV,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    try_conversion: 'tryConversion',
                    'aggregate': aggregate,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'limit': limit,
                    'toTs': tots,
                    'explain_path': explain_path,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def minute_pair_ohlcv(fsym: str = None, tsym: str = None, try_conversion: bool = True,
                      aggregate: str = None,
                      aggregate_predictable_time_periods: str = None, limit: str = None,
                      tots: str = None, explain_path: str = None,
                      extras: str = None,
                      sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.MINUTE_PAIR_OHLCV,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'tryConversion': try_conversion,
                    'aggregate': aggregate,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'limit': limit,
                    'toTs': tots,
                    'explain_path': explain_path,
                    'extraParams': extras,
                    'sign': sign
            })


def day_all_pairs_ohlcv_csv(trade_date: str = None):
    # essential parameters: trade_date
    return _generic_call(CryptoCompare.DAY_ALL_PAIRS_OHLCV_CSV,
                         essential={'date': trade_date})


def minute_pair_ohlcv_csv(fsym: str, tsym: str, exchange: str = None,
                          trade_date: str = None):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.MINUTE_PAIR_OHLCV_CSV,
            essential={
                    'fsym': fsym,
                    'tsyms': tsym
            },
            query={
                    'e': exchange,
                    'date': trade_date
            })


def day_pair_ohlcv_by_ts(fsym: str, tsyms: str, try_conversion: bool = True,
                         ts: str = None, exchange: str = None, extras: str = None,
                         calculation_type: str = None, sign: bool = True):
    # essential parameters: fsym, tsyms

    return _generic_call(
            CryptoCompare.DAY_PAIR_OHLCV_BY_TS,
            essential={
                    'fsym': fsym,
                    'tsyms': tsyms
            },
            query={
                    'tryConversion': try_conversion,
                    'ts': ts,
                    'e': exchange,
                    'extraParams': extras,
                    'calculation_type': calculation_type,
                    'sign': sign
            }
    )


def day_pair_ohlcv_hourly_vwap_by_ts(fsym: str, tsym: str, try_conversion: bool = True,
                                     exchange:
                                     str = None, avg_type: str = None,
                                     utc_hour_diff: str = None, tots: str = None,
                                     extras: str = None, sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.DAY_PAIR_OHLCV_HOURLY_VWAP_BY_TS,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'tryConversion': try_conversion,
                    'e': exchange,
                    'avg_type': avg_type,
                    'utc_hour_diff': utc_hour_diff,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def daily_exchange_vol(tsym: str, exchange: str = None, aggregate: str = None,
                       aggregate_predictable_time_periods: str = None,
                       limit: str = None, tots: str = None, extras: str = None,
                       sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.DAILY_EXCHANGE_VOL,
            essential={'tsym': tsym},
            query={
                    'aggregate': aggregate,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'limit': limit,
                    'e': exchange,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def hourly_exchange_vol(tsym: str, exchange: str = None, aggregate: str = None,
                        aggregate_predictable_time_periods: str = None,
                        limit: str = None, tots: str = None, extras: str = None,
                        sign: bool = True):
    # essential parameters: tsym

    return _generic_call(
            CryptoCompare.HOURLY_EXCHANGE_VOL,
            essential={'tsym': tsym},
            query={
                    'aggregate': aggregate,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'limit': limit,
                    'e': exchange,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def daily_symbol_vol(tsym: str, aggregate: str = None,
                     aggregate_predictable_time_periods: str = None, limit: str = None,
                     tots: str = None,
                     extras: str = None, sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.DAILY_SYMBOL_VOL,
            essential={'tsym': tsym},
            query={
                    'aggregate': aggregate,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'limit': limit,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def daily_symbol_vol_single_exchange(fsym: str, tsym: str,
                                     exchange: str = None, aggregate: str = None,
                                     limit: str = None, tots: str = None,
                                     extras: str = None,
                                     sign: bool = True):
    # essential parameters: fsym, tsym

    return _generic_call(
            CryptoCompare.DAILY_SYMBOL_VOL_SINGLE_EXCHANGE,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'aggregate': aggregate,
                    'limit': limit,
                    'e': exchange,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def hourly_symbol_vol_single_exchange(fsym: str, tsym: str,
                                      exchange: str = None, aggregate: str = None,
                                      limit: str = None, tots: str = None,
                                      extras: str = None,
                                      sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.HOURLY_SYMBOL_VOL_SINGLE_EXCHANGE,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'aggregate': aggregate,
                    'limit': limit,
                    'e': exchange,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def latest_mapping_from_symbol(fsym: str = None, extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LATEST_MAPPING_FROM_SYMBOL,
            essential=None,
            query={
                    'fsym': fsym,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def latest_mapping_exchange(exchange: str = None, extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LATEST_MAPPING_EXCHANGE,
            essential=None,
            query={
                    'e': exchange,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def latest_mapping_exchange_from_symbol(exchange_fsym: str = None, extras: str = None,
                                        sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LATEST_MAPPING_EXCHANGE_FROM_SYMBOL,
            essential=None,
            query={
                    'exchange_fsym': exchange_fsym,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def planned_pair_mapping_updates(extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.PLANNED_PAIR_MAPPING_UPDATES,
            essential=None,
            query={
                    'sign': sign,
                    'extraParams': extras
            }
    )


def toplist_by_24h_volume_full_data(tsym: str, limit: str = None, page: str = None,
                                    ascending: str = None, sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_24H_VOLUME_FULL_DATA,
            essential={'tsym': tsym},
            query={
                    'limit': limit,
                    'page': page,
                    'ascending': ascending,
                    'sign': sign
            }
    )


def toplist_by_24h_top_tier_volume_full_data(tsym: str, limit: str = None,
                                             page: str = None, ascending: str = None,
                                             sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_24H_TOP_TIER_VOLUME_FULL_DATA,
            essential={'tsym': tsym},
            query={
                    'page': page,
                    'limit': limit,
                    'ascending': ascending,
                    'sign': sign
            }
    )


def toplist_by_market_cap_full_data(tsym: str, limit: str = None, page: str = None,
                                    ascending: str = None, sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_MARKET_CAP_FULL_DATA,
            essential={'tsym': tsym},
            query={
                    'page': page,
                    'limit': limit,
                    'ascending': ascending,
                    'sign': sign
            }
    )


def top_exchanges_volume_data_by_pair(fsym: str, tsym: str,
                                      limit: str = None, extras: str = None,
                                      sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.TOP_EXCHANGES_VOLUME_DATA_BY_PAIR,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'limit': limit,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def top_exchanges_full_data_by_pair(fsym: str, tsym: str, limit: str = None,
                                    extras: str = None, sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.TOP_EXCHANGES_FULL_DATA_BY_PAIR,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'limit': limit,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def toplist_by_pair_volume(fsym: str, tsym: str, limit: str = None,
                           extras: str = None, sign: bool = True):
    # essential parameters: fsym, tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_PAIR_VOLUME,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'limit': limit,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def toplist_of_trading_pairs(fsym: str, limit: str = None, extras: str = None,
                             sign: bool = True):
    # essential parameters: fsym
    return _generic_call(
            CryptoCompare.TOPLIST_OF_TRADING_PAIRS,
            essential={'fsym': fsym},
            query={
                    'limit': limit,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def latest_coin_social_stats_data(coin: str = None, extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LATEST_COIN_SOCIAL_STATS_DATA,
            essential=None,
            query={
                    'coin': coin,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def historical_day_social_stats_data(coin: str = None, aggregate: str = None,
                                     aggregate_predictable_time_periods: str = None,
                                     limit: str = None, tots: str = None,
                                     extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.HISTORICAL_DAY_SOCIAL_STATS_DATA,
            essential=None,
            query={
                    'coinid': coin,
                    'aggregate': aggregate,
                    'limit': limit,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def historical_hour_social_stats_data(coin: str = None, aggregate: str = None,
                                      aggregate_predictable_time_periods: str = None,
                                      limit: str = None, tots: str = None,
                                      extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.HISTORICAL_HOUR_SOCIAL_STATS_DATA,
            essential=None,
            query={
                    'coinid': coin,
                    'aggregate': aggregate,
                    'limit': limit,
                    'aggregatePredictableTimePeriods':
                        aggregate_predictable_time_periods,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def latest_news_articles(feeds: str = 'ALL_NEWS_FEEDS', categories: str = None,
                         exclude_categories: str = None, lts: str = None, lang: str = None,
                         sort_order: str = None,
                         extras: str = None, sign: bool = True):
    # essential parameters: None

    return _generic_call(
            CryptoCompare.LATEST_NEWS_ARTICLES,
            essential=None,
            query={
                    'feeds': feeds,
                    'categories': categories,
                    'exclude_categories': exclude_categories,
                    'lts': lts,
                    'lang': lang,
                    'sort_order': sort_order,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def list_news_feeds(extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LIST_NEWS_FEEDS,
            essential=None,
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def news_article_categories(extras: str = None, sign: bool = True):
    # essential parameters: None

    return _generic_call(
            CryptoCompare.NEWS_ARTICLE_CATEGORIES,
            essential=None,
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def list_news_feeds_and_categories(extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LIST_NEWS_FEEDS_AND_CATEGORIES,
            essential=None,
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def exchanges_with_order_book_data(extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.EXCHANGES_WITH_ORDER_BOOK_DATA,
            essential=None,
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def order_book_l1_top(fsyms: str, tsyms: str, exchange: str = None,
                      extras: str = None, sign: bool = True):
    # essential parameters: fsyms, tsyms, e
    return _generic_call(
            CryptoCompare.ORDER_BOOK_L1_TOP,
            essential={
                    'fsyms': fsyms,
                    'tsyms': tsyms,
                    'e': exchange
            },
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def order_book_l2_snapshot(fsym: str, tsym: str, exchange: str = None,
                           limit: int = 10, extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.ORDER_BOOK_L2_SNAPSHOT,
            essential={
                    'fsym': fsym,
                    'tsym': tsym
            },
            query={
                    'limit': limit,
                    'e': exchange,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def toplist_by_24h_volume_subscriptions(tsym: str, limit: str = None, page: str = None,
                                        ascending: str = None,
                                        sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_24H_VOLUME_SUBSCRIPTIONS,
            essential={'tsym': tsym},
            query={
                    'page': page,
                    'limit': limit,
                    'ascending': ascending,
                    'sign': sign
            }
    )


def toplist_by_24h_top_tier_volume_subscriptions(tsym: str, limit: str = None, page: str =
None, ascending: str = None, sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_24H_TOP_TIER_VOLUME_SUBSCRIPTIONS,
            essential={'tsym': tsym},
            query={
                    'page': page,
                    'limit': limit,
                    'ascending': ascending,
                    'sign': sign
            }
    )


def toplist_by_market_cap_subscriptions(tsym: str = None, limit: str = None, page: str = None,
                                        ascending: str = None,
                                        sign: bool = True):
    # essential parameters: tsym
    return _generic_call(
            CryptoCompare.TOPLIST_BY_MARKET_CAP_SUBSCRIPTIONS,
            essential={'tsym': tsym},
            query={
                    'page': page,
                    'limit': limit,
                    'ascending': ascending,
                    'sign': sign
            }
    )


def subs_by_pair(fsym: str, tsyms: str = None, extras: str = None,
                 sign: bool = True):
    # essential parameters: fsym
    return _generic_call(
            CryptoCompare.SUBS_BY_PAIR,
            essential={'fsym': fsym},
            query={
                    'tsyms': tsyms,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def subs_watchlist(fsyms: str, tsyms: str, extras: str = None,
                   sign: bool = True):
    # essential parameters: fsyms, tsyms
    return _generic_call(
            CryptoCompare.SUBS_WATCHLIST,
            essential={
                    'fsyms': fsyms,
                    'tsyms': tsyms
            },
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def coins_general_info(fsyms: str, tsym: str, extras: str = None,
                       sign: bool = True):
    # essential parameters: fsyms, tsym
    return _generic_call(
            CryptoCompare.COINS_GENERAL_INFO,
            essential={
                    'fsyms': fsyms,
                    'tsym': tsym
            },
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def list_of_available_indices_on_the_api(extras: str = None, sign: bool = True):
    # essential parameters: None
    return _generic_call(
            CryptoCompare.LIST_OF_AVAILABLE_INDICES_ON_THE_API,
            essential=None,
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def single_index_value(index_name: str, extras: str = None, sign: bool = True):
    # essential parameters: index_name
    return _generic_call(
            CryptoCompare.SINGLE_INDEX_VALUE,
            essential={'index_name': index_name},
            query={
                    'extraParams': extras,
                    'sign': sign
            }
    )


def historical_minute_ohlc(index_name: str, aggregate: str = None,
                           limit: str = None, tots: str = None, extras: str = None,
                           sign: bool = True):
    # essential parameters: index_name
    return _generic_call(
            CryptoCompare.HISTORICAL_MINUTE_OHLC,
            essential={'index_name': index_name},
            query={
                    'aggregate': aggregate,
                    'limit': limit,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def historical_hourly_ohlc(index_name: str, aggregate: str = None,
                           limit: str = None, tots: str = None, extras: str = None,
                           sign: bool = True):
    # essential parameters: index_name
    return _generic_call(
            CryptoCompare.HISTORICAL_HOURLY_OHLC,
            essential={'index_name': index_name},
            query={
                    'aggregate': aggregate,
                    'limit': limit,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def historical_daily_ohlc(index_name: str, aggregate: str = None, limit: str = None,
                          tots: str = None, extras: str = None, sign: bool = True):
    # essential parameters: index_name
    return _generic_call(
            CryptoCompare.HISTORICAL_DAILY_OHLC,
            essential={'index_name': index_name},
            query={
                    'aggregate': aggregate,
                    'limit': limit,
                    'toTs': tots,
                    'extraParams': extras,
                    'sign': sign
            }
    )


def all_the_exchanges_and_trading_pairs(fsym: str = None, exchange: str = None,
                                        top_tier: bool = False, extras: str = None,
                                        sign: bool = True):
    return _generic_call(CryptoCompare.ALL_THE_EXCHANGES_AND_TRADING_PAIRS, essential=None,
                         query={
                                 'fsym': fsym,
                                 'e': exchange,
                                 'topTier': top_tier,
                                 'extraParams': extras,
                                 'sign': sign
                         })


def all_the_coins(built_on: str = None, extras: str = None, sign: bool = True):
    return _generic_call(CryptoCompare.ALL_THE_COINS, essential=None, query={
            'builtOn': built_on,
            'extraParams': extras,
            'sign': sign
    })


def exchanges_with_order_data(extras: str = None, sign: bool = True):
    return _generic_call(CryptoCompare.EXCHANGES_WITH_ORDER_BOOK_DATA, essential=None,
                         query={'extraParams': extras, 'sign': sign})


def all_the_coins_general_info(fsyms: str, tsym: str, extras: str = None,
                               sign: bool = True):
    return _generic_call(CryptoCompare.ALL_THE_COINS,
                         essential={'fsyms': fsyms, 'tsym': tsym},
                         query={'extraParams': extras, 'sign': sign})


def all_exchanges_general_info(tsym: str = None, extras: str = None, sign: bool = True):
    return _generic_call(CryptoCompare.ALL_EXCHANGES_GENERAL_INFO, essential=None,
                         query={
                                 'tsym': tsym,
                                 'extraParams': extras,
                                 'sign': sign
                         })


@network_log
def url_factory(named_url: Any, required: Mapping = None, params: Mapping = None) -> Any:
    """ Generate a url for the application based on the specified endpoint provided as a
    name or Enum"""

    named_func = sorted(('single_symbol_price', 'multiple_symbols_price',
                         'multiple_symbols_full_data', 'generate_custom_average',
                         'daily_pair_ohlcv', 'hourly_pair_ohlcv', 'minute_pair_ohlcv',
                         'day_all_pairs_ohlcv_csv', 'minute_pair_ohlcv_csv',
                         'day_pair_ohlcv_by_ts', 'day_pair_ohlcv_hourly_vwap_by_ts',
                         'daily_exchange_vol', 'hourly_exchange_vol', 'daily_symbol_vol',
                         'daily_symbol_vol_single_exchange',
                         'hourly_symbol_vol_single_exchange', 'latest_mapping_from_symbol',
                         'latest_mapping_exchange', 'latest_mapping_exchange_from_symbol',
                         'planned_pair_mapping_updates', 'toplist_by_24h_volume_full_data',
                         'toplist_by_24h_top_tier_volume_full_data',
                         'toplist_by_market_cap_full_data',
                         'top_exchanges_volume_data_by_pair',
                         'top_exchanges_full_data_by_pair', 'toplist_by_pair_volume',
                         'toplist_of_trading_pairs', 'latest_coin_social_stats_data',
                         'historical_day_social_stats_data',
                         'historical_hour_social_stats_data', 'latest_news_articles',
                         'list_news_feeds', 'news_article_categories',
                         'list_news_feeds_and_categories', 'exchanges_with_order_book_data',
                         'order_book_l1_top', 'order_book_l2_snapshot',
                         'toplist_by_24h_volume_subscriptions',
                         'toplist_by_24h_top_tier_volume_subscriptions',
                         'toplist_by_market_cap_subscriptions', 'subs_by_pair',
                         'subs_watchlist', 'coins_general_info',
                         'list_of_available_indices_on_the_api', 'single_index_value',
                         'historical_minute_ohlc', 'historical_hourly_ohlc',
                         'historical_daily_ohlc',
                         'all_the_exchanges_and_trading_pairs', 'all_the_coins',
                         'exchanges_with_order_data', 'all_the_coins_general_info',
                         'all_exchanges_general_info',
                         ), key=lambda x: x.lower())
    func_list = sorted((
            single_symbol_price, multiple_symbols_price, multiple_symbols_full_data,
            generate_custom_average, daily_pair_ohlcv, hourly_pair_ohlcv,
            minute_pair_ohlcv, day_all_pairs_ohlcv_csv, minute_pair_ohlcv_csv,
            day_pair_ohlcv_by_ts, day_pair_ohlcv_hourly_vwap_by_ts,
            daily_exchange_vol, hourly_exchange_vol, daily_symbol_vol,
            daily_symbol_vol_single_exchange, hourly_symbol_vol_single_exchange,
            latest_mapping_from_symbol, latest_mapping_exchange,
            latest_mapping_exchange_from_symbol, planned_pair_mapping_updates,
            toplist_by_24h_volume_full_data,
            toplist_by_24h_top_tier_volume_full_data,
            toplist_by_market_cap_full_data, top_exchanges_volume_data_by_pair,
            top_exchanges_full_data_by_pair, toplist_by_pair_volume,
            toplist_of_trading_pairs, latest_coin_social_stats_data,
            historical_day_social_stats_data, historical_hour_social_stats_data,
            latest_news_articles, list_news_feeds, news_article_categories,
            list_news_feeds_and_categories, exchanges_with_order_book_data,
            order_book_l1_top, order_book_l2_snapshot,
            toplist_by_24h_volume_subscriptions,
            toplist_by_24h_top_tier_volume_subscriptions,
            toplist_by_market_cap_subscriptions, subs_by_pair, subs_watchlist,
            coins_general_info, list_of_available_indices_on_the_api,
            single_index_value, historical_minute_ohlc, historical_hourly_ohlc,
            historical_daily_ohlc,
            all_the_exchanges_and_trading_pairs, all_the_coins,
            exchanges_with_order_data, all_the_coins_general_info,
            all_exchanges_general_info,), key=lambda x: x.__name__.lower())
    func_registry = dict(zip(named_func, func_list))
    cmd = None
    kwargs = None
    if isinstance(named_url, Enum):
        cmd = func_registry.get(str(named_url.value).lower())
    elif isinstance(named_url, str):
        cmd = func_registry.get(named_url.lower())
        kwargs = dict(**params)
        if required:
            kwargs.update(**required)
    return cmd(kwargs)
