import pandas as p
import random as r

def select_random_word():
    try:
        with open("words_to_learn.csv","r") as file:
            data = p.read_csv("words_to_learn.csv")
            data_in_dataframe = p.DataFrame(data)
            data_in_dictionary = data_in_dataframe.to_dict(
                orient="records")  # Converts the data-frame into a list of dictionaries

            random_number = r.randint(0, len(data_in_dictionary)-1)
            return data_in_dictionary
    except FileNotFoundError:
        data = p.read_csv("data/french_words.csv")
        data_in_dataframe = p.DataFrame(data)
        data_in_dictionary = data_in_dataframe.to_dict(
            orient="records")  # Converts the data-frame into a list of dictionaries

        return data_in_dictionary
