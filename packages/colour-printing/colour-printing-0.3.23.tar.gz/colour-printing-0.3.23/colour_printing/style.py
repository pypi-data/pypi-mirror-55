STYLE = {
    'fore':
        {  # 前景色
            'black': 30,  # 黑色
            'red': 31,  # 红色
            'green': 32,  # 绿色
            'yellow': 33,  # 黄色
            'blue': 34,  # 蓝色
            'purple': 35,  # 紫红色
            'cyan': 36,  # 青蓝色
            'white': 37,  # 白色
        },

    'back':
        {  # 背景
            'black': 40,  # 黑色
            'red': 41,  # 红色
            'green': 42,  # 绿色
            'yellow': 43,  # 黄色
            'blue': 44,  # 蓝色
            'purple': 45,  # 紫红色
            'cyan': 46,  # 青蓝色
            'white': 47,  # 白色
        },

    'mode':
        {  # 显示模式
            'normal': 0,  # 终端默认设置
            'bold': 1,  # 高亮显示
            'underline': 4,  # 使用下划线
            'blink': 5,  # 闪烁
            'invert': 7,  # 反白显示
            'hide': 8,  # 不可见
        },

    'default':
        {
            'end': 0,
        },
}


def setting(mode='', fore='', back=''):
    """
    linxu:转义序列以ESC开头，即ASCII码下的\033
               格式: \033[显示方式;前景色;背景色m
    """
    mode = '%s' % STYLE['mode'][mode] if STYLE['mode'].get(mode) else ''

    fore = '%s' % STYLE['fore'][fore] if STYLE['fore'].get(fore) else ''

    back = '%s' % STYLE['back'][back] if STYLE['back'].get(back) else ''

    style = ';'.join([s for s in [mode, fore, back] if s])

    style = '\033[%sm' % style if style else ''

    end = '\033[%sm' % STYLE['default']['end'] if style else ''

    return style, end


class CPStyle(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Fore:
    BLACK = CPStyle(name="fore", value="black")
    RED = CPStyle(name="fore", value="red")
    GREEN = CPStyle(name="fore", value="green")
    YELLOW = CPStyle(name="fore", value="yellow")
    BLUE = CPStyle(name="fore", value="blue")
    PURPLE = CPStyle(name="fore", value="purple")
    CYAN = CPStyle(name="fore", value="cyan")
    WHITE = CPStyle(name="fore", value="white")


class Back:
    BLACK = CPStyle(name="back", value="black")
    RED = CPStyle(name="back", value="red")
    GREEN = CPStyle(name="back", value="green")
    YELLOW = CPStyle(name="back", value="yellow")
    BLUE = CPStyle(name="back", value="blue")
    PURPLE = CPStyle(name="back", value="purple")
    CYAN = CPStyle(name="back", value="cyan")
    WHITE = CPStyle(name="back", value="white")


class Mode:
    NORMAL = CPStyle(name="mode", value="normal")
    BOLD = CPStyle(name="mode", value="bold")
    UNDERLINE = CPStyle(name="mode", value="underline")
    BLINK = CPStyle(name="mode", value="blink")
    INVERT = CPStyle(name="mode", value="invert")
    HIDE = CPStyle(name="mode", value="hide")
