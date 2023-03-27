import datetime
import random
import threading
import time
import tkinter as tk

import pyautogui
import win32api
import win32con
import win32gui

window_region = (0, 0, 800, 600)
list_window_region = []


def getallwindowregion():
    global list_window_region

    windows = pyautogui.getAllWindows()
    i = 0
    windowsList = list(filter(lambda x: x.title.startswith("雷电模拟器"), windows))

    def splitFun(title):
        s = title.split("-", 2)
        return int(s[1]) if len(s) > 1 else 0

    windowsList.sort(key=lambda x: splitFun(x.title))
    for item in windowsList:
        item.activate()
        # print(item)
        list_window_region.append((item.left, item.top, item.width, item.height, item))


# 获取梦幻西游窗口信息吗，返回一个矩形窗口四个坐标
def get_window_info():
    global handle
    windows = pyautogui.getAllWindows()
    # wdname = u'梦幻西游 - MuMu模拟器'
    wdname = "雷电模拟器"
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄

    if handle == 0:
        # text.insert('end', '提示：请打开梦幻西游\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)


def move_click(x, y, t=0):  # 移动鼠标并点击左键
    win32api.SetCursorPos((x, y))  # 设置鼠标位置(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # 点击鼠标左键
    if t == 0:
        time.sleep(random.random() * 2 + 1)  # sleep一下
    else:
        time.sleep(t)
    return 0


# 找指定任务
def findpng(Pngfile, windows):
    global list_window_region
    myConfidence = 0.8
    pyautogui.FAILSAFE = False
    result = pyautogui.locateOnScreen('images\\' + Pngfile, region=list_window_region[windows], confidence=myConfidence)
    # print("findpng=",Pngfile,"window=",windows, "result=",result)
    return result


def findpng_2(Pngfile, windows, myConfidence):
    global list_window_region
    pyautogui.FAILSAFE = False
    result = pyautogui.locateOnScreen('images\\' + Pngfile, region=list_window_region[windows], confidence=myConfidence)
    # print("findpng_2=",Pngfile,"window=",windows, "result=",result)
    return result


# 单击指定位置
def click(x, y):
    pyautogui.click(x=x, y=y)
    # move_click(x, y, 0.1)
    pyautogui.FAILSAFE = False
    # pyautogui.moveTo(x=window_size[0] + 10, y=window_size[1] + 10, duration=0.1)  # 鼠标移至窗口左上角


# 打开队伍
def openTeam():
    pyautogui.hotkey("alt", "t")  # 鼠标移至窗口左上角


# 接任务
def get_rw(rwm, windows):
    pos = findpng(rwm + ".png", windows)
    print(windows, rwm, pos)
    if pos is not None:
        x = pos[0] + pos[2] - 6
        y = pos[1] + pos[3] - 6
        click(x, y)
        time.sleep(0.5)
        return True
    else:
        return False


def get_rw_2(rwm, windows, myConfidence):
    pos = findpng_2(rwm + ".png", windows, myConfidence)
    print(windows, rwm, pos)
    if pos is not None:
        click(pos[0] + pos[2] - 6, pos[1] + pos[3] - 6)
        time.sleep(0.5)
        return True
    else:
        return False


# 等待直到打开活动界面
def open_huodong(windows):
    global is_start
    is_start = True
    time.sleep(1)  # 等待1秒
    huodongX = list_window_region[windows][0] + list_window_region[windows][2] / 2
    huodongY = list_window_region[windows][1] + list_window_region[windows][3] / 2
    print(huodongX, huodongY, list_window_region[windows])
    click(list_window_region[windows][0] + int(list_window_region[windows][2] / 2),
          list_window_region[windows][1] + int(list_window_region[windows][3] / 2))  # 移到窗口中间，点击以激活窗口
    while is_start:
        if get_rw("huodong", windows):
            break
        else:
            time.sleep(3)


# 执行任务操作
def do_action(windows):
    flag = 0  # 执行标志
    if get_rw("choice_do", windows):  # 选择任务
        flag = 1
        time.sleep(0.1)
    if get_rw("choice_do2", windows):  # 选择任务
        flag = 1
        time.sleep(0.1)
    if get_rw("shimenButton", windows):  # 师门确认按钮
        flag = 1
        time.sleep(0.1)
    elif get_rw("shiyong", windows):  # 使用物品
        flag = 1
        time.sleep(0.1)
    elif get_rw("goumai", windows) or get_rw("goumai1", windows) or get_rw("goumai2", windows) or get_rw("goumai3",
                                                                                                         windows):  # 购买物品
        # 同时还应该查看是否展示了 请选择物品 判断是否东西呗抢先购买了情况 然后关闭界面
        get_rw("guanbi", windows) or get_rw("guanbi_1", windows) or get_rw("guanbi_2", windows) or get_rw("guanbi_3",
                                                                                                          windows)
        flag = 1
        time.sleep(0.1)
    # elif get_rw("goumai2",windows):  # 购买物品摆摊购买
    #     flag = 1
    #     time.sleep(0.1)
    elif get_rw("juanxian", windows):  # 捐献
        flag = 1
        time.sleep(0.1)
    elif get_rw("jixu", windows):  # 点击任意地方继续
        flag = 1
        time.sleep(0.1)
        while True:
            if get_rw("jixu", windows):
                time.sleep(0.1)
            else:
                break
    elif get_rw("tiaoguo", windows):  # 点击跳过
        flag = 1
    elif get_rw("lingqu", windows):  # 领取
        flag = 1
        time.sleep(0.1)
    elif get_rw("cuansong", windows):  # 传送
        flag = 1
        time.sleep(0.1)
        get_rw("guanbi", windows)
    elif get_rw("shangjiao", windows):  # 上交
        flag = 1
        time.sleep(0.1)
    elif get_rw("shimenChoice", windows):  # 师门选择界面 去完成
        flag = 1
        time.sleep(0.1)
    elif get_rw("guanbi", windows) or get_rw("guanbi_1", windows) or get_rw("guanbi_2", windows) or get_rw("guanbi_3",
                                                                                                           windows):  # 关闭窗口
        flag = 1
        time.sleep(0.1)
    elif get_rw("queding", windows):  # 确定
        flag = 1
        time.sleep(0.1)
    elif get_rw("zidong", windows):  # 自动战斗
        flag = 1
        time.sleep(0.1)
    elif get_rw("denglu", windows):  # 登录游戏
        flag = 1
        time.sleep(0.1)
    elif get_rw("chongshi", windows):  # 重连失败重试
        flag = 1
        time.sleep(0.1)
    elif get_rw("dianjiFlag", windows):  # 一种做师门时候卡界面问题
        flag = 1
        time.sleep(0.1)
    # elif not findpng("huodong.png"):
    #     # 防止出现卡界面的情况 在活动都找不到的情况就随意点一下位置
    #     # click(huodongX, huodongY+300)
    #     print("应该随机点击")

    return flag


# 师门
def shi_men(windows):
    global is_start
    is_start = True
    open_huodong(windows)
    if not get_rw("richanghuodong", windows):
        print("打开日常活动失败")
        return
    if not get_rw("shimen_rw", windows):
        print("师门任务已完成")
        button_shimen["text"] = "师门（执行失败）"
        return
    # if not get_rw("richanghuodong"): 可能还需加上继续任务 以及选择任务
    #     print("打开日常活动失败")
    #     return

    button_shimen["text"] = "师门（执行中）"
    while is_start:
        flag = 0
        if get_rw("shimen", windows):  # 师门
            flag = 1
            time.sleep(1)

        result = do_action(windows)
        if findpng("renwu.png", windows) is not None and result == 0 and flag == 0:
            # if result == 0 and flag == 0:
            button_shimen["text"] = "师门（结束）"
            break
        time.sleep(1)


def mijing(windows):
    global is_start
    is_start = True
    open_huodong(windows)
    if not get_rw("richanghuodong", windows):
        print("打开日常活动失败")
        return
    if not get_rw("mjxy", windows):
        print("秘境打开失败")
        button_shimen["text"] = "秘境（执行失败）"
        return
    if not get_rw("mjxy2", windows):
        print("秘境选择界面打开失败")
        button_shimen["text"] = "秘境（执行失败）"
        return
    if not get_rw("mjxy3", windows) or get_rw("mjxy4", windows):
        print("秘境选择怪物失败")
        button_shimen["text"] = "秘境（执行失败）"
        return
    if not get_rw("tiaozhan", windows):
        print("秘境挑战怪物失败")
        button_shimen["text"] = "秘境（执行失败）"
        return

    button_mijing["text"] = "秘境（执行中）"
    for i in range(1, 100):
        get_rw("mjxy_rw", windows)
        get_rw("jinruzhandou", windows)
        time.sleep(6)
    # 退出秘境
    get_rw("mijinglikai", windows)


# 抓鬼
def zhua_gui(windows):
    global is_start
    is_start = True
    figghtCheckNumber = 0

    while is_start:
        if findpng("renwu.png", windows) and not get_rw("zuogui", windows):
            open_huodong(windows)
            get_rw("richanghuodong", windows)
            get_rw("zuogui_rw", windows)
            get_rw("zudui", windows)  # 自动组队
            get_rw("guanbi", windows)  # 关闭窗口
        get_rw("guanbi", windows)  # 关闭窗口
        # 战斗中
        if findpng("zidong.png", windows):
            figghtCheckNumber = 0
        else:
            # 连续五分钟未参与战斗
            figghtCheckNumber = figghtCheckNumber + 1
            if figghtCheckNumber > 10:
                print('捉鬼自动重选队伍')
                get_rw("duiwu", windows)  # 打开队伍队伍
                get_rw("tuidui", windows)  # 退出队伍
                get_rw("guanbi", windows)  # 关闭窗口
                figghtCheckNumber = 0

        time.sleep(60)
    return


# 帮派任务
def bang_pai(windows):
    global is_start
    is_start = True
    open_huodong(windows)
    get_rw("richanghuodong", windows)
    if not get_rw("bangpai_rw", windows):
        print("帮派任务已完成")
        button_bangpai["text"] = "帮派（已完成）"
        return
    button_bangpai["text"] = "帮派（执行中）"
    while is_start:
        if get_rw("bangpai_xw", windows) or get_rw("bangpai_xw1", windows):  # 玄武
            time.sleep(1)
        elif get_rw("bangpai_zq", windows):  # 朱雀
            time.sleep(1)
        elif get_rw("bangpai_ql", windows):  # 青龙
            time.sleep(1)
        # elif findpng("renwu.png",windows):   #在主界面，但以上任务都没找到，则任务已完成，退出
        #    button_bangpai["text"] = "帮派（已完成）"
        #    break

        do_action(windows)

        time.sleep(3)
    return


# 宝图任务
def bao_tu(windows):
    global is_start
    is_start = True
    open_huodong(windows)
    time.sleep(0.2)
    get_rw("richanghuodong", windows)
    if not get_rw_2("baotu_rw", windows, 0.8):
        print("宝图任务已完成")
        button_baotu["text"] = "宝图（已完成）"
        return
    button_baotu["text"] = "宝图（执行中）"
    # 选择任务
    if not get_rw("choice_do", windows) or get_rw("choice_do1", windows):
        print("未找到选择要做的事")

    time.sleep(10)
    get_rw("renwu", windows)  # 打开任务
    get_rw("dqrw", windows)  # 打开任务
    get_rw("btrw", windows)  # 打开宝图任务
    get_rw("mscs", windows)  # 点击马上传送
    get_rw("guanbi", windows)  # 关闭窗口
    time.sleep(1)
    button_baotu["text"] = "宝图（已完成）"


# 运镖任务
def yun_biao(windows):
    global is_start
    is_start = True
    yunbiaoCount = 0
    button_yunbiao["text"] = "运镖（进行中）"
    while is_start:
        open_huodong(windows)
        get_rw("richanghuodong", windows)
        if get_rw("yunbiao_rw", windows):
            time.sleep(1)
            get_rw("yasong", windows)
            clickd = get_rw("queding", windows)
            if clickd is True:
                yunbiaoCount = yunbiaoCount + 1
            get_rw("guanbi", windows)  # 关闭窗口
            time.sleep(1)
        elif yunbiaoCount >= 3:
            button_yunbiao["text"] = "运镖（已完成）"
            break


# 使用藏宝图
def cangbaotu(windows):
    # 打开包裹
    # 找到并点击藏宝图
    do_action(windows)


# 顺序执行任务，当天执行完成后等待日切后重新开始
def Start(windows):
    global is_start

    print("启动窗口=", windows)
    is_start = True
    AllDo = False
    beginDate = datetime.datetime.now().strftime('%Y%m%d')
    while True:
        curDate = datetime.datetime.now().strftime('%Y%m%d')
        if curDate > beginDate:
            beginDate = curDate
            AllDo = False

        if is_start == False:
            break

        if AllDo == False:
            if is_start == True:
                shi_men(windows)
            if is_start == True:
                bang_pai(windows)
            if is_start == True:
                bao_tu(windows)
            if is_start == True:
                mijing(windows)
            if is_start == True:
                yun_biao(windows)
            if is_start == True:
                zhua_gui(windows)
            AllDo = True
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "今天的任务已完成")
        else:
            time.sleep(60)


# 多开，并行执行
def multi_do():
    t = []
    for windows in range(len(list_window_region)):
        t.append(windows)
        t[windows] = threading.Thread(target=Start, args=(windows,))
        t[windows].setDaemon(True)
        t[windows].start()
        # print("t=",t)
    return


# 一键执行全部任务
def do_all(windows):
    global is_start

    is_start = True
    # 自动点击
    button_quanbu["text"] = "全部执行(执行中)"
    times = 0  # 连续无任何操作的次数
    while is_start:
        if do_action(windows):
            times = 0
            time.sleep(1)
        elif findpng("renwu.png", windows):
            x = list_window_region[windows][0] + 840
            y = list_window_region[windows][1] + 200
            xy = findpng("qidai.png", windows)
            if xy is not None and xy[1] < y:
                y = y + 70
            click(x, y)
            times = 0
            time.sleep(2)
        else:
            time.sleep(2)
    button_quanbu["text"] = "全部执行(已完成)"
    return


def stop():
    global is_start
    is_start = False
    button_baotu["text"] = "宝图"
    button_bangpai["text"] = "帮派"
    button_shimen["text"] = "师门"
    button_zhuagui["text"] = "带队抓鬼"
    button_quanbu["text"] = "全部执行"
    print("停止")


def jumpQueue():
    t = []
    for windows in range(len(list_window_region)):
        t.append(windows)
        t[windows] = threading.Thread(target=jumpQueueAction, args=(windows,))
        t[windows].daemon = True
        t[windows].start()


def jumpQueueAction(windows):
    global is_start
    is_start = True
    while is_start:
        get_rw("jq1", windows) or get_rw("jq5", windows)
        time.sleep(0.5)
        if get_rw("jq2", windows):
            get_rw("jq3", windows)
            get_rw("jq4", windows)


def SavePic():
    global window_region
    pyautogui.FAILSAFE = False
    img = pyautogui.screenshot(region=window_region)
    FileName = "./images/" + datetime.datetime.now().strftime('%H%M%S')
    img.save(FileName + ".png")
    """
    #后台截图
    hwnd = win32gui.FindWindow(None, "梦幻西游 - MuMu模拟器")
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("./images/new.png")
    """


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.daemon = True;
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


# 启动
if __name__ == "__main__":
    # global window_region
    window_size = get_window_info()
    print(window_size)
    if window_size is None:
        widow_region = (0, 0, 800, 600)
    else:
        window_region = (
            window_size[0], window_size[1], window_size[2] - window_size[0], window_size[3] - window_size[1])

    global is_start
    global huodongX
    global huodongY

    # shimen(window_size)
    # zhua_gui(window_size)
    # bang_pai(window_size)
    # baotu(window_size)

    # 创建主窗口
    root = tk.Tk()
    root.title("梦幻西游手游辅助")
    root.minsize(300, 800)
    root.maxsize(300, 800)
    root.wm_attributes('-topmost', 1)
    # 创建按钮
    button_shimen = tk.Button(root, text=u"师门", command=lambda: MyThread(shi_men, 0), width=15, height=2)
    button_shimen.place(relx=0.2, rely=0.15, width=100)
    button_shimen.pack()

    button_bangpai = tk.Button(root, text="帮派", command=lambda: MyThread(bang_pai, 0), width=15, height=2)
    button_bangpai.place(relx=0.2, rely=0.35, width=200)
    button_bangpai.pack()

    button_baotu = tk.Button(root, text="宝图", command=lambda: MyThread(bao_tu, 0), width=15, height=2)
    button_baotu.place(relx=0.4, rely=0.55, width=200)
    button_baotu.pack()

    button_mijing = tk.Button(root, text="秘境", command=lambda: MyThread(mijing, 0), width=15, height=2)
    button_mijing.place(relx=0.4, rely=0.55, width=200)
    button_mijing.pack()

    button_yunbiao = tk.Button(root, text="运镖", command=lambda: MyThread(yun_biao, 0), width=15, height=2)
    button_yunbiao.place(relx=0.4, rely=0.55, width=200)
    button_yunbiao.pack()

    button_zhuagui = tk.Button(root, text="带队抓鬼", command=lambda: MyThread(zhua_gui, 0), width=15,
                               height=2)
    button_zhuagui.place(relx=0.4, rely=0.65, width=100)
    button_zhuagui.pack()

    # button_quanbu = tk.Button(root, text="全部执行", command=lambda: MyThread(do_all), width=15, height=2)
    button_quanbu = tk.Button(root, text="全部执行", command=multi_do, width=15, height=2)
    button_quanbu.place(relx=0.4, rely=0.65, width=100)
    button_quanbu.pack()

    button_tingzhi = tk.Button(root, text=u"停止", command=lambda: MyThread(stop), width=15, height=2)
    button_tingzhi.place(relx=0.4, rely=0.85, width=200)
    button_tingzhi.pack()

    button_jietu = tk.Button(root, text=u"截图", command=lambda: MyThread(SavePic), width=15, height=2)
    button_jietu.place(relx=0.4, rely=0.95, width=200)
    button_jietu.pack()

    button_jp = tk.Button(root, text=u"挤区", command=lambda: MyThread(jumpQueue), width=15, height=2)
    button_jp.place(relx=0.4, rely=0.95, width=200)
    button_jp.pack()

    getallwindowregion()
    print(list_window_region, len(list_window_region))

    root.mainloop()
