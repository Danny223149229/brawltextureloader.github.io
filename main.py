import os
import yaml

stream = open('config.yaml', 'r')
data = yaml.load(stream)

print(data['source'])
print(data['destination'])
for source, source_location in data['source'].items():
    print(source_location)
    if source in data:
        for element, values in data[source].items():
            for key, value in values.items():
                for place in data['destination']:
                    source = os.path.join(source_location, value)
                    destination = os.path.join(place, source, value)
                    print(os.listdir(source))
