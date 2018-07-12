from datetime import datetime
from datetime import timedelta

import MySQLdb


class Database():
    def __init__(self):
        self.db = None
        self.cur = None

    def connect_to_db(self):
        self.db = MySQLdb.connect(host="localhost",    # host location
                                  user="test",         # username
                                  passwd="Test!234#",  # password
                                  db="steem")          # database
        self.cur = self.db.cursor()

    def close_connection(self):
        self.cur.close()
        self.db.close()

    # Retrieve current amount value, add new and update the record
    def update_record(self, amount, date, table):
        # retrieve current value for amount
        self.cur.execute(f"SELECT `amount` FROM `{table}` "
                         f"WHERE `date` = '{date}';")
        total = amount + self.cur.fetchone()[0]

        # update the record
        query = f"UPDATE `{table}` SET `amount` = {total} WHERE " \
                f"`{table}`.`date` = '{date}';"
        self.cur.execute(query)

    # Check if query comes back with any results
    def check_if_record_exist(self, date, table):
        self.cur.execute(f"SELECT 1 FROM `{table}` WHERE `date` = '{date}';")

        if len(self.cur.fetchall()) > 0:
            return True

    def get_data(self, date, table):
        # Convert string to datetime_object and calculate end_date
        start_date = datetime.strptime(date, '%Y-%m-%d').date()
        end_date = start_date + timedelta(days=1)

        query = (f"SELECT `date`,`amount` FROM `{table}` WHERE `date` " +
                 f"BETWEEN '{start_date}' AND '{end_date}' " +
                 "ORDER BY `date` ASC;")

        try:
            self.connect_to_db()
            self.cur.execute(query)

            x = []
            y = []

            for result in self.cur.fetchall():
                x.append(result[0])
                y.append(result[1])

            self.db.commit()

        except Exception as e:
            print('Error:', e)

        finally:
            # close connection afterwards
            self.close_connection()

        return x, y

    # Insert date, amount into table 'table'. Look if the record already
    # exists, update if needed else add.
    def insert_selection(self, date, amount, table):
        # sql query used to insert data into the mysql database
        query = f"INSERT INTO `{table}` (`date`, `amount`)" \
                " VALUES ('{}', '{}');".format(date, amount)

        try:
            self.connect_to_db()

            # Lock table
            self.cur.execute(f"LOCK TABLES {table} WRITE;")

            # Check if record exists, update if the case. Else create
            if self.check_if_record_exist(date, table):
                self.update_record(amount, date, table)
            else:
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
