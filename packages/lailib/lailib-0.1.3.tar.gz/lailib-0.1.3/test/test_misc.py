from lailib.misc.misc import *

class TestRandomStr:
    def test_len(self):
        gened_str = set([])
        for i in range(100):
            rand_str = gen_random_str()
            assert rand_str not in gened_str
            gened_str.add(rand_str)

    def test_heck_len(self):
        for i in range(100):
            str_len = random.randint(1,10)
            rand_str = gen_random_str(str_len)
            assert len(rand_str)==str_len
