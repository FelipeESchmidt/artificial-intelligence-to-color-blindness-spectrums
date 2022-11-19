from multiprocessing import Pool
import neurolab as nl
import numpy as np


def transform_line(arr_ai):
    """
    Transform one RGB line to a color blindness RGB line using received AI

    :param arr_ai: [The RGB line, the IA used to transform]
    :type arr_ai: array of (array of rgb color and AI)
    :return: array of rgb color transformed
    :rtype: array of rgb color
    """
    try:
        arr, ai = arr_ai
        arr_normalized = [color / 255 for color in arr]
        new_arr_normalized = ai.sim(arr_normalized)
        new_arr = [np.asarray(color * 255).tolist() for color in new_arr_normalized]
        new_arr_rounded = [[round(value) for value in color] for color in new_arr]
        return new_arr_rounded
    except Exception as e:
        print("Ex from transformation: " + e)
        return []


if __name__ == '__main__':
    ai_loaded = nl.load('intelligence_trit.net')

    columns = np.array([[[100, 10, 50], [100, 180, 160]], [[150, 90, 80], [200, 100, 160]], [[212, 30, 66], [160, 202, 220]]])

    print(columns.shape)

    with Pool(5) as p:
        result = (p.map_async(transform_line, [[line, ai_loaded] for line in columns]))
        result.wait()
        print(result.get())

