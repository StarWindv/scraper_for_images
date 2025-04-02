# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)


import os.path
from stv_scraper.core.stv_parse import *
from stv_scraper.core.WebProcessor import *
from stv_scraper.utils.utils import *
from stv_scraper.utils.change_text import main_text
from stv_scraper.utils.head import *
import warnings


warnings.filterwarnings("ignore", message="Corrupt EXIF data.*")
BLOCKED_DOMAINS = ["p3-pc-sign.douyinpic.com", "ts1.cn.mm.bing.net", "p9-pc-sign.douyinpic.com"]
"""# 目标阻止的域名，总是因为奇奇怪怪的原因而无法下载某些域名下的图片，比如抖音图床，索性直接ban了"""

global lines
def main():
    args = stv_parse()
    text = main_text()

    __version__ = "\n\033[96m0.0.0+Dev.Bing.GoogleChrome\033[0m\n"

    if args.license:
        try:
            from stv_scraper.utils.lic import return_license
            content = return_license()
            print(f"\n\n{content}\n")
        except Exception as e:
            print(f"\033[96m{text[0]}\033[0m")
        return

    if args.version:
        print(__version__)
        return

    keyword = args.keyword if args.keyword else get_user_input("keyword", "请输入关键词:\n\t")
    first_page = args.page if args.page else get_user_input("page", "\n请输入下载的页数:\n\t ")
    remove = args.remove if args.remove else "True"
    window = args.window if args.window else 2
    timeless = args.time if args.time else 4
    plate = args.plate if args.plate else 0
    global lines
    lines = args.lines if args.lines else 16

    father_path = args.path if args.path else None
    son_path = f"Download_Images/{keyword}_images"
    if father_path is None:
        save_directory = son_path
    else:
        save_directory = os.path.join(father_path, son_path)

    create_save_dir(save_directory)
    first_page = int(first_page)
    try:
        with ThreadPoolExecutor(max_workers=window) as executor:  # 默认2个页面
            futures = []
            for i in range(first_page):
                print(f"{text[1]}{i+1}{text[2]}", end='')
                # 提交异步
                lines = 16 if lines <= 0 else lines
                futures.append(executor.submit(download_page_images, i, keyword, save_directory, timeless, plate, lines))

            for future in futures:
                future.result()
                gc.collect()
    except KeyboardInterrupt:
        """注意，这里并不能真正捕获ctrl+c中断，也就是在多线程下载时不能中断，只能暂停去重阶段"""
        gc.collect()
        if input(f"{text[3]}").lower() == 'y':
            if save_directory is None:
                if input(f"{text[4]}").lower() == 'y':
                    remove_duplicates(save_directory)
                    rename_photos(save_directory)
            sys.exit(0)
    gc.collect()
    if remove == "True":
        # 执行去重操作
        remove_duplicates(save_directory)
        rename_photos(save_directory)
    else:
        print(f"{text[5]}")


if __name__ == "__main__":
    main()
