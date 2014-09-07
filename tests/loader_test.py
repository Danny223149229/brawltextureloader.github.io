import unittest
import os
import loader

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    def setUp(self):
        self.config = 'config.yaml'

    def test_load(self):
        self.data = loader.load(self)
        for name, path in self.data['source'].items():
            with self.subTest(path=path):
                self.assertTrue(os.path.exists(path))
        for name, path in self.data['destination'].items():
            with self.subTest(path=path):
                self.assertTrue(os.path.exists(path))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
