"""
Tests the functionality of the loader.
The config.yaml file in the tests directory should be
an index of all use/corner cases of a config.
When writing a test for a new config case, update the tests/config.yaml.
The primary config.yaml in root will be a clean template for getting started.
"""

import unittest
import os
import shutil
import glob
import yaml

import loader

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    """Tests the functions of the texture loader."""

    def setUp(self):
        """Set sane defaults, run the _singles_as_list wrapper."""
        self.data = yaml.load("""
            source:
              fighter: source/fighter
            destination: destination
            fighter:
              Peach:
                00: Peach/Rosalina
        """)
        # Should probably not use this helper directly from loader in the tests.
        loader._singles_as_list(self.data)

    def test_mkdirs(self):
        """Appropriate destination folders were created."""
        loader.load(self)

        self.assertTrue(os.path.exists(os.path.join(
            self.data['destination'][0], 'fighter', 'Peach', 'FitPeach00.pcs'
        )))

    def test_load(self):
        """Given a generic source name (no extension), files with correct 
        filetypes are copied from source to destination and renamed."""
        loader.load(self)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pcs'
        ))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pac'
        ))

    def test_explicit(self):
        """Source files with a specified extension are copied, not renamed."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: Peach/Rosalina.pcs
              01: Peach/Rosalina.pac
        """)
        loader._singles_as_list(self.data)
        loader.load(self)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/Rosalina.pcs'
        ))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/Rosalina.pac'
        ))

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
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach01.pcs'
        ))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach01.pac'
        ))

    def test_number_list(self):
        """When a number has a list, the list is handled properly."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00:
                - Peach/Rosalina
        """)
        loader._singles_as_list(self.data)
        loader.load(self)

        self.assertTrue(os.path.exists(os.path.join(
            self.data['destination'][0], 'fighter', 'Peach', 'FitPeach00.pcs'
        )))
        self.assertTrue(os.path.exists(os.path.join(
            self.data['destination'][0], 'fighter', 'Peach', 'FitPeach00.pac'
        )))

    def test_destination_list(self):
        """When list of destinations are given, copies are made to each one."""
        self.data['destination'] = yaml.load("""
              - destination
              - another_fighter
        """)
        loader._singles_as_list(self.data)
        loader.load(self)

        for destination in self.data['destination']:
            self.assertTrue(os.path.exists(
                destination + '/fighter/Peach/FitPeach00.pcs'
            ))
            self.assertTrue(os.path.exists(
                destination + '/fighter/Peach/FitPeach00.pac'
            ))

    def test_single_filetype_present(self):
        """When not all the default filetypes are present for a generic path,
        takes all of those present and ignores the lack of the rest."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: Peach_pcs/Rosalina
        """)
        loader._singles_as_list(self.data)
        loader.load(self)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pcs'
        ))
        self.assertFalse(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pac'
        ))

    def test_spaces(self):
        """Handle source files with spaces in their directory and file names."""
        self.data['fighter'] = yaml.load("""
            Peach:
              00: Peach as Rosalina/Rosalina skin
        """)
        loader._singles_as_list(self.data)
        loader.load(self)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pcs'
        ))

    def test_stage(self):
        """Stage textures (.pac and .rel) placed in the right places."""
        self.data['source'] = yaml.load("""
              stage: source/stage
        """)
        self.data['stage'] = yaml.load("""
            melee:
              PALUTENA: Palutena/Clocktower
        """)
        loader._singles_as_list(self.data)
        loader.load(self)

        self.assertTrue(os.path.exists(
            'destination/stage/melee/STGPALUTENA.PAC'
        ))
        self.assertTrue(os.path.exists(
            'destination/module/st_palutena.rel'
        ))

    def tearDown(self):
        for destination in self.data['destination']:
            shutil.rmtree(destination)

if __name__ == '__main__':
    unittest.main()
