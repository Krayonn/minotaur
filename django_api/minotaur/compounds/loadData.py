import json
from models import Compound

with open('fixtures/compounds.json') as data_file:
    json_data = json.loads(data_file.read())

    for compound_data in json_data:
        compound = Compound.create(**compound_data)
