from dedup.hash import MemoryDedup


class TestMemoryDedup:
    def test_init_save_exists(self):
        md = MemoryDedup()
        md.sync_save(b'1')
        md.sync_save('1')
        datas = ['1', b'1']
        for data in datas:
            if not md.sync_is_exists(data):
                md.sync_save(data)
        print(len(md.storage))
