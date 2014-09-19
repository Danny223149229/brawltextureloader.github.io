import unittest
import os
import shutil
import glob
import yaml

import loader

"""
Tests the functionality of the loader.  
The config.yaml file in the tests directory should be an index of all use/corner cases of a config. When writing a test for a new config case, update the tests/config.yaml.
The primary config.yaml in root will be kept as a clean template for getting started.
"""

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    def setUp(self):
        """Set sane defaults."""
        self.data = yaml.load("""
            source:
              fighter: source/fighter
            destination:
              fighter: destination/fighter
            filetype:
              - pcs
              - pac
            fighter:
              Peach:
                00: Peach/Rosalina
        """)
        # Should probably not use this helper directly from loader in the tests.
        loader._singles_as_list(self.data)

    def test_mkdirs(self):
        """Appropriate destination folders were created."""
        loader.load(self)
        self.assertTrue(os.path.exists(os.path.join(self.data['destination']['fighter'][0], 'Peach', 'FitPeach00.pcs')))

    def test_load(self):
        """Given a generic source name (no extension), files with specified filetypes are copied from source to destination and renamed."""
        loader.load(self)
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach00.pcs'))
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach00.pac'))

    def test_explicit(self):
        """Source files with an explicitly called extension are copied and renamed."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: Peach/Rosalina.pcs
              01: Peach/Rosalina.pac
        """)
        loader._singles_as_list(self.data)
        loader.load(self)
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach00.pcs'))
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach01.pac'))

    def test_reserved(self):
        """Numbers marked as RESERVED are ignored."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: RESERVED
              01: Peach/Rosalina
        """)
        loader._singles_as_list(self.data)
        loader.load(self)
        self.assertFalse(glob.glob('destination/fighter/Peach/*00*.*'))
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach01.pcs'))
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach01.pac'))

    def test_number_list(self):
        """When a number has a list, the list is handled properly."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00:
                - Peach/Rosalina.pcs
                - Peach/Rosalina.pac
        """)
        loader._singles_as_list(self.data)
        loader.load(self)
        self.assertTrue(os.path.exists(os.path.join(self.data['destination']['fighter'][0], 'Peach', 'FitPeach00.pcs')))
        self.assertTrue(os.path.exists(os.path.join(self.data['destination']['fighter'][0], 'Peach', 'FitPeach00.pac')))

    def test_destination_list(self):
        """When a list of destinations are given, copies are made to each one."""
        self.data['destination'] = yaml.load("""
            fighter:
              - destination/fighter
              - destination/another_fighter
        """)
        loader._singles_as_list(self.data)
        loader.load(self)
        for destination in self.data['destination']['fighter']:
            self.assertTrue(os.path.exists(destination + '/Peach/FitPeach00.pcs'))
            self.assertTrue(os.path.exists(destination + '/Peach/FitPeach00.pac'))
    
    def test_single_filetype_present(self):
        """When not all the default filetypes are present for a generic path, takes all of those present and ignores the lack of the rest."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: Peach_pcs/Rosalina
        """)
        loader._singles_as_list(self.data)
        loader.load(self)
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach00.pcs'))
        self.assertFalse(os.path.exists('destination/fighter/Peach/FitPeach00.pac'))

    def test_spaces(self):
        """Handle source files with spaces in their directory name and file name."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: Peach as Rosalina/Rosalina skin.pcs
        """)
        loader._singles_as_list(self.data)
        loader.load(self)
        self.assertTrue(os.path.exists('destination/fighter/Peach/FitPeach00.pcs'))

    def tearDown(self):
        for name, destinations in self.data['destination'].items():
            for destination in destinations:
                shutil.rmtree(destination)

if __name__ == '__main__':
    unittest.main()
