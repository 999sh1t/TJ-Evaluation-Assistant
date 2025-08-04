from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from tj_evaluation.core.api import autoLogin
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
class UserManagementScreen(Screen):
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(UserManagementScreen(main_layout))   # 注意同名
class UserManagementScreen(BoxLayout):
    """用户管理界面"""
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.main_layout = main_layout
        self.user_manager = main_layout.user_manager

        # 标题栏
        self.title_bar = BoxLayout(size_hint_y=None, height=dp(50))
        self.title_bar.add_widget(Label(
            text="用户管理",
            font_size=dp(24),
            halign='left',
            valign='middle',
            padding=[dp(10), 0]
        ))
        # 分隔线
        self.separator = Widget(size_hint_y=None, height=dp(1))
        with self.separator.canvas:
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(pos=self.separator.pos, size=self.separator.size)
        self.add_widget(self.separator)

        # 登录表单区域
        self.login_area = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint=(1, 0.8))
        self.username_input = TextInput(
            hint_text="请输入账号",
            multiline=False,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            padding=dp(10)
        )
        self.login_area.add_widget(self.username_input)

        self.password_input = TextInput(
            hint_text="请输入密码",
            multiline=False,
            password=True,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            padding=dp(10)
        )
        self.login_area.add_widget(self.password_input)

        # 登录按钮
        login_button = Button(
            text="登录",
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50)
        )
        login_button.bind(on_press=self.on_login)
        self.login_area.add_widget(login_button)

        # 状态提示
        self.status_label = Label(
            text="",
            color=(1, 0, 0, 1),  # 红色
            font_size=dp(14),
            size_hint_y=None,
            height=dp(20)
        )
        self.login_area.add_widget(self.status_label)

        # 用户列表区域
        self.user_list_area = ScrollView(size_hint=(1, 0.8))
        self.user_grid = GridLayout(cols=1, spacing=dp(10), padding=dp(10), size_hint_y=None)
        self.user_grid.bind(minimum_height=self.user_grid.setter('height'))
        self.user_list_area.add_widget(self.user_grid)

        # 添加用户按钮
        self.add_user_button = Button(
            text="添加新用户",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18)
        )
        self.add_user_button.bind(on_press=self.show_add_user_form)

        # 添加控件到布局
        self.add_widget(self.login_area)
        self.add_widget(self.user_list_area)
        self.add_widget(self.add_user_button)

        # 刷新用户列表
        self.refresh_user_list()

    def refresh_user_list(self):
        """刷新用户列表"""
        self.user_grid.clear_widgets()
        self.clear_widgets()
        self.add_widget(self.title_bar)
        self.add_widget(self.separator)

        # 获取所有用户
        users = self.user_manager.get_all_users()

        current_user = self.user_manager.get_current_user()

        # 始终显示用户列表区域和添加用户按钮
        self.add_widget(self.user_list_area)
        self.add_widget(self.add_user_button)

        if users:
            for username in users:
                user_info = self.user_manager.get_user_info(username)
                # 创建用户信息行
                user_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
                if not username:
                    username = "未知用户"
                xm = user_info.get('xm', '')
                # 构建显示文本
                display_text = f"{username} ({xm})"
                if username == current_user:
                    display_text += "（已登录）"
                # 创建标签
                user_info_label = Label(
                    text=display_text,
                    font_size=dp(16),
                    halign='left',
                    valign='middle',
                    color=(1, 1, 1, 1) if username != current_user else (0, 0.5, 0, 1),  # 当前用户显示为绿色
                    size_hint_x=0.7,
                )
                user_row.add_widget(user_info_label)

                # 操作按钮区域
                button_area = BoxLayout(size_hint_x=None, width=dp(250), spacing=dp(10))

                # 切换用户按钮
                switch_button = Button(
                    text="刷新" if username == current_user else "切换",
                    size_hint=(None, 1),
                    width=dp(80),
                    background_color=(0.2, 0.5, 0.8, 1) if username != current_user else (0, 0.7, 0, 1),  # 刷新按钮设置为绿色
                    color=(1, 1, 1, 1),
                    font_size=dp(14)
                )
                switch_button.bind(on_press=lambda instance, u=username: self.switch_to_user(u))
                button_area.add_widget(switch_button)

                # 删除用户按钮
                delete_button = Button(
                    text="删除",
                    size_hint=(None, 1),
                    width=dp(80),
                    background_color=(0.8, 0.2, 0.2, 1),
                    color=(1, 1, 1, 1),
                    font_size=dp(14)
                )
                delete_button.bind(on_press=lambda instance, u=username: self.confirm_delete_user(u))
                button_area.add_widget(delete_button)

                user_row.add_widget(button_area)

                self.user_grid.add_widget(user_row)
        else:
            # 没有用户时显示提示信息
            no_user_label = Label(
                text="暂无用户，请添加新用户",
                font_size=dp(16),
                halign='center',
                valign='middle',
                size_hint_y=None,
                height=dp(60)
            )
            self.user_grid.add_widget(no_user_label)

    def on_login(self, instance):
        """处理登录逻辑"""
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            self.status_label.text = "账号和密码不能为空"
            self.status_label.color = (1, 0, 0, 1)
            return

        # 验证登录
        # 替换为autoLogin函数调用
        login_success, eid = autoLogin(username, password)
        if login_success:
            self.user_manager.add_user(username, password)
            self.user_manager.current_user = username
            self.status_label.text = "登录成功"
            self.status_label.color = (0, 0.8, 0, 1)
            self.refresh_user_list()
        else:
            self.status_label.text = "账号或密码错误"
            self.status_label.color = (1, 0, 0, 1)

    def show_add_user_form(self, instance):
        """显示添加用户表单"""
        # 创建弹窗内容布局
        content_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 标题
        content_layout.add_widget(Label(
            text="添加新用户",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(40)
        ))

        # 账号输入框
        username_input = TextInput(
            hint_text="请输入账号",
            multiline=False,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            padding=dp(10)
        )
        content_layout.add_widget(username_input)

        # 密码输入框
        password_input = TextInput(
            hint_text="请输入密码",
            multiline=False,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            padding=dp(10)
        )
        content_layout.add_widget(password_input)

        # 按钮区域
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))

        # 确认按钮
        confirm_button = Button(
            text="确认",
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
        )

        # 取消按钮
        cancel_button = Button(
            text="取消",
            background_color=(0.7, 0.7, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
        )

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        content_layout.add_widget(button_layout)

        # 创建弹窗
        popup = Popup(
            title='添加新用户',
            content=content_layout,
            size_hint=(None, None),
            size=(dp(400), dp(300)),
            auto_dismiss=False
        )

        # 绑定按钮事件
        confirm_button.bind(on_press=lambda x: self.add_new_user(username_input.text, password_input.text, popup))
        cancel_button.bind(on_press=popup.dismiss)

        # 显示弹窗
        popup.open()

    def add_new_user(self, username, password, popup):
        """添加新用户"""
        if not username or not password:
            # 显示错误提示
            self.show_message("错误", "账号和密码不能为空")
            return

        # 检查用户是否已存在
        if self.user_manager.get_user_info(username) is not None:
            self.show_message("错误", "用户已存在")
            return

        # 尝试登录，验证账号密码是否有效
        login_success, eid = autoLogin(username, password)
        if not login_success:
            self.show_message("错误", "账号或密码错误")
            return

        # 添加新用户
        self.user_manager.add_user(username, password)

        # 自动登录新用户
        self.user_manager.current_user = username
        self.main_layout.login_success(username, eid)
        self.refresh_user_list()
        popup.dismiss()
        self.show_message("成功", "用户登录成功")

    def switch_to_user(self, username):
        """切换到指定用户"""
        # 显示加载中提示
        loading_popup = Popup(
            title='加载中',
            content=Label(
                text='正在刷新数据，请稍候...' if username == self.user_manager.get_current_user() else '正在切换用户，请稍候...',
                font_size=dp(16)),
            size_hint=(None, None),
            size=(dp(300), dp(150)),
            auto_dismiss=False
        )
        loading_popup.open()

        # 使用Clock.schedule_once来延迟执行登录操作
        def do_login(dt):
            try:
                # 从用户管理器获取密码
                password = self.user_manager.users[username]['password']
                # 重新登录获取新数据
                loginCheck, eid = autoLogin(username, password)
                if loginCheck:
                    # 先获取用户数据
                    user_data = self.user_manager.get_user_data(username)
                    # 设置当前登录用户
                    self.user_manager.current_user = username
                    # 调用login_success方法，传递用户数据
                    self.main_layout.login_success(username, eid, user_data)

                else:
                    self.show_message("错误", "登录失败，请检查账号和密码")
            finally:
                # 无论成功与否，都关闭加载弹窗
                loading_popup.dismiss()

        # 安排登录操作在主线程中执行
        Clock.schedule_once(do_login, 0.1)

    def confirm_delete_user(self, username):
        """确认删除用户"""
        # 创建确认弹窗
        content_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 提示文本
        content_layout.add_widget(Label(
            text=f"确定要删除用户 '{username}' 吗？\n此操作不可撤销。",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(80)
        ))

        # 按钮区域
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))

        # 确认按钮
        confirm_button = Button(
            text="确认",
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
        )

        # 取消按钮
        cancel_button = Button(
            text="取消",
            background_color=(0.7, 0.7, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
        )

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        content_layout.add_widget(button_layout)

        # 创建弹窗
        popup = Popup(
            title='确认删除',
            content=content_layout,
            size_hint=(None, None),
            size=(dp(400), dp(220)),
            auto_dismiss=False
        )

        # 绑定按钮事件
        confirm_button.bind(on_press=lambda x: self.delete_user(username, popup))
        cancel_button.bind(on_press=popup.dismiss)

        # 显示弹窗
        popup.open()

    def delete_user(self, username, popup):
        """删除用户"""
        self.user_manager.remove_user(username)
        self.refresh_user_list()
        popup.dismiss()
        self.show_message("成功", f"用户 '{username}' 已删除")

    def show_message(self, title, message):
        """显示消息弹窗"""
        # 创建弹窗内容布局
        content_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 提示文本
        content_layout.add_widget(Label(
            text=message,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(80)
        ))

        # 确认按钮
        confirm_button = Button(
            text="确定",
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50)
        )
        content_layout.add_widget(confirm_button)

        # 创建弹窗
        popup = Popup(
            title=title,
            content=content_layout,
            size_hint=(None, None),
            size=(dp(400), dp(220)),
            auto_dismiss=False,
            title_size=dp(18)
        )

        # 绑定按钮事件
        confirm_button.bind(on_press=popup.dismiss)

        # 显示弹窗
        popup.open()
