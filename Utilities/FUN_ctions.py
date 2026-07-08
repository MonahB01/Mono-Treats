#%% 
import os
import re
import math
import codecs
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle as pk

try:
    import PyPDF2 as pf
except:
    print("PyPDF2 not found, PDF utilities will not work. Please install PyPDF2 to use PDF utilities.")

repo = "~/Documents/GitHub/MonoSolutions/"

#%%------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data utilities
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def path_agnostic(filepath):
    pathsplit = re.split(r"\\|\/", filepath)
    agnostic = os.path.join(*pathsplit)
    agnostic_path = os.path.expanduser(agnostic)
    return(agnostic_path)

def data_import(filepath, excel_sheet=None, head=0):
    data_frame=[]
    pathsplit = re.split("\.", filepath)
    if "xl" in pathsplit[-1].lower():
        data_frame = pd.read_excel(filepath, sheet_name=excel_sheet, header=head)
        print("Success! Excel file!")        
    elif "csv" == pathsplit[-1].lower():
        data_frame = pd.read_csv(filepath, header=head, sep=',')
        print("Success! CSV delimited!")        
    elif "tsv" == pathsplit[-1].lower():
            data_frame = pd.read_csv(filepath, header=head, sep='\t')
            print("Success! TAB delimited!")        
    elif "txt" == pathsplit[-1].lower():
        try:
            data_frame = pd.read_csv(filepath, header=head, sep='\t')
            print("Success! TAB delimited!")
        except:
            try:
                data_frame = pd.read_csv(filepath, header=head, sep=';')
                print("Success! semi-colon delimited")
            except:
                try:
                    data_frame = pd.read_csv(filepath, header=head, sep=' ')
                    print("Success! Space delimited")
                except:
                    raise ValueError("FileType not found: Please check your Filepath and only use: \n excel ,.csv ,.tsv ,.txt extensions")
    return(data_frame)

def route_table(target, output, target_sheet, output_sheet, target_head=0, output_head=0):
    duplicate = data_import(target, target_sheet, target_head)
    with pd.ExcelWriter(output, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        duplicate.to_excel(writer, sheet_name=output_sheet)
    return("Routed!")

def Race_Recode(df, column):
    dummy_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    new_entry = False
    quiting = False

    with open(os.path.expanduser(repo + "pickles/Race_pkl.pkl"), "rb") as file:
        race_dict = pk.load(file)
    
    for value in df[column].unique():
        
        if value != value:
            continue
        
        val = value.strip().lower()
        
        for n, (key, recode_list) in enumerate(race_dict.items()):
                       
            if val in recode_list:
                if  "Race Recode" not in df.columns:
                    df["Race Recode"] = df[column].replace(value, key)
                    break
                else:
                    df["Race Recode"] = df["Race Recode"].replace(value, key)
                    break

            elif n == len(race_dict) - 1:
                print("================================")
                
                new_entry = True
                
                print(f"Race value '{val}' not found in pkl.\n Please add the category of the race\n accepted categories are:")
                for l, key in enumerate(race_dict.keys()):
                    print(f"{l}: {key}") 
                cat_fill = input(f"Remind: {val}, and press enter to continue.")
                
                while cat_fill.strip().lower() not in race_dict.keys():
                    
                    if cat_fill.strip().lower() in ["quit", "exit", "close", "stop", "end", "cancel", "no", "n", "q", "e", "c"]:
                        quiting = True
                        break
                    
                    try:
                        if quiting == True:
                            break
                        elif int(cat_fill) in dummy_list and int(cat_fill) < len(race_dict.keys()):
                            break
                    except ValueError:
                        pass

                    else:
                        print("Category not found, please add the category to the pkl and try again.")
                        print(f"Accepted Categories are:") 
                        for l, key in enumerate(race_dict.keys()):
                            print(f"{l}: {key}")  
                        cat_fill = input("Please add the category to the pkl and try again.")
                
                if quiting==True:
                    break
    
                try:
                    cat_fill_int = int(cat_fill)
                    if cat_fill_int in dummy_list:
                        cat_fill = list(race_dict.keys())[cat_fill_int]
                except ValueError:
                    pass

                race_dict[cat_fill.strip().lower()].append(val)
    
        if quiting==True:
            break
    
    if new_entry == True:
        if quiting==False:
            with open(os.path.expanduser(repo + "pickles/Race_pkl.pkl"), "wb") as file:
                pk.dump(race_dict, file)
            print("New entry added to pkl, please rerun the function to recode the new value.")
        elif quiting==True:
            print("No new entry added to pkl, quit command entered.")
    else:
        print("No new entries added, recoding complete.")


# +_+_+_+_+_+_+_+_+_+ WIP +_+_+_+_+_+_+_+_+_+_+_+

# def COVID_Recode(values):
#     with open(os.path.expanduser(repo + "pickles/COVID_pkl.pkl"), "rb") as file:
#         covid_dict = pk.load(file)

#     recoded_values = []
    
#     for value in values:
#         if value != value:
#             recoded_values.append(value)
#             continue
        
#         val = value.strip().lower()
        
#         recoded = False
        
#         for key, recode_list in covid_dict.items():
#             if val in recode_list:
#                 recoded_values.append(key)
#                 recoded = True
#                 break
        
#         if not recoded:
#             recoded_values.append(value)
#             print(f"COVID value '{val}' not found in pkl. Please add the mapping for the COVID strain")
#             print(f"Passing Old value '{value}' to recoded values.")
#             user_input = input("If Known Mapping, please add the mapping to the pkl and rerun the function. If unknown, please input 'quit' to continue without adding mapping.")
#             if user_input.strip().lower() in ["quit", "exit", "close", "stop", "end", "cancel", "no", "n", "q", "e", "c"]:
#                 print("No new entry added to pkl, quit command entered.")
#             else:
    
#     return(recoded_values)

#%%

variant_reference = pd.read_excel('~/library/CloudStorage/OneDrive-SharedLibraries-TheMountSinaiHospital/Simon Lab - Pathogen Surveillance/Sequencing/Lineage Mappings/variant reference.xlsx', sheet_name='Sheet1', header=0)

#%%-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PDF Utilities
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pdf_split(filepath="default", outfname="default"):
    pdf = pf.PdfFileReader(filepath)
    for page in range(pdf.getNumPages()):
        pdf_writer = pf.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        
        output = f'{outfname}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

def pdf_merge(folderpath='default', outfname="default"):
    merger = pf.PdfFileMerger
    for file in os.listdir(folderpath):
        merger.append(file)
    outfsplit = re.split('\.', outfname)
    if 'pdf' in outfsplit[-1]:
        merger.write(folderpath + outfname)
    else:
        merger.write(folderpath + outfname + '.pdf')


# %% -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Old Utilities - not currently in use but may be useful in the future
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# def bar_explore(filepath="default", df="default", excel_sheet='Sheet1', head=0):
    
#     if filepath != "default":
#         data_frame, int_cols, float_cols, obj_cols = data_split(filepath, excel_sheet=excel_sheet, head=head)
#     else:
#         int_cols, float_cols, obj_cols = data_split(df)
#         data_frame = df
    
#     fig_int, axes_int = graph_maker(quant=len(int_cols), columns=2, style="plots")
#     fig_float, axes_float = graph_maker(quant=len(float_cols), columns=2, style="plots")
#     fig_obj, axes_obj = graph_maker(quant=len(obj_cols), columns=2, style="plots")

#     int_df = data_frame[int_cols]
#     float_df = data_frame[float_cols]
#     obj_df = data_frame[obj_cols]

#     frames = [int_df,float_df,obj_df]
#     plot_axes = [axes_int,axes_float,axes_obj]
    
#     for df, ax_list in zip(frames, plot_axes):
#         for (name, col), ax in zip(df.items(),ax_list):
#             if col.dtype == object:
#                 try:
#                     col = col.apply(codecs.decode("UTF-8"))
#                 except:
#                     pass

#             if col.dtype == object:
#                 if len(col.unique()) > 30:
#                     ax.text(s=f"Length of unique variables \n {len(col.unique())}", x=0.5, y=0.5, fontsize=18, fontweight='bold', ha='center')
#                     ax.title.set_text(name)

#                 else:
#                     sns.countplot(x=col, ax=ax)
#                     ax.title.set_text(name)
#                     labels = ax.get_xticklabels()
#                     ax.set_xticklabels(labels, rotation=30, ha='right')
                   
#             elif len(col.unique()) <= 10:
#                 sns.countplot(x=col, ax=ax)
#                 ax.title.set_text(name)
            
#             else:
#                 sns.histplot(x=col, ax=ax, kde=True)
#                 ax.title.set_text(name)

#     fig_int.suptitle("Integer", fontsize=30, fontweight="bold")
#     fig_float.suptitle("Floats", fontsize=30, fontweight="bold")
#     fig_obj.suptitle("Objects", fontsize=30, fontweight="bold")

#     plt.show(fig_int)
#     plt.show(fig_float)
#     plt.show(fig_obj)

#     return(data_frame)

# def cat_explore(filepath, df=False, excel_sheet='Sheet1', head=0):
#     if filepath != "default":
#         data_frame, int_cols, float_cols, obj_cols = data_split(filepath, excel_sheet=excel_sheet, head=head)
#     else:
#         int_cols, float_cols, obj_cols = data_split(df)
#         data_frame = df


#     maybe_cat_list = []

#     for name, col in data_frame.items():
#         if len(col.unique()) <= 15:
#             maybe_cat_list.append(name)
    
#     cat_fig, cat_axes = graph_maker(quant=len(maybe_cat_list), columns=2, style='plots')

#     for name, ax in zip(maybe_cat_list, cat_axes):
#         sns.countplot(data=data_frame, x=name, ax=ax)
#         ax.title.set_text(name)
#         labels = ax.get_xticklabels()
#         ax.set_xticklabels(labels, rotation=30, ha='right')

#     plt.show(cat_fig)

#     return(data_frame)

# def cont_explore(filepath, df=False, excel_sheet='Sheet1', head=0):
    
#     if df != False:
#         int_cols, float_cols, obj_cols = data_split(df, data_types="all")
#         data_frame = df
#     else:
#         data_frame, int_cols, float_cols, obj_cols = data_split(filepath, excel_sheet=excel_sheet, head=head)

#     maybe_cont_list = []

#     for name, col in data_frame.items():
#         if len(col.unique()) >= 15 and len(col.unique()) <= (0.75 * len(col)):
#             maybe_cont_list.append(name)
    
#     cont_fig, cont_axes = graph_maker(quant=len(maybe_cont_list), columns=2, style='plots')

#     for name, ax in zip(maybe_cont_list, cont_axes):
#         sns.histplot(data=data_frame, x=name, ax=ax)
#         ax.title.set_text(name)

#     plt.show(cont_fig)

#     return(data_frame)
