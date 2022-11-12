from os.path import exists
import neurolab as nl
import numpy as np
import json


rgb_max_value = 255


def get_data_from_json_file(file_name, color_type):
    f = open(file_name)
    data = json.load(f)
    f.close()
    return data['base'], data[color_type]


def create_ai(color_type):
    entrances, outputs = get_data_from_json_file('full-data.json', color_type)

    entrances_np = np.array(entrances) / rgb_max_value
    outputs_np = np.array(outputs) / rgb_max_value

    limit_color = [0, 1]
    limits = [limit_color, limit_color, limit_color]
    layer_1 = 6
    layer_2 = 6
    layer_3 = 3
    layers = [layer_1, layer_2, layer_3]

    ai_created = nl.net.newff(limits, layers)

    errors = ai_created.train(entrances_np, outputs_np, epochs=10000, show=0, goal=0.000001)

    print("Training errors : " + str(errors[-1]))

    ai_created.save('intelligence_' + color_type + '.net')

    return ai_created


def load_ai(file_name):
    if exists(file_name):
        ai_loaded = nl.load(file_name)
        return ai_loaded
    return False


if __name__ == '__main__':
    prot_type = 'prot'
    ai = load_ai('intelligence_' + prot_type + '.net')
    if not ai:
        ai = create_ai(prot_type)

    test = ai.sim([np.array([127, 22, 29]) / rgb_max_value])
    print("test = " + str(test * rgb_max_value))


