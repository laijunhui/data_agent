from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import hashlib
import json


class CacheService:
    """缓存服务 - 支持 LRU 和 TTL"""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl  # 默认 TTL 1小时

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存 key"""
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        # 检查 TTL
        if datetime.now() > entry["expires_at"]:
            del self._cache[key]
            return None

        # LRU: 移到末尾
        self._cache[key]["last_accessed"] = datetime.now()
        return entry["value"]

    def set(self, key: str, value: Any, ttl: int = None):
        """设置缓存"""
        # LRU: 如果满了，删除最老的
        if len(self._cache) >= self._max_size:
            oldest_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k]["last_accessed"]
            )
            del self._cache[oldest_key]

        ttl = ttl or self._default_ttl
        self._cache[key] = {
            "value": value,
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "expires_at": datetime.now() + timedelta(seconds=ttl)
        }

    def delete(self, key: str):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """清空缓存"""
        self._cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "ttl": self._default_ttl
        }


# 全局缓存实例
sql_query_cache = CacheService(max_size=1000, default_ttl=3600)  # SQL 查询缓存
schema_cache = CacheService(max_size=100, default_ttl=86400)     # Schema 缓存 24小时
session_cache = CacheService(max_size=500, default_ttl=1800)     # 会话上下文缓存 30分钟