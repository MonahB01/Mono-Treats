#%%
import pandas as pd
import numpy as np
from bioblend.galaxy import GalaxyInstance
import Utilities.FUN_ctions as fun
import re
import os
import time

#%%
#API Pull Codes
gi = GalaxyInstance(url=fun.Galaxy_url, key=fun.Galaxy_Key)
hist_list = gi.histories.get_histories()

#%% Founder Functions for Easier Access

def Start_history(gi, hist_name, files=None):
    if type(files) is not list:
        return('Error: files must be a list of file paths')
    new_hist = gi.histories.create_history(name=hist_name)
    if files is not None:
        for file in files:
            gi.tools.upload_file(os.path.expanduser(file), history_id=new_hist['id'])

    hist_info = gi.histories.show_history(new_hist['id'], contents=True)

    return (new_hist, hist_info)

def grab_workflow_names(gi, dict_out=True):
    workflows = gi.workflows.get_workflows()
    ids = []
    names = []
    name_cast = {}
    for wf in workflows:
        ids.append(wf['id'])
        names.append(wf['name'])
        name_cast.update({wf['name']: wf['id']})
    if dict_out:
        return name_cast
    else:
        return ids, names

def grab_workflow_inputs(gi, wf_id):
    wf = gi.workflows.export_workflow_dict(wf_id)
    steps = wf['steps']
    out_dict = {}
    for name, step in steps.items():
        if step['type'] == 'data_input':
            out_dict[step['id']] = {
                'name': step['name'],
                'label': step.get('label', 'N/A'),
                'format': step.get('format', 'N/A')
            }
    return out_dict

def workflow_id_search(gi, search_str, is_list=False, exact=False):
    wf_dict = grab_workflow_names(gi, dict_out=True)
    if exact:
        results = {name: id for name, id in wf_dict.items() if name == search_str}
    else:
        results = {name: id for name, id in wf_dict.items() if search_str in name}
    if is_list:
        return list(results.values())
    return results

def grab_hist_names(hist_list, dict_out=True):
    ids = []
    names = []
    name_cast = {}
    for hist in hist_list:
        ids.append(hist['id'])
        names.append(hist['name'])
        name_cast.update({hist['name']: hist['id']})
    if dict_out:
        return name_cast
    else:
        return ids, names

def grab_hist_contents(gi, hist_id, dict_out=True):
    hist = gi.histories.show_history(history_id=hist_id, contents=True)
    ids = []
    names = []
    name_cast = {}
    for item in hist:
        ids.append(item['id'])
        names.append(item['name'])
        name_cast.update({item['name']: item['id']})
    if dict_out:
        return name_cast
    else:
        return ids, names

def hist_id_search(gi, search_str, is_list=False, exact=False):
    hist_dict = grab_hist_names(hist_list, dict_out=True)
    if exact:
        results = {name: id for name, id in hist_dict.items() if name == search_str}
    else:
        results = {name: id for name, id in hist_dict.items() if search_str in name}
    if is_list:
        return list(results.values())
    return results

def hist_content_search(gi, hist_id, search_str, is_list=False, exact=False):
    cont_dict = grab_hist_contents(gi, hist_id, dict_out=True)
    if exact:
        results = {name: id for name, id in cont_dict.items() if name == search_str}
    else:
        results = {name: id for name, id in cont_dict.items() if search_str in name}
    if is_list:
        return list(results.values())
    return results

#%%
# Compound functions
#Upload and start new IAV history
def Folder_Initialize_History(gi, file_folder, pathogen='IAV'):
    file_list = {}
    name_list = []
    hist_list = []
    Hist_info_list = []
    for file in os.listdir(os.path.expanduser(file_folder)):
        print(file)
        print(' ')
        if re.search(r'.fastq.gz$', file):
            file_name = file.split('/')[-1]
            print(file_name)
            print(' ')
            if re.search(r'_R1_', file_name):
                file_check = file_name.split('_R1_')[0]
            elif re.search(r'_R2_', file_name): 
                file_check = file_name.split('_R2_')[0]
            
            if file_check not in name_list:
                name_list.append(file_check)
                file_list[file_check] = os.path.join(os.path.expanduser(file_folder), file)
            else:
                file_list[file_check] = [file_list[file_check], os.path.join(os.path.expanduser(file_folder), file)]

    for file_key in file_list.keys():
        new_hist, hist_info = Start_history(gi, f'{pathogen}_{file_key}', files=file_list[file_key])
        hist_list.append(new_hist)
        Hist_info_list.append(hist_info)
    return hist_list, Hist_info_list

#%% Master Functions
#def IAV_Folder_Flow(gi, wf_id, hist_id):


#%% Testing environments and functions
hist_dict = grab_hist_names(hist_list, dict_out=True)

hist_flu = []
for name in hist_dict.keys():
    if re.search(r'IS', name):
        hist_flu.append(name)

hist_target = []
for name in hist_flu:
    Id_num = name[-3:]
    if Id_num.isdigit():
        hist_target.append(name)
working_dict = {}
for name, key in hist_dict.items():
    if name in hist_target:
        working_dict[name] = key

# %%
# final_download = {}
# for name, key in working_dict.items():
#     print(f'Working on {name}')
#     hist = gi.histories.show_history(history_id=key, contents=True)
#     contigs_dict =  {}
#     blast_dict = {}
#     for item in hist:
#         if re.search(r'metaSPAdes', item['name']):
#             if re.search(r'Contigs', item['name']):
#                 contigs_dict.update({'name':item['name'], 'Id': item['id']})
#         else: 
#             if re.search(r'megablast', item['name']):
#                 blast_dict.update({'name':item['name'], 'Id': item['id']})
#     final_download.update({name:[contigs_dict,blast_dict]})


# # %%
# gi = GalaxyInstance(url=fun.Galaxy_url, key=fun.Galaxy_Key)
# #download files
# for name, dicts in final_download.items():
#     for n, item in enumerate(dicts):
#         file_name = item['name']
#         file_id = item['Id']
#         print(f'Downloading {file_name} from {name}')
#         if not os.path.exists(os.path.join(os.path.expanduser('~/Downloads'), name)):
#             os.mkdir(os.path.join(os.path.expanduser('~/Downloads'), name))
#         out_path = os.path.join(os.path.expanduser('~/Downloads'), name, file_name)
        
#         if n == 0:
#             gi.datasets.download_dataset(file_id, out_path + ".fasta", use_default_filename=False)
#             print(f'Contigs file downloaded for {name}')
#         elif name == "IS036":
#             continue
#         else:
#             gi.datasets.download_dataset(file_id, out_path + ".csv", use_default_filename=False)
#             print(f'Blast file downloaded for {name}')
#         time.sleep(2.5)

# %%

def Flu_Hist_Invocation(gi, file_path, wf_name="Base Flu Pipe", pathogen='IAV', file_path_is_hist=False):
    wf_dict = workflow_id_search(gi, wf_name, is_list=False, exact=True)
    wf_info = grab_workflow_inputs(gi, wf_dict[wf_name])
    if not file_path_is_hist:
        hist_list, hist_info_list = Folder_Initialize_History(gi, file_path, pathogen=pathogen)
        for hist, hist_info in zip(hist_list, hist_info_list):
            R1_id = None
            R2_id = None
            for item in hist_info:
                if re.search(r'_R1_', item['name']):
                    R1_id = item['id']
                elif re.search(r'_R2_', item['name']):
                    R2_id = item['id']
            inputs = {}
            for step_id, step_info in wf_info.items():
                if re.search(r'R1', step_info['label'], re.IGNORECASE):
                    inputs.update({step_id: {'id': R1_id, 'src': 'hda'}})
                elif re.search(r'R2', step_info['label'], re.IGNORECASE):
                    inputs.update({step_id: {'id': R2_id, 'src': 'hda'}})
            
            gi.workflows.invoke_workflow(wf_dict[wf_name], inputs=inputs, history_id=hist['id'])
    else:
        hist = gi.histories.show_history(history_id=file_path, contents=True)
        R1_id = None
        R2_id = None
        for item in hist:
            if re.search(r'_R1_', item['name']):
                R1_id = item['id']
            elif re.search(r'_R2_', item['name']):
                R2_id = item['id']
        inputs = {}
        for step_id, step_info in wf_info.items():
            if re.search(r'R1', step_info['label'], re.IGNORECASE):
                inputs.update({step_id: {'id': R1_id, 'src': 'hda'}})
            elif re.search(r'R2', step_info['label'], re.IGNORECASE):
                inputs.update({step_id: {'id': R2_id, 'src': 'hda'}})
        
        gi.workflows.invoke_workflow(wf_dict[wf_name], inputs=inputs, history_id=file_path)

    return('Workflow Invoked: Check Galaxy for progress')