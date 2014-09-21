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
                for slot, paths in self.data[category][unit].items():
                    if paths != None and paths[0] != RESERVED:
                        for path in paths:
                            for destination in self.data['destination']:
                                source_fullpath = os.path.join(source, path)
                                if os.path.splitext(path)[1] is '':
                                    for filetype in FILETYPES[category]:
                                        if os.path.exists('{0}.{1}'.format(source_fullpath, filetype)):
                                            destination_filepath = os.path.join(destination, _filename_format(category, filetype, unit, slot))
                                            if not os.path.exists(os.path.dirname(destination_filepath)):
                                                os.makedirs(os.path.dirname(destination_filepath))
                                            shutil.copy2('{0}.{1}'.format(source_fullpath, filetype), destination_filepath)
                                else:
                                    destination_filepath = os.path.join(destination, category, unit, os.path.basename(path))
                                    if not os.path.exists(os.path.dirname(destination_filepath)):
                                        os.makedirs(os.path.dirname(destination_filepath))
                                    shutil.copy2(source_fullpath, destination_filepath)

def _singles_as_list(dictionary):
    """For a dictionary, Wraps single string entries in a list."""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            _singles_as_list(dictionary[key])
        elif isinstance(value, str):
            dictionary[key] = [value]

def _filename_format(category, extension, *args):
    """Formats the filename according to the category (e.g. stage, fighter)."""
    if category == 'fighter':
        return {
            'pcs': 'fighter/{0}/Fit{0}{1:02d}.pcs'.format(args[0], args[1]),
            'pac': 'fighter/{0}/Fit{0}{1:02d}.pac'.format(args[0], args[1]),
        }[extension]
    elif category == 'stage':
        return {
            'pac': 'stage/{0}/STG{1}.PAC'.format(args[0], args[1].upper()),
            'rel': 'module/st_{0}.rel'.format(args[1].lower()),
        }[extension]
