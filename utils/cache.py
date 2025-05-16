from cachetools import TTLCache

# 创建一个最大容量1000条，TTL为300秒（5分钟）的缓存
verify_code_cache = TTLCache(maxsize=1000, ttl=300)
