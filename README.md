# 作业：代办事件管理工具

* 工具名称：todo
* 采用语言：python3
* 环境版本：python3.7.6

## 说明

这是一个代办事项管理脚本，现已实现第一阶段功能，包含 add、done、list三个子功能 

其中add用以增加代办事项，done用以将代办标记完成，list用以打印代办事项，可以使用--all参数可打印所有事项

文件保存在用户根目录文件夹中的.todo_data文件中，以json格式保存，后附md5校验以判断数据正确性

## 版本升级：

1. 2020-12-30 第一版功能实现
2. 2020-12-31 增加说明、增加数据文件md5校验、整理代码并去除代码中部分“坏味道”使其更易于维护

## 环境搭建

### Windows

1. 官网下载最新python3的Windows版本并安装
2. 将安装目录添加到环境变量中（具体步骤可百度python3安装）
3. 在命令行中输入`python -V`并回车，打印出`Python 3.n.n`则安装成功

### Ubuntu

1. 打开shell
2. `sudo apt-get install python3`等待安装完成
3. `python -V`并回车，打印出`Python 3.n.n`则安装成功

### 获取作业版本

`git clone --branch todo-phase-1 https://github.com/mukuss/todo-list.git`

### 运行测试

1. `python todo.py add "hello wold"`
2. `python todo.py add "todo-phase-2"`
3. `python todo.py list`
4. `python todo.py done 2`
5. `python todo.py list`
6. `python todo.py list --all`


