"""
Loads Super Smash Brothers Brawl texture files from given source locations
to the destination(s), likely an SD card, per a config.yaml file.
"""

import os
import yaml
import shutil

RESERVED = 'RESERVED'

FILETYPES = {
    'fighter': ['pcs', 'pac'],
    'stage': ['pac', 'rel'],
}

def init(self, config='config.yaml'):
    """Open config.yaml, load the yaml data, wrap singles in a list."""
    stream = open(config, 'r')
    self.data = yaml.load(stream)
    stream.close()
    _singles_as_list(self.data)
    return self.data

def load(self):
    """Copies source files into the destination, according to the yaml data."""
    for category, sources in self.data['source'].items():
        for source in sources:
            for unit in self.data[category]:
                for number, paths in self.data[category][unit].items():
                    for path in paths:
                        if path != RESERVED:
                            for destination in self.data['destination']:
                                source_fullpath = os.path.join(source, path)
                                destination_dir = os.path.join(destination, category, unit)
                                if not os.path.exists(destination_dir):
                                    os.makedirs(destination_dir)
                                extension = os.path.splitext(path)[1]
                                if extension is '':
                                    for filetype in FILETYPES[category]:
                                        if os.path.exists('{0}.{1}'.format(source_fullpath, filetype)):
                                            shutil.copy2('{0}.{1}'.format(source_fullpath, filetype), '{0}/{1}.{2}'.format(destination_dir, _filename_format(category, unit, number), filetype))
                                else:
                                    shutil.copy2(source_fullpath, os.path.join(destination, category, unit, os.path.basename(path)))

def _singles_as_list(dictionary):
    """For a dictionary, Wraps single string entries in a list."""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            _singles_as_list(dictionary[key])
        elif isinstance(value, str):
            dictionary[key] = [value]

def _filename_format(category, *args):
    """Formats the filename according to the category (e.g. stage, fighter)."""
    return {
        'fighter': 'Fit{0}{1:02}'.format(args[0], args[1]),
    }[category]

