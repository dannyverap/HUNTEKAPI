import redis.asyncio as redis


class RedisService:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(
            host='redis-14984.c244.us-east-1-2.ec2.cloud.redislabs.com', port='14984', db=0, auto_close_connection_pool=True, password='w0PuiLpEBtG1JvmkO91CMxVxC4PSttaT', decode_responses=True
        )
    
    async def set(self, key, value):
        await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)
    
    async def delete(self, key):
        await self.redis.delete(key)

    async def exists(self, key):
        return await self.redis.exists(key)

    async def close(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()