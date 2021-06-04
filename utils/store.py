import sqlite3
from datetime import datetime
from .crypto import CryptoAES
from . import pretty
import argparse


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('user_data.db')

    def initialize(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS user (
            uid varchar(16) PRIMARY KEY,
            secret_key char(16) NOT NULL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS code (
            id integer PRIMARY KEY AUTOINCREMENT,
            title varchar(32) NULL,
            username varchar(32) NULL,
            password varchar(64) NULL,
            uid varchar(16) NULL,
            website varchar(32) NULL,
            ts integer NOT NULL)''')
        self.conn.commit()
        cur.close()

    def insert(self, args):
        uid = input('who are you [Cream | Forrest]: ')
        if uid != 'Cream' and uid != 'Forrest':
            print('插入失败')
            return
        title = input('The title of this record: ')
        username = input('username: ')
        password = input('password: ')
        website = input('website: ')
        ts = int(datetime.now().timestamp())
        aes = CryptoAES(str(ts))
        password = aes.encrypt(password)
        cursor = self.conn.cursor()
        sql = 'insert into code(title, username, password, uid, website, ts) values (?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, (title, username, password, uid, website, ts))
        self.conn.commit()
        cursor.close()
        print('插入成功')

    def find(self, args):
        if args.match is not None:
            condition_map = ['{} LIKE \'%{}%\''.format(x, args.match) for x in ['title', 'website', 'username']]
            condition = 'WHERE ' + ' OR '.join(condition_map)
        else:
            condition = ''
        limit = args.limit or 20
        offset = args.offset or 0
        cur = self.conn.cursor()
        res = cur.execute('select * from code ' + condition + ' limit ? offset ?', [limit, offset])
        if args.decrypt:
            rows = [(i + 1, row[1], row[2], CryptoAES(str(row[6])).decrypt(row[3]), row[4], row[5])
                    for i, row in enumerate(res)]
        else:
            rows = [(i + 1, row[1], row[2], row[3], row[4], row[5]) for i, row in enumerate(res)]
        pretty.pretty_print(rows)
        cur.close()
        return rows

    def import_file(self, args):
        filepath = args.filepath
        file_type = self.check_file(filepath)
        if file_type is None:
            print('导入不合法')
            return
        params = []
        for r in pretty.import_from_file(filepath, file_type):
            ts = int(datetime.now().timestamp())
            r[3] = CryptoAES(str(ts)).encrypt(r[3])
            r.append(ts)
            params.append(r)
        sql = 'insert into code(id, title, username, password, uid, website, ts) values (?, ?, ?, ?, ?, ?, ?)'
        cursor = self.conn.cursor()
        cursor.executemany(sql, params)
        self.conn.commit()
        cursor.close()
        print('导入成功')

    def export_file(self, args):
        filepath = args.filepath or '{}.json'.format(int(datetime.now().timestamp()))
        file_type = self.check_file(filepath)
        if file_type is None:
            print('导出不合法')
            return
        rows = self.find(argparse.Namespace(match=None, limit=9999, offset=None, decrypt=True))
        if file_type == 'xls' or file_type == 'xlsx':
            pretty.save_as_excel(rows, filepath)
        else:
            pretty.save_as_json(rows, filepath)

    @staticmethod
    def check_file(fp: str):
        if fp.endswith(('.json', '.xls', '.xlsx')):
            return fp.split('.')[-1]
        else:
            return None
