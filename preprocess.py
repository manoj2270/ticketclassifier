
import nltk
import pandas as pd
nltk.download("stopwords")
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings(action = 'ignore')
from sklearn import preprocessing
from nltk.stem import SnowballStemmer

stop = stopwords.words('english')

class PreprocessText():

    def __init__(self,df):
        self.df = df
        self.processed_df = pd.DataFrame()

    def _clean(self,column):
        column = column.astype(str).str.lower()
        column = column.astype(str).str.replace("\n+", " ")
        column = column.astype(str).str.replace(r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+', ' ')
        column = column.astype(str).str.replace(r'[^a-zA-Z  ]+', '')
        column = column.apply(lambda x: " ".join(y for y in x.split() if y not in stop))

        return column

    def _nlp_preprocessing(self,document):
        snowball_stemmer = SnowballStemmer('english')
        try:
            words = [snowball_stemmer.stem(word) for word in document.split() if word not in stop]
            doc = ' '.join(words)
        except AttributeError:
            print(document)
        return doc
    def transform(self):

        if isinstance(self.df,pd.core.series.Series):
            self.processed_df = self._clean(self.df)
            self.processed_df = self.processed_df.apply(
                lambda text: self._nlp_preprocessing(text))
        elif isinstance(self.df,pd.core.core.frame.DataFrame):
            for col in self.df.columns:
                self.processed_df.loc[:,col]= self._clean(self.df.loc[:,col])
                self.processed_df.loc[:, col] = self.processed_df.loc[:, col].apply(
                    lambda text: self._nlp_preprocessing(text))
        else:
            raise ValueError("Data Format should be dataframe or series")

        return self.processed_df






