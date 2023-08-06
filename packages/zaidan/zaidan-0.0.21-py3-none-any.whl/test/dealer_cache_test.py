from unittest import TestCase, main

from redis import Redis

from zaidan import DealerCache, encode_to_bytes, decode_from_bytes

# structure: [ [symbol, name], ]
test_vals = [['WETH/DAI', 123.5], ['ETH/USD', 0.88], ['ZRX/DAI', 471]]

test_exchange_name = "coinbarf"
test_market_symbol = "SPANK/USD"
test_bid_order_book = [[1.5, 0.01], [1.4, 0.02], [1.3, 0.04], [1.1, 1.3]]
test_ask_order_book = [[1.6, 0.02], [1.7, 0.04], [2.1, 0.88], [2.4, 2.08]]


class TestDealerCache(TestCase):

    redis = Redis()

    def _clear_all_positions(self):
        ids = self.redis.hgetall(DealerCache.unhedged_position_key)
        return [self.redis.hdel(DealerCache.unhedged_position_key, _id) for _id in ids]

    def test_set_unhedged_position(self):
        db = DealerCache()
        self._clear_all_positions()

        for test_val in test_vals:
            symbol = test_val[0]
            position = test_val[1]

            db.set_unhedged_position(symbol, position)
            from_redis = self.redis.hget(db.unhedged_position_key, symbol)
            self.assertEqual(from_redis.decode(), str(position))

    def test_get_unhedged_position(self):
        db = DealerCache()
        self._clear_all_positions()

        for test_val in test_vals:
            symbol = test_val[0]
            position = test_val[1]

            before = db.get_unhedged_position(symbol)
            self.assertEqual(before, 0.0)

            db.set_unhedged_position(symbol, position)
            after = db.get_unhedged_position(symbol)
            self.assertEqual(after, position)

    def test_set_order_book(self):
        db = DealerCache()

        compressed_ask_book = encode_to_bytes(test_ask_order_book)
        compressed_bid_book = encode_to_bytes(test_bid_order_book)

        db.set_order_book(test_exchange_name,
                          test_market_symbol, 'ask', test_ask_order_book)
        db.set_order_book(test_exchange_name,
                          test_market_symbol, 'bid', test_bid_order_book)

        raw_asks_from_redis = self.redis.get(
            f'{test_market_symbol}_{test_exchange_name}_ask')
        raw_bids_from_redis = self.redis.get(
            f'{test_market_symbol}_{test_exchange_name}_bid')
        self.assertEqual(raw_asks_from_redis, compressed_ask_book)
        self.assertEqual(raw_bids_from_redis, compressed_bid_book)


if __name__ == "__main__":
    main()
