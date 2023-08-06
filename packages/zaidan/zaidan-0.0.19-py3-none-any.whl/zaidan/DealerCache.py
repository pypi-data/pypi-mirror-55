from sys import path

from redis import Redis

from .utils import is_valid_uuid, encode_to_bytes, decode_from_bytes


class DealerCacheError(Exception):
    ''' Signifies an error encountered while interacting with the cache. '''


class NotFoundError(DealerCacheError):
    ''' Signifies an error arising when a requested item does not exist. '''


class DealerCache():
    '''
    Abstraction over a Redis database for dealer quotes and orders.

    Provides compression/encoding for storing structured data in redis.
    '''

    # redis key for quotes (order mark) hash table
    quotes_key = "QUOTES"

    # redis key for orders hash table (hedger positions)
    orders_key = "ORDERS"

    def __init__(self, host: str, port=6379, password=None):
        '''
        Create a new DealerCache instance.

        :param host: The hostname of the Redis server.
        :param port: The port of the Redis server (default: 6379)
        :param password: The password for the Redis server (default: None)
        '''

        self.db = Redis(host=host, port=port, password=password)

    def set_quote(self, quote_id: str, order_mark: object, status=0) -> None:
        '''
        Store an order mark object by its quote UUID.

        Used to initially store quotes, and to update their statuses.

        Status codes:
        - 0: Quote generated
        - 1: Validated and submitted for settlement
        - 2: Filled, sent to hedger

        :param quote_id: The quote UUID string.
        :param order_mark: The quote object.
        :param status: The new status of the quote.
        '''

        data = {'status': status, 'quote': order_mark}

        mark_compressed = encode_to_bytes(order_mark)
        self.db.hset(self.quotes_key, quote_id, mark_compressed)

    def update_quote_status(self, quote_id: str, new_status: int) -> None:
        '''
        Update an existing quote's status.

        :param quote_id: The ID of the quote to update.
        :param new_status: The new status code of the quote.
        '''

        if not self.db.hexists(self.quotes_key, quote_id):
            raise NotFoundError('quote with specified ID not found')

        order_mark_raw = self.db.hget(self.quotes_key, quote_id)
        order_mark = decode_from_bytes(order_mark_raw)

        if 'status' not in order_mark:
            raise DealerCacheError('malformed order mark')

        order_mark['status'] = new_status
        new_mark_raw = encode_to_bytes(order_mark)
        self.db.hset(self.quotes_key, quote_id, new_mark_raw)

    def get_quote(self, quote_id: str) -> object:
        '''
        Fetch an order mark by it's quote ID (if it exists).

        Will raise a NotFoundError if the quote does not exist, and a CacheError
        if the quote_id is invalid.

        :param quote_id: The quote ID generated on initial request.
        '''

        if not is_valid_uuid(quote_id):
            raise DealerCacheError("invalid quote ID")

        raw_order_mark = self.db.hget(self.quotes_key, quote_id)
        if not raw_order_mark:
            raise NotFoundError("quote not found", quote_id)

        order_mark = decode_from_bytes(raw_order_mark)
        return order_mark

    def remove_quote(self, quote_id: str) -> None:
        '''
        Remove a quote by its ID.

        :param quote_id: The UUID included when the quote was generated.
        '''

        self.db.hdel(self.quotes_key, quote_id)

    def get_quote_ids(self) -> list:
        '''
        Fetch an array of all quote ID's in the cache.
        '''

        return self.db.hkeys(self.quotes_key)

    def get_order_ids(self) -> list:
        '''
        Fetch an array of all order ID's in the cache.
        '''

        return self.db.hkeys(self.orders_key)
