# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)

from core.stv_parse import *
import utils.head
import warnings
from utils.utils import *
from core.WebProcessor import *
import sys

warnings.filterwarnings("ignore", message="Corrupt EXIF data.*")
# BLOCKED_DOMAINS = ["p3-pc-sign.douyinpic.com", "ts1.cn.mm.bing.net", "p9-pc-sign.douyinpic.com"]

global lines
def main():
    args = stv_parse()
    if args.license:
        license_path = "../LICENSE"
        with open(path, 'r', encoding='utf-8') as l:
            content = l.read()
        print(content)
        return
    keyword = args.keyword if args.keyword else get_user_input("keyword", "请输入关键词:\n\t")
    first_page = args.page if args.page else get_user_input("page", "\n请输入下载的页数:\n\t ")
    remove = args.remove if args.remove else "True"
    window = args.window if args.window else 2
    timeless = args.time if args.time else 4
    plate = args.plate if args.plate else 0
    global lines
    lines = args.lines if args.lines else 16

    save_directory = f"Download_Images\\{keyword}_images"
    create_save_dir(save_directory)
    first_page = int(first_page)
    try:
        with ThreadPoolExecutor(max_workers=window) as executor:  # 默认2个页面
            futures = []
            for i in range(first_page):
                print(f"开始下载第{i+1}页图片", end='\n\n')
                # 提交异步
                lines = 16 if lines <= 0 else lines
                futures.append(executor.submit(download_page_images, i, keyword, save_directory, timeless, plate, lines))

            # 等待所有任务完成
            for future in futures:
                future.result()
                gc.collect()
    except KeyboardInterrupt:
        gc.collect()
        if input("确定要退出吗？[y/n]\n\t").lower() == 'y':
            if save_directory is None:
                if input("是否进行去重？[y/Y]\n\t").lower() == 'y':
                    remove_duplicates(save_directory)
                    rename_photos(save_directory)
            sys.exit(0)

    gc.collect()
    if remove == "True":
        # 执行去重操作
        remove_duplicates(save_directory)
        rename_photos(save_directory)
    else:
        print("下载结束，请自行去重\n")

if __name__ == "__main__":
    main()
