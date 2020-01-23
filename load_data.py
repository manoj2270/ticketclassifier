#class to load the data from different input sources

import numpy as np
import pandas as pd
import os
import re
from preprocess import PreprocessText
class load_data():

    def __init__(self,file,target_cols=[],predictor_cols=[],header=0,sheet_name=0,txt_sep=","):
        self.filename = file
        self.target_cols = target_cols
        self.predictor_cols = predictor_cols
        self.header = header
        self.sheet_name = sheet_name
        self.df = None
        self.txt_sep = txt_sep

    def load(self):
        file_type = self.filename.split(".")[-1]

        if file_type=="csv":
            self.df = pd.read_csv(self.filename,header=self.header)

        elif re.findall("^xl[a-z]+",file_type)!=[]:
            self.df = pd.read_excel(self.filename,sheet_name=self.sheet_name)
        elif file_type=="tsv":
            self.df = pd.read_csv(self.filename,sep="\t",header=self.header)
        elif file_type=="txt":
            self.df = pd.read_table(self.filename, sep=self.txt_sep, header=self.header)
        else:
            raise ValueError("we cant handle this file type")

        if  not self.predictor_cols:
            for col in self.df.columns:
                if re.findall("desc[a-z]*", col, flags=re.I) != []:
                    self.predictor_cols.append(col)

        if self.predictor_cols and self.target_cols:
            self.df = self.df.loc[:,self.predictor_cols+self.target_cols]
            return self.df
        else:
            print("there are no description columns or target")
            return self.df


if __name__ == "__main__":
    data = load_data(r"C:\Users\1247565\Desktop\SAS\SAS Older data\Servicw-Now_Inc data (2).xlsx",target_cols=["assignment_group"])
    df = data.load()
    print(data.df.columns)
    print(data.predictor_cols)
    process_df = PreprocessText(df["Short description"]).transform()
    print(process_df.head())
