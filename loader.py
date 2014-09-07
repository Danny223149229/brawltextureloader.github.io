import os
import yaml

# for source, source_location in data['source'].items():
#     if source in data:
#         for element, values in data[source].items():
#             for key, value in values.items():
#                 for place in data['destination']:
#                     source = os.path.join(source_location, value)
#                     destination = os.path.join(place, source, value)

def load(self):
    stream = open(self.config, 'r')
    data = yaml.load(stream)
    stream.close()
    return data

