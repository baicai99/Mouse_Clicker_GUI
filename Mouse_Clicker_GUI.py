import tkinter as tk
from tkinter import ttk
import pyautogui
import random
import time
import keyboard
import threading
from pynput import mouse

global selected_x, selected_y, running
selected_x, selected_y = None, None
running = True

def on_middle_click(x, y, button, pressed):
    """
    鼠标中键点击事件，用于全局选定坐标
    """
    global selected_x, selected_y
    if pressed and button == mouse.Button.middle:
        selected_x, selected_y = x, y
        coordinates_label.config(text=f"选定坐标: ({selected_x}, {selected_y})")

# 启动鼠标监听器
mouse_listener = mouse.Listener(on_click=on_middle_click)
mouse_listener.start()

def continuous_click(x, y, interval_ms, max_clicks=float('inf')):
    global running
    count = 0
    interval = interval_ms / 1000  # 转换为秒
    while count < max_clicks and running:
        pyautogui.click(x, y)
        count += 1
        time.sleep(interval)

def double_click(x, y, interval_ms, max_clicks=float('inf')):
    global running
    count = 0
    interval = interval_ms / 1000  # 转换为秒
    while count < max_clicks and running:
        pyautogui.click(x, y)
        time.sleep(interval)
        pyautogui.click(x, y)
        count += 1
        time.sleep(interval)

def random_clicks_in_area(x, y, radius, interval_range_ms, max_clicks=float('inf')):
    global running
    count = 0
    while count < max_clicks and running:
        offset_x = random.uniform(-radius, radius)
        offset_y = random.uniform(-radius, radius)
        if offset_x**2 + offset_y**2 <= radius**2:  # 确保在圆内
            click_x, click_y = x + int(offset_x), y + int(offset_y)
            pyautogui.click(click_x, click_y)
            time.sleep(random.uniform(interval_range_ms[0], interval_range_ms[1]) / 1000)
        count += 1

def random_double_clicks_in_area(x, y, radius, interval_range_ms, max_clicks=float('inf')):
    """
    在以 (x, y) 为中心的范围内随机双击
    """
    global running
    count = 0
    while count < max_clicks and running:
        offset_x = random.uniform(-radius, radius)
        offset_y = random.uniform(-radius, radius)
        if offset_x**2 + offset_y**2 <= radius**2:  # 确保在圆内
            click_x, click_y = x + int(offset_x), y + int(offset_y)
            pyautogui.click(click_x, click_y)
            time.sleep(0.05)  # 两次点击之间的间隔
            pyautogui.click(click_x, click_y)
            time.sleep(random.uniform(interval_range_ms[0], interval_range_ms[1]) / 1000)
        count += 1

def set_placeholder(entry, placeholder_text):
    """
    设置输入框的占位符
    """
    entry.insert(0, placeholder_text)
    entry.config(foreground='grey')
    
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(foreground='black')
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(foreground='grey')
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def start_continuous_click():
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        interval_ms = float(interval_entry.get())
        threading.Thread(target=continuous_click, args=(selected_x, selected_y, interval_ms)).start()

def start_double_click():
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        interval_ms = float(interval_entry.get())
        threading.Thread(target=double_click, args=(selected_x, selected_y, interval_ms)).start()

def start_random_clicks():
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        radius = int(radius_entry.get())
        min_interval_ms = float(min_interval_entry.get())
        max_interval_ms = float(max_interval_entry.get())
        threading.Thread(target=random_clicks_in_area, args=(selected_x, selected_y, radius, (min_interval_ms, max_interval_ms))).start()

def start_random_double_clicks():
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        radius = int(radius_entry.get())
        min_interval_ms = float(min_interval_entry.get())
        max_interval_ms = float(max_interval_entry.get())
        threading.Thread(target=random_double_clicks_in_area, args=(selected_x, selected_y, radius, (min_interval_ms, max_interval_ms))).start()

def stop_clicking():
    global running
    running = False

def close_program():
    root.quit()

# 创建主窗口
root = tk.Tk()
root.title("Mouse Clicker GUI")

# 选定坐标标签
coordinates_label = ttk.Label(root, text="请按鼠标中键选定全局坐标")
coordinates_label.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

# 连续点击相关控件
ttk.Label(root, text="点击间隔（毫秒）:").grid(column=0, row=1, padx=10, pady=5)
interval_entry = ttk.Entry(root)
interval_entry.grid(column=1, row=1, padx=10, pady=5)
set_placeholder(interval_entry, "100")  # 默认占位符为100毫秒

continuous_click_button = ttk.Button(root, text="连击", command=start_continuous_click)
continuous_click_button.grid(column=0, row=2, padx=10, pady=5, columnspan=2)

# 双击相关控件
double_click_button = ttk.Button(root, text="双击", command=start_double_click)
double_click_button.grid(column=0, row=3, padx=10, pady=5, columnspan=2)

# 随机点击相关控件
ttk.Label(root, text="随机点击范围（半径n像素）:").grid(column=0, row=4, padx=10, pady=5)
radius_entry = ttk.Entry(root)
radius_entry.grid(column=1, row=4, padx=10, pady=5)
set_placeholder(radius_entry, "50")  # 默认占位符为50像素

ttk.Label(root, text="最小点击间隔（毫秒）:").grid(column=0, row=5, padx=10, pady=5)
min_interval_entry = ttk.Entry(root)
min_interval_entry.grid(column=1, row=5, padx=10, pady=5)
set_placeholder(min_interval_entry, "100")  # 默认占位符为100毫秒

ttk.Label(root, text="最大点击间隔（毫秒）:").grid(column=0, row=6, padx=10, pady=5)
max_interval_entry = ttk.Entry(root)
max_interval_entry.grid(column=1, row=6, padx=10, pady=5)
set_placeholder(max_interval_entry, "300")  # 默认占位符为300毫秒

random_clicks_button = ttk.Button(root, text="范围内随机点击", command=start_random_clicks)
random_clicks_button.grid(column=0, row=7, padx=10, pady=5, columnspan=2)

# 范围内随机双击相关控件
random_double_clicks_button = ttk.Button(root, text="范围内随机双击", command=start_random_double_clicks)
random_double_clicks_button.grid(column=0, row=8, padx=10, pady=5, columnspan=2)

# 停止按钮，显示快捷键
stop_button = ttk.Button(root, text="停止连点 (Alt+E)", command=stop_clicking)
stop_button.grid(column=0, row=9, padx=10, pady=5, columnspan=2)

# 监听快捷键
keyboard.add_hotkey('alt+e', stop_clicking)

# 启动主循环
root.mainloop()

# 退出时解除监听器和快捷键
mouse_listener.stop()
keyboard.remove_hotkey('alt+e')
