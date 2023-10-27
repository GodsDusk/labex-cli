import os
import json
import requests
from rich import print
from requests_toolbelt import MultipartEncoder


class Feishu:
    """Feishu API"""

    def __init__(self, app_id: str, app_secret: str) -> None:
        self.app_id = app_id
        self.app_secret = app_secret

    def tenant_access_token(self):
        """Get tenant access token"""
        r = requests.post(
            url="https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({"app_id": self.app_id, "app_secret": self.app_secret}),
        )
        return r.json()["tenant_access_token"]

    def get_bitable_records(self, app_token: str, table_id: str, params: str) -> None:
        """Get bitable records"""
        records = []
        r = requests.get(
            url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?{params}",
            headers={
                "Authorization": f"Bearer {self.tenant_access_token()}",
            },
        )
        if r.json()["data"]["total"] > 0:
            records += r.json()["data"]["items"]
            # 当存在多页时，递归获取
            while r.json()["data"]["has_more"]:
                page_token = r.json()["data"]["page_token"]
                r = requests.get(
                    url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_token={page_token}&{params}",
                    headers={
                        "Authorization": f"Bearer {self.tenant_access_token()}",
                    },
                )
                if r.json()["data"]["total"] > 0:
                    records += r.json()["data"]["items"]
                    print(
                        f"[green]✔ RECORDS:[/green] {len(records)}, page_token: {page_token}"
                    )
        return records

    def add_bitable_record(self, app_token: str, table_id: str, data: dict) -> None:
        """Add record to bitable"""
        r = requests.post(
            url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records",
            headers={
                "Authorization": f"Bearer {self.tenant_access_token()}",
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps(data),
        )
        return r.json()

    def update_bitable_record(
        self, app_token: str, table_id: str, record_id: str, data: dict
    ) -> None:
        """Update record in bitable"""
        r = requests.put(
            url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}",
            headers={
                "Authorization": f"Bearer {self.tenant_access_token()}",
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps(data),
        )
        return r.json()

    def delete_bitable_record(
        self, app_token: str, table_id: str, record_id: str
    ) -> None:
        """Delete record in bitable"""
        r = requests.delete(
            url=f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}",
            headers={
                "Authorization": f"Bearer {self.tenant_access_token()}",
                "Content-Type": "application/json; charset=utf-8",
            },
        )
        return r.json()

    def upload_media(self, file_path: str, parent_type: str, parent_node: str) -> None:
        """Upload media to feishu

        Args:
            file_path (str): file path
            parent_type (str): https://open.feishu.cn/document/server-docs/docs/drive-v1/media/introduction
            parent_node (str): https://open.feishu.cn/document/server-docs/docs/drive-v1/media/introduction

        Returns:
            _type_: _description_
        """
        file_path = os.path.abspath(file_path)
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
        form = {
            "file_name": file_name,
            "parent_type": parent_type,
            "parent_node": parent_node,
            "size": str(file_size),
            "file": (open(file_path, "rb")),
        }
        multi_form = MultipartEncoder(form)
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token()}",
        }
        headers["Content-Type"] = multi_form.content_type
        response = requests.request("POST", url, headers=headers, data=multi_form)
        return response.json()
