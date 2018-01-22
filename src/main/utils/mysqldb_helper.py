#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: mysqldb_helper
# author: eva
# date: 2018/1/17
# version:
# description:mysql助手类
# ----------------------------------------------------------------------------------------------------------------------


import MySQLdb


class MysqlHelper:
    def __init__(self, host, user, password, db, charset='utf8'):
        """初始化，建立连接

        :param host:
        :param user:
        :param password:
        :param db:
        :param charset:
        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
            self.conn.set_character_set(self.charset)
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as e:
            print ('MySql Error : %d %s' % (e.args[0], e.args[1]))

    def select(self, sql, params=()):
        """查询方法，使用con.cursor(MySQLdb.cursors.DictCursor)
        :param params:
        :param sql: 查询语句
        :return:返回结果为字典
        """
        try:
            self.cursor.execute(sql, params)
            fc = self.cursor.fetchall()
            return fc
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
            raise

    def update(self, sql, params=()):
        """更新

        :param sql:
        :param params:
        :return:
        """
        try:
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            return count
        except MySQLdb.Error, e:
            self.conn.rollback()
            print "Mysqldb Error:%s" % e
            raise

    def insert(self, sql, params=()):
        """ 插入数据，单条
        :param sql: sql语句
        :param params: 要插入的数据，元组形式
        :return: 记录数
        """
        try:
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            return count
        except MySQLdb.Error, e:
            self.conn.rollback()
            print "Mysqldb Error:%s" % e
            raise

    def insert_batch(self, sql, params):
        """ 插入数据，批量
        :param sql: sql语句
        :param params: 要插入的数据，元组的数组
        :return: 记录数
        """
        try:
            count = self.cursor.executemany(sql, params)
            self.conn.commit()
            return count
        except MySQLdb.Error, e:
            self.conn.rollback()
            print "Mysqldb Error:%s" % e
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()
