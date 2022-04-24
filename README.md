# 介绍
这里存放我写的脚本或工具，用于帮助处理一些繁琐的任务。

## CheckNet
CheckNet 可以简单的把Win10系统中的UWP应用添加至隔离排除列表，以便使其应用系统代理。简单的说，Win10应用商店中的软件无法使用系统代理，此工具可以让某一软件使用系统代理。

更多使用详情可以参考我博客中写的[介绍](https://yuan.ga/enable-win10-uwp-use-system-proxy/)。

### PowerShell Version

对于这个任务，实际上用 PowerShell 脚本处理会更为恰当一点，我们可以用更少的代码处理同样的任务。
```powershell
$BASE_PATH = 'HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Mappings\'
# 获取相关注册表信息，并进行筛选和排序
$mapping = Get-ChildItem -Pat $BASE_PATH | Where-Object {$_.GetValue('DisplayName') -NotLike '@{*'} | Sort-Object {$_.GetValue('DisplayName')}
# 格式化打印 APP List
$mapping | Format-Table @{label='Num'; expression={$mapping.IndexOf($_)}}, @{label='DisplayName'; expression={$_.GetValue('DisplayName')}}
$input = Read-Host '回复序号并回车提交，添加指定应用到排除列表中'
CheckNetIsolation LoopbackExempt -a -n=$mapping[$input].GetValue('Moniker')
```
了解 PowerShell 的人可以使用上面的代码实现同样的任务，核心代码就两行，非常简洁。

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
使用 Timg 需要 TinyPNG 的 API key，你可以使用自己的邮箱免费注册一个，也可以使用程序中自带的 key 试用。修改 key 的方法就是修改程序中 `tinify.key` 的值。
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
[自用脚本]用于递归的将某目录下的图片、视频文件复制到另一个目录中（不保留原目录结构）。

此脚本仅为自用，原先用于将 Google Photo 备份的照片拷贝到一个目录下，而不是分散出一堆以日期命名的子目录。

## get_git_log
查询近一周项目管理路径下的所有项目 git log，并将其格式化打印，输入 C 回车即可复制。使用效果如下：
```text
# 学习空间项目
1. 学习了 Python 的 3.10 的新语法
2. 学习了Python的网络编程

Press C to copy to the clipboard, Press Any Key to continue...
```
