import pickle
import unittest


class TestPickle(unittest.TestCase):
    """docstring for TestPickle"""
    @staticmethod
    def testPickleRW():

        a = {'hello': 'world'}

        with open('filename.pickle', 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('filename.pickle', 'rb') as handle:
            b = pickle.load(handle)

        assert a == b


if __name__ == '__main__':
    unittest.main()
