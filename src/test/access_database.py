# -*- coding: utf-8 -*-

import MySQLdb


def main():
    try:
        conn = MySQLdb.connect(host="localhost", user="crawler", passwd="crawler", db="car_data", charset="utf8")
        cursor = conn.cursor()
        conn.select_db('car_data')
        params = [("Alice", 21), ("Bob", 22), ("Chris", 20)]
        sql = "insert into test(name,age) values(%s, %s)"
        cursor.executemany(sql, params)
        conn.commit()
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    pass

if __name__ == '__main__':
    main()
