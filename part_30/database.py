from datetime import datetime
from datetime import timedelta
import MySQLdb

HOST = ""
USER = ""
PASSWD = ""
DB = ""


class Database():
    def __init__(self):
        self.db = None
        self.cur = None
        self.debug = False

    def connect_to_db(self):
        self.db = MySQLdb.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
        )
        self.cur = self.db.cursor()

    def close_connection(self):
        self.cur.close()
        self.db.close()

    def get_user_auth(self, voter):
        query = ("SELECT `access_token`,`refresh_token`,`expires_in` FROM " +
                f"`steem_authorization` WHERE `user_login` = '{voter}'")
        return self.get_data(query)

    def add_to_error_log(self, voter, author, permlink, weight, type, message,
                         timestamp):
        query = (
            'INSERT INTO `error_log` (`id`, `voter`, `author`, ' +
            '`permlink`, `weight`, `type`, `error`, `timestamp`) VALUES ' +
            f'(NULL, "{voter}", "{author}", "{permlink}", ' +
            f'"{weight}", "{type}", "{message}", "{timestamp}");')
        self.post_data(query, 'error_log')
        print(f"Vote failed: {message}\n")

    def update_authentication_tokens(self, voter, access_token, refresh_token,
                                     expires_in, timestamp):
        dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        expires_in = dt + timedelta(seconds=expires_in)

        query = ("UPDATE `steem_authorization` SET `access_token` = " +
                 f"'{access_token}', `expires_in` = '{expires_in}', " +
                 f"`refresh_token` = '{refresh_token}' WHERE " +
                 f"`user_login` = '{voter}';")
        self.post_data(query, 'steem_authorization')

    # Insert date, amount into table 'table'. Look if the record already
    # exists, update if needed else add.
    def post_data(self, query, table):
        try:
            self.connect_to_db()

            # Lock table
            self.cur.execute(f"LOCK TABLES {table} WRITE;")
            self.cur.execute(query)

            # Release table
            self.cur.execute(f"UNLOCK TABLES;")

            # Commite changes made to the db
            self.db.commit()

        except Exception as e:
            print('Error:', e)

        finally:
            # Close connections
            self.close_connection()

    def get_data(self, query):
        try:
            # Connect to DB and execute query
            self.connect_to_db()
            self.cur.execute(query)

            # Fetch results
            rows = self.cur.fetchall()

            # Commite changes made to the db
            self.db.commit()
        except Exception as e:
            print('Error:', e)

        finally:
            # Close connections
            self.close_connection()
            return rows
