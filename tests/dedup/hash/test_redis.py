from redis.asyncio import Redis

from dedup.hash.redis import RedisDedup


class TestRedisDedup:
    async def test_init_save_exists(self):
        rd = RedisDedup()
        assert rd.storage is None
        await rd.async_save('1')
        assert rd.storage
        rd.ensure_storage(Redis.from_url('redis://localhost:6379/0'))
        assert rd.storage

        datas = ['1', b'1']
        last_change_count = 0
        change_count = 0
        for data in datas:
            change_count = await rd.async_save(data)
        assert last_change_count == change_count