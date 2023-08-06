from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.cursor import MySQLCursor


class DealerDatabaseError(Exception):
    ''' Indicates an exception encountered while interacting with the DB. '''


class DealerDatabase():
    '''
    Wrapper for the Dealer MySQL database.
    '''

    def __init__(self, host: str, port: int, database: str, user: str, password=None, pool_size=5):
        '''
        Create a new DB wrapper class an instantiate the MySQL connection pool.
        '''

        self.connection_pool = MySQLConnectionPool(pool_name='connection_pool',
                                                   pool_size=pool_size,
                                                   host=host,
                                                   port=port,
                                                   user=user,
                                                   password=password,
                                                   database=database)

        self._init_tables()

    def add_exchange_order(self, order_id: str, exchange: str, symbol: str, side: str, qty: str, price: str, ts: str) -> None:
        '''
        Add an exchange order to the database.

        :param id: The exchange-specific order ID.
        :param exchange: The name of the exchange the order was posted to.
        :param symbol: The market symbol of the order.
        :param side: The side of the order (buy/sell).
        :param qty: The quantity of the base asset in the order (size).
        :param price: The price of the order in the quote asset.
        :param ts: The timestamp the order was posted at.
        '''

        qs = ("INSERT INTO `exchange_order_history` (`order_id`, `exchange`, `pair`, `side`, `size`, `price`, `time_placed`) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        try:
            self._execute_single_query(
                qs, (order_id, exchange, symbol, side, qty, price, ts))
        except Exception as error:
            raise DealerDatabaseError(
                'failed to add exchange order', error.args)

    def add_zero_ex_order(self, quote_id: str, side: str, pair: str, size: str, price: str, expiration: str, fee: str, status: str, tx_id: str) -> None:
        '''
        Add a filled (or failed) 0x order into the database.

        :param quote_id: The UUID sent with the quote.
        :param side: The side of the quote (bid or ask).
        :param pair: The market symbol the quote is for (BASE/QUOTE).
        :param size: The size of the quote in units of the base asset.
        :param price: The price of the quote in units of the quote asset.
        :param expiration: Quote expiration time.
        :param fee: The fee sent with the quote.
        :param status: Order status at time of insertion.
        :param tx_id: The order transaction hash.
        '''

        qs = ("INSERT INTO `zero_ex_order_history` ( `quote_id`, `side`, `pair`, `size`, `price`, `expiration`, `fee`, `status`, `transaction_id` ) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

        try:
            self._execute_single_query(qs, (quote_id, side, pair, size,
                                            price, expiration, fee, status, tx_id))
        except Exception as error:
            raise DealerDatabaseError('failed to add 0x order', error.args)

    def _init_tables(self) -> None:
        exchange_order_table_query = ("CREATE TABLE IF NOT EXISTS `dealer_db`.`exchange_order_history` "
                                      "(`id` INT AUTO_INCREMENT PRIMARY KEY, `order_id` VARCHAR(45) NOT NULL, `exchange` VARCHAR(45) NOT NULL,"
                                      "`pair` VARCHAR(45) NULL, `side` VARCHAR(45) NULL, `size` VARCHAR(45) NULL, `price` VARCHAR(45) NULL,"
                                      "`time_placed` VARCHAR(45) NULL, `filled_size` VARCHAR(45) NULL, `status` VARCHAR(45) NULL);")

        zrx_order_table_query = ("CREATE TABLE IF NOT EXISTS `dealer_db`.`zero_ex_order_history` (`id` INT AUTO_INCREMENT PRIMARY KEY, "
                                 "`quote_id` VARCHAR(45) NOT NULL, `side` VARCHAR(45) NULL, `pair` VARCHAR(45) NULL, `size` VARCHAR(45) NULL, "
                                 "`price` VARCHAR(45) NULL, `expiration` VARCHAR(45) NULL, `fee` VARCHAR(45) NULL, `status` VARCHAR(45) NULL, "
                                 "`transaction_id` VARCHAR(66) NULL);")

        try:
            connection = self._get_connection()
            cursor = self._get_cursor(connection)
            self._execute_query(cursor, exchange_order_table_query)
            self._execute_query(cursor, zrx_order_table_query)
            self._commit(connection)
            self._close_cursor(cursor)
            self._give_connection(connection)
        except Exception as error:
            raise DealerDatabaseError('failed to create tables', error.args)

    def _execute_single_query(self, query: str, args=None) -> None:
        '''
        Execute a provided SQL query, but do not return any values (write only).

        :param query: The valid SQL query string.
        '''
        connection = self._get_connection()
        cursor = self._get_cursor(connection)
        self._execute_query(cursor, query, args)
        self._commit(connection)
        self._close_cursor(cursor)
        self._give_connection(connection)

    def _get_connection(self) -> PooledMySQLConnection:
        return self.connection_pool.get_connection()

    def _give_connection(self, connection: PooledMySQLConnection) -> None:
        connection.close()

    def _get_cursor(self, connetion: PooledMySQLConnection) -> MySQLCursor:
        return connetion.cursor()

    def _close_cursor(self, cursor: MySQLCursor) -> None:
        cursor.close()

    def _execute_query(self, cursor: MySQLCursor, query: str, args=None) -> MySQLCursor:
        cursor.execute(query, args)
        return cursor

    def _commit(self, connection: PooledMySQLConnection) -> PooledMySQLConnection:
        connection.commit()
        return connection
