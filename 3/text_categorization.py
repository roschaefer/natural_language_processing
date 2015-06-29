import os

class DataSet:
    def __init__(self, folder):
        self.folder = folder
        self.init_target()

    def init_target(self):
        training_folder = self.folder + "/training/"
        self.target_names = sorted(next(os.walk(training_folder))[1])
        self.target = list(range(1, len(self.target_names)+1))






