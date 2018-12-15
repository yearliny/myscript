# -*- coding:utf-8 -*-
import os
import logging
import argparse
import tinify

__version_info__ = ('2018','12','14')
__version__ = '-'.join(__version_info__)

tinify.key = "We4LQK1PKcdzUbC-9Vt2ANGuLXdaF-qu"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Timg')

# 是否是支持的文件
def is_support_file(file):
    _, file_extension = os.path.splitext(os.path.basename(file))
    return True if file_extension in ['.jpg', 'png'] else False

def compress_img(target_img, optimized_img):
    source = tinify.from_file(target_img)
    logger.debug("Successfully compressed image {}".format(os.path.basename(target_img)))
    source.to_file(optimized_img)
    logger.info("Save compressed image {}".format(os.path.basename(target_img)))

def compress_img_dir(target_path, optimized_path, recursion):
    for root, dirs, files in os.walk(target_path):
        for f in [file for file in files if is_support_file(file)]:
            if not os.path.exists(optimized_path):
                logger.debug("{0} not exists, Create dir {0}".format(optimized_path))
                os.mkdir(optimized_path)
            compress_img(os.path.join(root, f), os.path.join(optimized_path, f))
        if recursion:
            for d in dirs:
                return compress_img_dir(os.path.join(root, d), os.path.join(optimized_path, d), recursion)

def compress_target(target, new_one=None, recursion=False):
    # 如果没有参数 new_one，就让其等同于 target，即覆盖源文件
    new_one = new_one if new_one else target
    if is_support_file(target):
        compress_img(target, new_one)
    elif os.path.isdir(target):
        compress_img_dir(target, new_one, recursion)
    else:
        raise argparse.ArgumentTypeError("Only supports png and jpg images")

def compression_count():
    tinify.validate()
    compressions_this_month = tinify.compression_count
    # print("{} images you have made this month.".format(compressions_this_month))
    logger.info("{} images you have made this month.".format(compressions_this_month))

def command_line():
    parser = argparse.ArgumentParser(prog='Timg', description='以 TinyPNG 为基础的图片压缩处理命令行工具。')
    parser.add_argument('target', metavar='IMG OR DIR', nargs='?', type=str, help='你要处理的图片，可以是目录')
    parser.add_argument('-c', '--create', metavar='NEW_ONE', type=str, help='创建为新文件，否则直接替换原文件')
    parser.add_argument('-r', '--recursion', action='store_true', help='递归的遍历目录下的所有路径，默认不遍历子目录')
    parser.add_argument('-d', '--debug', action='store_true', help='设置日志等级为 Debug，获得程序调试信息')
    parser.add_argument('-i', '--info', action='store_true', help='打印 API 当月的使用量')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if args.info:
        compression_count()
    if args.target:
        compress_target(args.target, args.create, args.recursion)

def main():
    try:
        command_line()
    except argparse.ArgumentTypeError as err:
        logger.error(err)
    except KeyboardInterrupt:
        logger.info("Bye~")

if __name__ == "__main__":
    main()