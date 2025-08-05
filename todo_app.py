# 引入多文件打包模块
import os
import sys


# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('')
os.chdir(cd)

# 导入所需库以创建Kivy应用程序
from kivy.app import App
from kivy import Config
Config.set('graphics', 'minimumengl', '110') # 降低OpenGL版本
Config.set('graphics', 'multisamples', '0')  # 关闭抗锯齿以减少图形需求
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout  # 用于创建布局的类
from kivy.uix.textinput import TextInput  # 用于输入文本
from kivy.uix.button import Button  # 创建按钮
from kivy.uix.recycleview import RecycleView  # 用于显示可回收视图的数据
from kivy.uix.recycleview.views import RecycleDataViewBehavior  # 为数据视图行为提供基础
from kivy.uix.label import Label  # 显示文本
from kivy.properties import StringProperty  # 用于定义对象属性
from kivy.uix.recycleboxlayout import RecycleBoxLayout  # 用于在RecycleView中创建布局
from kivy.uix.behaviors import FocusBehavior  # 添加焦点行为
from kivy.uix.recyclegridlayout import RecycleGridLayout  # 用于RecycleView的网格布局
from kivy.lang import Builder  # 用于加载kv语言文件

# 在TodoItem类中添加对on_release事件的绑定
class TodoItem(RecycleDataViewBehavior, Label):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(TodoItem, self).__init__(**kwargs)
        self.bind(on_release=self.on_release)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super(TodoItem, self).on_touch_down(touch)

    def on_release(self, instance):
        self.remove_self()

    def remove_self(self):
        app = App.get_running_app()
        app.root.todo_list.remove_item(self.text)

# 更新KV语言，移除on_release的直接绑定，使用系统默认字体
Builder.load_string("""
<TodoItem@RecycleDataViewBehavior+Label>:  
    text: root.text  
    size_hint_y: None  
    height: dp(50)  

<ToDoList>:  
    viewclass: 'TodoItem'  
    RecycleBoxLayout:  
        default_size: None, dp(50)  
        default_size_hint: 1, None  
        size_hint_y: None  
        height: self.minimum_height  
        orientation: 'vertical'  
""")

# 定义ToDoList类，继承自RecycleView
class ToDoList(RecycleView):
    def __init__(self, **kwargs):
        super(ToDoList, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in []]  # 初始化数据列表为空

    # 添加任务到列表
    def add_item(self, task):
        self.data.append({'text': task})  # 添加新任务
        self.refresh_from_data()  # 刷新视图

    # 删除任务
    def remove_item(self, task):
        self.data = [d for d in self.data if d['text'] != task]  # 移除指定任务
        self.refresh_from_data()  # 刷新视图

# 定义主应用程序类
class TodoApp(App):
    def build(self):
        # 创建主布局
        root = BoxLayout(orientation='vertical')

        with root.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # 设置背景颜色为深灰色
            self.rect = Rectangle(size=root.size, pos=root.pos)  # 创建一个覆盖整个布局的矩形

        self.todo_list = ToDoList()  # 确保todo_list是App类的一个属性，以便在TodoItem中访问

        # 添加输入框
        self.input_field = TextInput(text='', multiline=False)

        # 添加添加按钮
        add_button = Button(text='添加', on_press=self.add_task)
        
        # 添加删除按钮
        remove_button = Button(text='删除', on_press=self.remove_task)
        root.add_widget(remove_button)

        # 添加待办事项列表
        root.add_widget(self.todo_list)

        # 添加输入框和按钮到布局
        root.add_widget(self.input_field)
        root.add_widget(add_button)

        # 设置窗口标题
        self.title = "SDCOM的待办项目小程序" 

        # 软件图标
        self.icon = "res/icon.jpg" 

        # 返回根布局
        return root

    def on_size(self, *args):
        # 更新背景矩形的尺寸以匹配根布局
        self.rect.size = self.root.size

    # 添加任务按钮的回调函数
    def add_task(self, instance):
        task = self.input_field.text  # 获取输入的任务
        if task:  # 如果有任务
            self.todo_list.add_item(task)  # 添加到列表
            self.input_field.text = ''  # 清空输入框

    # 删除任务按钮的回调函数
    def remove_task(self, instance):
        task = self.input_field.text  # 获取输入的任务
        if task and task in [d['text'] for d in self.todo_list.data]:  # 如果有任务且任务存在于列表中
            self.todo_list.remove_item(task)  # 从列表中删除任务
            self.input_field.text = ''  # 清空输入框



# 运行应用程序
if __name__ == '__main__':
    TodoApp().run()



