from typing import Optional
from fastapi import Header


class TenantService:
    """多租户服务"""

    @staticmethod
    def get_tenant_id(x_tenant_id: Optional[str] = Header(None)) -> str:
        if not x_tenant_id:
            raise ValueError("Missing X-Tenant-ID header")
        return x_tenant_id

    @staticmethod
    def validate_tenant(tenant_id: str) -> bool:
        return bool(tenant_id)

    @staticmethod
    def get_tenant_filter(tenant_id: str) -> dict:
        return {"tenant_id": tenant_id}