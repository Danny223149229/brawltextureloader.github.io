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

from loader import Loader, _singles_as_list

os.chdir('tests')

class TestTextureLoaderFunctions(unittest.TestCase):
    """Tests the functions of the texture loader."""

    def setUp(self):
        """Set sane defaults, run the _singles_as_list wrapper."""
        self.loader = Loader()
        self.loader.data = yaml.load("""
            source:
              fighter: source/fighter
            destination: destination
            fighter:
              Peach:
                00: Peach/Rosalina
        """)
        # Should probably not use this helper directly from loader in the tests.
        _singles_as_list(self.loader.data)

    def test_mkdirs(self):
        """Appropriate destination folders were created."""
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(os.path.join(
            self.loader.data['destination'][0], 'fighter', 'Peach', 'FitPeach00.pcs'
        )))

    def test_load(self):
        """Given a generic source name (no extension), files with correct 
        filetypes are copied from source to destination and renamed."""
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pcs'
        ))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pac'
        ))

    def test_explicit(self):
        """Source files with a specified extension are copied, not renamed."""
        self.loader.data['fighter'] = yaml.load("""
            Peach:
              00: Peach/Rosalina.pcs
              01: Peach/Rosalina.pac
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/Rosalina.pcs'
        ))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/Rosalina.pac'
        ))

    def test_reserved(self):
        """Slots marked as RESERVED are ignored."""
        self.loader.data['fighter'] = yaml.load("""
            Peach:
              00: RESERVED
              01: Peach/Rosalina
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertFalse(glob.glob('destination/fighter/Peach/*00*.*'))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach01.pcs'
        ))
        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach01.pac'
        ))

    def test_blank(self):
        """A slot that has nothing is ignored."""
        self.loader.data['fighter'] = yaml.load("""
            Peach:
              00:
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertFalse(os.path.exists('destination/fighter/Peach'))

    def test_slot_list(self):
        """When a slot has a list, the list is handled properly."""
        self.loader.data['fighter'] = yaml.load("""
            Peach:
              00:
                - Peach/Rosalina
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(os.path.join(
            self.loader.data['destination'][0], 'fighter', 'Peach', 'FitPeach00.pcs'
        )))
        self.assertTrue(os.path.exists(os.path.join(
            self.loader.data['destination'][0], 'fighter', 'Peach', 'FitPeach00.pac'
        )))

    def test_destination_list(self):
        """When list of destinations are given, copies are made to each one."""
        self.loader.data['destination'] = yaml.load("""
              - destination
              - another_fighter
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        for destination in self.loader.data['destination']:
            self.assertTrue(os.path.exists(
                destination + '/fighter/Peach/FitPeach00.pcs'
            ))
            self.assertTrue(os.path.exists(
                destination + '/fighter/Peach/FitPeach00.pac'
            ))

    def test_single_filetype_present(self):
        """When not all the default filetypes are present for a generic path,
        takes all of those present and ignores the lack of the rest."""
        self.loader.data['fighter'] = yaml.load("""
            Peach:
              00: Peach_pcs/Rosalina
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pcs'
        ))
        self.assertFalse(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pac'
        ))

    def test_spaces(self):
        """Handle source files with spaces in their directory and file names."""
        self.loader.data['fighter'] = yaml.load("""
            Peach:
              00: Peach as Rosalina/Rosalina skin
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(
            'destination/fighter/Peach/FitPeach00.pcs'
        ))

    def test_stage(self):
        """Stage textures (.pac and .rel) placed in the right places."""
        self.loader.data['source'] = yaml.load("""
              stage: source/stage
        """)
        self.loader.data['stage'] = yaml.load("""
            melee:
              PALUTENA: Palutena/Clocktower
        """)
        _singles_as_list(self.loader.data)
        Loader.load(self.loader)

        self.assertTrue(os.path.exists(
            'destination/stage/melee/STGPALUTENA.PAC'
        ))
        self.assertTrue(os.path.exists(
            'destination/module/st_palutena.rel'
        ))

    def tearDown(self):
        for destination in self.loader.data['destination']:
            if os.path.exists(destination):
                shutil.rmtree(destination)

if __name__ == '__main__':
    unittest.main()
