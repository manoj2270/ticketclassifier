#class to load the data from different input sources

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

class load_data():

    def __init__(self,file):
        self.filename = file


if __name__ == "__main__":
    data = load_data("test.csv")