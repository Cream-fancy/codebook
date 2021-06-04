from utils import Database
import argparse

if __name__ == '__main__':
    db = Database()
    db.initialize()

    parser = argparse.ArgumentParser(description='欢迎使用本地密码存储库')
    subparsers = parser.add_subparsers(help='sub command help')

    # new
    parser_new = subparsers.add_parser('new', help='create a new code')
    parser_new.set_defaults(func=db.insert)

    # find
    parser_find = subparsers.add_parser('find', help='find some code')
    parser_find.add_argument('-m', '--match', metavar='', type=str, help='模糊匹配')
    parser_find.add_argument('-l', '--limit', metavar='', type=int, help='限制数量')
    parser_find.add_argument('-o', '--offset', metavar='', type=int, help='偏移量')
    parser_find.add_argument('-decrypt', action='store_true', default=False, dest='decrypt', help='decrypt password')
    parser_find.add_argument('-encrypt', action='store_false', default=False, dest='decrypt', help='encrypt password')
    parser_find.set_defaults(func=db.find)

    # import
    parser_import = subparsers.add_parser('import', help='import file', aliases=['in'])
    parser_import.add_argument('-f', '--filepath', type=str, help='文件路径', required=True)
    parser_import.set_defaults(func=db.import_file)

    # export
    parser_export = subparsers.add_parser('export', help='export file', aliases=['out'])
    parser_export.add_argument('-f', '--filepath', type=str, help='文件路径')
    parser_export.set_defaults(func=db.export_file)

    args = parser.parse_args()
    args.func(args)
