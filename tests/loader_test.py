import unittest
import os
import loader

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    def setUp(self):
        self.config = 'config.yaml'
        self.data = loader.load(self)

    def test_load(self):
        """Source folders exist."""
        for source_name, source in self.data['source'].items():
            for fighter in self.data['fighter']:
                for number, path in self.data['fighter'][fighter].items():
                    with self.subTest(path=path):
                        self.assertTrue(os.path.exists(os.path.join(source, fighter)))

    def test_mkdirs(self):
        """Appropriate destination folders were created."""
        for name, destination in self.data['destination'].items():
            for fighter in self.data['fighter']:
                with self.subTest(fighter=fighter):
                    self.assertTrue(os.path.exists(os.path.join(destination, fighter)))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
