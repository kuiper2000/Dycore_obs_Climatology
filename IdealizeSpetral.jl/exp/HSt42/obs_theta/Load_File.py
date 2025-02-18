import numpy as np
import h5py

class Load_File:
    def __init__(self, data_name: str):
        self.data_name = data_name
    def load_data(self, file_path):
        with h5py.File(file_path, "r") as file:
            return np.array(file[self.data_name], dtype=np.float32)