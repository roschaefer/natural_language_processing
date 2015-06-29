import os

class DataSet:
    def __init__(self, folder):
        self.folder = folder
        self.data  = list()
        self.target = list()
        training_folder = self.folder + "/training/"
        self.target_names = sorted(next(os.walk(training_folder))[1])

        for i,n in enumerate(self.target_names):
                folder = training_folder + "/" + n + "/"
                for subdir, dirs, files in os.walk(folder):
                    for file in files:
                        text = open(os.path.join(subdir,file),'r')
                        self.data.append(text)
                        self.target.append(i)



