import pandas as pd
import numpy as np
import os
from bioblend.galaxy import GalaxyInstance
repo = os.path.expanduser("~/Documents/GitHub/MonoSolutions/")

#%%------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Static utilities
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Galaxy_Key = "Your Galaxy API Key here"
Galaxy_url = "Your Galaxy URL here"

#%%-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Sequencing Utilities
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

def grab_hist_names(gi, hist_list, dict_out=True):
    
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

def hist_id_search(gi, target, is_list=False, exact=False):
    hist_dict = grab_hist_names(target, dict_out=True)
    if exact:
        results = {name: id for name, id in hist_dict.items() if name == target}
    else:
        results = {name: id for name, id in hist_dict.items() if target in name}
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
