# class MySQL
import pymysql


class MySQL(object):
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_port, mysql_db):
        self.db = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port,
                                  db=mysql_db, charset='utf8')
        self.cursor = self.db.cursor()

    def create(self, sql_create_table):
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql_create_table)
            self.db.commit()
        except Exception as e:
            print(e.args)


    def query(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.commit()
            return result
        except Exception as e:
            print(e.args)
            self.db.rollback()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e.args)
            self.db.rollback()

    # 保存到mysql
    def insert(self, item, table_name):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table_name,
                                                                                             keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        try:
            if self.cursor.execute(sql, tuple(data.values()) * 2):
                self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()

    def close(self):
        self.db.close()


if __name__ == '__main__':
    obj = MySQL()
    if obj:
        print('OK')
        obj.close()
