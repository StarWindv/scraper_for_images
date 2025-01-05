# MIT License
# Copyright (c) 2024 StarWindv

from head import *
import warnings

warnings.filterwarnings("ignore", message="Corrupt EXIF data.*")
BLOCKED_DOMAINS = ["p3-pc-sign.douyinpic.com", "ts1.cn.mm.bing.net", "p9-pc-sign.douyinpic.com"]


def get_user_input(param_name, prompt):
    value = input(f"{prompt}")
    return value if value else None


# 设置 Chrome WebDriver
def setup_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver


def get_f1_links(driver, url):
    driver.get(url)
    for _ in range(130):
        print(f"正在进行第{_}次翻页\n")
        body = driver.find_element("tag name", "body")
        body.send_keys(Keys.PAGE_DOWN)
    if os.name =='nt':
        os.system("cls")
    else:
        os.system("clear")
    time.sleep(3)
    page_source = driver.page_source  # 获取页面源码

    # 提取所有符合条件的 href 链接
    f1_links = re.findall(r'href="(/images/search\?view=detailV2&amp;ccid[^"]+)"', page_source)
    f1_links = [replace_symbol(link, "amp;") for link in f1_links]
    
    f1_links = [link for link in f1_links if not any(domain in link for domain in BLOCKED_DOMAINS)]

    driver.close()
    return f1_links


def replace_symbol(url, symbol):
    return url.replace(symbol, "")


# 解码
def decode_url(url):
    url = re.sub(r'%3A|%3a|%253a', ':', url)  # 替换 %3A 为 :
    url = re.sub(r'%2f|%2F|%252f', '/', url)  # 替换 %2F 为 /
    url = re.sub(r'%3d', '=', url)
    url = re.sub(r'%3f', '?', url)
    url = re.sub(r'%26|&amp;', "&", url)
    return url


# 自定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}



def download_image(url, save_path):
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"开始下载 {save_path}")
        else:
            print(f"\n图片\n{url}\n下载失败\n状态码: {response.status_code}", end='\n\n')
    except Exception as e:
        print(f"下载 {url} 时报错:\n\t{e}", end='\n\n')


def create_save_dir(directory):
    # os.path.join('Download_Images', directory)
    if not os.path.exists(directory):
        os.makedirs(directory)


# 多线程下载图片的函数
def download_images_in_parallel(f1_links, save_directory, page_num, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        count = 1
        image_count = 0  # 用于记录下载的图片数量
        for f1_link in f1_links:
            match = re.search(r'&mediaurl=([^&]+(?:\.png|\.jpg|\.jpeg|\.gif|\.bmp))', f1_link)
            
            if match:
                f1_link = match.group(1)
                f1_link = decode_url(f1_link)
                save_path = os.path.join(save_directory, f"image_{page_num}_{count}.jpg")
                futures.append(executor.submit(download_image, f1_link, save_path))
                count += 1
                image_count += 1

                # 每下载50张图片进行一次垃圾回收
                if image_count % 50 == 0:
                    gc.collect()  # 手动触发垃圾回收

        for future in futures:
            future.result()


def download_page_images(page_num, keyword, save_directory):
    url = f"https://cn.bing.com/images/search?q={keyword}&form=QBIR&first={page_num+1}"

    driver = setup_driver()
    f1_links = get_f1_links(driver, url)
    print(f"找到 {len(f1_links)} 个 F1 链接")

    download_images_in_parallel(f1_links, save_directory, page_num+1, lines)

    driver.quit()


def main():
    save_directory = None
    print("\033[1m\033[31m使用本脚本时，一切后果由使用者自行承担\033[0m\n") 
    # print("请时刻注意RAM占用，当页数>=8时，容易出现No space left on device\033[0m\n")
    try:
        parser = argparse.ArgumentParser(description="这是一个命令行参数解析示例")

        parser.add_argument('--keyword', type=str, help="想要下载的图片的简要描述")
        parser.add_argument('--page', type=int, help="想要下载的页数")
        parser.add_argument('--remove', choices=['True', 'False'], help="是否去除可能重复的图片？", default="True")
        parser.add_argument('--window', type=int, help="最大窗口数量")
        parser.add_argument('--lines', type=int, help="这里填入你想使用的线程数")
        
        args = parser.parse_args()

        keyword = args.keyword if args.keyword else get_user_input("keyword", "请输入关键词:\n\t")
        first_page = args.page if args.page else get_user_input("page", "\n请输入下载的页数:\n\t ")
        remove = args.remove if args.remove else "True" 
        window = args.window if args.window else 2
        global lines
        lines = args.lines if args.lines else 16
        # 创建保存图片的目录
        save_directory = f"Download_Images\\{keyword}_images"
        create_save_dir(save_directory)
        first_page = int(first_page)

        # 并行启动多页面
        with ThreadPoolExecutor(max_workers=window) as executor:  # 默认2个页面
            futures = []
            for i in range(first_page):
                print(f"开始下载第{i+1}页图片", end='\n\n')
                # 提交异步
                futures.append(executor.submit(download_page_images, i, keyword, save_directory))

            # 等待所有任务完成
            for future in futures:
                future.result()
                gc.collect()

    except KeyboardInterrupt:
        gc.collect()
        if input("确定要退出吗？[y/Y]\n\t").lower() == 'y':
            if save_directory != None:
                if input("是否进行去重？[y/Y]\n\t").lower() == 'y':
                    remove_duplicates(save_directory)
                    rename_photos(save_directory)
            sys.exit(0)
        else:
            pass
        
    gc.collect()
    if remove == "True":
        # 执行去重操作
        remove_duplicates(save_directory)
        rename_photos(save_directory)
    else:
        print("下载结束，请自行去重\n")


# 执行主函数
if __name__ == "__main__":
    main()  # 启动主函数
