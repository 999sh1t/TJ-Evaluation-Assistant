import requests, json, re
from bs4 import BeautifulSoup
from .crypto import aes_encrypt
session = requests.Session()
login_page_url = "https://www.tj.edu.cn/uc/wcms/login.htm"
login_url      = "https://www.tj.edu.cn/uc/j_hh_security_check"
sc_url         = "https://www.tj.edu.cn/sc/"
def extract_xn_xq_xm(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    username_label = soup.find('div', class_='form-group').find_next('div', class_='form-group').find('div',
                                                                                                      class_='col-sm-9').find(
        'label')
    username = username_label.get_text(strip=True)
    scripts = soup.find_all('script')
    target_vars = {'xn': None, 'xq': None}
    patterns = {
        'xn': re.compile(r"xn\s*:\s*['\"](\d+)['\"]"),
        'xq': re.compile(r"xq\s*:\s*['\"](\d+)['\"]")
    }
    for script in scripts:
        script_text = script.get_text()

        for var, pattern in patterns.items():
            if target_vars[var] is None:
                match = pattern.search(script_text)
                if match:
                    target_vars[var] = match.group(1)

    return target_vars['xn'], target_vars['xq'], username

def SamlLogin(SAMLRequest, appId, relayUrlText, relayUrl, logOutUrl):
    Samlrequestsdata = {
        "SAMLRequest": SAMLRequest,
        "appId": appId,
        relayUrl: relayUrlText,
        "bind": "0",
        "logOutUrl": logOutUrl,
    }
    soup = BeautifulSoup(session.post("https://www.tj.edu.cn/uc/DoSamlSso", data=Samlrequestsdata).text, 'html.parser')
    samlresponse_input = soup.find('input', {'name': 'SAMLResponse'})
    samlresponse = samlresponse_input['value']
    Samlresponsedata = {
        "SAMLResponse": samlresponse,
        "appId": appId,
        "logOutUrl": logOutUrl,
        relayUrl: relayUrlText,
        "bind": "0",
    }
    session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/UserAction", data=Samlresponsedata)

def getInformatonData(xq, xn, method, type):
    informationData = {
        "page": "0",
        "pageSize": "10",
        "dir": "",
        "sort": "",
        "method": method,
        "xn": xn,
        "xq": xq,
    }
    if type == "rzqk":  # 任职情况
        informationData.update({"sfDqXn": "0", "xsJbxxId": ""})
    elif type == "xghd":  # 相关活动
        informationData.update({"sfdqXnxq": "0"})
    elif type == "shsj":  # 社会实践
        informationData.update({"sfDqXnXq": "1"})
    elif type == "sthd":  # 社团活动
        informationData.update({"xn": f"{xn}-{int(xn) + 1}", "sfDqXnXq": "0"})
    elif type == "rcbx":  # 日常表现
        informationData.update({"sfDqXn": "0"})
    elif type in ("yjxxx", "ysxk", "kwtyxx"):  # 综合性学习、优势学科、课外体育修习
        del informationData["xn"]
        del informationData["xq"]
    elif type in ("kwysxx", "ysxsjl"):
        informationData.update({"sfDqXn": "0"})
    return informationData

def autoLogin(username, password):
    session.cookies.clear()
    soup = BeautifulSoup(session.get(login_page_url).text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'HHCSRFToken'})
    hhcsrf_token = csrf_input['value']
    encrypted_password = aes_encrypt(password)
    data = {
        'relayUrl': '',
        'j_username': username,
        'pwd': '',
        'verify_code': "",
        'login_salt': '',
        'hid_remember_me': '0',
        'hid_remember_login_state': '0',
        'j_password': encrypted_password,
        'verify': "",
        'HHCSRFToken': hhcsrf_token,
    }
    # 发送登录请求
    loginstatus = session.post(login_url, data=data).status_code
    if loginstatus == 200:
        SamlLogin(SAMLRequest="https://www.tj.edu.cn:443/sc/UserAction", appId="sc", relayUrlText="/sc/",
                  relayUrl="relay_url",
                  logOutUrl="https://www.tj.edu.cn:443/sc/j_hh_security_logout")
        basicInformation = session.get("https://zxszhsz.tj.edu.cn/zhszpjcz/uc/character.do?method=queryCharaterList")
        char_id = json.loads(basicInformation.text)['returnData'][0]['charId']
        eid = json.loads(basicInformation.text)['returnData'][0]['eid']
        soup = BeautifulSoup(session.get("https://zxszhsz.tj.edu.cn/zhszpjcz/uc/character.htm").text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'HHCSRFToken'})
        HHCSRFToken = csrf_input['value']
        session.headers.update({
            "HHCSRFToken": HHCSRFToken,
        })
        characterCheckData = {
            "HHCSRFToken": HHCSRFToken,
            "relayUrl": "/web/index/yhIndex.htm",
            "j_character": char_id
        }
        session.post("https://zxszhsz.tj.edu.cn/zhszpjcz/uc/j_hh_character_check", data=characterCheckData)
        return True, eid
    else:
        return False, None