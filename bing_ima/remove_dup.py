# MIT License
# Copyright (c) 2024 StarWindv

import os
import imagehash
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

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

if __name__ == '__main__':
    folder_path = input('请输入你的文件夹路径:\n\t')
    remove_duplicates(folder_path)
