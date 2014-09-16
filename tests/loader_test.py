import unittest
import os
import shutil

import loader

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    def setUp(self):
        self.data = loader.init(self)
        loader.load(self)

    def test_load_folders(self):
        """Source folders exist."""
        for source_name, source in self.data['source'].items():
            for fighter in self.data['fighter']:
                for number, path in self.data['fighter'][fighter].items():
                    with self.subTest(path=path):
                        self.assertTrue(os.path.exists(os.path.join(source, fighter)))

    def test_load_files(self):
        """Source files exist."""
        for source_name, source in self.data['source'].items():
            for fighter, textures in self.data['fighter'].items():
                for number, path in textures.items():
                    fullpath = os.path.join(
                        source, 
                        path + '.pcs'
                    )
                    with self.subTest(fullpath):
                        self.assertTrue(os.path.exists(fullpath))

    def test_mkdirs(self):
        """Appropriate destination folders were created."""
        for name, destination in self.data['destination'].items():
            for fighter in self.data['fighter']:
                with self.subTest(fighter=fighter):
                    self.assertTrue(os.path.exists(os.path.join(destination, fighter)))

    def test_cpfiles(self):
        """Files are copied from source to destination and renamed."""
        for name, destination in self.data['destination'].items():
            for fighter, textures in self.data['fighter'].items():
                for number in textures:
                    fullpath = os.path.join(
                        destination, 
                        fighter,
                        'Fit' + fighter + '{0:02d}'.format(number) + '.pcs'
                    )
                    with self.subTest(fullpath):
                        self.assertTrue(os.path.exists(fullpath))

    def tearDown(self):
        for name, destination in self.data['destination'].items():
            shutil.rmtree(destination)
            os.makedirs(destination)

if __name__ == '__main__':
    unittest.main()
