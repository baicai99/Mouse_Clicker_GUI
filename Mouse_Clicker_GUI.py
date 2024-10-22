# 导入必要的库
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from pynput import mouse, keyboard
import locale
import ctypes

# 语言显示名称与代码的映射
languages = {
    "中文": "zh",
    "English": "en",
    "हिन्दी": "hi",
    "Indonesian": "id",
    "Urdu": "ur",
    "Portuguese": "pt",
    "Español": "es",
    "Русский": "ru",
    "বাংলা": "bn",
    "العربية": "ar"
}

# 定义语言检测函数
# 可选：手动设置语言代码，如 'en', 'zh' 等。设为 None 时使用系统语言。
MANUAL_LANGUAGE = None  # 例如，设置为 'zh' 强制使用中文，或设为 None 使用系统语言

def get_system_language():
    """
    获取系统语言。如果设置了 MANUAL_LANGUAGE，则优先使用它。
    在 Windows 上，使用 ctypes 调用 Windows API 获取用户界面语言。
    在其他操作系统上，使用 locale.getlocale() 作为备选。
    """
    if MANUAL_LANGUAGE:
        return MANUAL_LANGUAGE.lower()
    
    try:
        # 检查操作系统类型
        import sys
        if sys.platform.startswith('win'):
            return get_system_language_windows()
        else:
            return get_system_language_unix()
    except:
        return 'en'  # 默认英语

def get_system_language_windows():
    """
    使用 Windows API 获取系统语言。
    """
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        print(f"Detected LANGID: {lang_id}")  # 调试信息
        # 常见语言 ID 映射
        lang_map = {
            1028: 'zh',  # Chinese (Simplified) - zh-CN
            2052: 'zh',  # Chinese (Simplified) - zh-CN
            3076: 'zh',  # Chinese (Traditional) - zh-TW
            4100: 'zh',  # Chinese (Traditional) - zh-HK
            1031: 'de',  # German
            1025: 'ar',  # Arabic
            1033: 'en',  # English (United States)
            1036: 'fr',  # French
            1046: 'pt',  # Portuguese
            1049: 'ru',  # Russian
            1051: 'tr',  # Turkish
            1060: 'uk',  # Ukrainian
            1061: 'es',  # Spanish
            1093: 'kn',  # Kannada
            1062: 'fi',  # Finnish
            # 添加更多语言 ID 映射
        }
        detected_lang = lang_map.get(lang_id, 'en')  # 默认英语
        print(f"Mapped language: {detected_lang}")  # 调试信息
        return detected_lang
    except:
        return 'en'  # 默认英语

def get_system_language_unix():
    """
    使用 locale 获取系统语言（适用于 Unix/Linux/MacOS）。
    """
    try:
        lang, encoding = locale.getlocale(locale.LC_ALL)
        if lang:
            lang_code = lang.split('_')[0]
            return lang_code.lower()
        else:
            return 'en'
    except:
        return 'en'

# 当前语言
current_language = get_system_language()
print(f"Detected language: {current_language}")  # 用于调试

# 内置翻译字典
translations = {
    "en": {
        "title": "Mouse Clicker GUI",
        "select_coords": "Please press the middle mouse button to select global coordinates",
        "click_interval": "Click interval (ms):",
        "continuous_click": "Continuous Click",
        "double_click": "Double Click",
        "random_click_radius": "Random click radius (pixels):",
        "min_interval": "Min click interval (ms):",
        "max_interval": "Max click interval (ms):",
        "random_clicks": "Random Clicks within Area",
        "random_double_clicks": "Random Double Clicks within Area",
        "stop_clicking": "Stop Clicking (Press Esc)",
        "language": "Language",
        "error": "Error",
        "invalid_interval": "Invalid interval value.",
        "invalid_parameters": "Invalid parameters entered.",
        "language_not_supported": "Selected language is not supported.",
        "country_rank": "Rank",
        "country_name": "Country",
        "country_language": "Language",
        "top_countries_title": "Top 10 Most Populous Countries and Their Main Languages"
    },
    "zh": {
        "title": "鼠标连点器",
        "select_coords": "请按鼠标中键选定全局坐标",
        "click_interval": "点击间隔（毫秒）:",
        "continuous_click": "连击",
        "double_click": "双击",
        "random_click_radius": "随机点击范围（半径n像素）:",
        "min_interval": "最小点击间隔（毫秒）:",
        "max_interval": "最大点击间隔（毫秒）:",
        "random_clicks": "范围内随机点击",
        "random_double_clicks": "范围内随机双击",
        "stop_clicking": "停止连点 (按 Esc)",
        "language": "语言",
        "error": "错误",
        "invalid_interval": "无效的间隔值。",
        "invalid_parameters": "输入了无效的参数。",
        "language_not_supported": "所选语言不受支持。",
        "country_rank": "排名",
        "country_name": "国家",
        "country_language": "主要语言",
        "top_countries_title": "前十大人口国家及其主要使用语言"
    },
    "hi": {
        "title": "माउस क्लिकर GUI",
        "select_coords": "वैश्विक निर्देशांक चुनने के लिए कृपया मध्य माउस बटन दबाएं",
        "click_interval": "क्लिक अंतराल (मिलीसेकंड):",
        "continuous_click": "लगातार क्लिक",
        "double_click": "दोहरा क्लिक",
        "random_click_radius": "यादृच्छिक क्लिक त्रिज्या (पिक्सेल में):",
        "min_interval": "न्यूनतम क्लिक अंतराल (मिलीसेकंड):",
        "max_interval": "अधिकतम क्लिक अंतराल (मिलीसेकंड):",
        "random_clicks": "क्षेत्र के भीतर यादृच्छिक क्लिक",
        "random_double_clicks": "क्षेत्र के भीतर यादृच्छिक दोहरा क्लिक",
        "stop_clicking": "क्लिकिंग रोकें (Esc दबाएं)",
        "language": "भाषा",
        "error": "त्रुटि",
        "invalid_interval": "अमान्य अंतराल मान।",
        "invalid_parameters": "अमान्य पैरामीटर दर्ज किए गए।",
        "language_not_supported": "चयनित भाषा समर्थित नहीं है।",
        "country_rank": "रैंक",
        "country_name": "देश",
        "country_language": "भाषा",
        "top_countries_title": "सबसे अधिक जनसंख्या वाले शीर्ष 10 देश और उनकी मुख्य भाषाएं"
    },
    "id": {
        "title": "GUI Pengklik Mouse",
        "select_coords": "Silakan tekan tombol tengah mouse untuk memilih koordinat global",
        "click_interval": "Interval klik (ms):",
        "continuous_click": "Klik Berkelanjutan",
        "double_click": "Klik Ganda",
        "random_click_radius": "Radius klik acak (piksel):",
        "min_interval": "Interval klik minimum (ms):",
        "max_interval": "Interval klik maksimum (ms):",
        "random_clicks": "Klik Acak dalam Area",
        "random_double_clicks": "Klik Ganda Acak dalam Area",
        "stop_clicking": "Hentikan Klik (Tekan Esc)",
        "language": "Bahasa",
        "error": "Kesalahan",
        "invalid_interval": "Nilai interval tidak valid.",
        "invalid_parameters": "Parameter tidak valid dimasukkan.",
        "language_not_supported": "Bahasa yang dipilih tidak didukung.",
        "country_rank": "Peringkat",
        "country_name": "Negara",
        "country_language": "Bahasa",
        "top_countries_title": "10 Negara dengan Populasi Terbanyak dan Bahasa Utamanya"
    },
    "ur": {
        "title": "ماؤس کلکر GUI",
        "select_coords": "براہ کرم عالمی نقاط کا انتخاب کرنے کے لئے ماؤس کا وسطی بٹن دبائیں",
        "click_interval": "کلک وقفہ (ملی سیکنڈ):",
        "continuous_click": "مسلسل کلک",
        "double_click": "ڈبل کلک",
        "random_click_radius": "اتفاقی کلک رداس (پکسلز میں):",
        "min_interval": "کم از کم کلک وقفہ (ملی سیکنڈ):",
        "max_interval": "زیادہ سے زیادہ کلک وقفہ (ملی سیکنڈ):",
        "random_clicks": "علاقے کے اندر اتفاقی کلک",
        "random_double_clicks": "علاقے کے اندر اتفاقی ڈبل کلک",
        "stop_clicking": "کلکنگ روکیں (Esc دبائیں)",
        "language": "زبان",
        "error": "خرابی",
        "invalid_interval": "غلط وقفہ قدر۔",
        "invalid_parameters": "غلط پیرامیٹر داخل کیے گئے۔",
        "language_not_supported": "منتخب زبان معاونت یافتہ نہیں ہے۔",
        "country_rank": "درجہ بندی",
        "country_name": "ملک",
        "country_language": "زبان",
        "top_countries_title": "سب سے زیادہ آبادی والے ٹاپ 10 ممالک اور ان کی بنیادی زبانیں"
    },
    "pt": {
        "title": "GUI de Cliques do Mouse",
        "select_coords": "Por favor, pressione o botão central do mouse para selecionar coordenadas globais",
        "click_interval": "Intervalo de clique (ms):",
        "continuous_click": "Clique Contínuo",
        "double_click": "Clique Duplo",
        "random_click_radius": "Raio de clique aleatório (pixels):",
        "min_interval": "Intervalo mínimo de clique (ms):",
        "max_interval": "Intervalo máximo de clique (ms):",
        "random_clicks": "Cliques Aleatórios na Área",
        "random_double_clicks": "Cliques Duplos Aleatórios na Área",
        "stop_clicking": "Parar Cliques (Pressione Esc)",
        "language": "Idioma",
        "error": "Erro",
        "invalid_interval": "Valor de intervalo inválido.",
        "invalid_parameters": "Parâmetros inválidos inseridos.",
        "language_not_supported": "Idioma selecionado não é suportado.",
        "country_rank": "Classificação",
        "country_name": "País",
        "country_language": "Idioma",
        "top_countries_title": "Top 10 Países Mais Populosos e Seus Principais Idiomas"
    },
    "es": {
        "title": "GUI de Clics del Ratón",
        "select_coords": "Por favor, presione el botón central del ratón para seleccionar coordenadas globales",
        "click_interval": "Intervalo de clic (ms):",
        "continuous_click": "Clic Continuo",
        "double_click": "Doble Clic",
        "random_click_radius": "Radio de clic aleatorio (píxeles):",
        "min_interval": "Intervalo mínimo de clic (ms):",
        "max_interval": "Intervalo máximo de clic (ms):",
        "random_clicks": "Clics Aleatorios dentro del Área",
        "random_double_clicks": "Doble Clic Aleatorio dentro del Área",
        "stop_clicking": "Detener Clics (Presione Esc)",
        "language": "Idioma",
        "error": "Error",
        "invalid_interval": "Valor de intervalo inválido.",
        "invalid_parameters": "Parámetros inválidos ingresados.",
        "language_not_supported": "El idioma seleccionado no está soportado.",
        "country_rank": "Rango",
        "country_name": "País",
        "country_language": "Idioma",
        "top_countries_title": "Top 10 Países Más Populosos y Sus Principales Idiomas"
    },
    "ru": {
        "title": "GUI Автокликера",
        "select_coords": "Пожалуйста, нажмите среднюю кнопку мыши, чтобы выбрать глобальные координаты",
        "click_interval": "Интервал клика (мс):",
        "continuous_click": "Непрерывный клик",
        "double_click": "Двойной клик",
        "random_click_radius": "Радиус случайного клика (пиксели):",
        "min_interval": "Минимальный интервал клика (мс):",
        "max_interval": "Максимальный интервал клика (мс):",
        "random_clicks": "Случайные клики в области",
        "random_double_clicks": "Случайные двойные клики в области",
        "stop_clicking": "Остановить клики (Нажмите Esc)",
        "language": "Язык",
        "error": "Ошибка",
        "invalid_interval": "Недопустимое значение интервала.",
        "invalid_parameters": "Введены недопустимые параметры.",
        "language_not_supported": "Выбранный язык не поддерживается.",
        "country_rank": "Ранг",
        "country_name": "Страна",
        "country_language": "Язык",
        "top_countries_title": "Топ 10 самых населенных стран и их основные языки"
    },
    "bn": {
        "title": "মাউস ক্লিকার GUI",
        "select_coords": "গ্লোবাল কোঅর্ডিনেট নির্বাচন করতে মধ্যম মাউস বোতাম চাপুন",
        "click_interval": "ক্লিক ইন্টারভাল (মি.সেক.):",
        "continuous_click": "অবিরত ক্লিক",
        "double_click": "ডবল ক্লিক",
        "random_click_radius": "যাদৃচ্ছিক ক্লিক রেডিয়াস (পিক্সেল):",
        "min_interval": "ন্যূনতম ক্লিক ইন্টারভাল (মি.সেক.):",
        "max_interval": "সর্বোচ্চ ক্লিক ইন্টারভাল (মি.সেক.):",
        "random_clicks": "এলাকা মধ্যে যাদৃচ্ছিক ক্লিক",
        "random_double_clicks": "এলাকা মধ্যে যাদৃচ্ছিক ডবল ক্লিক",
        "stop_clicking": "ক্লিক বন্ধ করুন (Esc চাপুন)",
        "language": "ভাষা",
        "error": "ত্রুটি",
        "invalid_interval": "অবৈধ ইন্টারভাল মান।",
        "invalid_parameters": "অবৈধ প্যারামিটার প্রবেশ করা হয়েছে।",
        "language_not_supported": "নির্বাচিত ভাষা সমর্থিত নয়।",
        "country_rank": "র‌্যাঙ্ক",
        "country_name": "দেশ",
        "country_language": "ভাষা",
        "top_countries_title": "শীর্ষ ১০ জনবহুল দেশ এবং তাদের প্রধান ভাষা"
    },
    "ar": {
        "title": "واجهة مستخدم برنامج نقر الفأرة",
        "select_coords": "يرجى الضغط على زر الفأرة الأوسط لتحديد الإحداثيات العالمية",
        "click_interval": "فترة النقر (مللي ثانية):",
        "continuous_click": "نقر مستمر",
        "double_click": "نقر مزدوج",
        "random_click_radius": "نطاق النقر العشوائي (بيكسل):",
        "min_interval": "أقل فترة للنقر (مللي ثانية):",
        "max_interval": "أقصى فترة للنقر (مللي ثانية):",
        "random_clicks": "نقرات عشوائية داخل المنطقة",
        "random_double_clicks": "نقرات مزدوجة عشوائية داخل المنطقة",
        "stop_clicking": "إيقاف النقرات (اضغط Esc)",
        "language": "اللغة",
        "error": "خطأ",
        "invalid_interval": "قيمة الفترة غير صالحة.",
        "invalid_parameters": "تم إدخال معلمات غير صالحة.",
        "language_not_supported": "اللغة المحددة غير مدعومة.",
        "country_rank": "الترتيب",
        "country_name": "الدولة",
        "country_language": "اللغة",
        "top_countries_title": "أعلى 10 دول من حيث عدد السكان ولغاتها الرئيسية"
    }
    # 您可以在此处添加更多语言
}

# 语言获取函数
def _(text_key):
    """
    根据当前语言返回对应的翻译文本。
    """
    return translations.get(current_language, translations.get('en', {})).get(text_key, text_key)

# 全局变量
selected_x, selected_y = None, None
running = False  # 初始状态为停止

# 初始化鼠标控制器
mouse_controller = mouse.Controller()

# 初始化键盘监听器变量
keyboard_listener = None

# 鼠标和键盘事件处理
def on_middle_click(x, y, button, pressed):
    """
    鼠标中键点击事件，用于全局选定坐标
    """
    global selected_x, selected_y
    if pressed and button == mouse.Button.middle:
        selected_x, selected_y = x, y
        coordinates_label.config(text=_('select_coords') + f": ({selected_x}, {selected_y})")

# 启动鼠标监听器
mouse_listener = mouse.Listener(on_click=on_middle_click)
mouse_listener.start()

def on_press(key):
    """
    键盘按下事件，用于监听快捷键 (Esc) 来停止点击
    """
    global running
    try:
        if key == keyboard.Key.esc:
            stop_clicking()
    except AttributeError:
        pass

def start_keyboard_listener():
    """
    启动键盘监听器
    """
    global keyboard_listener
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

# 鼠标点击功能
def click_mouse(x, y, button=mouse.Button.left, count=1):
    """
    执行鼠标点击
    """
    mouse_controller.position = (x, y)
    for _ in range(count):
        mouse_controller.click(button)
        time.sleep(0.05)  # 两次点击之间的间隔

def continuous_click(x, y, interval_ms, max_clicks=float('inf')):
    """
    连续点击
    """
    global running
    count = 0
    interval = interval_ms / 1000  # 转换为秒
    while count < max_clicks and running:
        click_mouse(x, y)
        count += 1
        time.sleep(interval)

def double_click(x, y, interval_ms, max_clicks=float('inf')):
    """
    连续双击
    """
    global running
    count = 0
    interval = interval_ms / 1000  # 转换为秒
    while count < max_clicks and running:
        click_mouse(x, y, count=2)
        count += 1
        time.sleep(interval)

def random_clicks_in_area(x, y, radius, interval_range_ms, max_clicks=float('inf')):
    """
    在指定范围内随机点击
    """
    global running
    count = 0
    while count < max_clicks and running:
        offset_x = random.uniform(-radius, radius)
        offset_y = random.uniform(-radius, radius)
        if offset_x**2 + offset_y**2 <= radius**2:  # 确保在圆内
            click_x, click_y = x + int(offset_x), y + int(offset_y)
            click_mouse(click_x, click_y)
            time.sleep(random.uniform(interval_range_ms[0], interval_range_ms[1]) / 1000)
        count += 1

def random_double_clicks_in_area(x, y, radius, interval_range_ms, max_clicks=float('inf')):
    """
    在指定范围内随机双击
    """
    global running
    count = 0
    while count < max_clicks and running:
        offset_x = random.uniform(-radius, radius)
        offset_y = random.uniform(-radius, radius)
        if offset_x**2 + offset_y**2 <= radius**2:  # 确保在圆内
            click_x, click_y = x + int(offset_x), y + int(offset_y)
            click_mouse(click_x, click_y, count=2)
            time.sleep(random.uniform(interval_range_ms[0], interval_range_ms[1]) / 1000)
        count += 1

# 输入框占位符功能
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
    """
    启动连续点击线程
    """
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        try:
            interval_ms = float(interval_entry.get())
            threading.Thread(target=continuous_click, args=(selected_x, selected_y, interval_ms), daemon=True).start()
        except ValueError:
            messagebox.showerror(_("error"), _("invalid_interval"))

def start_double_click():
    """
    启动连续双击线程
    """
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        try:
            interval_ms = float(interval_entry.get())
            threading.Thread(target=double_click, args=(selected_x, selected_y, interval_ms), daemon=True).start()
        except ValueError:
            messagebox.showerror(_("error"), _("invalid_interval"))

def start_random_clicks():
    """
    启动随机点击线程
    """
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        try:
            radius = int(radius_entry.get())
            min_interval_ms = float(min_interval_entry.get())
            max_interval_ms = float(max_interval_entry.get())
            threading.Thread(target=random_clicks_in_area, args=(selected_x, selected_y, radius, (min_interval_ms, max_interval_ms)), daemon=True).start()
        except ValueError:
            messagebox.showerror(_("error"), _("invalid_parameters"))

def start_random_double_clicks():
    """
    启动随机双击线程
    """
    global running
    running = True
    if selected_x is not None and selected_y is not None:
        try:
            radius = int(radius_entry.get())
            min_interval_ms = float(min_interval_entry.get())
            max_interval_ms = float(max_interval_entry.get())
            threading.Thread(target=random_double_clicks_in_area, args=(selected_x, selected_y, radius, (min_interval_ms, max_interval_ms)), daemon=True).start()
        except ValueError:
            messagebox.showerror(_("error"), _("invalid_parameters"))

def stop_clicking():
    """
    停止所有点击操作
    """
    global running
    running = False

def close_program():
    """
    关闭程序时清理资源
    """
    stop_clicking()
    mouse_listener.stop()
    if keyboard_listener:
        keyboard_listener.stop()
    root.quit()

def change_language(event=None):
    """
    更改当前语言并更新所有文本
    """
    global current_language
    selected_lang_name = language_var.get()
    if selected_lang_name in languages:
        selected_lang_code = languages[selected_lang_name]
        current_language = selected_lang_code
        update_texts()
    else:
        messagebox.showerror(_("error"), _("language_not_supported"))

# 更新 GUI 文本功能
def update_texts():
    """
    更新所有 GUI 元素的文本以匹配当前语言
    """
    root.title(_("title"))
    if selected_x is not None and selected_y is not None:
        coordinates_label.config(text=_('select_coords') + f": ({selected_x}, {selected_y})")
    else:
        coordinates_label.config(text=_('select_coords'))
    click_interval_label.config(text=_('click_interval'))
    continuous_click_button.config(text=_('continuous_click'))
    double_click_button.config(text=_('double_click'))
    random_click_radius_label.config(text=_('random_click_radius'))
    min_interval_label.config(text=_('min_interval'))
    max_interval_label.config(text=_('max_interval'))
    random_clicks_button.config(text=_('random_clicks'))
    random_double_clicks_button.config(text=_('random_double_clicks'))
    stop_button.config(text=_('stop_clicking'))
    language_label.config(text=_('language'))

# 创建主窗口
root = tk.Tk()
root.title(_("title"))

# 添加语言选择下拉菜单
language_label = ttk.Label(root, text=_('language'))
language_label.grid(column=0, row=10, padx=10, pady=5, sticky='e')

language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, state='readonly')
language_combobox['values'] = list(languages.keys())  # 修改为显示语言名称

# 设置默认语言索引
available_language_names = list(languages.keys())
if current_language in languages.values():
    # 找到对应的语言名称
    default_lang_name = [name for name, code in languages.items() if code == current_language][0]
    default_index = available_language_names.index(default_lang_name)
else:
    default_index = 0  # 默认选择第一个语言

if available_language_names:
    language_combobox.current(default_index)
else:
    print("No available languages found. Please check your translations.")

language_combobox.grid(column=1, row=10, padx=10, pady=5, sticky='w')
language_combobox.bind("<<ComboboxSelected>>", change_language)

# 选定坐标标签
coordinates_label = ttk.Label(root, text=_('select_coords'))
coordinates_label.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

# 连续点击相关控件
click_interval_label = ttk.Label(root, text=_('click_interval'))
click_interval_label.grid(column=0, row=1, padx=10, pady=5)
interval_entry = ttk.Entry(root)
interval_entry.grid(column=1, row=1, padx=10, pady=5)
set_placeholder(interval_entry, "100")  # 默认占位符为100毫秒

continuous_click_button = ttk.Button(root, text=_('continuous_click'), command=start_continuous_click)
continuous_click_button.grid(column=0, row=2, padx=10, pady=5, columnspan=2)

# 双击相关控件
double_click_button = ttk.Button(root, text=_('double_click'), command=start_double_click)
double_click_button.grid(column=0, row=3, padx=10, pady=5, columnspan=2)

# 随机点击相关控件
random_click_radius_label = ttk.Label(root, text=_('random_click_radius'))
random_click_radius_label.grid(column=0, row=4, padx=10, pady=5)
radius_entry = ttk.Entry(root)
radius_entry.grid(column=1, row=4, padx=10, pady=5)
set_placeholder(radius_entry, "50")  # 默认占位符为50像素

# 最小点击间隔相关控件
min_interval_label = ttk.Label(root, text=_('min_interval'))
min_interval_label.grid(column=0, row=5, padx=10, pady=5)
min_interval_entry = ttk.Entry(root)
min_interval_entry.grid(column=1, row=5, padx=10, pady=5)
set_placeholder(min_interval_entry, "100")  # 默认占位符为100毫秒

# 最大点击间隔相关控件
max_interval_label = ttk.Label(root, text=_('max_interval'))
max_interval_label.grid(column=0, row=6, padx=10, pady=5)
max_interval_entry = ttk.Entry(root)
max_interval_entry.grid(column=1, row=6, padx=10, pady=5)
set_placeholder(max_interval_entry, "300")  # 默认占位符为300毫秒

# 随机点击按钮
random_clicks_button = ttk.Button(root, text=_('random_clicks'), command=start_random_clicks)
random_clicks_button.grid(column=0, row=7, padx=10, pady=5, columnspan=2)

# 随机双击按钮
random_double_clicks_button = ttk.Button(root, text=_('random_double_clicks'), command=start_random_double_clicks)
random_double_clicks_button.grid(column=0, row=8, padx=10, pady=5, columnspan=2)

# 停止按钮，显示快捷键
stop_button = ttk.Button(root, text=_('stop_clicking'), command=stop_clicking)
stop_button.grid(column=0, row=9, padx=10, pady=5, columnspan=2)

# 启动键盘监听器
start_keyboard_listener()

# 处理窗口关闭事件
root.protocol("WM_DELETE_WINDOW", close_program)

# 启动主循环
root.mainloop()

# 退出时解除监听器
mouse_listener.stop()
if keyboard_listener:
    keyboard_listener.stop()
