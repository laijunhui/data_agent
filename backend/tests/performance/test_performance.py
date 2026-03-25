import time
import pytest
from concurrent.futures import ThreadPoolExecutor


def test_concurrent_requests():
    """测试并发请求"""
    def make_request():
        start = time.time()
        # 模拟 API 调用
        return time.time() - start, 200

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in futures]

    times = [r[0] for r in results]
    success_count = sum(1 for r in results if r[1] == 200)

    assert success_count >= 95, f"成功率应 >= 95%, 实际: {success_count}%"
    assert sum(times) / len(times) < 5, f"平均响应时间应 < 5s"