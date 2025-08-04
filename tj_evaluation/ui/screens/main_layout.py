from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.popup import Popup
import json
# 修正导入语句，移除重复项
from tj_evaluation.ui.widgets.comprehensive_evaluation_content import ComprehensiveEvaluationContent
from tj_evaluation.ui.widgets.evaluation_check_content import EvaluationCheckContent
# 修正导入的类名
from tj_evaluation.ui.screens.manual import ManualCheckScreen, ManualCheckScreenMain, ManualCheckSelectionContent
from tj_evaluation.core.user_manager import UserManager
from tj_evaluation.core.api import extract_xn_xq_xm, getInformatonData ,session
from tj_evaluation.ui.widgets.top_navigation import TopNavigation
from tj_evaluation.ui.screens.user_management import UserManagementScreen

class ScreenContent(BoxLayout):
    """屏幕内容容器类"""
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.title = title
        
    def set_content(self, content):
        """设置屏幕内容"""
        self.clear_widgets()
        self.add_widget(content)


class MainLayout(BoxLayout):
    current_user = StringProperty("未登录")
    is_logged_in = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # 初始化用户管理器
        self.user_manager = UserManager()

        # 顶部导航栏
        self.top_nav = TopNavigation()
        self.add_widget(self.top_nav)

        # 主内容区域
        self.screens = {}
        self.current_screen = None

        # 创建各个屏幕
        self.create_screens()

        # 默认显示首页
        self.show_screen('首页')

        # 更新用户按钮文本
        self.update_user_button()

    def update_user_button(self):
        """更新用户按钮文本"""
        current_user = self.user_manager.get_current_user()
        if current_user:
            self.top_nav.update_user_text(current_user)
            self.current_user = current_user
        else:
            self.top_nav.update_user_text("未登录")
            self.current_user = "未登录"

    def create_screens(self):
        # 首页
        home_screen = ScreenContent("首页")
        home_content = Label(
            text="欢迎使用本程序!\n\n请先登录账号",
            font_size=dp(20),
            halign='center',
            valign='middle'
        )
        home_screen.set_content(home_content)
        self.screens['首页'] = home_screen

        # 综评
        eval_screen = ScreenContent("综评")
        self.eval_content = ComprehensiveEvaluationContent(self)
        eval_screen.set_content(self.eval_content)
        self.screens['综评'] = eval_screen

        # 关于
        about_screen = ScreenContent("关于")
        about_content = Label(
            text="天津市综评自动化检查程序(教师端)\n版本:beta 1.0.0",
            font_size=dp(20),
            halign='center',
            valign='middle'
        )
        about_screen.set_content(about_content)
        self.screens['关于'] = about_screen

        # 用户管理
        user_management_screen = ScreenContent("用户管理")
        self.user_management_content = UserManagementScreen(self)
        user_management_screen.set_content(self.user_management_content)
        self.screens['用户管理'] = user_management_screen

        # 综评检查
        check_screen = ScreenContent("综评检查")
        self.check_content = EvaluationCheckContent(self)
        check_screen.set_content(self.check_content)
        self.screens['综评检查'] = check_screen

        # 手动检查
        manual_check_screen = ScreenContent("手动检查")
        self.manual_check_screen = ManualCheckScreen(self)  # 修正变量名
        manual_check_screen.set_content(self.manual_check_screen)
        self.screens['手动检查'] = manual_check_screen

        # 手动检查主界面
        manual_check_screen_main = ScreenContent("手动检查主界面")
        # 修正类名引用
        self.manual_check_selection_content = ManualCheckSelectionContent(self)
        self.manual_check_main_content = ManualCheckScreenMain(self, zpjc_instance=self.check_content)
        manual_check_screen_main.set_content(self.manual_check_main_content)
        self.screens['手动检查主界面'] = manual_check_screen_main

        # 标准数据制作
        standard_data_screen = ScreenContent("标准数据")
        from tj_evaluation.ui.screens.standard_data import StandardDataEditor
        self.standard_data_content = StandardDataEditor(self)
        standard_data_screen.set_content(self.standard_data_content)
        self.screens['标准数据'] = standard_data_screen
    def show_login_prompt(self):
        # 创建弹窗内容布局（垂直排列的标签和按钮）
        content_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 提示文本
        prompt_label = Label(
            text='请先登录账号',
            font_size=dp(16),
            halign='center'
        )
        content_layout.add_widget(prompt_label)

        # 确定按钮
        ok_button = Button(
            text='确定',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1)
        )

        # 创建弹窗（先定义，再绑定按钮事件）
        popup = Popup(
            title='登录提示',
            content=content_layout,
            size_hint=(None, None),
            size=(dp(300), dp(200)),
            auto_dismiss=False  # 关闭自动消失，只能通过按钮关闭
        )

        # 绑定按钮点击事件：关闭弹窗并跳转到用户管理界面
        ok_button.bind(on_press=lambda x: (popup.dismiss(), self.show_screen('用户管理')))
        content_layout.add_widget(ok_button)

        # 显示弹窗
        popup.open()

    def show_manual_check_main(self, selected_indices):
        """显示手动检查主界面并传递选中的项目索引"""
        self.show_screen('手动检查主界面')
        # 将选中的索引传递给主界面
        self.manual_check_main_content.set_selected_items(selected_indices) 

    def show_screen(self, screen_name):
        # 特殊处理登录页面
        if screen_name == "综评" and not self.is_logged_in:
            self.show_login_prompt()  # 显示登录提示
            return
        # 显示普通页面
        if screen_name in self.screens:
            if self.current_screen:
                self.remove_widget(self.current_screen)

            self.current_screen = self.screens[screen_name]
            self.add_widget(self.current_screen, index=1)
            self.top_nav.set_active_button(screen_name)

    def show_user_management(self):
        """显示用户管理页面"""
        # 刷新用户列表
        self.user_management_content.refresh_user_list()

        # 显示用户管理页面
        self.show_screen('用户管理')

    def compare_user_data(self, user_data, standard_data):
        issues = []  # 存储所有发现的问题
        # 遍历用户数据的每个部分
        for section_id, user_section in user_data.items():
            # 转换section_id为字符串以便统一比较
            section_id_str = str(section_id)
            # 检查标准数据中是否存在该部分
            if section_id_str not in standard_data['standard_data']['data']:
                continue
            std_section = standard_data['standard_data']['data'][section_id_str]
            section_name = self.eval_content.data_types[int(section_id)]  # 获取部分名称
            # 处理用户该部分的每个数据项
            if len(user_section) == 0:
                emptyi = 0
                if len(std_section) == 1:
                    for key, std_value in std_section[0].items():
                        if std_value == 'empty':
                            emptyi += 1
                    if emptyi != len(std_section[0]):
                        issues.append({
                            "section_name": section_name,
                            "issue_type": "用户漏填了此项",
                        })
                        return (issues)
                else:
                    for stdi in range(len(std_section)):
                        for key, std_value in std_section[stdi].items():
                            if std_value == "empty":
                                emptyi += 1
                            if emptyi != len(std_section) * len(std_section[0]):
                                issues.append({
                                    "section_name": section_name,
                                    "issue_type": "用户漏填了此项",
                                })
                                return (issues)
                continue
            elif not isinstance(user_section[0], dict):
                continue  # 跳过非字典格式的项
            elif len(user_section) != len(std_section):
                issues.append({
                    "section_name": section_name,
                    "issue_type": "存在多填/少填的情况",
                    "std_int": len(std_section),
                    "user_int": len(user_section),
                })
                continue
            if len(std_section) == 1:
                for key, std_value in std_section[0].items():
                    if std_value == "empty":
                        continue  # 跳过标记为empty的标准字段
                    user_value = user_section[0][key]
                    # 检查值是否匹配
                    if user_value != std_value:
                        issues.append({
                            "section_name": section_name,
                            "key": key,
                            "section_id": section_id,
                            "item_idx": 0,
                            "user_value": user_value,
                            "std_value": std_value,
                            "issue_type": "不匹配"
                        })
            else:
                for stdi in range(len(std_section)):
                    errori = 0
                    for key, std_value in std_section[stdi].items():
                        if std_value == "empty":
                            continue  # 跳过标记为empty的标准字段
                        user_value = user_section[stdi][key]
                        if user_value != std_value:
                            errori += 1
                        if errori == len(user_section):
                            issues.append({
                                "section_name": section_name,
                                "key": key,
                                "section_id": section_id,
                                "item_idx": stdi,
                                "user_value": user_value,
                                "std_value": std_value,
                                "issue_type": "不匹配"
                            })
        return issues

    def show_login_form(self):
        # 新增判断：如果登录表单已存在，则直接返回，不重复创建
        if hasattr(self, 'login_form') and self.login_form.parent:
            return

        if self.current_screen and self.current_screen in self.children:
            self.remove_widget(self.current_screen)

        self.login_form = LoginForm()
        self.add_widget(self.login_form, index=1)
        self.login_form.show()
        self.top_nav.set_active_button('登录')

    def remove_login_form(self):
        if hasattr(self, 'login_form') and self.login_form.parent:
            self.login_form.hide()

    def login_success(self, username, eid=None, user_data=None):
        # 更新当前用户
        self.is_logged_in = True
        self.current_user = username
        self.update_user_button()
        data = {i: [] for i in range(len(self.eval_content.data_types))}
        xn, xq, xm = extract_xn_xq_xm(session.get("https://zxszhsz.tj.edu.cn/zhszpjcz/web/jbqk/xsRzqk.htm").text)
        self.user_manager.users[username]['xm'] = xm
        # 任职情况
        rzqk = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/jbqk/xsRzqk.do",
                            data=getInformatonData(xq=xq, xn=xn, method="queryRzqkList", type="rzqk")).text
        rzqk_rows = json.loads(rzqk).get("rows", [])  # rows是列表
        # 遍历每条记录，转换为前端需要的格式
        rzqk_items = []
        for item in rzqk_rows:  # 遍历列表中的每条记录
            rzqk_items.append({
                "name": item.get("xm", ""),  # 用item（单条记录）访问字段
                "drzw": item.get("rzqk_drzw", ""),
                "kssj": item.get("rzqk_kssj", ""),
                "jssj": item.get("rzqk_jssj", ""),
                "zwms": item.get("rzqk_zwms", ""),
            })
        data[0] = rzqk_items  # 将处理好的列表赋值给data[0]（对应任职情况）

        zsbgGetData = {
            "method": "queryCsbgByXsJbxxId",
            "xsJbxxId": eid,
            "bgfl": "1"
        }
        zsbg = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/csbg/xsCsbg.do", data=zsbgGetData).text
        zsbgData = json.loads(zsbg)
        data[1] = zsbgData['xscsbg'].strip()

        xghd = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/sxpd/xsDxsl.do",
                            data=getInformatonData(xq=xq, xn=xn, method="queryDxslList", type="xghd")).text
        xghd_rows = json.loads(xghd).get("rows", [])
        xghd_items = []
        for item in xghd_rows:
            if item['dxsl_jb'] == "0":
                actionJb = "校级"
            elif item['dxsl_jb'] == "1":
                actionJb = "班级"
            if item['dxsl_xmlx'] == "1":
                actionType = "专题教育"
            elif item['dxsl_xmlx'] == "2":
                actionType = "班团队活动"
            xghd_items.append({
                "hdjb": actionJb,
                "hdlb": actionType,
                "hdcs": item.get("dxsl_cs", ""),
                "hdms": item.get("dxsl_ms", ""),
            })
            data[2] = xghd_items

            rcbx = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/sxpd/xsTcbx.do",
                                data=getInformatonData(xq=xq, xn=xn, method="queryRctcbxList", type="rcbx")).text
            rcbx_rows = json.loads(rcbx).get("rows", [])
            rcbx_items = []
            for item in rcbx_rows:
                rcbx_items.append({
                    "rcbx": item.get("rcbx_tcbx", ""),
                })
            data[3] = rcbx_items

            data[4] = [{"tip": "本项为选填项，暂不支持查看"}]

            sthd = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/xysp/xsSthd.do",
                                data=getInformatonData(xq=xq, xn=xn, method="queryXsXyspSthdList", type="sthd")).text
            sthd_rows = json.loads(sthd).get("rows", [])
            sthd_items = []
            for item in sthd_rows:
                sthd_items.append({
                    "sthdkssj": item.get("sthdKssj", ""),
                    "sthdjssj": item.get("sthdJssj", ""),
                    "sthdhddd": item.get("sthdHddd", ""),
                    "sthdhdnr": item.get("sthdHdnr", ""),
                    "sthdhdxghgrbx": item.get("sthdHdxggrbx", ""),
                })
            data[5] = sthd_items

            yjxxx = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/xysp/xsYjxxxjcxcg.do",
                                 data=getInformatonData(xq=None, xn=None, method="getYjxxxjcxcgList",
                                                        type="yjxxx")).text
            yjxxx_rows = json.loads(yjxxx).get("rows", [])
            yjxxx_items = []
            for item in yjxxx_rows:
                if item['sfsc'] == "0":
                    zl = "否"
                elif item['sfsc'] == "1":
                    zl = "是"
                if item['yjxxxbg_cgjl'] == "5":
                    jb = "无"
                elif item['yjxxxbg_cgjl'] == "4":
                    jb = "班级"
                elif item['yjxxxbg_cgjl'] == "3":
                    jb = "学校"
                elif item['yjxxxbg_cgjl'] == "2":
                    jb = "区"
                elif item['yjxxxbg_cgjl'] == "1":
                    jb = "市"
                elif item['yjxxxbg_cgjl'] == "0":
                    jb = "国家"
                yjxxx_items.append({
                    "kssj": item.get("yjxxxbg_kssj", ""),
                    "jssj": item.get("yjxxxbg_jssj", ""),
                    "ktmc": item.get("yjxxxbg_bt", ""),
                    "nrzy": item.get("yjxxxbg_yjnr", ""),
                    "zdls": item.get("yjxxxbg_zdjs", ""),
                    "sfsqzl": zl,
                    "jb": jb,
                })
            data[6] = yjxxx_items

            ysxk = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/xysp/xsXktc.do",
                                data=getInformatonData(xq=xq, xn=xn, method="getXktcList", type="ysxk")).text
            ysxk_rows = json.loads(ysxk).get("rows", [])
            ysxk_items = []
            for item in ysxk_rows:
                ysxk_items.append({
                    "kssj": item.get("xktc_kssj", ""),
                    "jssj": item.get("xktc_jssj", ""),
                    "hdmc": item.get("xktc_mc", ""),
                    "bx": item.get("xktc_bx", ""),
                })
            data[7] = ysxk_items

            shsj = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/shsj/xsShdc.do",
                                data=getInformatonData(xq=None, xn=None, method="queryXsShsjShdcList",
                                                       type="shsj")).text
            shsj_rows = json.loads(shsj).get("rows", [])
            shsj_items = []
            for item in shsj_rows:
                xmlb = item["shdcXmlb"]
                if xmlb == "1":
                    xmmc = "集中实践"
                elif xmlb == "2":
                    xmmc = "调查研究"
                elif xmlb == "3":
                    xmmc = "素质拓展课外活动"
                elif xmlb == "4":
                    xmmc = "科技活动"
                elif xmlb == "5":
                    xmmc = "其它"
                shsj_items.append({
                    "kssj": item.get("shdcKssj", ""),
                    "jssj": item.get("shdcJssj", ""),
                    "xmlb": xmmc,
                    "dd": item.get("shdcSjdd", ""),
                    "nr": item.get("shdcSjnr", ""),
                    "bxhcg": item.get("shdcBxhcg", ""),
                })
            data[8] = shsj_items

            kwtyxx = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/yssy/xsTyhd.do",
                                  data=getInformatonData(xq=xq, xn=xn, method="queryKwtyxxList", type="kwtyxx")).text
            kwtyxx_rows = json.loads(kwtyxx).get("rows", [])
            kwtyxx_items = []
            for item in kwtyxx_rows:
                kwtyxx_items.append({
                    "xiangmu": item.get("kwtyxx_xm", ""),
                    "sj": item.get("kwtyxx_sj", ""),
                    "xxsp": item.get("kwtyxx_xxsp", ""),
                })
            data[9] = kwtyxx_items

            data[10] = [{"tip": "本项为选填项，暂不支持查看"}]

            ygtycq = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/yssy/xsTyhd.do",
                                  data={"method": "queryYgtycqList"}).text
            ygtycqData = json.loads(ygtycq)
            data[11] = [{"ygtycq": ygtycqData["ygtycq_cq"]}]

            xljkdata = {
                "method": "queryXsXlsz",
                "dictType": "",
                "code": "",
            }
            xljk = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/sxjk/xsSxjk.do", data=xljkdata).text
            data[12] = [{"xlszzs": json.loads(xljk)['rows'][0]["XLSZZS_NR"]}]

            kwysxx = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/yssy/xsKwysxx.do",
                                  data=getInformatonData(xq=xq, xn=xn, method="getKwysxxList", type="kwysxx")).text
            kwysxx_rows = json.loads(kwysxx).get("rows", [])
            kwysxx_items = []
            for item in kwysxx_rows:
                kwysxx_items.append({
                    "xiangmu": item.get("kwysxx_xm", ""),
                    "sj": item.get("kwysxx_sj", ""),
                    "xxsp": item.get("kwysxx_xxsp", ""),
                })
            data[13] = kwysxx_items

            data[14] = [{"tip": "本项为选填项，暂不支持查看"}]

            ysxsjl = session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/web/yssy/xsYsxsjl.do",
                                  data=getInformatonData(xq=xq, xn=xn, method="getYsxsjlList", type="ysxsjl")).text
            ysxsjl_rows = json.loads(ysxsjl).get("rows", [])
            ysxsjl_items = []
            for item in ysxsjl_rows:
                ysxsjl_items.append({
                    "sj": item.get("ysxsjl_sj", ""),
                    "nr": item.get("ysxsjl_nr", ""),
                })
            data[15] = ysxsjl_items

            # 保存数据到用户管理器
            self.user_manager.set_user_data(username, data)
            self.eval_content.update_simulated_data(data)
        # 更新首页欢迎信息
        home_content = Label(
            text=f"欢迎回来，{username}!\n\n当前已登录账号: {username}",
            font_size=dp(20),
            halign='center',
            valign='middle'
        )
        self.screens['首页'].set_content(home_content)

        # 显示首页
        self.show_screen('首页')