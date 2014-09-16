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

# Consider remake using [asdf] instead of .items()

def init(self, config='config.yaml'):
    stream = open(config, 'r')
    self.data = yaml.load(stream)
    stream.close()
    return self.data

def load(self):
    for source_name, source in self.data['source'].items():
        for fighter, textures in self.data['fighter'].items():
                for number, source_path in textures.items():
                    for name, destination in self.data['destination'].items():
                        source_fullpath = os.path.join(
                            source,
                            source_path + '.pcs'
                        )
                        destination_fullpath = os.path.join(
                            destination, 
                            fighter,
                            'Fit' + fighter + '{0:02d}'.format(number) + '.pcs'
                        )
                        os.makedirs(os.path.join(destination, fighter))
                        shutil.copy2(source_fullpath,destination_fullpath)

if __name__ == '__main__':
    unittest.main()
