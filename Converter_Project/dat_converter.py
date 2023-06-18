"""
Created by Kimberly Stochaj - stochaj.k@northeastern.edu
IE 4515
creates all of three .dat files necessary from a single csv
5 June 2023
mod_converter.py
"""

# import necessary libraries and initialize constants
import pandas as pd
import numpy as np
import PySimpleGUI as psg

N_PAIRS = 30

def get_user_input_filename():
    """ gets information from the user on what file to use
    
        Args:
            None
            
        Returns:
            filename (string): name of file to open and use
            fn_augment (string): identifier that will be added to created files
    """
    l1 = psg.Text("Please enter the exact file name of the .csv file you would like to use for the analysis - include the file extension e.g. HeartData.csv")
    t2 = psg.Input(key = "filename")
    l3 = psg.Text("Please enter an identifier you would like to be included in the filenames of the generated files (optional):")
    t4 = psg.Input(key = "fn_augment")
    b5 = psg.Button("OK")
    
    layout = [[l1], [t2], [l3], [t4], [b5]]
    window = psg.Window("USER SELECTION", layout)
    
    while True:
        event, values = window.read()
        if event in (psg.WINDOW_CLOSED, "OK"):
            break
    
    window.close()
    
    filename = values["filename"]
    fn_augment = values['fn_augment']
    
    return filename, fn_augment

def get_user_input_vars(header):
   """ gets information from the user on what variables to use
   
       Args:
           header (list): list of all available columns
           
       Returns:
           treat (str): header of the column containing the treatment
           target (str): header of the column containing the target
           cov (list): headers of  columns to be used for matching (covariates)
   """
   # simple text lines
   l1 = psg.Text("please select the variables to be used for treatment, target, and covariates (mutually exclusive):")
   l2 = psg.Text("")
   l3 = psg.Text("Select treatment:")
   l5 = psg.Text("Select target:")
   l7 = psg.Text("Select covariates:")
   l9 = psg.Text("Use high or low value for treatment?:")
   
   # radio button for treatment
   rb4 = []
   for var in header:
       rb4.append(psg.Radio(var, "treat"))
   
   # radio button for target
   rb6 = []
   for var in header:
       rb6.append(psg.Radio(var, "target"))
   
   # checkbox for covariates
   cb8 = []
   for var in header:
       cb8.append(psg.Checkbox(var))
       
   rb10 = []
   rb10.append(psg.Radio("High", "hi_lo"))
   rb10.append(psg.Radio("Low", "hi_lo"))
    
   b11 = psg.Button("FINISHED")
   
   layout = [[l1], [l2], [l3], [rb4], [l5], [rb6], [l7], [cb8], [l9], [rb10], [b11]]
   window = psg.Window("USER SELECTION", layout)
   
   while True:
       event, values = window.read()
       if event in (psg.WINDOW_CLOSED, "FINISHED"):
           break
   
   treat = [x.Text for x in rb4 if x.get() == True][0]
   target = [x.Text for x in rb6 if x.get() == True][0]
   cov = [x.Text for x in cb8 if x.get() == True]
   hi_lo = [x.Text for x in rb10 if x.get() == True][0]
   
   window.close()
   
   if hi_lo == "High":
       hi_lo = 1
   else:
       hi_lo = 0
  
   return treat, target, cov, hi_lo
       
def get_user_input_binary():
    """ gets information from the user on how to break non-binary variables
    
        Args:
            None
            
        Returns:
            treatment_split (numeric or None): value on which to split treatment
                and control groups; returns None if no value provided
    """
    l1 = psg.Text("The treatment you selected is not binary - is there a value that you would like to use to split the treatment and control groups?")
    l2 = psg.Text("please input your answer as only a number e.g. 21.45")
    t3 = psg.Input(key = "split_val")
    b4 = psg.Button("OK")
    
    layout = [[l1], [l2], [t3], [b4]]
    window = psg.Window("USER SELECTION", layout)
    
    while True:
        event, values = window.read()
        if event in (psg.WINDOW_CLOSED, "OK"):
            break
    
    window.close()
    
    if values["split_val"].isnumeric():
        return float(values["split_val"])
    else:
        return None

def write_data (file, data, var_lst):
    """ performs data writing operation needed in create_file
        
        Args:
            file (file object): the file to write the information to
            data (dataframe): the information to write to the file
            var_lst (list): DESCRIPTION
                
        Returns:
            None
    """
    for index, row in data.iterrows():
        info_str = f"{index}\t"
        for var in var_lst:
            info_str += f"{row[var]}\t"
        if index == max(data.index):
            info_str += ";"
        info_str += "\n"
        
        file.write(info_str)
    

def create_file(filename, ftype, var_lst, data_control, data_treat):
    """ creates the desired .dat file
    
        Args:
            filename (string): file name and extension as a single string
            ftype (string): used to augment the opening comment
            var_lst (list): DESCRIPTION
            data_control (dataframe): df with information on control group
            data_treat (dataframe): df with information on treatment group
        
        Returns:
            None
    """
    
    # create file
    file = open(filename, "x")
    
    # opening comment
    file.write(f"# {ftype} data in AMPL format\n\n")
    
    # variable/headder line for control
    var_str = ""
    for var in var_lst:
        var_str += (f"{var}\t")
    file.write(f"param CC:\t{var_str}:=\n")
    
    # data for control
    write_data(file, data_control, var_lst)
    
    # variable/headder line for treatment
    file.write(f"\n\nparam CT:\t{var_str}:=")
    
    #data for treatment
    write_data(file, data_treat, var_lst)
    
    file.close()

def main():
    # import csv to dataframe
    filename, fn_augment = get_user_input_filename()
    df_initial = pd.read_csv(filename)
    header_initial = list(df_initial.columns.values)
    
    # get information from the user on what to include
    treatment, target, covariate_lst, high_low = get_user_input_vars(header_initial)
    
    # remove the columns that aren't being used to create reduced dataframe
    desired_cols = [i for i in covariate_lst]
    desired_cols.extend([treatment, target])
    remove_cols = [col_name for col_name in header_initial if col_name not in desired_cols]
    df_reduced = df_initial.drop(remove_cols, axis = 1)
    
    # split csv into treatment and control groups...
    # first, binarize non-binary treatments if needed
    binary_cols = df_initial.columns[df_initial.isin([0,1]).all()]
    
    if not treatment in binary_cols:
        treatment_split = get_user_input_binary()
        if treatment_split == None:
            # set split_val to the average value of the column
            binary_treat = pd.qcut(df_reduced[treatment], q=2, labels=[0,1])
            df_reduced[treatment] = binary_treat
        else:
            df_reduced.loc[df_reduced[treatment] < treatment_split, treatment] = 0
            df_reduced.loc[df_reduced[treatment] >= treatment_split, treatment] = 1
    
    # perform splitting operation for binary treatment
    df_grouped = df_reduced.groupby(treatment)

    df_control = df_grouped.get_group((high_low + 1) % 2)
    df_treat = df_grouped.get_group(high_low)
        
    # split the treatment and control groups into covariates and outcomes
    df_treat_cov = df_treat[covariate_lst]
    df_treat_outcome = df_treat[target].to_frame()
    
    df_control_cov = df_control[covariate_lst]
    df_control_outcome = df_control[target].to_frame()
    
    # "fix" indices of final dataframes
    final_dfs = [df_treat_cov, df_treat_outcome, df_control_cov, df_control_outcome]
    
    for df in final_dfs:
        df.reset_index(drop = True, inplace = True)
        df.index = np.arange(1, len(df) + 1)
    
    # create covariates.dat
    create_file(f"covariates{fn_augment}.dat", "Covariates", covariate_lst, df_control_cov, df_treat_cov)
    
    # create outcome.dat
    create_file(f"outcome{fn_augment}.dat", "Outcomes", [target], df_control_outcome, df_treat_outcome)
    
    
    # create fracture.dat
    fracture_file = open(f"fracture{fn_augment}.dat", "x")
    # opening comment
    fracture_file.write("#Other data (total # of treatment and control units, covariates set and total # of discordant pairs (n)) in AMPL format\n\n")
    
    # variables describing the number of treatment and control units
    fracture_file.write(f"param T2:={max(df_control_outcome.index)};\nparam T1:={max(df_treat_outcome.index)};\n\n")    
    
    # set listing the covariates used
    cov_str = ""
    for cov in covariate_lst:
        cov_str += (f"{cov}\t")
    
    fracture_file.write(f"set C1:=\t{cov_str};\n\n")
    
    # comment(?) with number of discordant pairs
    fracture_file.write(f"#param n:={N_PAIRS};\n")
    
main()