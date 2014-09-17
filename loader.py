import os
import yaml
import shutil

def init(self, config='config.yaml'):
    stream = open(config, 'r')
    self.data = yaml.load(stream)
    stream.close()
    return self.data

def load(self):
    for category, source in self.data['source'].items():
        for unit in self.data[category]:
            for number, path in self.data[category][unit].items():
                for destination in self.data['destination'].values():
                    source_fullpath = os.path.join(
                        source,
                        path + '.pcs'
                    )
                    destination_dirpath = os.path.join(
                        destination, 
                        unit
                    )
                    os.makedirs(destination_dirpath)
                    shutil.copy2(source_fullpath, os.path.join(destination_dirpath, _filename_format(category, unit, number)))

def _filename_format(category, *args):
    return {
        'fighter': 'Fit' + args[0] + '{0:02d}'.format(args[1]) + '.pcs',
    }[category]
