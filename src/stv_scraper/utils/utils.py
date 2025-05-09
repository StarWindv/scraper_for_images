# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)


from concurrent.futures import as_completed
from stv_scraper.utils.head import *


def create_save_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def decode_url(url):
    url = re.sub(r'%3A|%3a|%253a', ':', url)  # 替换 %3A 为 :
    url = re.sub(r'%2f|%2F|%252f', '/', url)  # 替换 %2F 为 /
    url = re.sub(r'%3d', '=', url)
    url = re.sub(r'%3f', '?', url)
    url = re.sub(r'%26|&amp;', "&", url)
    return url


def calculate_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return str(imagehash.phash(img))  # 返回图像的感知哈希值
    except Exception as e:
        pil_error = ['IOError', 'OSError', 'PIL.UnidentifiedImageError', 'UnidentifiedImageError']
        print(f"\n计算哈希时遇到错误：{e}")
        e = type(e).__name__
        if e in pil_error: # 咱也不知道为啥，但是在引入超时限制后会容易下载到不完整图片，比如一半绿色的、有彩色条纹的图片
            os.remove(image_path)
            print(f"已删除错误图片 {image_path}\n")
        return None


def process_image(image_path, image_hashes, deleted_count, lock):
    image_hash = calculate_image_hash(image_path)
    if image_hash:
        with lock:
            if image_hash in image_hashes:
                os.remove(image_path)
                print(f"删除重复图片: {os.path.basename(image_path)}")
                deleted_count[0] += 1
            else:
                image_hashes[image_hash] = image_path


def remove_duplicates(folder_path):
    if not os.path.exists(folder_path):
        print("文件夹不存在！")
        return
    image_hashes = {}
    deleted_count = [0]
    lock = threading.Lock() # 害怕误删，加了个锁
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for image_file in image_files:
            futures.append(executor.submit(process_image, image_file, image_hashes, deleted_count, lock))
        for future in as_completed(futures):
            future.result()
    print(f"共删除了 {deleted_count[0]} 张重复图片")


def rename_photos(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    photo_files = [f for f in files if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', 'bmp'])]
    count = 1
    for filename in photo_files:
        name, extension = os.path.splitext(filename)
        new_name = f"image_{count}{extension}"
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        os.rename(old_file, new_file)
        count += 1
    print(f"已成功重命名{count}张图片")