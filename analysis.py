import os
import matplotlib.pyplot as plt
import numpy
from statsmodels.tsa.ar_model import AutoReg as AR


MAIN_PATH_PATIENTS = ".\\patient"
MAIN_PATH_RESULTS = ".\\results"


def set_path(path, *args):
    # make sure path is exists
    new_path = os.path.join(path, *args)
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    return new_path


def calculate_coef_AR(data: list, pretend=False):

    train_model = numpy.array(data)
    if pretend:
        model = AR(train_model, lags=8)
    else:
        model = AR(train_model / 1000, lags=8)

    model_fit = model.fit()
    coef = model_fit.params

    return coef

def create_plot(data: list, title: str, title_x: str, title_y: str, path_to_save):

    plt.plot(data)
    plt.xlabel(title_x)
    plt.ylabel(title_y)
    plt.title(title)

    path = set_path(path_to_save, title)

    plt.savefig(path+'.jpg', dpi=80)
    plt.show()

def create_windows(data, quantity=1000):
    """
    The function divides the data into windows of specified lengths.        :param quantity:
    :param: quantity ( window length )
    """
    stop = len(data)
    for start in range(0, stop, quantity):
        yield data[start:min(start+quantity, stop)]

class Patient:

    def __init__(self, file_name):
        self.file_name = file_name
        self.gender = file_name[:1]
        self.age = file_name[1:3]
        self.id = file_name[4:9]
        self.data = None
        self.windows = None

        self.result_path_save = os.path.join(MAIN_PATH_RESULTS, self.gender, self.age, self.id)


    def get_data(self):
        """
        """
        with open(os.path.join(MAIN_PATH_PATIENTS, self.file_name)) as f:
            data = [float(line) for line in f]
        self.data = data
        return data

    def create_tachogram(self):

        if not self.data:
            raise NotImplementedError()

        create_plot(self.data, 'Tachograf', 'n', 'RR [ms]', self.result_path_save)
        print(f"The tachogram has been saved to: '{self.result_path_save}' as a file name 'Tachogram.jpg'")

    # def create_windows(self, quantity=1000):
    #     """
    #     The function divides the data into windows of specified lengths.        :param quantity:
    #     :param: quantity ( window length )
    #     """
    #     stop = len(self.data)
    #     for start in range(0, stop, quantity):
    #         yield self.data[start:min(start+quantity, stop)]

    # def calculate_coef_AR(self, data: list):
    #
    #     train_model = numpy.array(data)
    #     model = AR(train_model/1000, lags=8)
    #     model_fit = model.fit()
    #     coef = model_fit.params
    #
    #     return coef

    def create_coef_AR(self):
        """
        Create file and plot with coef
        :return:
        """
        coefs = []

        for index, window in enumerate(create_windows(self.data)):

            coef = calculate_coef_AR(window)
            plt.plot(numpy.arange(1,6), coef[:5], label=f'coafs {index}')
            coefs.append(coef)

        plt.legend(ncol=3, fontsize='x-small').set_title('Individual coefficients of a given window')
        plt.title("Windows with coefficients")
        plt.xticks(numpy.arange(1,6))

        path = set_path(self.result_path_save, 'Coefs')
        plt.savefig(path + '.jpg', dpi=150)
        plt.show()
        print(f"The figure with five first coefficients has been saved to {self.result_path_save} as a file name cofes.jpg ")

        # create file.txt with coefs
        path = set_path(self.result_path_save, 'coefs')
        with open(path+'.txt', 'w') as file:
            for list in coefs:
                for single_item in list:
                    file.write(f"{single_item:.18}    ")
                file.write('\n')


if __name__ == '__main__':
    a = Patient("k19_12.00.cut_500.txt")
    a.get_data()
    #a.create_tachogram()
    #print(a.calculate_coef_AR())
    a.create_coef_AR()


