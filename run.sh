#!/usr/bin/bash

cd `dirname $0`

# 进入虚拟环境
echo 切换虚拟环境...
. ~/.vir/env/bin/activate

echo 正在拉取最新代码...
git pull > logs/shell.log 2>&1

tarname="logs"

if [ ! -d "./${tarname}" ]; then
    mkdir ./${tarname}
fi
# 查看是否存在进程占用端口
echo 检测历史进程...
ps aux | grep 11111|cut -c 11-15|xargs kill  > logs/shell.log 2>&1

echo 启动程序...
nohup gunicorn -b 127.0.0.1:11111 manage:app > logs/shell.log 2>&1