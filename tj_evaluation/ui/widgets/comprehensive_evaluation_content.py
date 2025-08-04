from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget  # 新增这行导入
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.metrics import dp
class ComprehensiveEvaluationContent(BoxLayout):
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.main_layout = main_layout
        self.current_data_type = 0
        self.current_subitem = 0

        # 创建按钮区域
        self.button_area = ScrollView(size_hint=(1, 0.2))
        self.button_grid = GridLayout(cols=6, spacing=dp(10), padding=dp(10), size_hint_y=None)
        self.button_grid.bind(minimum_height=self.button_grid.setter('height'))
        self.button_area.add_widget(self.button_grid)
        self.add_widget(self.button_area)

        # 创建子项导航区域
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

        # 创建信息显示区域
        self.info_area = BoxLayout(orientation='horizontal', spacing=dp(30), padding=dp(20), size_hint=(1, 0.7))
        self.add_widget(self.info_area)

        # 左侧信息区域
        self.info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        self.info_area.add_widget(self.info_layout)

        # 生成模拟数据
        self.simulated_data = {}

        # 创建数据类型按钮
        self.data_types = [
            "任职情况", "自述报告", "相关活动", "日常表现", "个人荣誉",
            "社团活动", "研究性学习", "优势学科", "社会实践", "课外体育修习",
            "体育比赛", "阳光体育出勤", "心理素质展示", "课外艺术修习", "艺术实践活动", "艺术欣赏经历",
        ]

        for i, data_type in enumerate(self.data_types):
            btn = Button(
                text=data_type,
                background_color=(0.2, 0.5, 0.8, 1),
                color=(1, 1, 1, 1),
                font_size=dp(14),
                size_hint_y=None,
                height=dp(40)
            )
            btn.bind(on_press=lambda instance, idx=i: self.load_data_type(idx))
            self.button_grid.add_widget(btn)

            # 默认选中第一个按钮
            if i == 0:
                btn.background_color = (0.4, 0.7, 1, 1)
                self.load_data_type(0)

    def update_simulated_data(self, new_data):
        """更新模拟数据并刷新当前显示"""
        # 特殊处理自述报告数据
        for key, value in new_data.items():
            if key == 1 and isinstance(value, str):  # 自述报告
                new_data[key] = [value]  # 将字符串包装为列表

        self.simulated_data = new_data
        # 重新加载当前数据类型以显示新数据
        self.load_data_type(self.current_data_type)

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
        subitems = self.simulated_data.get(self.current_data_type, [])
        total_subitems = len(subitems)

        # 特殊处理自述报告，始终显示为1/1
        if self.current_data_type == 1:
            self.count_label.text = f"自述报告1/1"
            self.prev_button.disabled = True
            self.next_button.disabled = True
            self.prev_button.background_color = (0.7, 0.7, 0.7, 1)
            self.next_button.background_color = (0.7, 0.7, 0.7, 1)
        else:
            if subitems:
                data_type_name = self.data_types[self.current_data_type]
                self.count_label.text = f"{data_type_name}{self.current_subitem + 1}/{total_subitems}"

                self.prev_button.disabled = self.current_subitem == 0
                self.next_button.disabled = self.current_subitem == total_subitems - 1

                self.prev_button.background_color = (0.2, 0.6, 0.3, 1) if not self.prev_button.disabled else (0.7, 0.7,
                                                                                                              0.7, 1)
                self.next_button.background_color = (0.2, 0.6, 0.3, 1) if not self.next_button.disabled else (0.7, 0.7,
                                                                                                              0.7, 1)
            else:
                self.count_label.text = "无数据"
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
