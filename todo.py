import json
import hashlib
import argparse
import os
import getpass


class todo():
    def _read_todo_config_file(self):
        file_name = os.path.join(os.path.expanduser('~'), '.todo-config')
        try:
            f = open(file_name, 'r')
            file_content = f.read()
            if file_content[-32:] != hashlib.md5(bytes(file_content[:-32], encoding='utf8')).hexdigest():
                raise IOError("Config file validation error")
            f.close()
            return file_content[:-32]
        except (FileNotFoundError, IOError):
            raise IOError("Config file validation error")

    def _read_and_parse_config_file(self):
        try:
            data = json.loads(self._read_todo_config_file())
        except (IOError, json.decoder.JSONDecodeError):
            init_data = {
                "active_user": None,
                "users": {},
            }
            print("Initializes the config file")
            data = init_data 
        return data

    def _write_todo_config_file(self, data):
        file_name = os.path.join(os.path.expanduser('~'), '.todo-config')
        try:
            with open(file_name, 'w') as f:
                f.write(data + hashlib.md5(bytes(data, encoding='utf8')).hexdigest())
        except PermissionError as e:
            raise IOError(
                "Error: Unable to open file %s, unblock or grant read/write access to the file" % file_name)

    def _pack_and_write_config_file(self,data):
        try:
            self._write_todo_config_file(json.dumps(data))
        except IOError as e:
            print(str(e))

    def _read_todo_data_file(self):
        file_name = os.path.join(os.path.expanduser('~'), '.todo-data')
        try:
            f = open(file_name, 'r')
            file_content = f.read()
            if file_content[-32:] != hashlib.md5(bytes(file_content[:-32], encoding='utf8')).hexdigest():
                raise IOError("Data file validation error")
            f.close()
            return file_content[:-32]
        except (FileNotFoundError, IOError):
            raise IOError("Data file validation error")

    def _read_and_parse_data_file(self):
        try:
            data = json.loads(self._read_todo_data_file())
        except (IOError, json.decoder.JSONDecodeError):
            init_data = {
            }
            print("Initializes the data file")
            data = init_data 
        return data

    def _write_todo_data_file(self, data):
        file_name = os.path.join(os.path.expanduser('~'), '.todo-data')
        try:
            with open(file_name, 'w') as f:
                f.write(data + hashlib.md5(bytes(data, encoding='utf8')).hexdigest())
        except PermissionError as e:
            raise IOError(
                "Error: Unable to open file %s, unblock or grant read/write access to the file" % file_name)

    def _pack_and_write_data_file(self,data):
        try:
            self._write_todo_data_file(json.dumps(data))
        except IOError as e:
            print(str(e))

    def _import_user_data(self):
        self.user = self.config['active_user']
        if self.user != None:
            if self.user not in self.file_data.keys():
                self.file_data[self.user] = {'items': [], }
            self.items = self.file_data[self.user]['items']
        else:
            print('Please log in')
            exit()

    def __init__(self):
        self.file_data = self._read_and_parse_data_file()
        self.config = self._read_and_parse_config_file()

    def __del__(self):
        self._pack_and_write_data_file(self.file_data)
        self._pack_and_write_config_file(self.config)

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
        self._import_user_data()
        itemIndex = len(self.items)+1
        self.items.append(
            {'index': itemIndex, 'text': item, 'state': 'undone'})
        self._print_items(False)
        print('Item %d added' % itemIndex)

    def done(self, itemIndex):
        self._import_user_data()
        self.items[itemIndex-1]['state'] = 'done'
        self._print_items(False)
        print('Item %d done' % itemIndex)

    def list(self, list_all):
        self._import_user_data()
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

    def register(self, user_name):
        if user_name == None:
            user_name = input("register user name:")
        password = getpass.getpass(prompt="password:")
        retype_password = getpass.getpass(prompt="retype password:")
        if password != retype_password:
            print("The two passwords are inconsistent. Please register again")
            exit()
        if user_name in self.config['users'].keys():
            print("registration failed! This user name has been registered")
            exit()
        password = hashlib.sha256(bytes(password, encoding='utf8')).hexdigest() 
        self.config['users'][user_name] = password
        print("Register successfully, log in and start using")
    def login(self,user_name):
        if user_name == None:
            user_name = input("user:")
        password = getpass.getpass()
        password = hashlib.sha256(bytes(password, encoding='utf8')).hexdigest() 
        if user_name not in self.config['users'].keys():
            print("Longin failed!")
            exit()
        if password != self.config['users'][user_name]:
            print("Longin failed!")
            exit()

        if self.config['active_user'] != None:
            print("User %d has logged out" % self.config['active_user'])
        self.config['active_user'] = user_name
        print("Login success!")
    def logout(self):
        self.config['active_user'] = None
        print("Logout success!")
        pass


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

    parser_register = subparsers.add_parser('register')
    parser_register.add_argument('-u', '--user', nargs='?', default=None, help='')
    parser_register.set_defaults(func=lambda args: todo().register(args.user))

    parser_login = subparsers.add_parser('login')
    parser_login.add_argument('-u', '--user', nargs='?', default=None, help='')
    parser_login.set_defaults(func=lambda args: todo().login(args.user))

    parser_logout = subparsers.add_parser('logout')
    parser_logout.set_defaults(func=lambda args: todo().logout())


    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.parse_args(['--help'])
        raise
