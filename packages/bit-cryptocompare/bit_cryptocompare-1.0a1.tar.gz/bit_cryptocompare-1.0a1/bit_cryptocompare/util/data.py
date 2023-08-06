from collections import UserDict
from enum import Enum
from typing import Mapping, Sequence, Any, Callable


class CryptoCompare(Enum):
    """ List the various services as Enum """
    SINGLE_SYMBOL_PRICE = 'SINGLE_SYMBOL_PRICE'
    MULTIPLE_SYMBOLS_PRICE = 'MULTIPLE_SYMBOLS_PRICE'
    MULTIPLE_SYMBOLS_FULL_DATA = 'MULTIPLE_SYMBOLS_FULL_DATA'
    GENERATE_CUSTOM_AVERAGE = 'GENERATE_CUSTOM_AVERAGE'
    DAILY_PAIR_OHLCV = 'DAILY_PAIR_OHLCV'
    HOURLY_PAIR_OHLCV = 'HOURLY_PAIR_OHLCV'
    MINUTE_PAIR_OHLCV = 'MINUTE_PAIR_OHLCV'
    DAY_ALL_PAIRS_OHLCV_CSV = 'DAY_ALL_PAIRS_OHLCV_CSV'
    MINUTE_PAIR_OHLCV_CSV = 'MINUTE_PAIR_OHLCV_CSV'
    DAY_PAIR_OHLCV_BY_TS = 'DAY_PAIR_OHLCV_BY_TS'
    DAY_PAIR_OHLCV_HOURLY_VWAP_BY_TS = 'DAY_PAIR_OHLCV_HOURLY_VWAP_BY_TS'
    DAILY_EXCHANGE_VOL = 'DAILY_EXCHANGE_VOL'
    HOURLY_EXCHANGE_VOL = 'HOURLY_EXCHANGE_VOL'
    DAILY_SYMBOL_VOL = 'DAILY_SYMBOL_VOL'
    DAILY_SYMBOL_VOL_SINGLE_EXCHANGE = 'DAILY_SYMBOL_VOL_SINGLE_EXCHANGE'
    HOURLY_SYMBOL_VOL_SINGLE_EXCHANGE = 'HOURLY_SYMBOL_VOL_SINGLE_EXCHANGE'
    LATEST_MAPPING_FROM_SYMBOL = 'LATEST_MAPPING_FROM_SYMBOL'
    LATEST_MAPPING_EXCHANGE = 'LATEST_MAPPING_EXCHANGE'
    LATEST_MAPPING_EXCHANGE_FROM_SYMBOL = 'LATEST_MAPPING_EXCHANGE_FROM_SYMBOL'
    PLANNED_PAIR_MAPPING_UPDATES = 'PLANNED_PAIR_MAPPING_UPDATES'
    TOPLIST_BY_24H_VOLUME_FULL_DATA = 'TOPLIST_BY_24H_VOLUME_FULL_DATA'
    TOPLIST_BY_24H_TOP_TIER_VOLUME_FULL_DATA = 'TOPLIST_BY_24H_TOP_TIER_VOLUME_FULL_DATA'
    TOPLIST_BY_MARKET_CAP_FULL_DATA = 'TOPLIST_BY_MARKET_CAP_FULL_DATA'
    TOP_EXCHANGES_VOLUME_DATA_BY_PAIR = 'TOP_EXCHANGES_VOLUME_DATA_BY_PAIR'
    TOP_EXCHANGES_FULL_DATA_BY_PAIR = 'TOP_EXCHANGES_FULL_DATA_BY_PAIR'
    TOPLIST_BY_PAIR_VOLUME = 'TOPLIST_BY_PAIR_VOLUME'
    TOPLIST_OF_TRADING_PAIRS = 'TOPLIST_OF_TRADING_PAIRS'
    LATEST_COIN_SOCIAL_STATS_DATA = 'LATEST_COIN_SOCIAL_STATS_DATA'
    HISTORICAL_DAY_SOCIAL_STATS_DATA = 'HISTORICAL_DAY_SOCIAL_STATS_DATA'
    HISTORICAL_HOUR_SOCIAL_STATS_DATA = 'HISTORICAL_HOUR_SOCIAL_STATS_DATA'
    LATEST_NEWS_ARTICLES = 'LATEST_NEWS_ARTICLES'
    LIST_NEWS_FEEDS = 'LIST_NEWS_FEEDS'
    NEWS_ARTICLE_CATEGORIES = 'NEWS_ARTICLE_CATEGORIES'
    LIST_NEWS_FEEDS_AND_CATEGORIES = 'LIST_NEWS_FEEDS_AND_CATEGORIES'
    EXCHANGES_WITH_ORDER_BOOK_DATA = 'EXCHANGES_WITH_ORDER_BOOK_DATA'
    ORDER_BOOK_L1_TOP = 'ORDER_BOOK_L1_TOP'
    ORDER_BOOK_L2_SNAPSHOT = 'ORDER_BOOK_L2_SNAPSHOT'
    ALL_THE_EXCHANGES_AND_TRADING_PAIRS = 'ALL_THE_EXCHANGES_AND_TRADING_PAIRS'
    DISPLAY_INSTRUMENT_CONSTITUENT_PAIRS = 'DISPLAY_INSTRUMENT_CONSTITUENT_PAIRS'
    DISPLAY_CCCAGG_CONSTITUENT_PAIRS = 'DISPLAY_CCCAGG_CONSTITUENT_PAIRS'
    DISPLAY_CCCAGG_EXCLUDED_PAIRS = 'DISPLAY_CCCAGG_EXCLUDED_PAIRS'
    DISPLAY_CCCAGG_ABSENT_PAIRS = 'DISPLAY_CCCAGG_ABSENT_PAIRS'
    DISPLAY_CCCAGG_ABSENT_COINS = 'DISPLAY_CCCAGG_ABSENT_COINS'
    ALL_THE_COINS = 'ALL_THE_COINS'
    ALL_EXCHANGES_GENERAL_INFO = 'ALL_EXCHANGES_GENERAL_INFO'
    ALL_GAMBLING_GENERAL_INFO = 'ALL_GAMBLING_GENERAL_INFO'
    ALL_WALLETS_GENERAL_INFO = 'ALL_WALLETS_GENERAL_INFO'
    ALL_CRYPTO_CARDS_GENERAL_INFO = 'ALL_CRYPTO_CARDS_GENERAL_INFO'
    ALL_MINING_CONTRACTS_GENERAL_INFO = 'ALL_MINING_CONTRACTS_GENERAL_INFO'
    ALL_MINING_COMPANIES_GENERAL_INFO = 'ALL_MINING_COMPANIES_GENERAL_INFO'
    ALL_MINING_EQUIPMENT_GENERAL_INFO = 'ALL_MINING_EQUIPMENT_GENERAL_INFO'
    ALL_MINING_POOLS_GENERAL_INFO = 'ALL_MINING_POOLS_GENERAL_INFO'
    ALL_RECOMMENDED_ENTITIES = 'ALL_RECOMMENDED_ENTITIES'
    RATE_LIMIT = 'RATE_LIMIT'
    RATE_LIMIT_HOUR = 'RATE_LIMIT_HOUR'
    TOPLIST_BY_24H_VOLUME_SUBSCRIPTIONS = 'TOPLIST_BY_24H_VOLUME_SUBSCRIPTIONS'
    TOPLIST_BY_24H_TOP_TIER_VOLUME_SUBSCRIPTIONS = \
        'TOPLIST_BY_24H_TOP_TIER_VOLUME_SUBSCRIPTIONS'
    TOPLIST_BY_MARKET_CAP_SUBSCRIPTIONS = 'TOPLIST_BY_MARKET_CAP_SUBSCRIPTIONS'
    SUBS_BY_PAIR = 'SUBS_BY_PAIR'
    SUBS_WATCHLIST = 'SUBS_WATCHLIST'
    COINS_GENERAL_INFO = 'COINS_GENERAL_INFO'
    LIST_OF_AVAILABLE_INDICES_ON_THE_API = 'LIST_OF_AVAILABLE_INDICES_ON_THE_API'
    SINGLE_INDEX_VALUE = 'SINGLE_INDEX_VALUE'
    HISTORICAL_MINUTE_OHLC = 'HISTORICAL_MINUTE_OHLC'
    HISTORICAL_HOURLY_OHLC = 'HISTORICAL_HOURLY_OHLC'
    HISTORICAL_DAILY_OHLC = 'HISTORICAL_DAILY_OHLC'


class BusinessDataObject(UserDict):
    """ Provides a means of wrapping a data structure as key-value pair """

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__bon__ = kwargs.get('business_object_name') or self.__class__.__qualname__
        super(BusinessDataObject, self).__init__(*args, **kwargs)

    def __getattribute__(self, item):
        fields = self.__dict__.keys()
        if item not in fields:
            return self.data.get(item)


class Command:
    """
    Models a means of encapsulating a request as an object. The request object can be passed
    as Python object
    """
    __slots__ = '_rank', '_label', '_cmd', '_group', '_args', '_kwargs'

    def __init__(self, cmd: Callable, group: Any, rank: Any, label: str = None, *args,
                 **kwargs) -> None:
        """
        @param cmd: defines the callable object which represents a command
        @param group: string identifying a command by friendly user name
        @param rank: a hashable type or int depicting the rank of a command
        where it belongs to a family or group.
        The rank can be used to order commands if a group of commands in
        the same family are to be prioritized and
        executed.
        @param args: list of positional parameters for the command
        @param kwargs: list of keyword parameters for the command
        """
        self._rank = None
        self._args = []
        self._kwargs = {}
        self._group = None
        self._cmd = None
        self._label = None
        if isinstance(rank, int) or isinstance(rank, Enum):
            self._rank = rank
        if isinstance(args, Sequence):
            self._args = [*args]
        if isinstance(kwargs, Mapping):
            self._kwargs = {**kwargs}
        if isinstance(label, str) and label.isalnum():
            self._label = label
        if isinstance(group, str):
            self._group = group if group.isalnum() and len(group) < 50 else None
        elif isinstance(group, Enum):
            self._group = group
        if callable(cmd):
            self._cmd = cmd

    def __call__(self, *args, **kwargs):
        if isinstance(args, Sequence):
            self._args += args
        if isinstance(kwargs, dict):
            self._kwargs.update(**kwargs)
        _args = self._args.copy()
        _kwargs = self._kwargs.copy()
        return self._cmd(*_args, **_kwargs)

    @property
    def rank(self):
        return self._rank

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        raise RuntimeError('Attribute cannot be modified')

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = value if callable(value) else lambda: None

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        raise RuntimeError('Attribute cannot be modified')

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if isinstance(value, Sequence) and len(value):
            self._args.append(*value)

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if isinstance(value, dict) and len(value):
            self._kwargs.update(**value)


class ExplorerCommand(Command):

    def __init__(self, cmd: Callable, group: Any = None, rank: Any = None, label: str = None,
                 *args,
                 **kwargs) -> None:
        super(ExplorerCommand, self).__init__(cmd, group, rank, label, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super(ExplorerCommand, self).__call__(*args, **kwargs)
