import argparse

def get_user_input(param_name, prompt):
    value = input(f"{prompt}")
    return value if value else None

def stv_parse():
    parser = argparse.ArgumentParser(description="\n=========================Options=========================")

    parser.add_argument('-k', '--keyword', type=str, help="想要下载的图片的简要描述")
    parser.add_argument('-p', '--page', type=int, help="想要下载的页数")
    parser.add_argument('-r', '--remove', choices=['True', 'False'], help="是否去除可能重复的图片？", default="True")
    parser.add_argument('-w', '--window', type=int, help="最大窗口数量")
    parser.add_argument('-l', '--lines', type=int, help="这里填入你想使用的线程数")
    parser.add_argument('-t', '--time', type=int, help="这里填入限制超时时间")
    parser.add_argument('-pl', '--plate', type=int, help="横屏=2，竖屏=1，正方形=3，无限制就空着")

    args = parser.parse_args()

    return args