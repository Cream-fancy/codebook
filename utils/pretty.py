import pandas as pd
from prettytable import PrettyTable


def import_from_file(filepath, file_type):
    if file_type == 'xls' or file_type == 'xlsx':
        df = pd.read_excel(filepath, index_col=False)
    else:
        df = pd.read_json(filepath, orient='records')
    return [[r[1], r[2], r[3], r[4], r[5], r[6]] for r in df.itertuples()]


def save_as_json(rows, filepath):
    df = pd.DataFrame()
    df = df.append(rows)
    df.columns = ['id', 'title', 'username', 'password', 'uid', 'website']
    df.to_json(filepath, orient='records', force_ascii=False)  # lines=True
    print('导出成功')


def save_as_excel(rows, filepath):
    df = pd.DataFrame()
    df = df.append(rows)
    df.columns = ['序号', '名称', '用户名', '密码', '用户', '网址']
    df.to_excel(filepath, index=False)
    print('导出成功')


def pretty_print(rows):
    table = PrettyTable(['序号', '名称', '用户名', '密码', '用户', '网址'])
    table.add_rows(rows)
    print(table)
