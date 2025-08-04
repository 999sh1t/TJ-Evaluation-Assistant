from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from tj_evaluation.ui.widgets.custom_checkbox import CustomCheckBox
class ManualCheckSelectionContent(BoxLayout):
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.main_layout = main_layout  # 保存主布局引用
        self.padding = dp(10)
        self.spacing = dp(5)
        title_label = Label(
            text='手动选择检查项目',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(40),
            color=(0.95, 0.95, 0.95, 1)
        )
        self.add_widget(title_label)

        # 创建滚动视图
        scroll_view = ScrollView(size_hint=(1, 0.85))

        # 创建包含所有项目的网格布局
        grid_layout = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            padding=dp(5)
        )
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # 项目列表
        projects = [
            "任职情况", "自述报告", "相关活动", "日常表现", "个人荣誉",
            "社团活动", "研究性学习", "优势学科", "社会实践", "课外体育修习",
            "体育比赛", "阳光体育出勤", "心理素质展示", "课外艺术修习",
            "艺术实践活动", "艺术欣赏经历"
        ]

        # 存储所有复选框引用
        self.checkboxes = {}

        # 为每个项目创建自定义复选框
        for project in projects:
            custom_checkbox = CustomCheckBox(text=project)
            self.checkboxes[project] = custom_checkbox.checkbox
            grid_layout.add_widget(custom_checkbox)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

        # 创建底部按钮布局
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=dp(10)
        )

        # 返回按钮
        back_button = Button(
            text='返回',
            font_size=dp(16),
            size_hint_x=0.5,
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=lambda x: self.main_layout.show_screen('综评检查'))

        # 确认按钮
        confirm_button = Button(
            text='确认选择',
            font_size=dp(16),
            size_hint_x=0.5,
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        confirm_button.bind(on_press=self.on_confirm)

        bottom_layout.add_widget(back_button)
        bottom_layout.add_widget(confirm_button)
        self.add_widget(bottom_layout)
        # 项目列表与数据类型索引的映射（与ComprehensiveEvaluationContent对应）
        self.project_to_index = {
            "任职情况": 0, "自述报告": 1, "相关活动": 2, "日常表现": 3,
            "个人荣誉": 4, "社团活动": 5, "研究性学习": 6, "优势学科": 7,
            "社会实践": 8, "课外体育修习": 9, "体育比赛": 10, "阳光体育出勤": 11,
            "心理素质展示": 12, "课外艺术修习": 13, "艺术实践活动": 14, "艺术欣赏经历": 15
        }

    def on_confirm(self, instance):
        # 处理选中的项目
        selected_projects = [project for project, checkbox in self.checkboxes.items() if checkbox.active]
        if not selected_projects:
            # 显示提示：未选择项目
            popup = Popup(
                title='提示',
                content=Label(text='请至少选择一个项目'),
                size_hint=(None, None),
                size=(dp(300), dp(200)),
                auto_dismiss=False
            )
            ok_btn = Button(text='确定')
            ok_btn.bind(on_press=popup.dismiss)
            popup.content = BoxLayout(orientation='vertical', padding=dp(20))
            popup.content.add_widget(Label(text='请至少选择一个项目'))
            popup.content.add_widget(ok_btn)
            popup.open()
            return

        # 将项目名称转换为对应的索引（与ComprehensiveEvaluationContent对应）
        selected_indices = [self.project_to_index[proj] for proj in selected_projects]

        # 显示提示
        content_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content_layout.add_widget(Label(text=f'已选择 {len(selected_projects)} 个项目'))
        confirm_btn = Button(
            text='确定',
            size_hint=(1, 0.5),
            background_color=(0.2, 0.6, 0.9, 1)
        )

        popup = Popup(
            title='选择完成',
            content=content_layout,
            size_hint=(None, None),
            size=(dp(300), dp(200)),
            auto_dismiss=False,
        )

        def go_to_new_screen(instance):
            popup.dismiss()
            # 跳转到主界面并传递选中的索引
            self.main_layout.manual_check_main_content.set_selected_items(selected_indices)
            self.main_layout.show_screen('手动检查主界面')

        confirm_btn.bind(on_press=go_to_new_screen)
        content_layout.add_widget(confirm_btn)
        popup.open()


class ManualCheckScreenMain(BoxLayout):
    def __init__(self, main_layout, zpjc_instance, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.main_layout = main_layout
        self.zpjc = zpjc_instance
        self.selected_indices = []
        self.issues = []
        self.current_data_type = 0
        self.now_chosen = 0
        self.simulated_data = {}
        self.user_status = {}  # 记录用户检查状态 {username: {"status": "pass"/"markwrong", "selected_type": type}}

        # 顶部区域
        self.top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=[dp(10), dp(5)]
        )

        # 返回按钮区域
        back_button_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(180), dp(40)),
            spacing=dp(5)
        )

        # 返回选择按钮
        self.back_select_button = Button(
            text="返回选择",
            size_hint=(None, None),
            size=(dp(85), dp(40)),
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14)
        )
        self.back_select_button.bind(on_press=lambda x: self.main_layout.show_screen('手动检查'))

        # 返回主界面按钮
        self.back_main_button = Button(
            text="返回检查主界面",
            size_hint=(None, None),
            size=(dp(85), dp(40)),
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(12)
        )
        self.back_main_button.bind(on_press=lambda x: self.main_layout.show_screen('综评检查'))

        back_button_container.add_widget(self.back_select_button)
        back_button_container.add_widget(self.back_main_button)

        # 标题区域
        title_area = BoxLayout(orientation='horizontal', size_hint_x=1)
        self.title_label = Label(
            text="手动检查 - 选中项目",
            font_size=dp(20),
            size_hint_x=1,
            halign='left',
            valign='middle',
            padding=[dp(10), 0]
        )
        title_area.add_widget(self.title_label)

        # 用户导航按钮区域
        self.user_nav_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(300), dp(40)),
            spacing=dp(10)
        )
        # 组装顶部栏
        self.top_bar.add_widget(back_button_container)
        self.top_bar.add_widget(title_area)
        self.add_widget(self.top_bar)

        # 当前用户显示标签
        self.current_user_label = Label(
            text="当前用户: ",
            font_size=dp(16),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.current_user_label)

        # 用户状态提示
        self.user_status_label = Label(
            text="用户状态:未检查",
            font_size=dp(16),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(40),
            color=(1, 0, 0, 1)
        )
        self.add_widget(self.user_status_label)

        # 操作按钮区域
        self.buttons_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            padding=dp(20),
            spacing=dp(15)
        )

        # 占位空间
        self.buttons_container.add_widget(Widget(size_hint_x=1))

        # 标记为错误按钮
        self.mark_error_btn = Button(
            text="标记为错误",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            disabled=False
        )
        self.mark_error_btn.bind(on_press=lambda x: self.set_user_status("markwrong"))
        self.buttons_container.add_widget(self.mark_error_btn)

        # 通过按钮
        self.pass_btn = Button(
            text="通过",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            disabled=False
        )
        self.pass_btn.bind(on_press=lambda x: self.set_user_status("pass"))
        self.buttons_container.add_widget(self.pass_btn)

        self.add_widget(self.buttons_container)

        # 项目按钮区域
        self.button_area = ScrollView(size_hint=(1, 0.2))
        self.button_grid = GridLayout(cols=6, spacing=dp(10), padding=dp(10), size_hint_y=None)
        self.button_grid.bind(minimum_height=self.button_grid.setter('height'))
        self.button_area.add_widget(self.button_grid)
        self.add_widget(self.button_area)

        # 用户导航按钮区域（新增）
        self.user_navigation_area = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            padding=dp(20),
            spacing=dp(15)
        )
        
        # 占位空间
        self.user_navigation_area.add_widget(Widget(size_hint_x=1))
        
        # 上一个用户按钮
        self.prev_user_btn = Button(
            text="上一个用户",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            background_color=(0.6, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        self.prev_user_btn.bind(on_press=self.prev_user)
        self.user_navigation_area.add_widget(self.prev_user_btn)
        
        # 下一个用户按钮
        self.next_user_btn = Button(
            text="下一个用户",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            background_color=(0.6, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        )
        self.next_user_btn.bind(on_press=self.next_user)
        self.user_navigation_area.add_widget(self.next_user_btn)
        
        self.add_widget(self.user_navigation_area)

        # 子项导航区域
        self.subitem_nav_area = BoxLayout(size_hint=(1, 0.15), padding=[dp(20), 0])
        self.left_spacer = Widget(size_hint_x=0.3)
        self.subitem_nav_area.add_widget(self.left_spacer)

        self.control_container = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(250), spacing=dp(5))
        self.button_row = BoxLayout(spacing=dp(5))

        self.prev_button = Button(
            text="上一条",
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            size_hint=(None, 1),
            width=dp(120)
        )
        self.prev_button.bind(on_press=self.prev_subitem)
        self.button_row.add_widget(self.prev_button)

        self.next_button = Button(
            text="下一条",
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            size_hint=(None, 1),
            width=dp(120)
        )
        self.next_button.bind(on_press=self.next_subitem)
        self.button_row.add_widget(self.next_button)

        self.control_container.add_widget(self.button_row)
        self.count_label = Label(
            text="1/1",
            font_size=dp(16),
            color=get_color_from_hex('#0066CC'),
            halign='center'
        )
        self.control_container.add_widget(self.count_label)
        self.subitem_nav_area.add_widget(self.control_container)
        self.right_spacer = Widget(size_hint_x=0.3)
        self.subitem_nav_area.add_widget(self.right_spacer)
        self.add_widget(self.subitem_nav_area)

        # 信息显示区域
        self.info_area = BoxLayout(orientation='horizontal', spacing=dp(30), padding=dp(20), size_hint=(1, 0.7))
        self.add_widget(self.info_area)

        self.info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        self.info_area.add_widget(self.info_layout)
        # 数据类型列表（与ComprehensiveEvaluationContent保持一致）
        self.data_types = [
            "任职情况", "自述报告", "相关活动", "日常表现", "个人荣誉",
            "社团活动", "研究性学习", "优势学科", "社会实践", "课外体育修习",
            "体育比赛", "阳光体育出勤", "心理素质展示", "课外艺术修习", "艺术实践活动", "艺术欣赏经历",
        ]
        self.choose_different_users_data(type="first")

    # 以下方法与之前保持一致（set_selected_items、load_data_type等）
    def set_selected_items(self, selected_indices):
        """接收选中的项目索引，生成对应按钮并显示第一个项目"""
        self.selected_indices = selected_indices
        if not self.selected_indices:
            return

        # 清空现有按钮，只添加选中的项目
        self.button_grid.clear_widgets()
        for idx in self.selected_indices:
            btn = Button(
                text=self.data_types[idx],
                background_color=(0.2, 0.5, 0.8, 1),
                color=(1, 1, 1, 1),
                font_size=dp(14),
                size_hint_y=None,
                height=dp(40)
            )
            btn.bind(on_press=lambda instance, i=idx: self.load_data_type(i))
            self.button_grid.add_widget(btn)

        # 默认显示第一个选中的项目
        self.current_data_type = self.selected_indices[0]
        self.load_data_type(self.current_data_type)

        # 更新标题
        self.title_label.text = f"手动检查 - 共 {len(self.selected_indices)} 个项目"
    def set_user_status(self, status):
        """设置用户状态并同步更新到evaluation_check_content"""
        users = self.main_layout.user_manager.get_all_users()
        if not users or self.now_chosen >= len(users):
            return
            
        username = users[self.now_chosen]
        xm = self.main_layout.user_manager.get_user_data(username).get('xm', username)
        current_section = self.data_types[self.current_data_type]
        
        # 更新本地状态
        self.user_status[username] = {
            "status": status,
            "selected_type": self.current_data_type,
            "section_name": current_section
        }
        
        if status == "pass":
            # 标记为通过：删除该用户的手动issues
            self.zpjc.remove_manual_issues(username, current_section)
            
            # 检查是否还有自动检查的issues
            auto_issues = self.main_layout.compare_user_data(
                self.main_layout.user_manager.get_user_data(username), 
                self.zpjc.standard_data
            )
            
            if auto_issues:
                # 还有自动检查的issues
                self.zpjc.update_user_status(username, f"{xm} ({username}) - 有问题(自动检查)", (0.8, 0.2, 0.2, 1))
            else:
                # 完全通过
                self.zpjc.update_user_status(username, f"{xm} ({username}) - 已通过", (0.2, 0.6, 0.3, 1))
                
        elif status == "markwrong":
            # 标记为错误：添加手动issue
            current_issue = {
                "section_name": current_section,
                "issue_type": "manual",
                "description": "手动标记的错误"
            }
            
            # 先删除同部分的手动issues（避免重复）
            self.zpjc.remove_manual_issues(username, current_section)
            
            # 再添加新的手动issue
            self.zpjc.record_manual_issue(username, current_issue)
            self.zpjc.update_user_status(username, f"{xm} ({username}) - 有问题(手动标记)", (0.8, 0.2, 0.2, 1))
        
        # 更新本地标签显示
        self.update_user_status_label()
        
        # 继续处理下一个用户
        self.choose_different_users_data(type=status)
    def choose_different_users_data(self, type):
        """选择不同用户数据时更新用户状态标签"""
        all_data = []
        users = self.main_layout.user_manager.get_all_users()
        if not users:
            return
        for username in users:
            all_data.append(self.main_layout.user_manager.get_user_data(username))
        self.users_number = len(all_data)

        if type == "first":
            self.update_simulated_data(all_data[0])
            self.update_user_status_label()  # 添加状态标签更新
        elif type in ("pass", "markwrong"):
            if type == "pass":
                if self.now_chosen + 1 < self.users_number:
                    self.now_chosen += 1
                    self.update_simulated_data(all_data[self.now_chosen])
                    self.update_user_status_label()  # 添加状态标签更新
                else:
                    popup = Popup(
                        title='完成',
                        content=Label(text='已完成所有用户的检查'),
                        size_hint=(None, None),
                        size=(dp(300), dp(150))
                    )
                    popup.open()
            else:  # markwrong
                current_issue = {
                    "section_name": self.data_types[self.current_data_type],
                    "issue_type": "manual",
                    "description": "手动标记的错误"
                }
                username = users[self.now_chosen]
                button = self.zpjc.user_buttons[username]
                button.disabled = False
                self.zpjc.record_manual_issue(username, current_issue)
                button.text = f"{button.text.split(' - ')[0]} - 有问题"
                button.background_color = (0.8, 0.2, 0.2, 1)

                if self.now_chosen + 1 < self.users_number:
                    self.now_chosen += 1
                    self.update_simulated_data(all_data[self.now_chosen])
                    self.update_user_status_label()  # 添加状态标签更新
                else:
                    popup = Popup(
                        title='完成',
                        content=Label(text='已完成所有用户的检查'),
                        size_hint=(None, None),
                        size=(dp(300), dp(150))
                    )
                    popup.open()
                self.update_user_status_label()

    def load_data_type(self, data_index):
        """加载特定类型的数据 - 可自定义各类型显示的字段"""
        self.current_data_type = data_index
        self.current_subitem = 0

        # 重置按钮颜色
        for i, child in enumerate(self.button_grid.children):
            if i == len(self.button_grid.children) - data_index - 1:
                child.background_color = (0.4, 0.7, 1, 1)
            else:
                child.background_color = (0.2, 0.5, 0.8, 1)

        # 清空当前信息区域
        self.info_layout.clear_widgets()
        self.info_grid = GridLayout(cols=2, spacing=dp(20), size_hint_y=None)
        self.info_grid.bind(minimum_height=self.info_grid.setter('height'))
        self.info_layout.add_widget(self.info_grid)

        # 根据数据类型添加不同的字段
        if data_index == 0:  # 任职情况
            self.add_label_pair("姓名:", "name")
            self.add_label_pair("任职岗位:", "drzw")
            self.add_label_pair("开始时间:", "kssj")
            self.add_label_pair("结束时间:", "jssj")
            self.add_label_pair("职务描述:", "zwms")
        elif data_index == 1:  # 自述报告
            self.info_grid.add_widget(Label(
                text="自述报告:",
                font_size=dp(18),
                halign='right',
                size_hint_y=None,
                height=dp(40)
            ))
            self.zsbg_label = Label(
                text="",
                font_size=dp(16),
                text_size=(None, None),
                halign='left',
                valign='top',
                size_hint_y=None
            )
            self.zsbg_label.bind(size=lambda s, w: s.setter('text_size')(s, (w[0], None)))
            self.info_grid.add_widget(self.zsbg_label)
        elif data_index == 2:
            self.add_label_pair("活动类别:", "hdlb")
            self.add_label_pair("活动级别", "hdjb")
            self.add_label_pair("活动次数", "hdcs")
            self.add_label_pair("活动描述", "hdms")
        elif data_index == 3:
            self.add_label_pair("日常中的突出表现:", "rcbx")
        elif data_index in (4, 10, 14):
            self.add_label_pair("提示:", "notSupport")
        # 可继续添加其他数据类型的字段配置
        elif data_index == 5:
            self.add_label_pair("开始时间:", "sthdkssj")
            self.add_label_pair("结束时间:", "sthdjssj")
            self.add_label_pair("活动地点:", "sthdhddd")
            self.add_label_pair("活动内容:", "sthdhdnr")
            self.add_label_pair("活动效果和个人表现:", "sthdhdxghgrbx")
        elif data_index == 6:
            self.add_label_pair("开始时间:", "kssj")
            self.add_label_pair("结束时间:", "jssj")
            self.add_label_pair("课题名称:", "ktmc")
            self.add_label_pair("内容摘要:", "nrzy")
            self.add_label_pair("指导教师:", "zdls")
            self.add_label_pair("是否申请专利:", "sfsqzl")
            self.add_label_pair("级别:", "jb")
        elif data_index == 7:
            self.add_label_pair("开始时间:", "kssj")
            self.add_label_pair("结束时间:", "jssj")
            self.add_label_pair("活动名称:", "hdmc")
            self.add_label_pair("表现:", "bx")
        elif data_index == 8:
            self.add_label_pair("开始时间:", "kssj")
            self.add_label_pair("结束时间:", "jssj")
            self.add_label_pair("项目类别:", "xmlb")
            self.add_label_pair("地点:", "dd")
            self.add_label_pair("内容:", "nr")
            self.info_grid.add_widget(Label(
                text="表现或成果:",
                font_size=dp(18),
                halign='right',
                size_hint_y=None,
                height=dp(40)
            ))
            self.bxhcg_label = Label(
                text="",
                font_size=dp(16),
                text_size=(None, None),
                halign='left',
                valign='top',
                size_hint_y=None
            )
            self.bxhcg_label.bind(size=lambda s, w: s.setter('text_size')(s, (w[0], None)))
            self.info_grid.add_widget(self.bxhcg_label)
        elif data_index in (9, 13):
            self.add_label_pair("项目:", "xiangmu")
            self.add_label_pair("时间:", "sj")
            self.add_label_pair("修习水平:", "xxsp")
        elif data_index == 11:
            self.add_label_pair("本学期阳光体育出勤:", "ygtycq")
        elif data_index == 12:
            self.info_grid.add_widget(Label(
                text="心理素质展示:",
                font_size=dp(18),
                halign='right',
                size_hint_y=None,
                height=dp(40)
            ))
            self.xlszzs_label = Label(
                text="",
                font_size=dp(16),
                text_size=(None, None),
                halign='left',
                valign='top',
                size_hint_y=None
            )
            self.xlszzs_label.bind(size=lambda s, w: s.setter('text_size')(s, (w[0], None)))
            self.info_grid.add_widget(self.xlszzs_label)
        elif data_index == 15:
            self.add_label_pair("时间:", "sj")
            self.info_grid.add_widget(Label(
                text="内容:",
                font_size=dp(18),
                halign='right',
                size_hint_y=None,
                height=dp(40)
            ))
            self.nr_label = Label(
                text="",
                font_size=dp(16),
                text_size=(None, None),
                halign='left',
                valign='top',
                size_hint_y=None
            )
            self.nr_label.bind(size=lambda s, w: s.setter('text_size')(s, (w[0], None)))
            self.info_grid.add_widget(self.nr_label)
        self.update_subitem_display()
        self.update_user_status_label()

    def add_label_pair(self, label_text, data_key):
        """辅助方法：添加标签对"""
        self.info_grid.add_widget(Label(
            text=label_text,
            font_size=dp(18),
            halign='right',
            size_hint_y=None,
            height=dp(40)
        ))

        # 创建对应的动态标签
        dynamic_label = Label(
            text="",
            font_size=dp(18),
            size_hint_y=None,
            height=dp(40)
        )

        # 将标签存储为类属性，以便后续更新
        setattr(self, f"{data_key}_label", dynamic_label)
        self.info_grid.add_widget(dynamic_label)

    def update_subitem_display(self):
        """更新子项显示"""
        # 获取当前用户信息
        users = self.main_layout.user_manager.get_all_users()
        username = users[self.now_chosen]
        user_data = self.main_layout.user_manager.get_user_data(username)
        xm = user_data.get('xm', username)  # 获取姓名，如果没有则使用用户名

        # 更新当前用户显示
        self.current_user_label.text = f"当前用户: {xm}"

        subitems = self.simulated_data.get(self.current_data_type, [])
        total_subitems = len(subitems)

        # 特殊处理自述报告，始终显示为1/1
        if self.current_data_type == 1:
            self.count_label.text = f"{xm}的自述报告1/1"
            self.prev_button.disabled = True
            self.next_button.disabled = True
            self.prev_button.background_color = (0.7, 0.7, 0.7, 1)
            self.next_button.background_color = (0.7, 0.7, 0.7, 1)
        else:
            if subitems:
                data_type_name = self.data_types[self.current_data_type]
                self.count_label.text = f"{xm}的{data_type_name}{self.current_subitem + 1}/{total_subitems}"

                self.prev_button.disabled = self.current_subitem == 0
                self.next_button.disabled = self.current_subitem == total_subitems - 1

                self.prev_button.background_color = (0.2, 0.6, 0.3, 1) if not self.prev_button.disabled else (0.7, 0.7,
                                                                                                              0.7, 1)
                self.next_button.background_color = (0.2, 0.6, 0.3, 1) if not self.next_button.disabled else (0.7, 0.7,
                                                                                                              0.7, 1)
            else:
                self.count_label.text = f"{xm}的此项无数据"
                self.prev_button.disabled = True
                self.next_button.disabled = True
                self.prev_button.background_color = (0.7, 0.7, 0.7, 1)
                self.next_button.background_color = (0.7, 0.7, 0.7, 1)
                # 当没有数据时，清空信息区域并直接返回
                self.info_layout.clear_widgets()
                no_info_label = Label(
                    text="无(学生未填报此项或本项为空)",
                    font_size=dp(24),
                    halign='center',
                    valign='middle'
                )
                self.info_layout.add_widget(no_info_label)
                return

        # 添加过渡动画
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(
            on_complete=lambda *args: self._update_info_content(subitems[self.current_subitem] if subitems else {}))
        anim.start(self.info_layout)

    def _update_info_content(self, data):
        """更新信息内容"""
        # 根据当前数据类型更新对应标签
        if self.current_data_type == 0:  # 任职情况
            self.name_label.text = data.get("name", "")
            self.drzw_label.text = data.get("drzw", "")
            self.kssj_label.text = data.get("kssj", "")
            self.jssj_label.text = data.get("jssj", "")
            self.zwms_label.text = data.get("zwms", "")
        elif self.current_data_type == 1:  # 自述报告
            self.zsbg_label.text = data if isinstance(data, str) else data.get("zsbg", "")
        elif self.current_data_type == 2:  # 相关活动
            self.hdlb_label.text = data.get("hdlb", "")
            self.hdjb_label.text = data.get("hdjb", "")
            self.hdcs_label.text = data.get("hdcs", "")
            self.hdms_label.text = data.get("hdms", "")
        elif self.current_data_type == 3:  # 日常表现
            self.rcbx_label.text = data.get("rcbx", "")
        elif self.current_data_type in (4, 10, 14):
            self.notSupport_label.text = data.get("tip", "")
        elif self.current_data_type == 5:  # 社团活动
            self.sthdkssj_label.text = data.get("sthdkssj", "")
            self.sthdjssj_label.text = data.get("sthdjssj", "")
            self.sthdhddd_label.text = data.get("sthdhddd", "")
            self.sthdhdnr_label.text = data.get("sthdhdnr", "")
            self.sthdhdxghgrbx_label.text = data.get("sthdhdxghgrbx", "")
        elif self.current_data_type == 6:
            self.kssj_label.text = data.get("kssj", "")
            self.jssj_label.text = data.get("jssj", "")
            self.ktmc_label.text = data.get("ktmc", "")
            self.nrzy_label.text = data.get("nrzy", "")
            self.zdls_label.text = data.get("zdls", "")
            self.sfsqzl_label.text = data.get("sfsqzl", "")
            self.jb_label.text = data.get("jb", "")
        elif self.current_data_type == 7:
            self.kssj_label.text = data.get("kssj", "")
            self.jssj_label.text = data.get("jssj", "")
            self.hdmc_label.text = data.get("hdmc", "")
            self.bx_label.text = data.get("bx", "")
        elif self.current_data_type == 8:
            self.kssj_label.text = data.get("kssj", "")
            self.jssj_label.text = data.get("jssj", "")
            self.xmlb_label.text = data.get("xmlb", "")
            self.dd_label.text = data.get("dd", "")
            self.nr_label.text = data.get("nr", "")
            self.bxhcg_label.text = data.get("bxhcg", "")
        elif self.current_data_type in (9, 13):
            self.xiangmu_label.text = data.get("xiangmu", "")
            self.sj_label.text = data.get("sj", "")
            self.xxsp_label.text = data.get("xxsp", "")
        elif self.current_data_type == 11:
            self.ygtycq_label.text = data.get("ygtycq", "")
        elif self.current_data_type == 12:
            self.xlszzs_label.text = data.get("xlszzs", "")
        elif self.current_data_type == 15:
            self.sj_label.text = data.get("sj", "")
            self.nr_label.text = data.get("nr", "")
        # 淡入动画
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self.info_layout)

    def prev_subitem(self, instance):
        """显示上一个子项"""
        if self.current_subitem > 0:
            self.current_subitem -= 1
            self.update_subitem_display()

    def next_subitem(self, instance):
        """显示下一个子项"""
        subitems = self.simulated_data.get(self.current_data_type, [])
        if self.current_subitem < len(subitems) - 1:
            self.current_subitem += 1
            self.update_subitem_display()

    def update_simulated_data(self, new_data):
        converted_data = {}
        for key, value in new_data.items():
            if key == 'xm':  # 保留姓名字段（非数字键）
                converted_data[key] = value
                continue
            try:
                # 尝试将字符串键转换为整数（如'0'→0）
                int_key = int(key)
                converted_data[int_key] = value
            except ValueError:
                # 非数字键忽略（避免报错）
                pass

        # 2. 特殊处理自述报告数据（保持原逻辑）
        for key, value in converted_data.items():
            if key == 1 and isinstance(value, str):  # 自述报告
                converted_data[key] = [value]  # 将字符串包装为列表

        # 3. 更新模拟数据并刷新显示
        self.simulated_data = converted_data
        self.load_data_type(self.current_data_type)  # 重新加载当前类
        self.update_user_status_label()
    def prev_user(self, instance):
        """切换到上一个用户"""
        if self.now_chosen > 0:
            self.now_chosen -= 1
            all_data = []
            users = self.main_layout.user_manager.get_all_users()
            for username in users:
                all_data.append(self.main_layout.user_manager.get_user_data(username))
            self.update_simulated_data(all_data[self.now_chosen])
            self.update_user_status_label()  # 更新状态标签和按钮状态

    def next_user(self, instance):
        """切换到下一个用户"""
        all_data = []
        users = self.main_layout.user_manager.get_all_users()
        for username in users:
            all_data.append(self.main_layout.user_manager.get_user_data(username))
        
        if self.now_chosen + 1 < len(all_data):
            self.now_chosen += 1
            self.update_simulated_data(all_data[self.now_chosen])
            self.update_user_status_label()  # 更新状态标签和按钮状态
    def update_user_status_label(self):
        """更新用户状态标签显示和按钮状态"""
        users = self.main_layout.user_manager.get_all_users()
        if not users or self.now_chosen >= len(users):
            return
            
        username = users[self.now_chosen]
        
        # 重置按钮状态为启用
        self.mark_error_btn.disabled = False
        self.pass_btn.disabled = False
        
        # 检查当前数据类型的状态
        if username in self.user_status:
            user_type_status = self.user_status[username].get("type_status", {})
            current_type_status = user_type_status.get(self.current_data_type)
            
            if current_type_status == "pass":
                self.user_status_label.text = f"当前数据类型状态:已通过 ({self.data_types[self.current_data_type]})"
                self.user_status_label.color = (0, 1, 0, 1)  # 绿色
                self.pass_btn.disabled = True  # 当前类型已通过，禁用通过按钮
            elif current_type_status == "markwrong":
                self.user_status_label.text = f"当前数据类型状态:已标记错误 ({self.data_types[self.current_data_type]})"
                self.user_status_label.color = (1, 0.5, 0, 1)  # 橙色
                self.mark_error_btn.disabled = True  # 当前类型已标记错误，禁用标记按钮
            else:
                self.user_status_label.text = f"当前数据类型状态:未检查 ({self.data_types[self.current_data_type]})"
                self.user_status_label.color = (1, 0, 0, 1)  # 红色
        else:
            self.user_status_label.text = f"当前数据类型状态:未检查 ({self.data_types[self.current_data_type]})"
            self.user_status_label.color = (1, 0, 0, 1)  # 红色

    def set_user_status(self, status):
        """设置当前数据类型的状态"""
        users = self.main_layout.user_manager.get_all_users()
        if not users or self.now_chosen >= len(users):
            return
            
        username = users[self.now_chosen]
        xm = self.main_layout.user_manager.get_user_data(username).get('xm', username)
        
        # 初始化或更新用户状态数据结构
        if username not in self.user_status:
            self.user_status[username] = {"type_status": {}}
        
        # 记录当前数据类型的状态
        self.user_status[username]["type_status"][self.current_data_type] = status
        
        # 同步更新evaluation_check_content中的显示
        type_name = self.data_types[self.current_data_type]
        if status == "pass":
            self.zpjc.update_user_status(username, f"{xm} ({username}) - {type_name}已通过", (0.2, 0.6, 0.3, 1))
        elif status == "markwrong":
            current_issue = {
                "section_name": type_name,
                "issue_type": "manual",
                "description": f"{type_name}部分被手动标记为错误"
            }
            self.zpjc.record_manual_issue(username, current_issue)
            self.zpjc.update_user_status(username, f"{xm} ({username}) - {type_name}有问题", (0.8, 0.2, 0.2, 1))
        
        # 更新本地标签显示
        self.update_user_status_label()
        self.choose_different_users_data(type=status)

class ManualCheckScreen(Screen):
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ManualCheckSelectionContent(main_layout))
class ManualCheckMainScreen(Screen):
    def __init__(self, main_layout, zpjc_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ManualCheckScreenMain(main_layout, zpjc_instance))