# -*- coding:utf-8 -*-
import argparse
import os
import re
import winreg as wr

BASE_PATH = r"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Mappings"


# 获得所有程序的 SID
def get_apps_sid():
    sid_list = []
    with wr.OpenKeyEx(wr.HKEY_CURRENT_USER, BASE_PATH) as key:
        max_index = wr.QueryInfoKey(key)[0]
        for i in range(max_index):
            sid_list.append(wr.EnumKey(key, i))
    return sid_list


# 通过 SID 获取程序的详细信息，返回的数组包含信息为 (显示名Human-Readable， SID, 应用名)
def get_apps_detail():
    apps_sid = get_apps_sid()
    apps_detail = []
    for i in apps_sid:
        app_reg_path = os.path.join(BASE_PATH, i)
        with wr.OpenKeyEx(wr.HKEY_CURRENT_USER, app_reg_path) as key:
            app_display_name, _ = wr.QueryValueEx(key, "DisplayName")
            # 跳过非应用程序
            if app_display_name.startswith("@{"):
                continue
            app_name, _ = wr.QueryValueEx(key, "Moniker")
            # A touple with (app_display_name, SID, app_name)
            app_detail = (app_display_name, i, app_name)
            apps_detail.append(app_detail)
    # 根据显示名进行排序，然后返回排序后的列表
    apps_detail_sorted = sorted(apps_detail, key=lambda display_name: apps_detail[0])
    return apps_detail_sorted


def print_list(apps_detail):
    num = 0
    for app in apps_detail:
        print("[{0}]\t{1}".format(num, app[0]))
        num += 1


if __name__ == '__main__':
    apps_detail = get_apps_detail()

    parser = argparse.ArgumentParser(description='管理并排除被网络隔离的UWP应用。')
    parser.add_argument("-l", action="store_true", help="仅打印所有UWP应用列表。", default=False)
    parser.add_argument("-s", action="store_true", help="打印已被添加到排除列表中的UWP应用。", default=False)
    parser.add_argument("-c", action="store_true", help="清除所有已被添加到排除列表中的UWP应用。", default=False)
    parser.add_argument("-f", "--find", type=str, help="通过名字搜索UWP应用（忽略大小写）。")
    args = parser.parse_args()

    if args.l:
        print_list(apps_detail)
    elif args.s:
        os.system("CheckNetIsolation LoopbackExempt -s")
    elif args.find:
        match = []
        regex = re.compile(args.find, re.I)
        for app in apps_detail:
            result = regex.search(app[0])
            if result:
                match.append(app)
        if match:
            print_list(match)
            select = int(input("搜索到以上应用，回复序号添加指定应用到排除列表中："))
            os.system("CheckNetIsolation LoopbackExempt -a -n={}".format(apps_detail[select][2]))
        else:
            print("没有匹配到任何应用，请检查关键词后重试")
    else:
        print_list(apps_detail)
        select = int(input("回复序号并回车提交，添加指定应用到排除列表中："))
        os.system("CheckNetIsolation LoopbackExempt -a -n={}".format(apps_detail[select][2]))
