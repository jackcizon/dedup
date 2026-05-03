from dedup.hash.mysql.mysql_dedup import MysqlDedup


class TestMysqlDedup:
    async def test_init_save_exist(self):
        md = MysqlDedup(url='mysql+aiomysql://root:jack021213@localhost/test')
        await md.async_save('1')
        if not md.async_is_exists('1'):
            await md.async_save(b'1')
        else:
            print('exists')
