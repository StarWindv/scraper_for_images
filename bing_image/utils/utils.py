# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)

import os
import imagehash
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import re


def create_save_dir(directory):
    # os.path.join('Download_Images', directory)
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
        print(f"\n计算哈希时遇到错误：{e}") # 更详细的错误名称
        e = type(e).__name__
        # print(f"\n计算哈希时遇到错误：{e}") ## 错误类别
        if e in pil_error:
            os.remove(image_path)
            print(f"已删除错误图片 {image_path}\n")
        return None

def process_image(image_path, image_hashes, deleted_count, lock):
    # 计算图片的哈希值
    image_hash = calculate_image_hash(image_path)
    if image_hash:
        with lock:  # 使用锁来确保对 image_hashes 的线程安全访问
            if image_hash in image_hashes:
                os.remove(image_path)  # 删除重复图片
                print(f"删除重复图片: {os.path.basename(image_path)}")
                deleted_count[0] += 1
            else:
                image_hashes[image_hash] = image_path

def remove_duplicates(folder_path):
    if not os.path.exists(folder_path):
        print("文件夹不存在！")
        return

    image_hashes = {}  # 存储已处理的图片的哈希值
    deleted_count = [0]  # 使用列表来存储删除计数，以便在多个线程中共享数据
    lock = threading.Lock()  # 创建一个锁来保证线程安全

    # 获取文件夹中的所有图片文件
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]

    # 创建一个线程池，设置最大线程数为 10
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for image_file in image_files:
            futures.append(executor.submit(process_image, image_file, image_hashes, deleted_count, lock))

        # 等待所有线程完成
        for future in as_completed(futures):
            future.result()  # 确保所有任务完成

    print(f"共删除了 {deleted_count[0]} 张重复图片")

def rename_photos(folder_path):
    # 获取文件夹中的所有文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 过滤出图片文件（你可以根据需要调整图片文件的扩展名）
    photo_files = [f for f in files if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', 'bmp'])]

    count = 1
    for filename in photo_files:
        # 分离文件名和扩展名
        name, extension = os.path.splitext(filename)

        # 构造新文件名
        new_name = f"image_{count}{extension}"

        # 获取旧文件的完整路径和新文件的完整路径
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(old_file, new_file)
        count += 1
    print(f"已成功重命名{count}张图片")
