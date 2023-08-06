from bit_cryptocompare.parsers import AllExchangesGeneralInfo, AllTheCoins, \
    AllTheExchangesAndTradingPairs, ExchangesWithOrderBookData, GenerateCustomAverage, \
    LatestNewsArticles, ListNewsFeeds, ListNewsFeedsAndCategories, MultipleSymbolsFullData, \
    MultipleSymbolsPrice, NewsArticleCategories, OrderBookL1Top, OrderBookL2Snapshot, \
    SingleSymbolPrice, extract_group
from bit_cryptocompare.util.url_factory import single_symbol_price, multiple_symbols_full_data, \
    multiple_symbols_price, generate_custom_average, latest_news_articles, list_news_feeds, \
    list_news_feeds_and_categories, news_article_categories, exchanges_with_order_data, \
    order_book_l2_snapshot, all_the_exchanges_and_trading_pairs, all_the_coins_general_info, \
    all_exchanges_general_info, order_book_l1_top
from bit_cryptocompare.util.validate import validate


def test_single_symbol_price():
    out = single_symbol_price('BTC', 'USD,GBP', try_conversion=False,
                              relaxed_validation=True,
                              exchange='Kraken',
                              extras='Bitmast Explorer', sign=False)
    price = SingleSymbolPrice.parse(response=out, field='USD')
    assert out
    assert price


def test_multiple_symbols_price():
    out = MultipleSymbolsPrice.parse(
            multiple_symbols_price(try_conversion=True, fsyms='BTC,ETH',
                                   tsyms='USD,EUR', relaxed_validation=True,
                                   exchange='Kraken',
                                   extras='Bitmast Explorer',
                                   sign=False))
    prices = MultipleSymbolsPrice.parse(response=out, field='USD')
    assert out
    assert prices
    print(out)


def test_multiple_symbols_full_data():
    out = MultipleSymbolsFullData.parse(
            multiple_symbols_full_data(
                    fsyms='BTC,ETH',
                    tsyms='USD',
                    try_conversion=True,
                    relaxed_validation=True,
                    exchange='Kraken',
                    extras='Bitmast Explorer',
                    sign=False
            ))
    extra = MultipleSymbolsFullData.parse(out, currency='USD', information='OPENDAY',
                                          display=None)
    assert out
    assert extra


def test_generate_custom_average():
    out = GenerateCustomAverage.parse(
            generate_custom_average(
                    fsym='BTC',
                    tsym='USD',
                    exchange='Kraken',
                    relaxed_validation=True,
                    extras='Bitmast Explorer',
                    sign=False
            ))
    price = GenerateCustomAverage.parse(out, currency='USD', information='PRICE', display=None)
    assert out


def test_latest_news_articles():
    news = latest_news_articles(
                    feeds='ALL_NEWS_FEEDS',
                    categories='BTC,ETH',
                    exclude_categories='XLM,ETN',
                    lts=None,
                    lang='EN',
                    sort_order='latest',
                    extras='Bitmast Explorer',
                    sign=False,
            )
    out = LatestNewsArticles.parse(response=news, index=0)
    assert news
    assert out


def test_list_news_feeds():
    out = ListNewsFeeds.parse(
            list_news_feeds(extras='Bitmast Explorer', sign=False))
    assert out


def test_news_article_categories():
    out = NewsArticleCategories.parse(
            response=news_article_categories(extras='Bitmast Explorer', sign=False))
    assert out


def test_list_news_feeds_and_categories():
    out = ListNewsFeedsAndCategories.parse(
            list_news_feeds_and_categories(extras='Bitmast Explorer', sign=False))
    assert out


def test_exchanges_with_order_book_data():
    out = ExchangesWithOrderBookData.parse(
            exchanges_with_order_data(extras='Bitmast Explorer', sign=False))
    assert out


def test_order_book_l1_top():
    out = OrderBookL1Top.parse(
            order_book_l1_top(
                    fsyms='BTC,ETH',
                    tsyms='USD,EUR',
                    exchange='coinbase',
                    extras='Bitmast Explorer',
                    sign=False
            ))
    assert out


def test_order_book_l2_snapshot():
    out = OrderBookL2Snapshot.parse(
            order_book_l2_snapshot(
                    fsym='XLM',
                    tsym='USD',
                    exchange='Kraken',
                    extras='Bitmast Explorer',
                    sign=False,
                    limit=10
            ))
    assert out


def test_all_the_exchanges_and_trading_pairs():
    out = AllTheExchangesAndTradingPairs.parse(
            all_the_exchanges_and_trading_pairs(
                    fsym='LTC',
                    top_tier=True,
                    extras='Bitmast Explorer',
                    exchange='Coinbase',
                    sign=False
            ))
    assert out


def test_all_the_coins_general_info():
    out = AllTheCoins.parse(
            all_the_coins_general_info(
                    fsyms='BTC,ETH,LTC',
                    tsym='XLM',
                    extras='Bitmast Explorer',
                    sign=False
            ))
    assert out


def test_all_exchanges_general_info():
    out = AllExchangesGeneralInfo.parse(
            all_exchanges_general_info(
                    tsym='BTC',
                    extras='Bitmast Explorer',
                    sign=False
            ))
    assert out


def test_validate():
    assert validate(2)
    assert validate(3.45)
    assert validate(False)
    assert validate({'a': 1, 'b': 2})
    assert validate('Testing name', patterns=[r'\w+', r'.+'], length=100)
