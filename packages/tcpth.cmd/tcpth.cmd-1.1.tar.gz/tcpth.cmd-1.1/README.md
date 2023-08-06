# tcpthrough-cmd
>注：该项目是tcp穿透项目的辅助项目。

通过交互式的命令行操作tcpthrough server ，该项目只是辅助功能，通过命令行来可视化 http api的数据.

具体项目请看 [https://github.com/longshengwang/tcpthrough-server](https://github.com/longshengwang/tcpthrough-server)

# 安装
python setup.py install
或者
pip install tcpth.cmd

# 运行
```
➜  tcp-console git:(master) ✗ tcpthcmd
Welcome to use the tcp through.
  ______              ________                           __
 /_  __/________     /_  __/ /_  _________  __  ______ _/ /_
  / / / ___/ __ \     / / / __ \/ ___/ __ \/ / / / __ `/ __ \
 / / / /__/ /_/ /    / / / / / / /  / /_/ / /_/ / /_/ / / / /
/_/  \___/ .___/    /_/ /_/ /_/_/   \____/\__,_/\__, /_/ /_/
        /_/                                    /____/


tcpthrough> help
    list                                 -- get all registration
    get <name>                           -- get special name information
    register add <name> <localhost:port> <proxy port>    -- add registration
    register delete <name> <proxy port>                  -- delete registration
    trust add <name> [<proxy port>] <trusted ip>        -- add trust ip
    trust delete <name> [<proxy port>]  <trusted ip>     -- delete trust ip
    trust get <name> [<proxy port>]     -- get trust ip
tcpthrough>

```
