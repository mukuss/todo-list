import json
import hashlib
import argparse
import os


class todo():
    def _read_todo_data_file(self):
        file_name = os.path.join(os.path.expanduser('~'), '.todo_data')
        try:
            f = open(file_name, 'r')
            file_content = f.read()
            if file_content[-32:] != hashlib.md5(bytes(file_content[:-32], encoding='utf8')).hexdigest():
                raise IOError("Data file validation error")
            f.close()
            return file_content[:-32]
        except (FileNotFoundError, IOError):
            raise IOError("file validation error")

    def _write_todo_data_file(self, data):
        file_name = os.path.join(os.path.expanduser('~'), '.todo_data')
        try:
            with open(file_name, 'w') as f:
                f.write(data + hashlib.md5(bytes(data, encoding='utf8')).hexdigest())
        except PermissionError as e:
            raise IOError(
                "Error: Unable to open file %s, unblock or grant read/write access to the file" % file_name)

    def _read_and_parse_data_file(self):
        try:
            data = json.loads(self._read_todo_data_file())
        except (IOError, json.decoder.JSONDecodeError):
            init_data = {
                'active_user': 'default',
                'users': {
                    'default': {
                        'items': [],
                    },
                },
            }
            print("Initializes the data file")
            data = init_data 
        return data

    def _pack_and_write_data_file(self,data):
        try:
            self._write_todo_data_file(json.dumps(data))
        except IOError as e:
            print(str(e))

    def __init__(self):
        self.file_data = self._read_and_parse_data_file()
        active_user = self.file_data['active_user']
        self.items = self.file_data['users'][active_user]['items']

    def __del__(self):
        self._pack_and_write_data_file(self.file_data)

    def _print_items(self, print_all):
        print('')
        print('')
        for item in self.items:
            if item['state'] == 'undone':
                print("%d. %s" % (item['index'], item['text']))
            elif print_all:
                print("%d. [Done] %s" % (item['index'], item['text']))
        print('')
        print('')

    def add(self, item):
        itemIndex = len(self.items)+1
        self.items.append(
            {'index': itemIndex, 'text': item, 'state': 'undone'})
        self._print_items(False)
        print('Item %d added' % itemIndex)

    def done(self, itemIndex):
        self.items[itemIndex-1]['state'] = 'done'
        self._print_items(False)
        print('Item %d done' % itemIndex)

    def list(self, list_all):
        self._print_items(list_all)
        items_number = len(self.items)
        done_number = len(
            [item for item in self.items if item['state'] == 'done'])
        undone_number = len(
            [item for item in self.items if item['state'] == 'undone'])
        if list_all == False:
            print('Total: %d items' % undone_number)
        else:
            print('Total: %d items, %d item done' %
                  (items_number, done_number))


# 程序从这里开始，主要为使用argparse处理输入参数，业务代码均在todo类中
if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="todo")
    subparsers = parser.add_subparsers(description='subcommands')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('item')

    parser_add.set_defaults(func=lambda args: todo().add(args.item))

    parser_done = subparsers.add_parser('done')
    parser_done.add_argument('itemIndex')
    parser_done.set_defaults(
        func=lambda args: todo().done(int(args.itemIndex)))

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('-a', '--all', nargs='?',
                             default=False, const=True, help='')
    parser_list.set_defaults(func=lambda args: todo().list(args.all))

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.parse_args(['--help'])
        raise
