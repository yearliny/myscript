import os
import shutil


TYPE_LIST = ('.png', '.jpeg', '.mp4', '.jpg', '.gif')
TOTAL_NUM = 0

# 使用递归的方法来拷贝文件
def copy_images(src, des):
    global TOTAL_NUM
    # 遍历目标文件夹
    for root, dirs, files in os.walk(src):
        for name in files:
            # 如果目标路径为文件，则进一步判断目标文件格式
            file_path = os.path.join(root, name)
            if os.path.isfile(file_path):
                if os.path.splitext(file_path)[1] in TYPE_LIST:
                    shutil.copy2(file_path, des)
                    TOTAL_NUM += 1
                    print("Current copy file num is:" + str(TOTAL_NUM))
            elif os.path.isdir(file_path):
                return copy_images(file_path, des)


def get_images(src, des):
    filename_set = set()
    for root, dirs, files in os.walk(src):
        for name in files:
            filepath = os.path.join(root, name)
            if os.path.splitext(filepath)[1] in TYPE_LIST:
                filename = os.path.split(filepath)[1]
                
                if filename not in filename_set:
                    shutil.copy2(filepath, des)
                    filename_set.add(filename)
                    print("{0} ---> {1}".format(filepath, des))


def main():
    print("start!")
    root = 'E:\\Photo\\Google Photos'
    copy_images(root, 'E:\\test')


if __name__ == '__main__':
    main()
