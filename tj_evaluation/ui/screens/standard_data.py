from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from tkinter import Tk, filedialog
import json
import os

class StandardDataEditor(BoxLayout):
    """标准数据文档编辑器"""
    
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = main_layout
        self.orientation = 'vertical'
        self.spacing = dp(15)  # 增加主间距
        self.padding = [dp(20), dp(15), dp(20), dp(15)]  # 增加内边距
        
        # 标准数据结构模板 - 默认空列表
        self.standard_data = {
            "standard_data": {
                "data": {
                    "0": [],  # 任职情况
                    "1": [],  # 自述报告
                    "2": [],  # 相关活动
                    "3": [],  # 日常表现
                    "4": [],  # 个人荣誉
                    "5": [],  # 社团活动
                    "6": [],  # 研究性学习
                    "7": [],  # 优势学科
                    "8": [],  # 社会实践
                    "9": [],  # 课外体育修习
                    "10": [],  # 体育比赛
                    "11": [],  # 阳光体育出勤
                    "12": [],  # 心理素质展示
                    "13": [],  # 课外艺术修习
                    "14": [],  # 艺术实践活动
                    "15": []   # 艺术欣赏经历
                }
            }
        }
        
        # 部分名称映射
        self.section_names = {
            "0": "任职情况",
            "1": "自述报告",
            "2": "相关活动",
            "3": "日常表现",
            "4": "个人荣誉",
            "5": "社团活动",
            "6": "研究性学习",
            "7": "优势学科",
            "8": "社会实践",
            "9": "课外体育修习",
            "10": "体育比赛",
            "11": "阳光体育出勤",
            "12": "心理素质展示",
            "13": "课外艺术修习",
            "14": "艺术实践活动",
            "15": "艺术欣赏经历"
        }
        
        self.create_ui()
    
    def create_ui(self):
        """创建用户界面"""
        # 标题
        title_label = Label(
            text="标准数据文档制作",
            font_size=dp(28),
            size_hint_y=None,
            height=dp(60),
            color=(0.2, 0.5, 0.8, 1),
            bold=True
        )
        self.add_widget(title_label)
    
    # 文件操作区域
        file_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15),
            padding=[0, dp(10), 0, dp(10)]
        )
    
        self.filename_input = TextInput(
            hint_text="输入文件名",
            size_hint_x=0.6,
            font_size=dp(16),
            height=dp(45),
         padding=[dp(12), dp(12), dp(12), dp(12)]
        )
        file_layout.add_widget(self.filename_input)
    
        save_btn = Button(
            text="保存标准数据",
            size_hint_x=0.2,
            height=dp(45),
            background_color=(0.2, 0.8, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14),
            bold=True
        )
        save_btn.bind(on_press=self.save_standard_data)
        file_layout.add_widget(save_btn)
    
        load_btn = Button(
            text="加载标准数据",
            size_hint_x=0.2,
            height=dp(45),
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14),
            bold=True
        )
        load_btn.bind(on_press=self.load_standard_data)
        file_layout.add_widget(load_btn)
        
        self.add_widget(file_layout)
        
        # 红色提示信息
        warning_layout = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            padding=[dp(10), dp(5), dp(10), dp(5)]
        )
        
        warning_label = Label(
            text="注意：请将不想检查的项目/条目留空，则在自动检查中会自动跳过此项/此条",
            font_size=dp(14),
            color=(1, 0, 0, 1),  # 红色
            bold=True,
            halign='center',
            valign='middle'
        )
        warning_label.bind(size=warning_label.setter('text_size'))
        warning_layout.add_widget(warning_label)
        self.add_widget(warning_layout)
        
        # 创建滚动视图（其余代码保持不变）
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=dp(10),
            bar_color=[0.2, 0.5, 0.8, 0.8],
            bar_inactive_color=[0.2, 0.5, 0.8, 0.3]
        )
        
        self.content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(10), dp(15), dp(10), dp(15)],
            size_hint_y=None
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        scroll_view.add_widget(self.content_layout)
        self.add_widget(scroll_view)
        
        # 加载编辑器内容
        self.load_sections()
    
    def load_sections(self):
        """加载所有部分的编辑器"""
        self.content_layout.clear_widgets()
        
        for section_id, section_data in self.standard_data["standard_data"]["data"].items():
            section_card = self.create_section_editor(section_id, section_data)
            self.content_layout.add_widget(section_card)
    
    def create_section_editor(self, section_id, section_data):
        """创建部分的编辑器卡片"""
        # 创建卡片容器
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(15),  # 卡片内部间距
            padding=[dp(20), dp(15), dp(20), dp(15)]
        )
        card.bind(minimum_height=card.setter('height'))
        
        # 标题和操作区域
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        section_name = self.section_names.get(section_id, f"部分 {section_id}")
        title_label = Label(
            text=f"{section_name} ({len(section_data)}项)",
            font_size=dp(20),
            size_hint_x=0.7,
            color=(0.2, 0.5, 0.8, 1),
            bold=True,
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        add_btn = Button(
            text="+ 添加",
            size_hint_x=0.3,
            height=dp(40),
            background_color=(0.2, 0.8, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(14),
            bold=True
        )
        add_btn.bind(on_press=lambda instance, sid=section_id: self.add_sub_item(sid))
        
        header.add_widget(title_label)
        header.add_widget(add_btn)
        card.add_widget(header)
        
        # 子项容器
        self.items_container = BoxLayout(
            orientation='vertical',
            spacing=dp(12),  # 子项间距
            size_hint_y=None
        )
        self.items_container.bind(minimum_height=self.items_container.setter('height'))
        
        # 加载现有子项
        for i, item_data in enumerate(section_data):
            item_editor = self.create_item_editor(section_id, i, item_data)
            self.items_container.add_widget(item_editor)
        
        card.add_widget(self.items_container)
        
        return card
    
    def create_item_editor(self, section_id, item_index, item_data):
        """创建单个项目的编辑器"""
        fields = self.get_fields_for_section(section_id)
        
        # 项目容器
        item_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(8),
            padding=[dp(15), dp(12), dp(15), dp(12)]
        )
        item_box.bind(minimum_height=item_box.setter('height'))
        
        # 项目头部
        header = BoxLayout(
            size_hint_y=None,
            height=dp(35),
            spacing=dp(10)
        )
        
        item_label = Label(
            text=f"第{item_index + 1}项",
            font_size=dp(16),
            color=(0.5, 0.7, 0.9, 1),
            bold=True,
            size_hint_x=0.7,
            halign='left',
            valign='middle'
        )
        item_label.bind(size=item_label.setter('text_size'))
        
        delete_btn = Button(
            text="删除",
            size_hint_x=0.3,
            height=dp(30),
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=dp(12)
        )
        delete_btn.bind(on_press=lambda instance, sid=section_id, idx=item_index: self.delete_sub_item(sid, idx))
        
        header.add_widget(item_label)
        header.add_widget(delete_btn)
        item_box.add_widget(header)
        
        # 字段编辑器
        for field_name, field_key in fields.items():
            field_layout = BoxLayout(
                size_hint_y=None,
                height=dp(45),
                spacing=dp(10)
            )
            
            field_label = Label(
                text=field_name,
                size_hint_x=0.3,
                font_size=dp(14),
                color=(0.4, 0.4, 0.4, 1),
                halign='right',
                valign='middle'
            )
            field_label.bind(size=field_label.setter('text_size'))
            
            value = item_data.get(field_key, "empty")
            if value == "empty":
                value = ""
            
            text_input = TextInput(
                text=str(value),
                multiline=False,
                size_hint_x=0.7,
                font_size=dp(14),
                padding=[dp(8), dp(8), dp(8), dp(8)]
            )
            text_input.bind(text=lambda instance, value, sid=section_id, idx=item_index, key=field_key: self.update_item_field(sid, idx, key, value))
            
            field_layout.add_widget(field_label)
            field_layout.add_widget(text_input)
            item_box.add_widget(field_layout)
        
        return item_box
    
    def get_fields_for_section(self, section_id):
        """获取部分的字段配置"""
        field_configs = {
            "0": {"姓名": "name", "任职岗位": "drzw", "开始时间": "kssj", "结束时间": "jssj", "职务描述": "zwms"},
            "1": {"自述报告":""},
            "2": {"活动类别": "hdlb", "活动级别": "hdjb", "活动次数": "hdcs", "活动描述": "hdms"},
            "3": {"日常中的突出表现": "rcbx"},
            "4": {"提示": "notSupport"},
            "5": {"开始时间": "sthdkssj", "结束时间": "sthdjssj", "活动地点": "sthdhddd", "活动内容": "sthdhdnr", "活动效果和个人表现": "sthdhdxghgrbx"},
            "6": {"开始时间": "kssj", "结束时间": "jssj", "课题名称": "ktmc", "内容摘要": "nrzy", "指导教师": "zdls", "是否申请专利": "sfsqzl", "级别": "jb"},
            "7": {"开始时间": "kssj", "结束时间": "jssj", "活动名称": "hdmc", "表现": "bx"},
            "8": {"开始时间": "kssj", "结束时间": "jssj", "项目类别": "xmlb", "地点": "dd", "内容": "nr", "表现或成果": "bxhcg"},
            "9": {"项目": "xiangmu", "时间": "sj", "修习水平": "xxsp"},
            "10": {"提示": "notSupport"},
            "11": {"本学期阳光体育出勤": "ygtycq"},
            "12": {"心理素质展示": "xlszzs"},
            "13": {"项目": "xiangmu", "时间": "sj", "修习水平": "xxsp"},
            "14": {"提示": "notSupport"},
            "15": {"时间": "sj", "内容": "nr"}
        }
        return field_configs.get(section_id, {"名称": "name", "时间": "time", "描述": "description"})
    
    def add_sub_item(self, section_id):
        """添加子项"""
        # 检查是否为不支持的项目
        unsupported_sections = ["4", "10", "14"]
        if section_id in unsupported_sections:
            self.show_message("暂时不支持该项")
            return
            
        fields = self.get_fields_for_section(section_id)
        new_item = {key: "empty" for key in fields.values()}
        
        self.standard_data["standard_data"]["data"][section_id].append(new_item)
        self.load_sections()
    
    def delete_sub_item(self, section_id, item_index):
        """删除子项"""
        if 0 <= item_index < len(self.standard_data["standard_data"]["data"][section_id]):
            del self.standard_data["standard_data"]["data"][section_id][item_index]
            self.load_sections()
    
    def update_item_field(self, section_id, item_index, field_key, value):
        """更新子项字段"""
        if value.strip() == "":
            value = "empty"
        
        if 0 <= item_index < len(self.standard_data["standard_data"]["data"][section_id]):
            self.standard_data["standard_data"]["data"][section_id][item_index][field_key] = value
    
    def save_standard_data(self, instance):
        """保存标准数据"""
        try:
            filename = self.filename_input.text.strip()
            if not filename:
                filename = "standard_data_template"
            
            if not filename.endswith('.json'):
                filename += '.json'
            
            # 使用tkinter选择保存位置
            try:
                root = Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                    initialfile=filename,
                    title="保存到本地"
                )
                root.destroy()
                
                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.standard_data, f, ensure_ascii=False, indent=4)
                    
                    self.show_message(f"标准数据已保存到：{os.path.basename(file_path)}")
                else:
                    self.show_message("取消保存")
                    
            except ImportError:
                # 如果tkinter不可用，使用默认路径
                file_path = os.path.join(os.getcwd(), filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.standard_data, f, ensure_ascii=False, indent=4)
                
                self.show_message(f"标准数据已保存到：{file_path}")
                
        except Exception as e:
            self.show_message(f"保存失败：{str(e)}")
    
    def load_standard_data(self, instance):
        """加载标准数据"""
        try:
            root = Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="选择标准数据文件"
            )
            root.destroy()
            
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                if "standard_data" in loaded_data and "data" in loaded_data["standard_data"]:
                    self.standard_data = loaded_data
                    self.load_sections()
                    self.show_message(f"已加载：{os.path.basename(file_path)}")
                else:
                    self.show_message("文件格式不正确")
            else:
                self.show_message("取消加载")
                
        except Exception as e:
            self.show_message(f"加载失败：{str(e)}")
    
    def show_message(self, message):
        """显示消息"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        
        popup = Popup(
            title="提示",
            content=Label(text=message),
            size_hint=(None, None),
            size=(dp(300), dp(150))
        )
        popup.open()