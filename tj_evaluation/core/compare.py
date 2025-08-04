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