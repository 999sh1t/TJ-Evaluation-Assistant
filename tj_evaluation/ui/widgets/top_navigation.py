from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
class TopNavigation(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = None
        self.rows = 1
        self.size_hint = (1, None)
        self.height = dp(60)
        self.spacing = dp(5)
        self.buttons = {}

        # 添加导航按钮
        self.add_button("首页")
        self.add_button("综评")
        self.add_button("关于")
        self.add_button("综评检查")
        self.add_button("标准数据") 
        # 用户管理按钮
        self.user_button = Button(
            text="用户: 未登录",
            size_hint=(None, 1),
            width=dp(150),
            background_normal='',
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        self.user_button.bind(on_press=lambda x: self.parent.show_user_management())
        self.add_widget(self.user_button)

    def add_button(self, text):
        btn = Button(
            text=text,
            size_hint=(None, 1),
            width=dp(120),
            background_normal='',
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        btn.bind(on_press=lambda x: self.parent.show_screen(text))
        self.add_widget(btn)
        self.buttons[text] = btn

    def set_active_button(self, screen_name):
        # 重置所有按钮颜色
        for name, btn in self.buttons.items():
            btn.background_color = (0.2, 0.5, 0.8, 1)

        # 设置当前按钮为激活状态
        if screen_name in self.buttons:
            self.buttons[screen_name].background_color = (0.4, 0.7, 1, 1)

    def update_user_text(self, username):
        """更新用户按钮文本"""
        self.user_button.text = f"用户: {username}"