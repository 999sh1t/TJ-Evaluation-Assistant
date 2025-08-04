from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.metrics import dp
from tj_evaluation.core.api import autoLogin
class LoginForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(400), dp(350))  # 增加高度以容纳"添加新用户"按钮
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.padding = dp(20)
        self.spacing = dp(15)
        self.opacity = 0
        self.scale = 0.9

        # 标题
        self.add_widget(Label(
            text="用户登录",
            font_size=dp(24),
            size_hint_y=None,
            height=dp(40)
        ))

        # 账号选择下拉框
        self.username_input = TextInput(
            hint_text="请输入账号",
            multiline=False,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            padding=dp(10)
        )
        self.add_widget(self.username_input)

        # 密码输入框
        self.password_input = TextInput(
            hint_text="请输入密码",
            multiline=False,
            password=True,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            padding=dp(10)
        )
        self.add_widget(self.password_input)

        # 按钮区域
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))

        # 登录按钮
        self.login_button = Button(
            text="登录",
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),
            size_hint_x=1  # 按钮占满可用宽度
        )
        self.login_button.bind(on_press=self.on_login)
        button_layout.add_widget(self.login_button)

        # 添加新用户按钮
        self.add_user_button = Button(
            text="添加新用户",
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=dp(18),  # 与登录按钮字体大小一致
            size_hint_x=1  # 按钮占满可用宽度
        )
        self.add_user_button.bind(on_press=self.on_add_user)
        button_layout.add_widget(self.add_user_button)

        self.add_widget(button_layout)

        # 状态提示
        self.status_label = Label(
            text="",
            color=(1, 0, 0, 1),  # 红色
            font_size=dp(14),
            size_hint_y=None,
            height=dp(20)
        )
        self.add_widget(self.status_label)

    def on_login(self, instance):
        """处理登录逻辑"""
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            self.status_label.text = "账号和密码不能为空"
            self.status_label.color = (1, 0, 0, 1)
            return

        # 这里可以添加登录验证逻辑
        login_success, eid = autoLogin(username, password)
        if login_success:
            self.status_label.text = "登录成功"
            self.status_label.color = (0, 0.8, 0, 1)
            # 可以添加登录成功后的逻辑
        else:
            self.status_label.text = "账号或密码错误"
            self.status_label.color = (1, 0, 0, 1)

    def show(self):
        # 显示登录表单的动画
        anim = Animation(opacity=1, scale=1, d=0.3, t='out_back')
        anim.start(self)

    def hide(self):
        # 隐藏登录表单的动画
        anim = Animation(opacity=0, scale=0.9, d=0.2, t='in_cubic')
        anim.bind(on_complete=self._remove_from_parent)
        anim.start(self)

    def _remove_from_parent(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

    def on_add_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # 简单验证
        if not username or not password:
            self.show_error("账号和密码不能为空")
            return

        # 检查用户是否已存在
        user_manager = self.parent.user_manager
        if user_manager.get_user_info(username) is not None:
            self.show_error("用户已存在")
            return

        # 添加新用户
        user_manager.add_user(username, password)
        self.show_success("用户添加成功，请登录")

    def show_error(self, message):
        self.status_label.text = message
        self.status_label.color = (1, 0, 0, 1)  # 红色

    def show_success(self, message):
        self.status_label.text = message
        self.status_label.color = (0, 0.8, 0, 1)  # 绿色