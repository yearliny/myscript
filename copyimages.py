import os
import shutil

TYPE_LIST = ('.png', '.jpeg', '.mp4', '.jpg', '.gif')
TOTAL_NUM = 0


# 使用递归的方法来拷贝文件
def copy_images(src, des):
    global TOTAL_NUM
    # 遍历目标文件夹
    for root, dirs, files in os.walk(src):
        for f in files:
            _, file_extension = os.path.splitext(src)
            if file_extension in TYPE_LIST:
                shutil.copy2(os.path.join(root, f), des)
                TOTAL_NUM += 1
                print("Current copy file num is:" + str(TOTAL_NUM))
        for d in dirs:
            return copy_images(os.path.join(root, d), des)


def main():
    print("start!")
    root = 'E:\\Photo\\Google Photos'
    copy_images(root, 'E:\\test')


if __name__ == '__main__':
    main()
