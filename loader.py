import os
import yaml
import shutil

RESERVED = 'RESERVED'

def init(self, config='config.yaml'):
    stream = open(config, 'r')
    self.data = yaml.load(stream)
    stream.close()
    _singles_as_list(self.data) 
    print(self.data)
    return self.data

def load(self):
    for category, sources in self.data['source'].items():
        for source in sources:
            for unit in self.data[category]:
                print(self.data[category][unit].items())
                for number, paths in self.data[category][unit].items():
                    for path in paths:
                        if path != RESERVED:
                            for destinations in self.data['destination'].values():
                                for destination in destinations:
                                    source_fullpath = os.path.join(source, path)
                                    destination_fullpath = os.path.join(destination, unit, _filename_format(category, unit, number))
                                    if not os.path.exists(os.path.dirname(destination_fullpath)):
                                        os.makedirs(os.path.dirname(destination_fullpath))
                                    extension = os.path.splitext(path)[1]
                                    if extension is '':
                                        for filetype in self.data['filetype']:
                                            shutil.copy2('{0}.{1}'.format(source_fullpath, filetype)
                , '{0}.{1}'.format(destination_fullpath, filetype))
                                    else:
                                        shutil.copy2(source_fullpath, destination_fullpath + extension)

def _singles_as_list(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            _singles_as_list(dictionary[key])
        elif not isinstance(value, list):
            dictionary[key] = [value]

def _filename_format(category, *args):
    return {
        'fighter': 'Fit{0}{1:02}'.format(args[0], args[1]),
    }[category]

