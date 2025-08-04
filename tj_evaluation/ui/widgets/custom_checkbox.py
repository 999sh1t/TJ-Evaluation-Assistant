from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.metrics import dp
class CustomCheckBox(BoxLayout):
    def __init__(self, text, **kwargs):
        super(CustomCheckBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(35)

        # 自定义复选框 - 设置为白色
        self.checkbox = CheckBox(
            active=False,
            size_hint_x=0.5,
            color=(1, 1, 1, 1)  # 设置复选框颜色为白色
        )

        # 自定义标签
        self.label = Label(
            text=text,
            font_size=dp(16),
            size_hint_x=0.85,
            halign='left',
            color=(0.9, 0.9, 0.9, 1)  # 文本颜色
        )

        # 绑定复选框状态变化事件
        self.checkbox.bind(active=self.on_checkbox_active)

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

    def on_checkbox_active(self, instance, value):
        if value:
            # 选中状态，添加"(已选择)"
            self.label.text = f"{self.label.text.split(' (已选择)')[0]} (已选择)"
            self.label.color = (0.2, 0.8, 0.2, 1)  # 选中时文字变绿色
        else:
            # 未选中状态，恢复原始文本
            self.label.text = self.label.text.split(' (已选择)')[0]
            self.label.color = (0.9, 0.9, 0.9, 1)  # 未选中时恢复灰色