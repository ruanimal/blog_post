title: 在 Linux 虚拟机中使用 PyAutoGUI 做自动化
date: 2025-05-27 9:48 PM
categories: 编程
tags: [Python, ]

---

PyAutoGUI 是 GUI 功能强大自动化方案，但 UI 程序的运行环境选择与配置也是一大难题。
<!--more-->

## 系统选择

为了让环境可迁移，免维护，资源消耗少，必须使用虚拟化的方案。
虽然 PyAutoGUI 支持 Windows/macOS/Linux 三个平台。但是各有各的弊端。
- Windows 的系统臃肿且开发环境不友好
- macOS 的权限管理过于严格且虚拟化难度大，高dpi的屏幕也不适合自动化
- Linux 就是最好的选择了，但执行的应用可能不支持 Linux，必须引入 Wine 

综合以上情况考虑，系统环境选择如下
- pve: 宿主机系统，也可以选择别的环境
- debian: 客户机系统，目前是 debian 12, 方便使用 deepin 的 wine 程序
- mate: 桌面环境，比较轻量，实测兼容性比 xfce 好
- [星火应用商店](https://gitee.com/spark-store-project/spark-store): 方便安装各种国内软件和 Wine 程序
- 统信 Windows 应用兼容引擎: 在星火应用商店中安装，可以用于安装和打包商店中没有的程序

## 虚拟机配置
步骤
1. 创建好 pve 虚拟机， 安装 debian，选择 mate 桌面
2. 设置分辨率：控制中心 -> 显示器 -> 设置为 1920x1080
3. 关闭自动睡眠：控制中心 -> 电源管理 -> 动作和显示修改为`从不`
4. 关闭屏幕保护：控制中心 -> 屏幕保护程序 -> 取消勾选所有选项
5. 安装`gnome-screenshot`:  用于 PyAutoGUI 内部调用截图
6. 安装星火应用商店（可选）
7. 安装统信 Windows 应用兼容引擎（可选）：在星火应用商店中安装
8. 火焰截图（可选）：在星火应用商店中安装，更方便对应用的按钮和文字截图。

其他说明：
- 如果不关闭自动睡眠和屏幕保护，PyAutoGUI 就无法截取到应用的图像，也就无法操作了。
- 图形显示协议默认选 x11，wayland 对显卡有要求，虚拟机不方便处理。

### 睡眠后时间不对
虚拟机睡眠唤醒后时间没有更新，不知道为什么没有触发时间更新。
目前只能通过强行同步来解决

在脚本里执行同步命令
```
# 和阿里云ntp服务器同步
sudo ntpdig -S ntp.aliyun.com
```

或者，理论上可以通过虚拟机中的 systemd-suspend hook，或者 pve hookscript 来解决（没试成功）

## PyAutoGUI 使用技巧
### 远程登录调试
pve 默认图片控制台不太方便，不能复制粘贴，所以使用远程登录调试
由于系统使用 x11 环境，这里使用 xrdp 作为远程服务端。
如果以后更新到 wayland，可以使用 `gnome-remote-desktop`。
```
sudo apt update
sudo apt install xorgxrdp xrdp
```

### 远程登录时找不到显示器
xrdp 或者 ssh 远程登录执行脚本时，窗口相关命令可能会提示找不到显示器。
可以在自动化脚本中设置以下环境变量
```
os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY'] = '/home/<your-name>/.Xauthority'
```

### 过滤没必要的截图日志
gnome-screenshot 截图时会产生一些无用日志
```
** Message: 17:36:31.888: Unable to use GNOME Shell's 
builtin screenshot interface, resorting to fallback X11.
```

新建一个 `gnome-screenshot` 文件，赋予执行权限，放到 PATH 环境变量中比 `/usr/bin` 靠前的路径
```
#!/bin/bash
exec /usr/bin/gnome-screenshot "$@" >> /tmp/gnome-screenshot.log 2>&1
```

### 验证码识别

#### pytesseract
常见的方案是 `pytesseract`， 但是效果不好，识别率比较一般。

安装
```
sudo apt install tesseract-ocr
pip install pytesseract
```

使用
```python
pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789')
```

#### ddddocr

[ddddocr](https://github.com/sml2h3/ddddocr) 是基于机器学习的验证码识别库，识别效果比较好。

这里使用 docker 安装 [fastapi接口](https://github.com/sml2h3/ddddocr-fastapi)
```
docker run -d -p 8000:8000 oozzbb/ddddocr-fastapi:latest
```

使用
```python
def ocr_image(file='region.png'):
    url = 'http://your-address:8000/ocr'
    with open(file, 'rb') as fp:
        files = {
            'file': fp,
        }
    data = {
        'probability': 'false',
        'png_fix': 'false',
        'charsets': '0123456789'  # 验证码可能的字符列表
    }
    response = requests.post(url, files=files, data=data)
    assert response.ok
    return response.json()['data']
```

### 高效执行自动化脚本

可以在宿主机远程调用自动化脚本，并且脚本执行完成后挂起虚拟机
```bash
HOST=your-name@vm-ip-address
VMID=109   # pve 虚拟机id

qm resume $VMID   # 唤醒虚拟机
sleep 2

ssh $HOST "SOME_VAR=foobar python your-script.py"  # 执行脚本
sleep 1

qm suspend $VMID   # 关闭虚拟机
```

### 其他有用的函数
```python
# 切换窗口到前台
def wm_to_front(title: str):
    if sys.platform == 'linux':
        return subprocess.check_call(['wmctrl', '-a', title])
    raise NotImplementedError

# 点击或者移到到图片位置
def click_image(image, confidence=0.9, grayscale=True, delay=1.5, 
        duration=0.6, offset=(1, 0), abort=True, click=True):
    try:
        loc = pyautogui.locateOnScreen(image, confidence=confidence, grayscale=grayscale)
    except pyautogui.ImageNotFoundException:
        loc = None
    if loc:
        x, y = pyautogui.center(loc)
        if click:
            pyautogui.click(x+offset[0], y+offset[1], duration=duration)
        else:
            pyautogui.moveTo(x+offset[0], y+offset[1], duration=duration)
        time.sleep(delay)
        return loc
    else:
        if abort:
            raise RuntimeError(f"can not find {image}!")
        else:
            return None

# 等待某个图片出现
def wait_button(image, timeout, interval=10):
    for _ in range(timeout//interval):
        time.sleep(interval)
        loc = click_image(image, abort=False)
        if loc:
            break
    else:
        raise RuntimeError(f'wait {image} failed')
    time.sleep(interval/2)
```

## 使用感受
PyAutoGUI 是基于图像而不是图型控件来识别目标，没有确认反馈。
相比于网页自动化的 Selenium 就感觉落后些了。
当然，Windows 平台有 `pywinauto` 支持控件识别，但我不咋熟悉。
总之，PyAutoGUI 就像手枪，虽然比较简陋，但还是很直观的，执行简单的任务也够用了。


## 注意事项

- 自动化代码中不要编码用户名密码相关信息，建议用环境变量传入
- 不要轻易调整系统的 dpi(建议设为1.0) 和分辨率，可能导致图片无法识别
- xfce 对 wine 应用的兼容性似乎不好，wine 文件保存对话框被可能被反复触发，原因不明。