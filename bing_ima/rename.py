import os

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
        new_name = f"{count}{extension}"

        # 获取旧文件的完整路径和新文件的完整路径
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(old_file, new_file)
        count += 1
    print(f"已成功重命名{count}张图片")

if __name__ == "__main__":
    folder_path = input("enter your path")  # 这里填入你的照片文件夹路径
    rename_photos(folder_path)
