import os
import yaml
import shutil

RESERVED = 'RESERVED'

def init(self, config='config.yaml'):
    stream = open(config, 'r')
    self.data = yaml.load(stream)
    stream.close()
    return self.data

def load(self):
    for category, source in self.data['source'].items():
        for unit in self.data[category]:
            for number, path in self.data[category][unit].items():
                if path != RESERVED:
                    for destination in self.data['destination'].values():
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

def _filename_format(category, *args):
    return {
        'fighter': 'Fit{0}{1:02}'.format(args[0], args[1]),
    }[category]
