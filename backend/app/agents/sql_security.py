import sqlglot
from typing import List, Tuple


class SQLSecurityChecker:
    """SQL 安全检查器 - 使用 sqlglot 进行语法解析和安全校验"""

    # 允许的 SQL 操作类型
    ALLOWED_OPERATIONS = {"SELECT", "WITH"}

    # 危险关键词
    DANGEROUS_KEYWORDS = {
        "DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE",
        "INSERT", "UPDATE", "GRANT", "REVOKE"
    }

    def __init__(self):
        self.errors: List[str] = []

    def check(self, sql: str) -> Tuple[bool, List[str]]:
        """检查 SQL 安全性"""
        self.errors = []

        if not sql or not sql.strip():
            self.errors.append("SQL 不能为空")
            return False, self.errors

        try:
            statements = sqlglot.parse(sql, dialect="postgres")
            for stmt in statements:
                self._check_operation(stmt)
                self._check_dangerous_keywords(sql)
                self._check_injection(stmt)

        except sqlglot.errors.ParseError as e:
            self.errors.append(f"SQL 语法错误: {str(e)}")
            return False, self.errors

        return len(self.errors) == 0, self.errors

    def _check_operation(self, stmt):
        operation = stmt.key.upper()
        if operation not in self.ALLOWED_OPERATIONS:
            self.errors.append(f"不支持的操作类型: {operation}，仅允许 SELECT/WITH")

    def _check_dangerous_keywords(self, sql: str):
        sql_upper = sql.upper()
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in sql_upper:
                self.errors.append(f"检测到危险关键词: {keyword}")

    def _check_injection(self, stmt):
        pass  # 可扩展更多检查

    def validate_and_sanitize(self, sql: str) -> str:
        """验证并清理 SQL"""
        is_safe, errors = self.check(sql)
        if not is_safe:
            raise ValueError(f"SQL 安全检查失败: {errors}")
        return sql.strip()
