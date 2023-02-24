"""
Kimberly Stochaj
IE 4525
Data Formatting
22 February 2023
HeartDiseaseOneHot.py
"""

# import necessary libraries and initialize constants
import pandas as pd

DESIRED_COLS = ["age", "sex", "chest pain type", "resting bp s", "cholesterol", "fasting blood sugar", "target"]
NUMERIC_COLS = ["age", "chest pain type", "resting bp s", "cholesterol", "max heart rate", "oldpeak"]
NUM_BUCKETS = 4
TREATMENT = "cholesterol"
HIGH_LOW = 1

def main():
    # read in the data file
    df_heart = pd.read_csv("HeartData.csv")
    
    # get rid of the undesired columns
    remove_cols = [col_name for col_name in df_heart.columns if col_name not in DESIRED_COLS]
    df_heart.drop(remove_cols, axis = 1, inplace = True)
    
    # "bucketize" necessary columns, perform one hot encoding
    for col in NUMERIC_COLS:
        if col in df_heart.columns and col != TREATMENT:
            new_cols = pd.get_dummies(pd.qcut(df_heart[col], q=NUM_BUCKETS, duplicates = "drop"), prefix = col)
            df_heart[new_cols.columns] = new_cols
            df_heart.drop(col, axis = 1, inplace = True)
        elif col == TREATMENT:
            new_cols = pd.get_dummies(pd.qcut(df_heart[col], q=2, duplicates = "drop"), prefix = col)
            df_heart[new_cols.columns] = new_cols
            df_heart.drop(col, axis = 1, inplace = True)
            new_treatment = new_cols.columns.to_list()[HIGH_LOW]
    
    if TREATMENT not in NUMERIC_COLS:
        new_treatment = TREATMENT
            
    # move the target column to the last position (mostly aesthetics)
    all_cols = df_heart.columns.to_list()
    target_idx = all_cols.index("target")
    all_cols.insert(len(all_cols), all_cols.pop(target_idx))
    df_heart = df_heart[all_cols]
    
    # split the data frame based on the target value
    grouped_df = df_heart.groupby(new_treatment)
    
    df_no_disease = grouped_df.get_group(0)
    df_no_disease.reset_index(inplace = True)
    df_no_disease.drop("index", axis = 1, inplace = True)
    
    df_yes_disease = grouped_df.get_group(1)
    df_yes_disease.reset_index(inplace = True)
    df_yes_disease.drop("index", axis = 1, inplace = True)
               
    # write new df to a csv file
    df_heart.to_csv("Binary_HeartData.csv")
    df_yes_disease.to_csv("Binary_DiseaseTrue.csv")
    df_no_disease.to_csv("Binary_DiseaseFalse.csv")
    
    
main()
