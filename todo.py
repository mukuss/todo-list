import json
import argparse
import os

class todo():
    def __init__(self):
        try:
            f = open(os.path.expanduser('~/.todo-data'), 'r')
            self.data = json.load(f)
            f.close()
        except FileNotFoundError:  # 初始化数据
            self.data = {'user': 'default', 'data': {
                'default': {'item': [], 'done': []}}}

    # 打印任务列表，all为是否打印已结束任务的标志，可False或True
    def _print_item(self,all):
        user = self.data['user']
        data = self.data['data'][user]
        print('')
        print('')
        for no in range(len(data['item'])):
            if data['done'][no] == False:
                print("%d. %s"%(no+1,data['item'][no]))
            elif all:
                print("%d. [Done] %s"%(no+1,data['item'][no]))
        print('')
        print('')

    # 添加任务
    def add(self, item):
        user = self.data['user']
        data = self.data['data'][user]
        data['item'].append(item)
        data['done'].append(False)
        self._print_item(False)
        itemIndex = len(data['item'])
        print('Item %d added' % itemIndex)

    # 结束任务
    def done(self, itemIndex):
        user = self.data['user']
        data = self.data['data'][user]
        data['done'][itemIndex] = True
        self._print_item(False)
        print('Item %d done' % itemIndex)

    # 打印任务列表，all为是否打印已结束任务的标志，可False或True
    def list(self,all):
        user = self.data['user']
        data = self.data['data'][user]
        self._print_item(all)
        all_items_number = len(data['item'])
        done_number = len([f for f in data['done'] if f == True])
        items_number = len([f for f in data['done'] if f == False])
        if all == False:
            print('Total: %d items' % items_number)
        else:
            print('Total: %d items, %d item done' %
                  (all_items_number, done_number))

    # 将数据写入文件
    def __del__(self):
        with open(os.path.expanduser('~/.todo_data'), 'w') as f:
            json.dump(self.data, f)
            f.close()
        
# 程序从这里开始
# 分析命令参数找到处理函数
if(__name__=='__main__'):
    parser = argparse.ArgumentParser(description="todo")
    subparsers = parser.add_subparsers(description='subcommands')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('item')
    
    parser_add.set_defaults(func=lambda args: todo().add(args.item))

    parser_done = subparsers.add_parser('done')
    parser_done.add_argument('itemIndex')
    parser_done.set_defaults(func=lambda args: todo().done(int(args.itemIndex)-1))

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('-a', '--all', nargs='?',
                             default=False, const=True, help='')
    parser_list.set_defaults(func=lambda args: todo().list(args.all))

    args = parser.parse_args()
    if args.func:
        args.func(args)
