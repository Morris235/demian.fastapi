import os
from dotenv import load_dotenv
import redis

# .env 파일 로드
load_dotenv()


def redis_config():
    try:
        # 환경 변수에서 Redis 설정 불러오기
        REDIS_HOST = os.getenv("REDIS_HOST")
        REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))  # 기본값을 6379로 설정
        REDIS_DATABASE = int(os.getenv("REDIS_DATABASE", 0))  # 기본값을 0으로 설정

        # Redis 클라이언트 생성
        rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)

        # 연결 확인
        rd.ping()
        print("Connected to Redis")
        return rd

    except redis.ConnectionError as e:
        print(f"Redis connection failure: {e}")
        return None
