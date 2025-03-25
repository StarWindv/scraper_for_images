def parse_text():
    from stv_utils import is_ch
    if is_ch():
        key_world_help = '想要下载的图片的简要描述'
        page_help = '想要下载的页数'
        remove_help = "是否去除可能重复的图片？"
        window_help = '最大窗口数量'
        lines_help = "这里填入你想使用的线程数"
        time_less_help = "这里填入限制超时时间"
        plate_help = "竖屏=1，横屏=2，正方形=3，无限制就空着"
        license_help = '输出本项目所用的许可证'
    else:
        key_world_help = 'Brief description of the images to downloadBrief description of the images to download'
        page_help = 'Number of pages to download'
        remove_help = "Whether to remove potentially duplicate images?"
        window_help = 'Maximum number of windows'
        lines_help = "Number of threads to use"
        time_less_help = "Timeout limit in seconds"
        plate_help = "Portrait=1, Landscape=2, Square=3, no restriction if left blank"
        license_help = 'Output the licenses used'

    help_text = [key_world_help, page_help, remove_help, window_help, lines_help, time_less_help, plate_help, license_help]
    return help_text


def main_text():
    from stv_utils import is_ch
    if is_ch():
        license_text = "本项目遵循MIT许可证"
        start_download1 = "开始下载第"
        start_download2 = "页图片\n\n"
        ensure_exit = "确定要退出吗？[y/n]\n\t"
        ensure_remove = "是否进行去重？[y/n]\n\t"
        self_remove = "下载结束，请自行去重\n"
    else:
        license_text = "This project is licensed under the MIT License"
        start_download1 = "Starting download of page "
        start_download2 = " images\n\n"
        ensure_exit = "Are you sure you want to exit? [y/n]\n\t"
        ensure_remove = "Perform deduplication? [y/n]\n\t"
        self_remove = "Download completed. Please remove duplicates manually.\n"

    main_text_list = [
        license_text, start_download1, start_download2,
        ensure_exit, ensure_remove, self_remove
    ]

    return main_text_list