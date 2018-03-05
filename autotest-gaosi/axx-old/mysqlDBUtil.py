# -*- encoding:utf8 -*-
'''
@author: PGQ
@version: 2016-12-22
@comment:
'''
import MySQLdb
class dbUtil:
    def __init__(self,host,user,password,charset="utf8"):
        self.host=host
        self.user=user
        self.password=password
        self.charset=charset
        try:
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password)
            self.conn.set_character_set(self.charset)
            self.cur=self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


    def selectDb(self,db):
      try:
          self.conn.select_db(db)
      except MySQLdb.Error as e:
          print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def query(self,sql):
        try:
           n=self.cur.execute(sql)
           return n
        except MySQLdb.Error as e:
           print("Mysql Error:%s\nSQL:%s" %(e,sql))

    def queryRow(self,sql):
        self.query(sql)
        result = self.cur.fetchone()
        return result

    def queryAll(self,sql):
        self.query(sql)
        result=self.cur.fetchall()
        desc =self.cur.description
        d = []
        for inv in result:
             _d = {}
             for i in range(0,len(inv)):
                 _d[desc[i][0]] = str(inv[i])
             d.append(_d)
        return d

    def insert(self,p_table_name,p_data):
        for key in p_data:
            p_data[key] = "'"+str(p_data[key])+"'"
        key   = ','.join(p_data.keys())
        value = ','.join(p_data.values())
        real_sql = "INSERT INTO " + p_table_name + " (" + key + ") VALUES (" + value + ");"
        print real_sql
        #self.query("set names 'utf8'")
        return self.query(real_sql)

    def update(self,p_table_name,dictset,dictwhere):
        for key in dictset:
            dictset[key] = str(key) +"='"+str(dictset[key])+"'"
        value = ','.join(dictset.values())
        for keycon in dictwhere:
            dictwhere[keycon] = str(keycon) +"='"+str(dictwhere[keycon])+"'"
        valuecon = ' AND '.join(dictwhere.values())
        real_sql = "UPDATE " + p_table_name + " SET " + value + " WHERE "+ valuecon + ";"
        print real_sql
        #self.query("set names 'utf8'")
        return self.query(real_sql)

    def getLastInsertId(self):
        return self.cur.lastrowid

    def getRow(self,strZD):
        results = self.cur.fetchone()
        print results
        #for row in results:
         #   print "%s" % (row[strZD])
        return results[strZD]

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()