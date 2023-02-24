import os.path

import numpy
import matplotlib.pyplot as plt
from analysis import calculate_coef_AR, create_windows, set_path
import json

MODEL_PATH = ".\\models"

def standard_deviation(data: numpy):
    return numpy.std(data, axis=0)

def average_coef(data):
    avg_results = []
    len_single_data = len(data[0])

    for i in range(len_single_data):
        suma = 0
        for arr in data:
            suma += arr[i]
        avg_results.append(suma/len(data))

    return avg_results

def save_as_json(data):

    json_object = json.dumps(data, indent=4)

    with open("models\\model.json", 'w') as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    # I created here default nonREM and REM signal

    # Create mock signals REM and nonREM sleep
    signal = numpy.linspace(0, 300, 10000)
    default_sleep_signal = numpy.sin(0.25 * numpy.pi * signal) + numpy.sin(0.10 * 2 * numpy.pi * signal)

    plt.plot(default_sleep_signal)
    plt.title("Default sleep signal without noise")
    plt.show()

    # Create noise
    noise = numpy.random.normal(1,0.1,10000)

    plt.subplot(2,1,1)
    plt.plot(signal[:2000], default_sleep_signal[:2000])
    plt.title("Interfals for default sleep signal")
    plt.savefig(os.path.join(set_path(MODEL_PATH), "intervals_default_signals.jpg"), dpi=100)
    plt.show()

    ## Create nonREM signal
    pretend_nonREM_sleep = (float(0.01) * default_sleep_signal + float(1)* noise)

    plt.subplot(2,1,1)
    plt.plot(signal[:200], pretend_nonREM_sleep[:200])
    plt.title("Intervals nonREM sleep signal first 200 samples")
    plt.savefig(os.path.join(set_path(MODEL_PATH), "intervals_nonREM_sleep.jpg"), dpi=100)
    plt.show()

    ## create nonREM coef
    coef_nonrem = []

    for index, window in enumerate(create_windows(pretend_nonREM_sleep)):
        coef = calculate_coef_AR(window, pretend=True)
        plt.plot(coef, label=f'coafs {index}')
        coef_nonrem.append(coef)
    plt.title("All coef for nonREM sleep (pretend)")
    plt.savefig(os.path.join(set_path(MODEL_PATH), "coefs_nonREM_pretend.jpg"), dpi=100)
    plt.show()

    ## calculation standard deviation and average
    std_nonrem = standard_deviation(numpy.array(coef_nonrem))
    avg = average_coef(coef_nonrem)

    nonrem = {
        'coef': [ c.tolist() for c in coef_nonrem],
        'std_coef': std_nonrem.tolist(),
        'avg_coef': avg
    }

    ## REM sleep

    pretend_REM_sleep = (float(1)*default_sleep_signal) + (float(0.01)* noise)

    plt.subplot(2,1,2)
    plt.plot(signal[:200],pretend_REM_sleep[:200])
    plt.savefig(os.path.join(set_path(MODEL_PATH), "intervals_REM_sleep.jpg"), dpi=100)
    plt.show()

    ## create REM coef
    coef_rem = []

    for index, window in enumerate(create_windows(pretend_REM_sleep)):
        coef = calculate_coef_AR(window, pretend=True)
        plt.plot(coef, label=f'coafs {index}')
        coef_rem.append(coef)
    plt.title("All coef for REM sleep (pretend)")
    plt.savefig( os.path.join( set_path(MODEL_PATH), "coefs_REM_pretend.jpg" ), dpi=100 )
    plt.show()

    ## calculation standard deviation and average
    std_rem = standard_deviation(numpy.array(coef_rem))
    avg = average_coef(coef_rem)

    rem = {
        'coef': [ c.tolist() for c in coef_rem],
        'std_coef': std_rem.tolist(),
        'avg_coef': avg
    }

    data = {}
    data['nonREM'] = nonrem
    data['REM'] = rem

    save_as_json(data)

    ## Display pretend nonREM and REM sleep

    plt.plot( data['nonREM']['avg_coef'], label='nonREM')
    plt.plot( data['REM']['avg_coef'], label='REM')
    plt.title("Compare nonREM and REEM (pretend)")
    plt.savefig( os.path.join( set_path(MODEL_PATH), "nonREM_and_REM_compare.jpg"), dpi=100 )
    plt.show()

