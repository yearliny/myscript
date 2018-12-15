# 介绍
这里存放我写的脚本或工具，用于帮助处理一些繁琐的任务。

## CheckNet
CheckNet 可以简单的把Win10系统中的UWP应用添加至隔离排除列表，以便使其应用系统代理。简单的说，Win10应用商店中的软件无法使用系统代理，此工具可以让某一软件使用系统代理。

更多使用详情可以参考我博客中写的[介绍](https://yuan.ga/enable-win10-uwp-use-system-proxy/)。

## Timg

> 以 TinyPNG 为基础的图片压缩处理命令行工具。

TinyPNG 是一个很好用的在线图片压缩工具，它相比起其他图片压缩工具来说，它的最大优点在于在不影响肉眼可见图片清晰度的情况下最大程度的压缩图片体积。

因为 TinyPNG 本身提供了良好的接口，所以开发此命令行程序很简单，Github 上也存在其他实现方式，但 Timg 的优点在于在命令行的使用上具有更良好的体验和功能。

### 使用环境

* Python3
* tinify

Timg 使用 [tinify](https://github.com/tinify/tinify-python) 模块作为 TinyPNG 的接口，所以在使用前需要安装此依赖，用 pip 可以轻松解决这个问题。

```bash
pip install --upgrade tinify
```

### 简单使用

```bash
# 查看程序帮助
python timg.py -h

# 压缩一个图片，直接替换源文件
python timg.py example.png
# 压缩一个图片，不覆盖源文件，创建为 optimized.png
python timg.py example.png -c optimized.png

# 压缩 Picture 目录下的图片，直接替换源文件
python timg.py Picture
# 压缩 Picture 目录下的图片，压缩完成后的图片放到 Optimized 文件夹中
python timg.py Picture -c Optimized
# 递归的压缩 Picture 目录下的图片（即包含子目录），压缩完成后的图片放到 Optimized 文件夹中
python timg.py -r Picture -c Optimized

# TinyPNG 接口每个月有 500 张图片的限制，我们可以使用[-f | --info] 参数查看使用量。
python timg.py -i
> 6 images you have made this month.
```

## copyimages
用于递归的将某目录下的图片、视频文件复制到另一个目录中（不保留原目录结构）。

此脚本使用场景较为小众，原先用于将Google Photo备份的照片拷贝到一个目录下，而不是分散出一堆以日期命名的子目录。
