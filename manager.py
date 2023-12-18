# coding: utf-8
import sys
import loggus

from utils.env import Env
from cmds.cmd_proxy import main as proxyCmd
from cmds.cmd_server import main as serverCmd
from cmds.cmd_spider import main as spiderCmd


def main():
    if Env.LOG_FORMAT.lower() == "json":
        loggus.SetFormatter(loggus.JsonFormatter)
    args = sys.argv[1:]
    if len(args) < 1:
        loggus.panic("未指定启动指令")
    cmd = args[0]
    defaultCmd = lambda: loggus.variables(cmd).warning("未指定有效启动指令")
    ({
        "proxy": proxyCmd,
        "server": serverCmd,
        "spider": spiderCmd,
    }).get(cmd, defaultCmd)()


if __name__ == '__main__':
    main()
