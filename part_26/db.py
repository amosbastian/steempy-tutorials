import MySQLdb


def insert_selection(block, index, timestamp, to, user, amount, memo):

    query = "INSERT INTO `transfers` (`block`, `index`, `timestamp`,`to`, `from`, `amount`, `memo`)" \
            " VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(block, index, timestamp, to, user, amount, memo)

    try:
        db = MySQLdb.connect(host="localhost",
                             user="test",
                             passwd="Test!234#",
                             db="steem")

        db.set_character_set('utf8mb4')

        cur = db.cursor()
        cur.execute('SET NAMES utf8mb4;')
        cur.execute('SET CHARACTER SET utf8mb4;')
        cur.execute('SET character_set_connection=utf8mb4;')
        cur.execute(query)

        db.commit()

    except Exception as e:
        print('Error:', e)

    finally:
        cur.close()
        db.close()
