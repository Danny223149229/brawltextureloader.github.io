import os
import yaml
import shutil

# for source, source_location in data['source'].items():
#     if source in data:
#         for element, values in data[source].items():
#             for key, value in values.items():
#                 for place in data['destination']:
#                     source = os.path.join(source_location, value)
#                     destination = os.path.join(place, source, value)

def init(self, config='config.yaml'):
    stream = open(config, 'r')
    self.data = yaml.load(stream)
    stream.close()
    return self.data

def load(self):
    for category, source in self.data['source'].items():
        for unit in self.data[category]:
            for number, path in self.data[category][unit].items():
                for name, destination in self.data['destination'].items():
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
