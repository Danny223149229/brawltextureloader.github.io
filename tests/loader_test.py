import unittest
import os
import shutil
import glob

import loader

# Tests should probably be highly specific cases and not use config file.

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    def setUp(self):
        self.data = loader.init(self)

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
                for number, path in self.data['fighter'][fighter].items():
                    if path != 'RESERVED':
                        fullpath = os.path.join(source, path)
                        extension = os.path.splitext(path)[1]
                        if extension == '':
                            for filetype in self.data['filetype']:
                                with self.subTest('{0}.{1}'.format(fullpath, filetype)):
                                    self.assertTrue(os.path.exists('{0}.{1}'.format(fullpath, filetype)))
                        else:
                            with self.subTest('{0}.{1}'.format(fullpath, path[:3])):
                                self.assertTrue(os.path.exists(fullpath))

    def test_mkdirs(self):
        """Appropriate destination folders were created."""
        loader.load(self)
        for name, destination in self.data['destination'].items():
            for fighter in self.data['fighter']:
                    with self.subTest(fighter=fighter):
                        self.assertTrue(os.path.exists(os.path.join(destination, fighter)))

    def test_cpfiles(self):
        """Files are copied from source to destination and renamed."""
        loader.load(self)
        for name, destination in self.data['destination'].items():
            for fighter in self.data['fighter']:
                for number, path in self.data['fighter'][fighter].items():
                    if path != 'RESERVED':
                        fullpath = os.path.join(destination, fighter, 'Fit{0}{1:02}'.format(fighter, number))
                        source_name, extension = os.path.splitext(path)
                        if extension == '':
                            for filetype in self.data['filetype']:
                                with self.subTest('{0}.{1}'.format(fullpath, filetype)):
                                    self.assertTrue(os.path.exists('{0}.{1}'.format(fullpath, filetype)))
                        else:
                            with self.subTest(fullpath + extension):
                                self.assertTrue(os.path.exists(fullpath + extension))

    def test_reserved(self):
        """Numbers marked as RESERVED are ignored."""
        loader.load(self)
        for name, destination in self.data['destination'].items():
            for fighter in self.data['fighter']:
                for number, path in self.data['fighter'][fighter].items():
                    if path == 'RESERVED':
                        with self.subTest('{0}, {1}'.format(fighter, number)):
                            self.assertFalse(glob.glob('{0}/{1}/*{2:02d}*.*'.format(destination, fighter, number)))

    def tearDown(self):
        for name, destination in self.data['destination'].items():
            shutil.rmtree(destination)
            os.makedirs(destination)

if __name__ == '__main__':
    unittest.main()
