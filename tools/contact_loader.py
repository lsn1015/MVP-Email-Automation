"""
联系人加载器
"""

import pandas as pd
from typing import List, Dict


class ContactLoader:
    """联系人加载器"""

    def load(self, file_path: str) -> List[Dict[str, str]]:
        """
        加载联系人
        :param file_path: 文件路径，支持 xlsx 和 csv
        :return: 联系人列表
        """
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        # 统一字段为小写
        df.columns = [col.lower() for col in df.columns]

        contacts = []
        for _, row in df.iterrows():
            name = row.get("name")
            email = row.get("email")

            if pd.notna(name) and pd.notna(email):
                contacts.append({
                    "name": str(name).strip(),
                    "email": str(email).strip()
                })

        return contacts
