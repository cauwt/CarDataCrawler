#!/usr/bin/env python
#  -*- coding: utf-8 -*-


import MySQLdb


class MysqldbHelper:

    def get_connection(self):
        """ 获取数据库连接
        :return: 数据库连接
        """
        try:
            conn = MySQLdb.connect(host='localhost', user='crawler', passwd='crawler', db='car_data', port=3306,
                                   charset='utf8')
            return conn
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
            # ,返回结果为字典

    def select(self, sql):
        """查询方法，使用con.cursor(MySQLdb.cursors.DictCursor)
        :param sql: 查询语句
        :return:返回结果为字典
        """
        try:
            con = self.get_connection()
            print con
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()
            # 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')

    def update_by_param(self, sql, params):
        try:
            con = self.get_connection()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()
            # 不带参数的更新方法

    def update(self, sql):
        try:
            con = self.get_connection()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()

    def insert(self, sql, params):
        """ 插入数据，单条
        :param sql: sql语句
        :param params: 要插入的数据，元组形式
        :return: 记录数
        """
        try:
            con = self.get_connection()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()

    def insert_batch(self, sql, params):
        """ 插入数据，批量
        :param sql: sql语句
        :param params: 要插入的数据，元组的数组
        :return: 记录数
        """
        try:
            con = self.get_connection()
            cur = con.cursor()
            count = cur.executemany(sql, params)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()
