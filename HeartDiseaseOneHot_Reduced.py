"""
Kimberly Stochaj
IE 4525
Data Formatting
22 February 2023
HeartDiseaseOneHot.py
"""

# import necessary libraries and initialize constants
import pandas as pd
import numpy as np

DESIRED_COLS = ["age", "sex", "chest pain type", "resting bp s","cholesterol", "target"]
NUMERIC_COLS = ["age", "chest pain type", "resting bp s", "cholesterol", "max heart rate", "oldpeak"]
NUM_BUCKETS = 4
TREATMENT = "resting bp s"
CHAR_LST = ["(", ")", "[", "]", ","]
# identifies the treatment, 0 for the low bucket, 1 for the high bucket
HIGH_LOW = 1
# adds an additional string to the filename
FN_AUGMENT = "_Reduced"

def clean_str(my_str):
    """ clean string so acceptable as AMPL variable name
        
        Args: 
            my_str (str): column header created by pandas qcut
            
        Returns:
            my_str (str): column header without (, ), [, ], and commas"
    """
    my_str = my_str.replace(" ", "_")
    for char in CHAR_LST: 
        my_str = my_str.replace(char, "")
        
    return my_str
    

def main():
    # read in the data file
    df_heart = pd.read_csv("HeartData.csv")
    
    # get rid of the undesired columns
    remove_cols = [col_name for col_name in df_heart.columns if col_name not in DESIRED_COLS]
    df_heart.drop(remove_cols, axis = 1, inplace = True)
    
    # "bucketize" necessary columns, perform one hot encoding
    # all cols are split into NUM_BUCKETS buckets except treatment (always two buckets)
    for col in NUMERIC_COLS:
        '''
        if col in df_heart.columns and col != TREATMENT:
            new_cols = pd.get_dummies(pd.qcut(df_heart[col], q=NUM_BUCKETS, duplicates = "drop"), prefix = col)
            df_heart[new_cols.columns] = new_cols
            df_heart.drop(col, axis = 1, inplace = True)
        '''
            
        if col == TREATMENT:
            new_cols = pd.get_dummies(pd.qcut(df_heart[col], q=2, duplicates = "drop"), prefix = col)
            df_heart[new_cols.columns] = new_cols
            df_heart.drop(col, axis = 1, inplace = True)
            new_treatment = new_cols.columns.to_list()[HIGH_LOW]
            # TODO drop "control" column? 
    
    # assign the value of "new_treatment" if not done already
    if TREATMENT not in NUMERIC_COLS:
        new_treatment = TREATMENT
    '''        
    # move the target column to the last position (mostly aesthetics)
    all_cols = df_heart.columns.to_list()
    target_idx = all_cols.index("target")
    all_cols.insert(len(all_cols), all_cols.pop(target_idx))
    df_heart = df_heart[all_cols]
    '''
    
    # split the data frame based on the target value
    # TODO refactor to use a loop for this section and next?
    grouped_df = df_heart.groupby(new_treatment)
    
    df_control = grouped_df.get_group(0)
    df_control.reset_index(drop = True, inplace = True)
    
    df_treatment = grouped_df.get_group(1)
    df_treatment.reset_index(drop = True, inplace = True)
    
    # move the target column from both DataFrames to their own DataFrame
    df_control_results = pd.DataFrame().assign(target = df_control["target"])
    df_control.drop("target", axis = 1, inplace = True)
    
    df_treatment_results = pd.DataFrame().assign(target = df_treatment["target"])
    df_treatment.drop("target", axis = 1, inplace = True)
    
    updated_col_lst = []
    for col_name in df_treatment.columns:
        updated_col_lst.append(clean_str(col_name))
        
    df_control.columns = updated_col_lst
    df_treatment.columns = updated_col_lst
    
    print(df_control.columns[4:])
    

    df_control.drop(df_control.columns[4:], axis = 1, inplace = True)
    df_treatment.drop(df_treatment.columns[4:], axis = 1, inplace = True)
    
    my_df = [df_control, df_control_results, df_treatment, df_treatment_results]
    
    for df in my_df:
        df.index = np.arange(1, len(df) + 1)
    
    # write necessary DataFrames to csv files
    df_heart.to_csv("Binary_HeartData.csv")
    
    df_control.to_csv(f"ControlData{FN_AUGMENT}.txt", sep = "\t")
    df_treatment.to_csv(f"TreatmentData{FN_AUGMENT}.txt", sep = "\t")
    
    df_control_results.to_csv(f"ControlResults{FN_AUGMENT}.txt", sep = "\t")
    df_treatment_results.to_csv(f"TreatmentResults{FN_AUGMENT}.txt", sep = "\t")

    
    
main()
