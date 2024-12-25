import os
import imagehash
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def calculate_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return str(imagehash.phash(img))  # 返回图像的感知哈希值
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def process_image(image_path, image_hashes, deleted_count):
    # 计算图片的哈希值
    image_hash = calculate_image_hash(image_path)
    if image_hash:
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

    # 获取文件夹中的所有图片文件
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]

    # 创建一个线程池，设置最大线程数为 10
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for image_file in image_files:
            futures.append(executor.submit(process_image, image_file, image_hashes, deleted_count))
        
        # 等待所有线程完成
        for future in as_completed(futures):
            future.result()  # 确保所有任务完成

    print(f"共删除了 {deleted_count[0]} 张重复图片")

if __name__ == '__main__':
    folder_path = input('请输入你的文件夹路径:\n\t')
    remove_duplicates(folder_path)
