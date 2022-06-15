import redis

conn = redis.Redis(host="202.85.223.98", port=30096, db=1, password="dppc")
conn = redis.Redis(host="172.16.0.150", port=32380, db=1, password="dppc")
print(conn.exists('key1'))