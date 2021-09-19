# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
import requests
from time import time

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 ⌘F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

    s = time()

    _timeout = 25
    url = 'https://twitter.com'
    _session = requests.Session()
    req = _session.prepare_request(requests.Request('GET', url))
    r = _session.send(req, allow_redirects=True, timeout=_timeout)

    run_time = time() - s
    print(f'Status Code : {r.status_code}')
    print(f'Request Took {run_time} ms')
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
