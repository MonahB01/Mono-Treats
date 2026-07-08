import argparse
import random
import pandas as pd
import numpy as np
from scipy.integrate import simpson
from scipy.integrate import trapezoid
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d
from datetime import date

def spk_calc(x):
    if x<=0:
        result= start_dil/2
    elif x <= 1:
        result= start_dil
    else:
        result=((start_dil)*((dil_fact))**(x-1))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='16 sample elisa plate analysis',
        description= 'Feed in elisa plate data spit out AUC and End Titer data',
            epilog="||||| ver 0.3.0: Cosmopolitan ||||| Added OVRFLW error parsing")
    parser.add_argument('filepath', help='Filename of the file to be processed *CASE SENSITIVE* .CSV or XLSX format only!')
    parser.add_argument('-sn','--sheetname', help='*EXCEL ONLY* If data is in a specific sheet specify sheet name *CASE SENSITIVE*', action='store' ,default='Sheet1')
    parser.add_argument('-i', '--initials', help='Initials of the User: *FOR AUTOMATED OUTPUT ONLY*', action='store', default="Unk")
    parser.add_argument('-sd', '--start_dil', help="Starting dilution * #'s only and no 0*", action='store', default=100)
    parser.add_argument('-r', '--round', help='Change the number of decimal points. Default = 2', action='store', default=2)
    parser.add_argument('-df', '--dil_fact', help="Dilution factor of assay whole * #'s only and no 0*", action='store', default=2)
    parser.add_argument('-c', '--cut_off', help="Cutoff for your analysis", action='store', default=0.15)
    parser.add_argument('-of', '--outfile', help='Custom destination of output file. *Default value only works on mac with sharepoint synced!*', 
                    action='store',

                    #If you want the automated save to work change the file path here:
                    default='~/The Mount Sinai Hospital/Krammer Lab Serology Core - Documents/Python Output/')

    args=parser.parse_args()

    r2=[]
    c_end_spk=[]
    auc=[]
    plate_list=[]
    long_label=[]
    plate_list_2=[]
    plate_list_3=[]
    plate_skip=[]
    n=0
    dil_fact = int(args.dil_fact)
    start_dil = int(args.start_dil)
    sname = str(args.sheetname)
    cut = float(args.cut_off)
    rnd = int(args.round)

    xvals=[(1/2)*start_dil]
    
    i=0
    while i<12:
        if i == 0:
            xvals.append(xvals[i]*2)
            i+=1
        else:
            xvals.append(xvals[i]* dil_fact)
            i+=1

    print(xvals) 
#add more functionality here

    try:
        plates_from_file = pd.read_excel(args.filepath, sheet_name=sname, header=None)
    except:
        try:
            plates_from_file = pd.read_csv(args.filepath, header=None, sep=',')
        except:
            pass


    plates_from_file.dropna(axis=0, thresh=4, inplace=True)
    plates_from_file.dropna(axis=1, inplace=True)
    plates_from_file.index = np.arange(plates_from_file.shape[0])
    
    plate_list = [plates_from_file.iloc[9*i:9*(i+1), : ].copy().rename(index=lambda val: val % 9) for i in range(plates_from_file.shape[0] // 9)]

    for plate in plate_list:
        plate_1 = plate.iloc[:,2:7]
        plate_2 = plate.iloc[:,7:12]
        plate_list_2.append(plate_1)
        plate_list_2.append(plate_2)

    for plate in plate_list_2:

        overflow = 0

        plate.drop(0, axis=0, inplace=True)
        
        ovrflw = plate[plate == 'OVRFLW'].count()
        overflow = ovrflw[ovrflw > 0].count()

        if overflow >= 1:
            print('Over Flow Error! Skipping Plate '+ str(n+1))
            plate_skip.append(n)
            n+=1
            continue

        n+=1

        plate.columns = range(plate.columns.size)
        mapper = {col: i for i, col in enumerate(plate.columns)}
        # print("index", plate.index)
        # print("columns", plate.columns)
        #plate3 = plate2.drop(0,axis=1)
        plate['Over_Cut'] = (plate.iloc[:9,:]>=cut).sum(axis=1)
        plate['Dilutions'] = ((plate.iloc[:9,:]<=cut).idxmax(axis=1).apply(lambda col: mapper[col]))
        plate['End_Titer'] = plate['Dilutions'].apply(spk_calc)
        plate['Pre Flag'] = ((plate['Over_Cut']) - plate['Dilutions'])
        plate.loc[plate['Pre Flag'] < 0, "Flag"] = "SYS ERR"
        plate.loc[plate['Pre Flag'] <= 4, "Flag"] = "Check Trend"
        plate.loc[plate['Pre Flag'] == 0, "Flag"] = "Ok"
        plate.loc[plate['Pre Flag'] <= 5, "Flag"] = "Titer High"
        plate.drop('Pre Flag', inplace=True, axis=1)

        plate_list_3.append(plate)

    if len(plate_skip) == len(plate_list):
        print("All plates invalid! Review source file!")
        print("Program Stopped Early!")
        quit()
    
    for plate in plate_list_3:
        auc=[]
        c_end_spk=[]
        for name,row in plate.iterrows():
            i=0
            r2=[]
            if row[3] > cut:
                if row[4] > cut:
                    auc.append('N/A')
                    c_end_spk.append('N/A')
                    continue

            for val in row:
                if val <= cut:
                   li= i
                   gi= i-1
                   break
                else:
                    i+=1
            if i==0:
                auc.append('N/A')
                c_end_spk.append('N/A')
                continue

            r = row[:6].tolist()
            for val in r:
                r2.append(val-cut)
            intpx = xvals[gi+1],xvals[li+1]
            intpy = [r2[gi],r2[li]]
            intlf = interp1d(intpy,intpx)

            ycross = intlf(0)
    
            c_end_spk.append(ycross)
            trend = r2[:gi+1]
            newxvals = xvals[1:len(trend)+1]
            newxvals.append(float(ycross))
            trend.append(0)
            auc.append(round(trapezoid(trend,newxvals), rnd))
        
        plate['AUC'] = auc
        plate['Inter_point'] = c_end_spk
    
    AUC_final=pd.concat(plate_list_3, axis = 0)

    label_beg = xvals[0:5]
    label_end = AUC_final.columns[5:].tolist()
    label_list = label_beg + label_end

    AUC_final.columns = label_list

    td = date.today()
    td=td.strftime("%d_%m_%Y")
    try:
        AUC_final.to_excel(args.outfile , sheet_name='AUC/Endpoint')
    except:
        try:
            AUC_final.to_csv(args.outfile , sep=',')
        except:
            AUC_final.to_csv(args.outfile + '16_sample_plate_' + args.initials + '_' + td + '.csv', sep=',')

    out_mess = random.randint(0,100)

    if out_mess <= 25:
        print("What's the meaning of life?")
    elif out_mess <= 50:
        print("Done already?, Yea I'm that good ;)")
    elif out_mess <= 60:
        print("I'm finished, you can stop staring")
    elif out_mess <= 70:
        print("#daayyuuuummm")
    elif out_mess <= 80:
        print("Jack of no trades master of one!")
    elif out_mess <= 85:
        print("DiD iT fInIsH yEt?!?!?")
    elif out_mess <= 90:
        print("When your brain doesn't work like it used to before")
    elif out_mess <= 95:
        print("would you like cheese with that wine?")
    elif out_mess <= 99:
        print("SysError: Not Enough tomato")
    elif out_mess <= 100:
        print("42! The Best Answer!")
