# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)


from stv_scraper.utils.head import *
from stv_scraper.utils.utils import *


BLOCKED_DOMAINS = ["p3-pc-sign.douyinpic.com", "ts1.cn.mm.bing.net", "p9-pc-sign.douyinpic.com"]


def setup_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver


def replace_symbol(url, symbol):
    return url.replace(symbol, "")


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


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}


def download_image(url, save_path, timeless):
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=timeless)  # 设置超时时间为3秒
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"开始下载 {save_path}")
        else:
            print(f"\n图片\n{url}\n下载失败\n状态码: {response.status_code}", end='\n\n')
    except requests.exceptions.Timeout:
        print(f"下载 {url} 超时，跳过该图片", end='\n\n')
    except Exception as e:
        print(f"下载 {url} 时报错:\n\t{e}", end='\n\n')


def download_images_in_parallel(f1_links, save_directory, page_num, num_threads, timeless, plate):
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
                futures.append(executor.submit(download_image, f1_link, save_path, timeless))
                count += 1
                image_count += 1

                # 每下载50张图片进行一次垃圾回收
                if image_count % 50 == 0:
                    gc.collect()  # 手动触发垃圾回收

        for future in futures:
            future.result()


def download_page_images(page_num, keyword, save_directory, timeless, plate, lines):
    url = f"https://cn.bing.com/images/search?q={keyword}&form=QBIR&first={page_num+1}" # 无限制

    if plate == 2: # 横板
        url = f"https://cn.bing.com/images/search?q={keyword}&qft=+filterui:aspect-wide&form=QBIR&first={page_num+1}"
    elif plate == 1: # 竖版
        url = f"https://cn.bing.com/images/search?q={keyword}&qft=+filterui:aspect-tall&form=QBIR&first={page_num+1}"
    elif plate == 3: # 方形
        url = f"https://cn.bing.com/images/search?q={keyword}&qft=+filterui:aspect-square&form=QBIR&first={page_num+1}"

    driver = setup_driver()
    f1_links = get_f1_links(driver, url)
    print(f"找到 {len(f1_links)} 个 F1 链接")

    download_images_in_parallel(f1_links, save_directory, page_num+1, lines, timeless, plate)

    driver.quit()
