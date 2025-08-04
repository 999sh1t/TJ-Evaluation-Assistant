import json, os
from datetime import datetime
from .config import USERS_FILE
class UserManager:
    """用户管理器，用于管理多个用户账号"""

    def __init__(self):
        self.users = {}  # 格式: {username: {'password': password, 'data': {}}}
        self.current_user = None
        self.load_users()

    def get_user_info(self, username):
        """获取用户信息"""
        if username in self.users:
            user_data = self.get_user_data(username)
            xm = user_data.get('xm', '')
            return {
                'username': username,
                'last_login': self.users[username].get('last_login', '未知'),
                'xm': xm
            }
        return None

    def load_users(self):
        """从文件加载用户数据"""
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except Exception as e:
                self.users = {}

    def save_users(self):
        """保存用户数据到文件"""
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def add_user(self, username, password):
        """添加新用户"""
        if username not in self.users:
            self.users[username] = {
                'password': password,
                'data': {},
                'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.save_users()
            return True
        return False

    def remove_user(self, username):
        """删除用户"""
        if username in self.users:
            del self.users[username]
            self.save_users()
            if self.current_user == username:
                self.current_user = None
            return True
        return False

    def get_user_data(self, username):
        """获取用户数据"""
        if username in self.users:
            user_data = self.users[username].get('data', {})
            # 确保xm字段被正确获取
            xm = self.users[username].get('xm', '')
            if xm:
                user_data['xm'] = xm
            return user_data
        return {}

    def set_user_data(self, username, data):
        """设置用户数据"""
        if username in self.users:
            self.users[username]['data'] = data
            self.users[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_users()
            return True
        return False

    def login_user(self, username, password):
        """用户登录，验证密码并返回是否成功"""
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            self.users[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_users()
            return True
        return False

    def switch_to_user(self, username):
        """切换到指定用户"""
        # 获取用户密码
        password = self.main_layout.users[username]['password']
        # 执行登录流程
        loginCheck, eid = autoLogin(username, password)

        if loginCheck:
            self.main_layout.login_success(username, eid)
            self.refresh_user_list()
        else:
            self.show_message("错误", "登录失败，请检查账号和密码")

    def get_current_user(self):
        """获取当前用户"""
        return self.current_user

    def get_all_users(self):
        """获取所有用户"""
        return list(self.users.keys())