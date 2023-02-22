import os
import matplotlib.pyplot as plt

MAIN_PATH_PATIENTS = ".\\patient"
MAIN_PATH_RESULTS = ".\\results"


def check_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return True


def create_plot(data, title, title_x, title_y, path_to_save):

    plt.plot(data)
    plt.xlabel(title_x)
    plt.ylabel(title_y)
    plt.title(title)


    if check_path_exists(path_to_save):
        path = os.path.join(path_to_save, title)
        plt.savefig(path+'.jpg', dpi=80)


    plt.show()

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
        print(f"The tachogram has been saved to: '{self.result_path_save}' as a file named 'Tachogram.jpg'")

    def create_windows(self, quantity=1000):
        """
        The function divides the data into windows of specified lengths.        :param quantity:
        :param: quantity ( window length )
        """
        stop = len(self.data)
        for start in range(0, stop, quantity):
            self.windows.append(self.data[start:min(start+quantity, stop)])

a = Patient("k19_12.00.cut_500.txt")
print(a.file_name)
print(a.gender)
print(a.age)
print(a.id)
a.get_data()
a.create_tachogram()

