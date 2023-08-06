import itertools
from abc import ABC, abstractmethod
from typing import Mapping, List, Callable, Tuple, Sequence, Any, Dict

# Define the various parsers for the selected endpoints
"""
Parser will cover the following categories:
    price: --all--
    historic_data: none
    pair_mapping: none
    toplist: none
    social_data: none
    news: --all--
    order_book: exchange order book
    general_info: all coins, all exchanges, exchanges pair
    streaming: none
    index: none
"""


def extract_field_records(field: str, data: Mapping, found: List = None) -> Tuple:
    """
    Extract the given field or node from the data structure passed as a dictionary or
    mapping type
    :param field: Node or key to be extracted
    :param data: Source of data or dictionary. Nested dictionaries are supported
    :param found: Retrieved results from the data returned as a tuple or sequence
    :return: Tuple
    """
    if isinstance(data, Mapping) and field in data and isinstance(found, List):
        found.append(data[field])
    else:
        if isinstance(data, Mapping):
            for _, v in data.items():
                extract_field_records(field, v, found)
    return field, found


def extract_group(field: str, data: Mapping, sort: Callable = None) -> Any:
    """
    Extract given field from nested dictionary or mapping. Informtion retrieved are grouped
    by the provided field
    :param field: Node or key to be extracted
    :param data: Source of data or dictionary. Nested dictionaries are supported
    :param sort: A sorting algorithm or function to use in comparison or sorting
    :return: Dict
    """
    groups = []
    unique_keys = []
    key_func = sort if callable(sort) else None
    data = sorted(data, key=key_func)
    for k, g in itertools.groupby(data, key_func):
        groups.append(list(g))
        unique_keys.append(k)
    out = dict(zip(unique_keys, groups))
    return out.get(field)


def process_information(response: Dict, node: str = None, information: str = None):
    if not isinstance(response, Dict):
        raise ValueError('Data structure should be a dictionary or support the mapping '
                         'interface')
    if not (isinstance(node, str) or isinstance(information, str)):
        raise ValueError('Search variables should be string types')
    record = response.get(node)
    if record:
        return extract_field_records(information, record, found=[])


def extract_by_index(data: Sequence, index: int = 0, start: int = 0, end: int = 0) -> Any:
    if index:
        return data[index]
    elif start and end:
        return data[start: end]
    elif start:
        return data[start:]
    elif end:
        return data[:end]
    return data


class Parser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, response: Any = None, **kwargs) -> Any:
        pass


class SingleSymbolPrice(Parser):

    @classmethod
    def parse(cls, response: Dict = None, field: str = None) -> Any:
        """
        Get the current price of any cryptocurrency in any other currency that you need.
        If the crypto does not trade directly into the currency requested, BTC will be used for
        conversion. If the opposite pair trades, it is inverted and processed.  Eg.:
        BTC-XMR
        :param response: Server response
        :param field: Given response node or field as depicted in JSON data
        :return: Any
        """
        if field:
            return response.get(field)
        else:
            return response


class MultipleSymbolsPrice(Parser):

    @classmethod
    def parse(cls, response: Dict = None, field: str = None) -> Any:
        """
        Same as single API path but with multiple crypto-currencies or fiat currencies for
        conversion.
        :param response: Server response
        :param field: Given response node or field as depicted in JSON data
        :return: Any
        """
        if field:
            return extract_field_records(field=field, data=response, found=[])
        return response


class MultipleSymbolsFullData(Parser):

    @classmethod
    def parse(cls, response: Dict = None, currency: str = None, information: str = None,
              display: Any = None, raw: Any = None, source: str = 'DISPLAY') -> \
            Any:
        """
        Get all the current trading info (price, vol, open, high, low etc) of any list of
        crypto-currencies in any other currency that you need. If the crypto does not trade
        directly into the toSymbol requested, BTC will be used for conversion. This API also
        returns Display values for all the fields. If the opposite pair trades we invert it
        (eg.: BTC-XMR)
        :param response: Server response with the display and raw nodes or fields
        :param currency: Target currency to be extracted from response
        :param information: Target information about currency to be extracted
        :param display: Node or field of server response for display
        :param raw: Node or field of server response as raw data
        :param source: Define what data source is used between DISPLAY AND RAW. Default is
        set to DISPLAY
        :return: Any
        """
        if not display:
            display = response.get('DISPLAY')
        if not raw:
            raw = response.get('RAW')

        if display and currency and information and source == 'DISPLAY':
            if currency in display:
                return process_information(response=display, node=currency,
                                           information=information)
        elif raw and currency and information and source == 'RAW':
            if currency in raw:
                return process_information(response=raw, node=currency,
                                           information=information)
        return response


class GenerateCustomAverage(Parser):

    @classmethod
    def parse(cls, response: Dict = None, display: Any = None, raw: Any = None,
              currency: str = None, information: str = None, source: str = None) -> Any:
        """
        Parse the computed current trading info (price, vol, open, high, low etc) of the
        requested pair as a volume weighted average based on the exchanges requested.
        :param response: Server response
        :param currency: 
        :param information: 
        :param display: 
        :param raw:
        :param source: Define what node between DISPLAY and RAW will be data source.
        Default is set to 'DISPLAY'
        :return: 
        """
        if not display:
            display = response.get('DISPLAY')
        if not raw:
            raw = response.get('RAW')
        if display and currency and information and source == 'DISPLAY':
            return process_information(response=display, node=currency,
                                       information=information)
        elif raw and currency and information and source == 'RAW':
            return process_information(response=raw, node=currency, information=information)
        return response


class LatestNewsArticles(Parser):

    @classmethod
    def parse(cls, response: Dict = None, promoted: str = None, data: Dict = None,
              index: int = 0, start: int = 0, end: int = 0, **kwargs) -> Any:
        """
        Returns news articles from the providers that CryptoCompare has integrated with.
        :param response: Server response
        :param promoted: Server response field. JSON key as 'Promoted'
        :param data: Server response field. JSON key as 'Data'
        :param index: Index of the news object where only a single object is required
        :param start: Start index of the news object where only a single object is required
        :param end: End index of the news object where only a single object is required
        function
        :return: Any
        """
        if not promoted:
            promoted = response.get('Promoted')
        if not data:
            data = response.get('Data')
        out = list()
        if promoted and isinstance(promoted, Sequence):
            return extract_by_index(promoted, index=index, start=start, end=end)
        if data and isinstance(data, Sequence):
            return extract_by_index(data, index=index, start=start, end=end)
        return response


class ListNewsFeeds(Parser):

    @classmethod
    def parse(cls, response: Any = None, index: int = 0, start: int = 0, end: int = 0) -> Any:
        """
        Returns all the news feeds (providers) that CryptoCompare has integrated with.
        :param response:
        :param index: Index of the news object where only a single object is required
        :param start: Start index of the news object where only a single object is required
        :param end: End index of the news object where only a single object is required
        :return: Any
        """

        if isinstance(response, Sequence):
            return extract_by_index(response, index=index, start=start, end=end)
        return response


class NewsArticleCategories(Parser):

    @classmethod
    def parse(cls, response: Any = None, category: str = None,
              associated_words: str = None,
              excluded_words: str = None, index: int = 0, start: int = 0,
              end: int = 0) -> Any:
        """
        Returns news articles categories, you can use them to filter news.
        :param response: Server response
        :param category: Server response field. JSON key as 'categoryName'
        :param associated_words: Server response field. JSON key as
        'wordsAssociatedWithCategory'
        :param excluded_words: Server response field. JSON key as 'excludedPhrases'
        :param index: Index of the news object where only a single object is required
        :param start: Start index of the news object where only a single object is required
        :param end: End index of the news object where only a single object is required
        :return: Any
        """
        if response and isinstance(response, Sequence):
            record = extract_by_index(response, index=index, start=start, end=end)
            if isinstance(record, Dict) and (category or associated_words or excluded_words):
                return record.get(category) or record.get(associated_words) \
                       or record.get(excluded_words)
        return response


class ListNewsFeedsAndCategories(Parser):

    @classmethod
    def parse(cls, response: Dict = None, message: str = None,
              has_warning: str = None, type_key: str = None,
              **kwargs) -> Any:
        """
        Returns all the news feeds (providers) that CryptoCompare has integrated with and the
        full list of categories.
        :param response: Server response
        :param message: Server response field. JSON key as 'Message'
        :param has_warning: Server response field. JSON key as 'HasWarning'
        :param type_key: Server response field. JSON key as 'Type'
        :param data: Server response field. JSON key as 'Data'
        :param kwargs: Additional keyword arguments that can be passed to the parsing function.
        :return: Any
        """
        if isinstance(response, Dict) and 'Data' in response:
            record = response.get('Data')
            if record:
                return NewsArticleCategories.parse(record, **kwargs)
            else:
                return response.get(message) or response.get(has_warning) \
                       or response.get(type_key)
        return response


class ExchangesWithOrderBookData(Parser):

    @classmethod
    def parse(cls, response: Dict = None, message: str = None,
              has_warning: str = None, type_node: str = None,
              rate_limit: str = None, data: str = None, index: int = 0,
              start: int = 0, end: int = 0) -> Any:
        """

        :param response: Server response for given request
        :param message: 'Message'
        :param has_warning: 'HasWarning'
        :param type_node: 'Type'
        :param rate_limit: 'RateLimit'
        :param data: 'Data'
        :param index: Index of the news object where only a single object is required
        :param start: Start index of the news object where only a single object is required
        :param end: End index of the news object where only a single object is required
        :return:
        """
        if response and isinstance(response, Dict):
            record = response.get(data)
            if isinstance(record, Sequence):
                return extract_by_index(record, index=index, start=start, end=end)
        if any([message, has_warning, type_node, rate_limit]):
            return response.get(message) or response.get(has_warning) \
                   or response.get(type_node) or response.get(rate_limit)
        return response


class OrderBookL1Top(Parser):

    @classmethod
    def parse(cls, response: Dict = None, message: str = None,
              has_warning: str = None, type_node: str = None, display: Any = None,
              raw: Any = None, node: str = None, information: str = None, source: str =
              'DISPLAY') -> \
            Any:
        """

        :param response:
        :param message: 'Message'
        :param has_warning: 'HasWarning'
        :param type_node: 'Type'
        :param display:
        :param raw:
        :param node:
        :param information:
        :param source: Define the source of data as either DISPLAY or RAW
        :return:
        """
        data = response.get('Data')
        if not display:
            display = data.get('DISPLAY')
        if not raw:
            raw = data.get('RAW')
        if not node:
            node = str()
        if not information:
            information = str()
        if display and node and information and source == 'DISPLAY':
            return process_information(response=display, node=node,
                                       information=information)
        elif raw and node and information and source == 'RAW':
            return process_information(response=raw, node=node,
                                       information=information)
        elif any([has_warning, type_node, message]):
            return response.get(has_warning) or response.get(type_node) \
                   or response.get(message)
        return response


class OrderBookL2Snapshot(Parser):

    @classmethod
    def parse(cls, response: Dict = None, node: str = None, information: str = None,
              message: str = 'Message', has_warning: str = 'HasWarning',
              type_node: str = 'Type', rate_limit: str = 'RateLimit', data: str = 'Data',
              raw: Any = None, display: Any = None, source: str = 'DISPLAY') -> Any:
        if not raw:
            raw = response.get('RAW')
        if not display:
            display = response.get('DISPLAY')
        if isinstance(raw, Dict) and source == 'RAW':
            return process_information(response=raw, node=node, information=information)
        elif isinstance(display, Dict) and source == 'DISPLAY':
            return process_information(response=display, node=node, information=information)
        if any([message, has_warning, type_node, rate_limit, data]):
            return response.get(message) or response.get(has_warning) \
                   or response.get(type_node) or response.get(rate_limit) or response.get(data)
        return response


class AllTheExchangesAndTradingPairs(Parser):

    @classmethod
    def parse(cls, response: Dict = None, message: str = None,
              has_warning: str = None, type_node: str = None,
              rate_limit: str = None, seq: str = None,
              key_node: str = None, **kwargs) -> Any:
        """
        Returns all the exchanges that CryptoCompare has integrated with. You can filter by
        exchange and from symbol
        :param response:
        :param message: Server response field. JSON key as 'Message'
        :param has_warning: Server response field. JSON key as 'HasWarning'
        :param type_node: Server response field. JSON key as 'Type'
        :param rate_limit: Server response field. JSON key as 'RateLimit'
        :param seq: Server response field. JSON key as 'seq'
        :param key_node: Server response field. JSON key as 'key'
        :param kwargs:
        :return: Any
        """
        data = response.get('Data')
        node = kwargs.get('node')
        information = kwargs.get('information')
        if data and isinstance(data, Dict) and node and information:
            return process_information(response=data, node=node, information=information)
        if any([message, has_warning, type_node, rate_limit, seq, key_node]):
            return response.get(message) or response.get(has_warning) or response.get(
                    type_node) \
                   or response.get(rate_limit) or response.get(seq) or response.get(key_node)
        return response


class AllTheCoins(Parser):
    @classmethod
    def parse(cls, response: Dict = None, message: str = None,
              image: str = None, link: str = None, rate_limit: str = None,
              has_warning: str = None, type_node: str = None, **kwargs) -> Any:
        """
        Returns all the coins listed by CryptoCompare to be published from their REST
        service endpoint or coins they have added to their system. This may not be
        the full list of coins in their database.
        :param response: Server response as JSON
        :param message: JSON key as 'Message'
        :param image: Response field with JSON key as 'BaseImageUrl'
        :param link: Response field with default key value, 'BaseLinkUrl'
        :param rate_limit: Response field with JSON key as 'RateLimit'
        :param has_warning: Response field with JSON key as 'HasWarning'
        :param type_node: Response field with JSON key as 'Type'
        :param kwargs: Any keyword arguments that may be retrieved from the server's
        response or added to the parsing function.
        :return: Any
        """
        data = response.get('Data')
        index = kwargs.get('index')
        start = kwargs.get('start')
        end = kwargs.get('end')
        if data and isinstance(data, Sequence):
            if index:
                return data[index]
            elif start and end:
                return data[start: end]
            elif start:
                return data[start:]
            elif end:
                return data[:end]
            else:
                return data
        if any([message, image, link, rate_limit, has_warning, type_node]):
            return response.get(message) or response.get(image) or response.get(link) or \
                   response.get(rate_limit) or response.get(has_warning) \
                   or response.get(type_node)

        return response


class AllExchangesGeneralInfo(Parser):

    @classmethod
    def parse(cls, response: Dict = None, message: str = None, has_warning: str = None,
              type_node: str = None, rate_limit: str = None, **kwargs) -> Any:
        """
        Returns general info and 24h volume for all the exchanges we have integrated with.
        :param response: The server response from sending a HTTP request
        :param message: The message attribute or field of the response. JSON key as
        'Message'
        :param has_warning: The warning attribute/field from server response. JSON key
        as 'HasWarning'
        :param type_node: Type attribute/field of the response. JSON key as 'Type'
        :param rate_limit: Rate limit attribute/field of the response. JSON key as
        'RateLimit'
        :param kwargs: Any keyword arguments that may be retrieved from the server's
        response or added to the parsing function.
        :return:
        """
        data = response.get('Data')
        node = kwargs.get('node')
        information = kwargs.get('information')
        if data and isinstance(data, Dict) and node and information:
            return process_information(response=data, node=node, information=information)
        if any([message, has_warning, type_node, rate_limit]):
            return response.get(message) or response.get(has_warning) \
                   or response.get(type_node) or response.get(rate_limit)
        return response
