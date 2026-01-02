import pandas as pd 
import json

data_base_word = pd.read_csv('Data_base_word.csv')
Emotional_base = pd.read_csv('Emotional_base.csv')
Word_base_ru = pd.read_csv('Word_base_ru.csv')

with open("Data_base.json", "r", encoding="utf-8") as f:
    data_base = json.load(f)
    
with open("education_matrix.json", "r", encoding="utf-8") as f:
    education_matrix = json.load(f)
    
class perseptron1:
    def __init__(self, education_matrix, data_base, data_base_word):
        self.education_matrix = education_matrix
        self.data_base = data_base
        self.data_base_word = data_base_word