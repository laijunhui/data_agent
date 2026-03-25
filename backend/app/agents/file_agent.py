import pandas as pd
from io import BytesIO
from typing import Dict, Any
from supabase import create_client, Client
from app.config import settings


class FileAgent:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    def upload_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """上传文件到 Supabase Storage"""
        bucket = self.supabase.storage.from_("files")
        result = bucket.upload(filename, file_content)
        return {"path": result.path, "name": filename}

    def parse_csv(self, file_path: str) -> pd.DataFrame:
        """解析 CSV 文件"""
        response = self.supabase.storage.from_("files").download(file_path)
        df = pd.read_csv(BytesIO(response))
        return df

    def parse_excel(self, file_path: str, sheet_name: str = 0) -> pd.DataFrame:
        """解析 Excel 文件"""
        response = self.supabase.storage.from_("files").download(file_path)
        df = pd.read_excel(BytesIO(response), sheet_name=sheet_name)
        return df

    def get_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """获取数据框结构信息"""
        return {
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "shape": df.shape,
            "preview": df.head(5).to_dict(orient="records")
        }
