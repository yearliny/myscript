import os
import subprocess
from datetime import datetime, timedelta

PROJECTS_ROOT_LIST: [str] = [r"C:\Users\yearliny\IdeaProjects", r"C:\Users\yearliny\WebstormProjects"]
# 过滤 git 用户，如果想查询多个用户，需要用正则表达式匹配，如 \(Tom\)\|\(Jerry\)
GIT_AUTHOR: str = r"yearliny"

# 项目名称映射，格式为 project_name to project_display_name
PROJECT_NAME_MAP = {
    'study_space': '学习项目',
}


def get_git_log_map() -> dict[str, set[str]]:
    """
    遍历项目目录下的所有路径，找出含有 .git 的项目路径，并查询 git
    :return: 返回 (项目名 to 更新日志) 格式的更新日志
    """

    last_week_datetime: datetime = datetime.now() - timedelta(7)

    git_log_map: dict[str, set[str]] = {}
    # 遍历项目文件夹列表
    for projects_root in PROJECTS_ROOT_LIST:
        # 遍历项目文件夹中的项目
        for project_dir in os.listdir(projects_root):
            git_dir = os.path.join(projects_root, project_dir, ".git")
            # 如果没有 .git 目录则跳过
            if not os.path.exists(git_dir):
                continue

            # 跳过近一周没有修改的项目，以提高程序运行速度
            path_getmtime = os.path.getmtime(git_dir)
            if path_getmtime < last_week_datetime.timestamp():
                continue

            # 存在则查询 git log 记录
            git_log_command = ["git", "--no-pager", "log", "--author", GIT_AUTHOR, "--since=1.weeks",
                               "--pretty=format:%s"]
            work_dir = os.path.join(projects_root, project_dir)
            completed_process = subprocess.run(git_log_command, capture_output=True, cwd=work_dir)
            result_str = completed_process.stdout.decode('utf-8')

            # 如果不存在 git 更新日志，则跳过
            if not result_str:
                continue

            # 拼接成集合，加入到 git_log_map 中
            result_set = {item for item in result_str.split('\n') if not item.startswith("Merge")}
            git_log_map[project_dir] = result_set
    return git_log_map


def join_output_str() -> str:
    """
    查询所有项目日志，并按照项目更新量倒序打印
    """
    log_map = get_git_log_map()
    join_str = ""
    for project_name, git_log in sorted(log_map.items(), key=lambda item: len(item[1]), reverse=True):
        project_cn = PROJECT_NAME_MAP.get(project_name, project_name)
        join_str += f"# {project_cn}\n"

        index_list = range(1, len(git_log) + 1)
        git_log_with_index = ["{}.{}".format(i, g) for i, g in zip(index_list, git_log)]
        join_str += "\n".join(git_log_with_index)
        join_str += "\n\n"
    return join_str


if __name__ == '__main__':
    output_str = join_output_str()
    print(output_str)
    user_input = input("Press C to copy to the clipboard, Press Any Key to continue...\n")
    if user_input.lower() == 'c':
        ps_command = f"Set-Clipboard -Value '{output_str}'"
        res = subprocess.run(["powershell.exe", "-Command", ps_command])
