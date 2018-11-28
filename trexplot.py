
# coding: utf-8

# Plotting script for TREACTMECH files written by Hamish Robertson - hr0392 at bristol.ac.uk
#
# Run the script within the directory containing the flowdata, flowvector, stress strain, displacement files. Output by default is within same directory.
#
# Displacement gives the corner nodes, everything else gives the centre of the cells.
#
#
#

import pandas as pd
import os
import numpy as np
import matplotlib.dates as mdates
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages
import sys
from trexoptions import *     #import the option file from within the same folder

cwd = os.getcwd()

def flowdata_import():
    """
    Imports the flowdata file from current working directory. Column names are largely preserved. Takes in only the last time step values.
    Returns a dictionary 'flowfaces' that contains the flowdata for each of the default and user specificed faces.
    """
    flowdata=pd.read_csv(cwd+'/flowdata.tec',sep=r"\s*",skiprows=[0],engine='python')
    flowdata_modified= flowdata[flowdata.columns[:-1]]
    flowdata_modified.columns = flowdata.columns[1:]

    flowdata=flowdata_modified.rename(index=str,columns={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"P(Pa)"':"Pressure(Pa)", '"T(C)"':"Temperature(C)",
    '"SatGas"':"SatGas",'"SatLiq"':"SatLiq",'"X1"':"X1", '"X2"':"X2", '"Pcap(Pa)"':"Pcap", '"DGas_kg/m3"':"DGas_kg_m3",
    '"DLiq_kg/m3"':"DLiq_kg_m3", '"Porosity"':"Porosity", '"Perm_X(m2)"':"Perm_X(m2)", '"Perm_Y(m2)"':"Perm_Y(m2)",
    '"Perm_Z(m2)"':"Perm_Z(m2)", '"Krel_Gas"':"Krel_Gas", '"Krel_Liq"':"Krel_Liq", '"HGas(J/kg)"':"HGas(J_kg)",
    '"HLiq(J/kg)"':"HLiq(J_kg)", '"Cp(J/kg/C)"':"Cp(J_kg_C)", '"TC(W/m/C)"':"TC(W_m_C)", '"DBlk_kg/m3"':"DBlk_kg_m3",
    '"Tdif(m2/s)"':"Tdif(m2_s)"})


    #Last time step - top, bottom, side walls
    val=int(flowdata.loc[flowdata["X"] == 'Zone'][-1:].index[0])#value of the last time zone
    lastval=int(flowdata.index[-1])
    length=lastval - val #length of last time zone
    zone=flowdata[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z) #2D array of the top surface
    bot,btval =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)#bottom surface
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)#MaxY face
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)#MinY face
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)#MaxX face
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)#MinX face

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    flowfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
           'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
               'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            flowfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            flowfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return flowfaces

def flowvector_import():
    """
    Imports the flowvector file from current working directory. Column names are largely preserved. Takes in only the last time step values.
    Returns a dictionary 'vecfaces' that contains the vector data for each of the default and user specificed faces.
    """
    flowvector=pd.read_csv(cwd+'/flowvector.tec',sep=r"\s*",skiprows=[0],engine='python')
    flowvector_modified= flowvector[flowvector.columns[:-1]]
    flowvector_modified.columns = flowvector.columns[1:]

    flowvector=flowvector_modified.rename(index=str,columns={'"X(m)"':"X", '"Y(m)"':"Y",'"Z(m)"':"Z",
    '"FluxLiq"':"FluxLiq", '"FluxLiq_X"':"FluxLiq_X",'"FluxLiq_Y"':"FluxLiq_Y", '"FluxLiq_Z"':"FluxLiq_Z",
    '"PorVelLiq"':"PorVelLiq", '"PorVelLiqX"':"PorVelLiqX",'"PorVelLiqY"':"PorVelLiqY", '"PorVelLiqZ"':"PorVelLiqZ",
    '"FluxGas"':"FluxGas",'"FluxGas_X"':"FluxGas_X",'"FluxGas_Y"':"FluxGas_Y", '"FluxGas_Z"':"FluxGas_Z",
    '"PorVelGas"':"PorVelGas",'"PorVelGasX"':"PorVelGasX",'"PorVelGasY"':"PorVelGasY", '"PorVelGasZ"':"PorVelGasZ",
    '"HeatFlux"':"HeatFlux", '"HeatFlux_X"':"HeatFlux_X",'"HeatFlux_Y"':"HeatFlux_Y", '"HeatFlux_Z"':"HeatFlux_Z"})


    val=int(flowvector.loc[flowvector["X"] == 'Zone'][-1:].index[0])
    lastval=int(flowvector.index[-1])
    length=lastval - val
    zone=flowvector[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval  =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z)
    bot,btval  =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    vecfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
       'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
              'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}


    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            vecfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            vecfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})




    return vecfaces

def displace_import():
    """
    Imports the displacement file from current working directory. Column names are largely preserved. Takes in only the last time step values.
    Returns a dictionary 'dispfaces' that contains the vector data for each of the default and user specificed faces.

    Note I added one to xsec user and half values as you get an extra datapoint for displacement output files.

    """

    column_names=["X","Y","Z","Disp_x","Disp_y","Disp_z"]
    displace=pd.read_csv(cwd+'/displacement.tec',sep=r"\s+",skiprows=[0,1],usecols=[0,1,2,3,4,5],
                         names=column_names,engine='python')

    val=int(displace.loc[displace["X"] == 'Zone'][-1:].index[0])
    lastval=int(displace.index[-1])
    length=lastval - val
    zone=displace[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval  =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z)
    bot,btval  =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)+1]],zone.Y.unique()[int(len(zone.Y.unique())/2)+1]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)+1]],zone.X.unique()[int(len(zone.X.unique())/2)+1]

    dispfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
           'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
               'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True: #added one to xsec half values as you get an extra datapoint
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]+1]
            dispfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]+1]
            dispfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return dispfaces

def aq_conc_import():
    """
    Imports the aq_conc file
    """
    aqconcdata=pd.read_csv(cwd+'/aqconc.tec',sep=r"\s*",skiprows=[0],engine='python')
    aqconcdata_modified= aqconcdata[aqconcdata.columns[:-1]]
    aqconcdata_modified.columns = aqconcdata.columns[1:]

    aqconcdata=aqconcdata_modified.rename(index=str,columns=aqconc_name)
    print(aqconcdata.columns.values)

    print(aqconcdata.head())
    #Last time step - top, bottom, side walls
    val=int(aqconcdata.loc[aqconcdata["X"] == 'Zone'][-1:].index[0])#value of the last time zone
    lastval=int(aqconcdata.index[-1])
    length=lastval - val #length of last time zone
    zone=aqconcdata[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z) #2D array of the top surface
    bot,btval =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)#bottom surface
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)#MaxY face
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)#MinY face
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)#MaxX face
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)#MinX face

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    aqconcfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
           'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
               'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            aqconcfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            aqconcfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return aqconcfaces

def gas_volfrac_import():
    """
    Imports the gas_volfrac file

    Why? See https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
     I need the 'bad lines' - specifically the time-step lines which are 11 values long and wanted to re-use other code that reads in those
     lines for simplicity sake. Theres probably a much cleaner pandas import rule that could have been applied to all file Imports
     that could be worked up fairly quickly... All the importing functions Im sure could be better/cleaner but y'know....

     BE CAREFUL and make sure you wipe the written-in header in the .tec file if you go chaning stuff in here. The function will write a new header if the
     gas_volfrac_name dictionary changes at all. Also because I'm writing inplace for simplicity I make a backup .tec file by default for caution
    """

    with open(cwd+'/gas_volfrac.tec', 'r') as original: data = original.read()
    header=str([i for i in gas_volfrac_name.values()]).strip('[]').replace(',','')
    print (header)
    print (data[0:len(header)])
    if data[0:len(header)]!=header:
        with open(cwd+'/gas_volfrac.tec', 'w') as modified: modified.write(header + "\n" + data)

    gas_volfracdata=pd.read_csv(cwd+'/gas_volfrac.tec',sep=r"\s*",skiprows=[2],engine='python')
    gas_volfracdata=gas_volfracdata.rename(columns=gas_volfrac_name) #fit the column name values with the dictionary

    #Last time step - top, bottom, side walls
    val=int(gas_volfracdata.loc[gas_volfracdata["X"] == 'Zone'][-1:].index[0])#value of the last time zone
    lastval=int(gas_volfracdata.index[-1])
    length=lastval - val #length of last time zone
    zone=gas_volfracdata[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z) #2D array of the top surface
    bot,btval =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)#bottom surface
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)#MaxY face
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)#MinY face
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)#MaxX face
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)#MinX face

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    gas_volfracfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
           'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
               'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            gas_volfracfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            gas_volfracfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return gas_volfracfaces

def mineral_ab_import():
    """
    Imports the mineral.tec file - mineral Abundances
    """
    mineral_ab_data=pd.read_csv(cwd+'/mineral.tec',sep=r"\s*",skiprows=[0],engine='python')
    mineral_ab_data_modified= mineral_ab_data[mineral_ab_data.columns[:-1]]
    mineral_ab_data_modified.columns = mineral_ab_data.columns[1:]

    mineral_ab_data=mineral_ab_data_modified.rename(index=str,columns=min_ab_name)

    #Last time step - top, bottom, side walls
    val=int(mineral_ab_data.loc[mineral_ab_data["X"] == 'Zone'][-1:].index[0])#value of the last time zone
    lastval=int(mineral_ab_data.index[-1])
    length=lastval - val #length of last time zone
    zone=mineral_ab_data[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z) #2D array of the top surface
    bot,btval =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)#bottom surface
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)#MaxY face
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)#MinY face
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)#MaxX face
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)#MinX face

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    mineral_ab_faces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
           'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
               'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            mineral_ab_faces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            mineral_ab_faces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return mineral_ab_faces

def mineral_si_import():
    """
    Imports the min_SI.tec file - mineral saturation index
    """
    mineral_si_data=pd.read_csv(cwd+'/mineral.tec',sep=r"\s*",skiprows=[0],engine='python')
    mineral_si_data_modified= mineral_si_data[mineral_si_data.columns[:-1]]
    mineral_si_data_modified.columns = mineral_si_data.columns[1:]

    mineral_si_data=mineral_si_data_modified.rename(index=str,columns=min_si_name)

    #Last time step - top, bottom, side walls
    val=int(mineral_si_data.loc[mineral_si_data["X"] == 'Zone'][-1:].index[0])#value of the last time zone
    lastval=int(mineral_si_data.index[-1])
    length=lastval - val #length of last time zone
    zone=mineral_si_data[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')

    top,tpval =zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z) #2D array of the top surface
    bot,btval =zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)#bottom surface
    MaxY,MxYval=zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)#MaxY face
    MinY,MnYval=zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)#MinY face
    MaxX,MxXval=zone.loc[zone["X"] == max(zone.X) ],max(zone.X)#MaxX face
    MinX,MnXval=zone.loc[zone["X"] == min(zone.X) ],min(zone.X)#MinX face

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    mineral_si_faces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,'Max-X':MaxX,'Min-X':MinX,
           'tpval' : tpval, 'btval' : btval, 'MxYval' : MxYval, 'MnYval' : MnYval,
               'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            mineral_si_faces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            mineral_si_faces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return mineral_si_faces

def stress_strain_import():
    """
    Imports the stress-strain file from current working directory. Column names are largely preserved. Takes in only the last time step values.
    Returns a dictionary 'stressfaces' that contains the stress_strain data for each of the default and user specificed faces.
    """

    column_names=["X","Y","Z","Sigma_xx","Sigma_yy","Sigma_zz","Sigma_yz","Sigma_xz","Sigma_xy",
                  "Strain_xx","Strain_yy","Strain_zz","Strain_yz", "Strain_xz", "Strain_xy","Vol_Strain",
                  "E_fail_xx", "E_fail_yy", "E_fail_zz","E_fail_yz2","E_fail_xz2","E_fail_xy2","E_fail_vol"]
    stress=pd.read_csv(cwd+'/stress_strain.tec',sep=r"\s+",skiprows=[1],names=column_names,engine='python')

    val=int(stress.loc[stress["X"] == 'Zone'][-1:].index[0])
    lastval=int(stress.index[-1])
    length=lastval - val
    zone=stress[val+1:lastval+1]

    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore',
                                                                          downcast='float')

    top,tpval  = zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z)
    bot,btval  = zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)
    MaxY,MxYval= zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)
    MinY,MnYval= zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)
    MaxX,MxXval= zone.loc[zone["X"] == max(zone.X) ],max(zone.X)
    MinX,MnXval= zone.loc[zone["X"] == min(zone.X) ],min(zone.X)

    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]


    stressfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,
                 'Max-X':MaxX,'Min-X':MinX,'tpval' : tpval, 'btval' : btval,
                 'MxYval' : MxYval, 'MnYval' : MnYval, 'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}

    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
            stressfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
            stressfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})

    return stressfaces


def corner_val_import():
    """
    By default in trexoptions.py op_corner=False the corner values from the displacement output are used.
    If you set op_corner =True and input into arrays you can override/if no displacement.tec has been output.
    The reason is that flowvector, data etc all output the value of the centre of the cell. Plotting
    functions require us to know the indices.

    These values arent used in the facechoose function (see plotting running order) unless its actually for
    displacement values (which are recorded as the corner indices).

    The function returns a shaped 3D mesh 'vals' with each value in the mesh the actual co-ordinate location.

    """

    if op_corner == False:
        column_names=["X","Y","Z"]
        displace=pd.read_csv(cwd+'/displacement.tec',sep=r"\s+",skiprows=[0,1],usecols=[0,1,2],
                             names=column_names,engine='python')

        val=int(displace.loc[displace["X"] == 'Zone'][-1:].index[0])
        lastval=int(displace.index[-1])
        length=lastval - val
        zone=displace[val+1:lastval+1]

        zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore', downcast='float')
        zone['xyz'] = list(zip(zone.X,zone.Y,zone.Z))
        vals=zone.xyz.values.reshape(len(zone.Z.unique()),len(zone.Y.unique()),len(zone.X.unique()))
    if op_corner == True:
        corner_x=op_corner_x
        corner_y=op_corner_y
        corner_z=op_corner_z
        a=[]
        for z in corner_z:
            for y in corner_y:
                for x in corner_x:
                    a.append(tuple([x,y,z]))
        df1 = pd.DataFrame(data=pd.Series(a))
        vals=df1.values.reshape(len(corner_z),len(corner_y),len(corner_x))

    return vals

def face_choose(axis1,axis2,param):
  """
  Returns a shapped array based on the input parameter (e.g. porosity) for the face (e.g. top face)
  """
  face_data=np.reshape(param.values,(len(axis1.unique()),len(axis2.unique())))
  return face_data

def plot_pcolormesh(axis1,axis2,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Plots parameter values for each cell using the pcolormesh function. Uses the corner point values output by corner_point_vals()
    """
    if info==True:
        print ('Making pcolormesh (colored_cells) of %(name)s surface (%(surlabel)s %(name2).1f) - %(data)s '
                        %{'name':name,'surlabel':surlabel,'name2':name2,'data':data })
    if rotate == True:
        axis2,axis1 = np.meshgrid(axis1,axis2)
    else:
        axis1,axis2 = np.meshgrid(axis1,axis2)
    fig,ax=plt.subplots(1,1,figsize=(10,10))
    ax.set_title(label=('%(name)s surface (%(surlabel)s %(name2).1f) - %(data)s - min/max/mean (%(min).4e /%(max).4e / %(mean).2e) '
                        %{'name':name,'surlabel':surlabel,'name2':name2,'data':data,'min':np.min(facedata),
                          'max':np.max(facedata),'mean':np.mean(facedata) }),pad=15)
    if colored_cells_log_plot ==True:
        if np.min(facedata) <= 0:
            print('np.min(facedata) <  0 - cant log a negative number or zero values - non-log plot is now displayed for %(name)s surface (%(surlabel)s %(name2).1f) - %(data)s - min/max/mean (%(min).4e /%(max).4e / %(mean).2e) '
                                %{'name':name,'surlabel':surlabel,'name2':name2,'data':data,'min':np.min(facedata),'max':np.max(facedata),'mean':np.mean(facedata) } )
            c=ax.pcolormesh(axis1,axis2,facedata,edgecolors='k',cmap='jet',vmin=np.min(facedata), vmax=np.max(facedata))
        else:
            c=ax.pcolormesh(axis1,axis2,facedata,edgecolors='k',cmap='jet',norm=colors.LogNorm(vmin=np.min(facedata), vmax=np.max(facedata)))
    if colored_cells_log_plot==False:
        c=ax.pcolormesh(axis1,axis2,facedata,edgecolors='k',cmap='jet',vmin=np.min(facedata), vmax=np.max(facedata))
    ax.set_xlabel('%(xlabel)s'%{'xlabel':xlabel})
    ax.set_ylabel('%(ylabel)s'%{'ylabel':ylabel})
    cbar=fig.colorbar(c, ax=ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('%(data)s'%{'data':data}, rotation=270)
    return fig,ax

def plot_contour(axis1,axis2,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Plots contours of the parameter values. Uses the centre of cell cordinates.
    Optionally, easily could overlay this output ontop of plot_colormesh
    """
    if info==True:
        print ('Making contour of %(name)s surface (%(surlabel)s %(name2).1f) - %(data)s '
                    %{'name':name,'surlabel':surlabel,'name2':name2,'data':data })

    if rotate == True:
        axis2,axis1 = np.meshgrid(axis1,axis2)

    else:
        axis1,axis2 = np.meshgrid(axis1,axis2)


    fig, ax = plt.subplots()
    cont = ax.contour(axis1, axis2, facedata, cmap='gist_earth', vmin=facedata.min(), vmax=facedata.max()) #see cont.levels for info on changing
    ax.set_title(label=('%(name)s surface (%(surlabel)s %(name2).1f) - %(data)s - min/max/mean (%(min).4e /%(max).4e / %(mean).2e) '
                        %{'name':name,'surlabel':surlabel,'name2':name2,'data':data,'min':np.min(facedata),
                          'max':np.max(facedata),'mean':np.mean(facedata) }),pad=15)
    ax.set_xlabel('%(xlabel)s'%{'xlabel':xlabel})
    ax.set_ylabel('%(ylabel)s'%{'ylabel':ylabel})
    ax.clabel(cont,fmt='%1.1e')
    return fig,ax

def plot_flowvectors_no_cont(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Following based on this: https://stackoverflow.com/questions/25342072/computing-and-drawing-vector-fields
    Uses both the centre (or corner for displacement) values (graident function) and the corner values (plotting) for constructing the quiver plot
    """
    if info==True:
        print ('Making flow vectors no-contour of %(name)s surface (%(surlabel)s %(name2).1f) - %(data)s '
                    %{'name':name,'surlabel':surlabel,'name2':name2,'data':data })

    if rotate == True:
        dy,dx=np.gradient(facedata, axis2, axis1)
        axis4,axis3 = np.meshgrid(axis3,axis4)

    else:
        dy,dx=np.gradient(facedata, axis2, axis1)
        axis3,axis4 = np.meshgrid(axis3,axis4)


    fig, ax = plt.subplots()
    quiv=ax.quiver(axis3, axis4, dx, dy,facedata)
    ax.set_title(label=('%(name)s surface (%(surlabel)s %(name2).1f) - %(data)s - min/max/mean (%(min).4e /%(max).4e / %(mean).2e) '
                        %{'name':name,'surlabel':surlabel,'name2':name2,'data':data,'min':np.min(facedata),
                          'max':np.max(facedata),'mean':np.mean(facedata) }),pad=15)
    ax.set_xlabel('%(xlabel)s'%{'xlabel':xlabel})
    ax.set_ylabel('%(ylabel)s'%{'ylabel':ylabel})
    cbar=fig.colorbar(quiv, ax=ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('%(data)s'%{'data':data}, rotation=270)
    return fig,ax

def plot_flowvectors_cont(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Following based on this: https://stackoverflow.com/questions/25342072/computing-and-drawing-vector-fields
    Uses both the centre (or corner for displacement) values (graident function) and the corner values (plotting) for constructing the quiver plot
    Overlay of contours of the parameter data. Not of the gradient.
    """

    if info==True:
        print ('Making flow vectors contour of %(name)s surface (%(surlabel)s %(name2).1f) - %(data)s '
                    %{'name':name,'surlabel':surlabel,'name2':name2,'data':data })

    if rotate == True:
        dy,dx=np.gradient(facedata, axis2, axis1)
        axis4,axis3 = np.meshgrid(axis3,axis4)
        axis2,axis1 = np.meshgrid(axis1,axis2)

    else:
        dy,dx=np.gradient(facedata, axis2, axis1)
        axis3,axis4 = np.meshgrid(axis3,axis4)
        axis1,axis2 = np.meshgrid(axis1,axis2)


    fig, ax = plt.subplots()
    quiv=ax.quiver(axis3, axis4, dx, dy,facedata)
    cont = ax.contour(axis1, axis2, facedata, cmap='gist_earth', vmin=facedata.min(), vmax=facedata.max()) #see cont.levels for info on changing
    ax.set_title(label=('%(name)s surface (%(surlabel)s %(name2).1f) - %(data)s - min/max/mean (%(min).4e /%(max).4e / %(mean).2e) '
                        %{'name':name,'surlabel':surlabel,'name2':name2,'data':data,'min':np.min(facedata),
                          'max':np.max(facedata),'mean':np.mean(facedata) }),pad=15)
    ax.set_xlabel('%(xlabel)s'%{'xlabel':xlabel})
    ax.set_ylabel('%(ylabel)s'%{'ylabel':ylabel})
    cbar=fig.colorbar(quiv, ax=ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('%(data)s'%{'data':data}, rotation=270)
    ax.clabel(cont,fmt='%1.1e')
    return fig,ax


flowdata_params=[]
flowvector_params=[]
displacement_params=[]
stress_strain_params=[]
gas_volfrac_params=[]
aqconc_params=[]
min_si_params=[]
min_ab_params=[]


if op_Porosity				== True:flowdata_params.append('Porosity')
if op_Perm_X				== True:flowdata_params.append('Perm_X(m2)')
if op_Perm_Y				== True:flowdata_params.append('Perm_Y(m2)')
if op_Perm_Z				== True:flowdata_params.append('Perm_Z(m2)')
if op_Pressure				== True:flowdata_params.append('Pressure(Pa)')
if op_Temperature			== True:flowdata_params.append('Temperature(C)')
if op_SatGas				== True:flowdata_params.append('SatGas')
if op_SatLiq				== True:flowdata_params.append('SatLiq')
if op_X1					== True:flowdata_params.append('X1')
if op_X2					== True:flowdata_params.append('X2')
if op_Pcap					== True:flowdata_params.append('Pcap')
if op_DGas					== True:flowdata_params.append('DGas_kg_m3')
if op_DLiq					== True:flowdata_params.append('DLiq_kg_m3')
if op_Krel_Gas				== True:flowdata_params.append('Krel_Gas')
if op_Krel_Liq				== True:flowdata_params.append('Krel_Liq')
if op_HGas					== True:flowdata_params.append('HGas(J_kg)')
if op_HLiq					== True:flowdata_params.append('HLiq(J_kg)')
if op_Cp					== True:flowdata_params.append('Cp(J_kg_C)')
if op_TC					== True:flowdata_params.append('TC(W_m_C)')
if op_DBlk					== True:flowdata_params.append('DBlk_kg_m3')
if op_Tdif					== True:flowdata_params.append('Tdif(m2_s)')

if op_FluxLiq				== True:flowvector_params.append('FluxLiq')
if op_FluxLiq_X			    == True:flowvector_params.append('FluxLiq_X')
if op_FluxLiq_Y			    == True:flowvector_params.append('FluxLiq_Y')
if op_FluxLiq_Z			    == True:flowvector_params.append('FluxLiq_Z')
if op_PorVelLiq			    == True:flowvector_params.append('PorVelLiq')
if op_PorVelLiqX			== True:flowvector_params.append('PorVelLiqX')
if op_PorVelLiqY			== True:flowvector_params.append('PorVelLiqY')
if op_PorVelLiqZ			== True:flowvector_params.append('PorVelLiqZ')
if op_FluxGas				== True:flowvector_params.append('FluxGas')
if op_FluxGas_X			    == True:flowvector_params.append('FluxGas_X')
if op_FluxGas_Y			    == True:flowvector_params.append('FluxGas_Y')
if op_FluxGas_Z			    == True:flowvector_params.append('FluxGas_Z')
if op_PorVelGas			    == True:flowvector_params.append('PorVelGas')
if op_PorVelGasX			== True:flowvector_params.append('PorVelGasX')
if op_PorVelGasY			== True:flowvector_params.append('PorVelGasY')
if op_PorVelGasZ			== True:flowvector_params.append('PorVelGasZ')
if op_HeatFlux				== True:flowvector_params.append('HeatFlux')
if op_HeatFlux_X			== True:flowvector_params.append('HeatFlux_X')
if op_HeatFlux_Y			== True:flowvector_params.append('HeatFlux_Y')
if op_HeatFlux_Z			== True:flowvector_params.append('HeatFlux_Z')

if op_Disp_x				== True:displacement_params.append('Disp_x')
if op_Disp_y				== True:displacement_params.append('Disp_y')
if op_Disp_z				== True:displacement_params.append('Disp_z')

if op_Sigma_xx				== True:stress_strain_params.append('Sigma_xx')
if op_Sigma_yy				== True:stress_strain_params.append('Sigma_yy')
if op_Sigma_zz				== True:stress_strain_params.append('Sigma_zz')
if op_Sigma_yz				== True:stress_strain_params.append('Sigma_yz')
if op_Sigma_xz				== True:stress_strain_params.append('Sigma_xz')
if op_Sigma_xy				== True:stress_strain_params.append('Sigma_xy')
if op_Strain_xx			    == True:stress_strain_params.append('Strain_xx')
if op_Strain_yy			    == True:stress_strain_params.append('Strain_yy')
if op_Strain_zz			    == True:stress_strain_params.append('Strain_zz')
if op_Strain_yz			    == True:stress_strain_params.append('Strain_yz')
if op_Strain_xz			    == True:stress_strain_params.append('Strain_xz')
if op_Strain_xy			    == True:stress_strain_params.append('Strain_xy')
if op_Vol_Strain			== True:stress_strain_params.append('Vol_Strain')
if op_E_fail_xx			    == True:stress_strain_params.append('E_fail_xx')
if op_E_fail_yy			    == True:stress_strain_params.append('E_fail_yy')
if op_E_fail_zz			    == True:stress_strain_params.append('E_fail_zz')
if op_E_fail_yz2			== True:stress_strain_params.append('E_fail_yz2')
if op_E_fail_xz2			== True:stress_strain_params.append('E_fail_xz2')
if op_E_fail_xy2			== True:stress_strain_params.append('E_fail_xy2')
if op_E_fail_vol			== True:stress_strain_params.append('E_fail_vol')

def aqconc_params_selector():
    for key,value in aqconc_variable.items():
        if value==True:
            aqconc_params.append(key)
    return aqconc_params

def gas_volfrac_params_selector():
    for key,value in gas_volfrac_variable.items():
        if value==True:
            gas_volfrac_params.append(key)
    return gas_volfrac_params

def mineral_ab_params_selector():
    for key,value in min_ab_variable.items():
        if value==True:
            min_ab_params.append(key)
    return min_ab_params

def mineral_si_params_selector():
    for key,value in min_si_variable.items():
        if value==True:
            min_si_params.append(key)
    return min_si_params


def corner_point_vals():
    """
    Collects the shaped 3D mesh 'vals' with each value in the mesh the actual co-ordinate location from the displacement file.
    corner_val_import returns mesh where cordinates are arranged in a shapped mesh of format [z,y,x]. Here we index

    e.g. Top_X - top surfaces (so z=0m and 1st value [0]). We also want to look at it along the 1st y-column
    [0]. i.e a[[0],[0],:]
    We flatten this and then return a list of the x values of the coordinates which are tuples in (x,y,z) format

    Returns a dictionary cpvs containing the corner point values for each face's X,Y or Z index


    Yeh this indexing is really horrible to think about or look at. I'm sure there are better not so custom ways to do this....

    """

    a=corner_val_import()
    cpvs={'Top_X':[x[0] for x in a[[0],[0],:].flatten()],
            'Top_Y':[x[1] for x in a[[0],:,[0]].flatten()],
            'Bot_X':[x[0] for x in a[[-1],[0],:].flatten()],
            'Bot_Y':[x[1] for x in a[[-1],:,[0]].flatten()],
            'Max-Y_Z':[x[2] for x in a[:,[-1],[0]].flatten()],
            'Max-Y_X':[x[0] for x in a[[0],[-1],:].flatten()],

            'Min-Y_Z':[x[2] for x in a[:,[0],[0]].flatten()],
            'Min-Y_X':[x[0] for x in a[[0],[0],:].flatten()],

            'Max-X_Z':[x[2] for x in a[:,[0],[-1]].flatten()],
            'Max-X_Y':[x[1] for x in a[[0],:,[-1]].flatten()],

            'Min-X_Z':[x[2] for x in a[:,[0],[0]].flatten()],
            'Min-X_Y':[x[1] for x in a[[0],:,[0]].flatten()],

            'xsec_y_half_Z':[x[2] for x in a[:,[0],[(a[[0],[0],:].size//2)]].flatten()],
            'xsec_y_half_Y':[x[1] for x in a[[0],:,[(a[[0],[0],:].size//2)]].flatten()],



            'xsec_x_half_Z':[x[2] for x in a[:,[(a[[0],:,[0]].size//2)],[0]].flatten()],
            'xsec_x_half_X':[x[0] for x in a[[0],[(a[[0],:,[0]].size//2)],:].flatten()]}

    if op_xsec_Y_user == True:
        for i in list(range(len(xsec_user_yvals))):
            cpvs.update({'xsec_y_user_'+str(xsec_user_yvals[i])+'_Z':[x[2] for x in a[:,[0],[xsec_user_yvals[i]]].flatten()],
                        'xsec_y_user_'+str(xsec_user_yvals[i])+'_Y':[x[1] for x in a[[0],:,[xsec_user_yvals[i]]].flatten()]})


    if op_xsec_X_user == True:
        for i in list(range(len(xsec_user_xvals))):
            cpvs.update({'xsec_x_user_'+str(xsec_user_xvals[i])+'_Z':[x[2] for x in a[:,[xsec_user_xvals[i]],[0]].flatten()],
                         'xsec_x_user_'+str(xsec_user_xvals[i])+'_X':[x[0] for x in a[[0],[xsec_user_xvals[i]],:].flatten()]})


    return cpvs

def centre_vals(axis):
    """Short function that simply returns the unique values of an axis - typically the centre cordinate values"""
    centre=axis.unique()
    return centre

def plotting(faces,name,name2,surlabel,dim1,dim2,xlabel,ylabel,data,rotate):
    """
    Master controlling plotting script, run the individual plotting functions e.g. flow_vectors_cont

    Returns a dictionary containing the relevant figure

    """
    a=face_choose(faces[name][dim1],faces[name][dim2],faces[name][data])
    c=corner_point_vals()[str(name+'_'+dim1)]#displacement values
    f=corner_point_vals()[str(name+'_'+dim2)]
    h=centre_vals(faces[name][dim1])#cell centres (flowdata,vector etc) or edges (displacement)
    j=centre_vals(faces[name][dim2])
    if colored_cells==True:
        fig_pcolor,axes_pcolor=plot_pcolormesh(f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    if contour_plot==True:
        fig_contour,axes_contour=plot_contour(j,h,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    if flow_vectors_no_cont==True:
        fig_vectors_no_cont,axes_vectors_no_cont=plot_flowvectors_no_cont(j,h,f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    if flow_vectors_cont==True:
        fig_vectors_cont,axes_vectors_cont=plot_flowvectors_cont(j,h,f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    figdict={'pcolor':[fig_pcolor,axes_pcolor],'contour':[fig_contour,axes_contour],
            'vectors_no_cont':[fig_vectors_no_cont,axes_vectors_no_cont],'vectors_cont':[fig_vectors_cont,axes_vectors_cont]}
    return figdict

def pdf_png_fig_plotting(faces,params,file_name):
    """
    Pdf plotting - opens a pdf file, loops through parameters for selected faces and calls plotting() function
    Writes the resulting figure to the pdf file.
    Png plotting - Save the figure output to a png file in a sub folder called 'trexplot_output_pngs' in the current working directory.
    Fig dict -  Return a dictionary containing figures from which they can be modified in other programs

    """
    pp=PdfPages(filename=file_name)
    fig_dictionary={}

    if op_Top == True:
        for i in list(params):
            for key,value in plotting(faces      ,'Top'  ,'tpval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'Top'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_Top'+str(i)+key:value})
                plt.close('all')
    if op_Bot == True:
        for i in list(params):
            for key,value in plotting(faces      ,'Bot'  ,'btval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'Bot'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_Bot'+str(i)+key:value})
                plt.close('all')
    if op_Max_Y== True:
        for i in list(params):
            for b in plotting(faces      ,'Max-Y','MxYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'Max-Y'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_Max-Y'+str(i)+key:value})
                plt.close('all')
    if op_Min_Y== True:
        for i in list(params):
            for key,value in plotting(faces      ,'Min-Y','MnYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'Min-Y'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_Min-Y'+str(i)+key:value})
                plt.close('all')
    if op_Max_X== True:
        for i in list(params):
            for key,value in plotting(faces      ,'Max-X','MxXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'Max-X'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_Max-X'+str(i)+key:value})
                plt.close('all')
    if op_Min_X== True:
        for i in list(params):
            for key,value in plotting(faces      ,'Min-X','MnXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'Min-X'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_Min-X'+str(i)+key:value})
                plt.close('all')
    if op_xsec_Y_half == True:
        for i in list(params):
            for key,value in plotting(faces      ,'xsec_y_half','xsec_y_val_half','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items() :
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'xsec_y_half'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_xsec_y_half'+str(i)+key:value})
                plt.close('all')
    if op_xsec_X_half == True:
        for i in list(params):
            for key,value in plotting(faces      ,'xsec_x_half','xsec_x_half_val','Y=','Z','X','X(m)','Z(m)',i,rotate=False ).items():
                if op_pdf==True:
                    pp.savefig(value[0])
                if op_png==True:
                    value[0].savefig(cwd+'/trexplot_output_pngs/'+'xsec_x_half'+str(i))
                if op_fig==True:
                    fig_dictionary.update({'fig_xsec_x_half'+str(i)+key:value})
                plt.close('all')
    if op_xsec_X_user  == True:
        for a in list(range(len(xsec_user_xvals))):
            for i in list(params):
                for key,value in plotting(faces,'xsec_x_user_'+str(xsec_user_xvals[a]),
                                'xsec_x_user_val'+str(xsec_user_xvals[a]),
                                'Y=','Z','X','X(m)','Z(m)',i,rotate=False ).items():
                                if op_pdf==True:
                                    pp.savefig(value[0])
                                if op_png==True:
                                    value[0].savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_x_user_val'+str(xsec_user_xvals[a])+str(i))
                                if op_fig==True:
                                    fig_dictionary.update({'xsec_x_user_val'+str(xsec_user_xvals[a])+str(i)+key:value})
                                plt.close('all')
    if op_xsec_Y_user  == True:
        for a in list(range(len(xsec_user_yvals))):
            for i in list(params):
                for key,value in plotting(faces,'xsec_y_user_'+str(xsec_user_yvals[a]),
                                    'xsec_y_user_val'+str(xsec_user_yvals[a]),
                                    'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
                                    if op_pdf==True:
                                        pp.savefig(value[0])
                                    if op_png==True:
                                        value[0].savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_y_user_val'+str(xsec_user_yvals[a])+str(i))
                                    if op_fig==True:
                                        fig_dictionary.update({'xsec_y_user_val'+str(xsec_user_yvals[a])+str(i)+key:value})
                                    plt.close('all')
    pp.close()
    return fig_dictionary

def main():
    """
    The main script which runs when you call trexplot.py from the commandline
    """
    flowfig=None
    flowvecfig=None
    dispfig=None
    stress_strain_fig=None
    aqconcfig=None
    gas_volfrac_fig=None
    min_si_fig=None
    min_ab_fig=None
    if op_Flowdata==True:
        if info==True:
            print('Running flowdata.tec')
        flowfaces=flowdata_import()
        pdf_png_fig_plotting(flowfaces,flowdata_params,cwd+"/flow_data.pdf")
    if op_Flowvector==True:
        if info==True:
            print('Running flowvector.tec')
        flowvecfaces=flowvector_import()
        pdf_png_fig_plotting(flowvecfaces,flowvector_params,cwd+"/flow_vector.pdf")
    if op_Displacement==True:
        if info==True:
            print('Running displacement.tec')
        dispfaces=displace_import()
        pdf_png_fig_plotting(dispfaces,displacement_params,cwd+"/displacement.pdf")
    if op_Stress_Strain==True:
        if info==True:
            print('Running stress_strain.tec')
        stressfaces=stress_strain_import()
        pdf_png_fig_plotting(stressfaces,stress_strain_params,cwd+"/stress_strain.pdf")
    if op_aqconc==True:
        if info==True:
            print('Running aqconc.tec')
        aqconcfaces=aq_conc_import()
        aqconc_params=aqconc_params_selector()
        pdf_png_fig_plotting(aqconcfaces,aqconc_params,cwd+"/aq_conc.pdf")
    if op_gas_volfrac==True:
        if info==True:
            print('Running gas_volfrac.tec')
        gas_volfrac_faces=gas_volfrac_import()
        gas_volfrac_params=gas_volfrac_params_selector()
        pdf_png_fig_plotting(gas_volfrac_faces,gas_volfrac_params,cwd+"/gas_volfrac.pdf")
    if op_min_ab==True:
        if info==True:
            print('Running min_ab.tec')
        min_ab_faces=mineral_ab_import()
        min_ab_params=mineral_ab_params_selector()
        pdf_png_fig_plotting(min_ab_faces,min_ab_params,cwd+"/min_ab.pdf")
    if op_min_si==True:
        if info==True:
            print('Running min_si.tec')
        min_si_faces=mineral_si_import()
        min_si_params=mineral_si_params_selector()
        pdf_png_fig_plotting(min_si_faces,min_si_params,cwd+"/min_si.pdf")

    return flowfig, flowvecfig, dispfig, stress_strain_fig, aqconcfig, gas_volfrac_fig, min_si_fig, min_ab_fig


if __name__ == "__main__":
    main()








#Possible future code if plasticity has anything in

#def plasticity_params_selector():
    #Started this - probably defunct
#    for key,value in min_si_variable.items():
#        if value==True:
#            min_si_params.append(key)
#    return min_si_params

#def plasticity_import():
    """
    Imports the plasticity file from current working directory. Column names are largely preserved. Takes in only the last time step values.
    Returns a dictionary 'plasticity faces' that contains the stress_strain data for each of the default and user specificed faces.
    DEFUNCT ATM
    """

#
#    column_names=["X(m)", "Y(m)", "Z(m)", "ielem", "N_shear", "N_tensl",     "N_Surf",   "E_fail_xx",   "E_fail_yy" , "E_fail_zz*2 " , "E_fail_yz*2", "E_fail_xz*2" , "E_fail_xy*2", "E_fail_vol"]
#    plasticity=pd.read_csv(cwd+'/Plasticity.tec',sep=r"\s+",skiprows=[1],names=column_names,engine='python')
#
#    val=int(plasticity.loc[plasticity["X"] == 'Zone'][-1:].index[0])
#    lastval=int(plasticity.index[-1])
#    length=lastval - val
#    zone=plasticity[val+1:lastval+1]
#
#    zone[zone.columns] = zone[zone.columns].apply(pd.to_numeric, errors='ignore',
#                                                                          downcast='float')
#
#    top,tpval  = zone.loc[zone["Z"] == max(zone.Z) ],max(zone.Z)
#    bot,btval  = zone.loc[zone["Z"] == min(zone.Z) ],min(zone.Z)
#    MaxY,MxYval= zone.loc[zone["Y"] == max(zone.Y) ],max(zone.Y)
#    MinY,MnYval= zone.loc[zone["Y"] == min(zone.Y) ],min(zone.Y)
#    MaxX,MxXval= zone.loc[zone["X"] == max(zone.X) ],max(zone.X)
#    MinX,MnXval= zone.loc[zone["X"] == min(zone.X) ],min(zone.X)
#
#    xsec_x,xsec_x_val=zone.loc[zone["Y"] == zone.Y.unique()[int(len(zone.Y.unique())/2)]],zone.Y.unique()[int(len(zone.Y.unique())/2)]
#    xsec_y,xsec_y_val=zone.loc[zone["X"] == zone.X.unique()[int(len(zone.X.unique())/2)]],zone.X.unique()[int(len(zone.X.unique())/2)]
#
#
#    plasticityfaces={'Top':top,'Bot':bot,'Max-Y':MaxY,'Min-Y':MinY,
#                 'Max-X':MaxX,'Min-X':MinX,'tpval' : tpval, 'btval' : btval,
#                 'MxYval' : MxYval, 'MnYval' : MnYval, 'MxXval' : MxXval, 'MnXval' : MnXval,'xsec_x_half':xsec_x,'xsec_x_half_val':xsec_x_val,
#              'xsec_y_half':xsec_y,'xsec_y_val_half':xsec_y_val}
#
#    if op_xsec_X_user == True:
#        for i in list(range(len(xsec_user_xvals))):
#            xsec_x_user,xsec_x_user_val=zone.loc[zone["Y"] == zone.Y.unique()[xsec_user_xvals[i]]],zone.Y.unique()[xsec_user_xvals[i]]
#            plasticityfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,'xsec_x_user_val'+str(xsec_user_xvals[i]):xsec_x_user_val})
#
#    if op_xsec_Y_user == True:
#        for i in list(range(len(xsec_user_yvals))):
#            xsec_y_user,xsec_y_user_val=zone.loc[zone["X"] == zone.X.unique()[xsec_user_yvals[i]]],zone.X.unique()[xsec_user_yvals[i]]
#            plasticityfaces.update({'xsec_y_user_'+str(xsec_user_yvals[i]):xsec_y_user,'xsec_y_user_val'+str(xsec_user_yvals[i]):xsec_y_user_val})
#
#    return plasticityfaces


## Old code

#def pngplotting(faces,params):
#    """
#    Save the figure output to a png file in a sub folder called 'trexplot_output_pngs' in the current working directory.
#    """
#    if op_Top == True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Top'  ,'tpval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'Top'+str(i))
#                plt.close('all')
#    if op_Bot == True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Bot'  ,'btval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'Bot'+str(i))
#                plt.close('all')
#    if op_Max_Y== True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Max-Y','MxYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'Max-Y'+str(i))
#                plt.close('all')
#    if op_Min_Y== True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Min-Y','MnYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'Min-Y'+str(i))
#                plt.close('all')
#    if op_Max_X== True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Max-X','MxXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'Max-X'+str(i))
#                plt.close('all')
#    if op_Min_X== True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Min-X','MnXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'Min-X'+str(i))
#                plt.close('all')
#    if op_xsec_Y_half == True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'xsec_y_half','xsec_y_val_half','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'xsec_y_half'+str(i))
#                plt.close('all')
#    if op_xsec_X_half == True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'xsec_x_half','xsec_x_half_val','Y=','Z','X','X(m)','Z(m)',i,rotate=False ).items():
#                value[0].savefig(cwd+'/trexplot_output_pngs/'+'xsec_x_half'+str(i))
#                plt.close('all')
#    if op_xsec_X_user  == True:
#        for a in list(range(len(xsec_user_xvals))):
#            for i in list(params):
#                for key,value in plotting(faces,'xsec_x_user_'+str(xsec_user_xvals[a]),
#                                    'xsec_x_user_val'+str(xsec_user_xvals[a]),
#                                   'Y=','Z','X','X(m)','Z(m)',i,rotate=False ).items():
#                    value[0].savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_x_user_val'+str(xsec_user_xvals[a])+str(i))
#                plt.close('all')
#    if op_xsec_Y_user  == True:
#        for a in list(range(len(xsec_user_yvals))):
#            for i in list(params):
#                for key,value in plotting(faces,'xsec_y_user_'+str(xsec_user_yvals[a]),
#                                    'xsec_y_user_val'+str(xsec_user_yvals[a]),
#                                    'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                    value[0].savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_y_user_val'+str(xsec_user_yvals[a])+str(i))
#                plt.close('all')

#def fig_return(faces,params):
#    """
#    Return a dictionary containing figures from which they can be modified in other programs
#    """
#    if op_Top == True:
#        for i in list(params):
#            for key,value in plotting(faces      ,'Top'        ,'tpval'          ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).items():
#                fig_dictionary.update({'fig_Top'+str(i)+key:value})
#    if op_Bot == True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'Bot'        ,'btval'          ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).items():
#                fig_dictionary.update({'fig_Bot'+str(i)+key:value})
#    if op_Max_Y== True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'Max-Y'      ,'MxYval'         ,'Y=','Z','X','X(m)','Z(m)',i,rotate=False).items():
#                fig_dictionary.update({'fig_Max-Y'+str(i)+key:value})
#    if op_Min_Y== True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'Min-Y'      ,'MnYval'         ,'Y=','Z','X','X(m)','Z(m)',i,rotate=False).items():
#                fig_dictionary.update({'fig_Min-Y'+str(i)+key:value})
#    if op_Max_X== True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'Max-X'      ,'MxXval'         ,'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                fig_dictionary.update({'fig_Max-X'+str(i)+key:value})
#    if op_Min_X== True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'Min-X'      ,'MnXval'         ,'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                fig_dictionary.update({'fig_Min-X'+str(i)+key:value})
#    if op_xsec_Y_half == True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'xsec_y_half','xsec_y_val_half','X=','Y','Z','Y(m)','Z(m)',i,rotate=True).items():
#                fig_dictionary.update({'fig_xsec_y_half'+str(i)+key:value})
#    if op_xsec_X_half == True:
#        for i in list(params):
#             for key,value in plotting(faces      ,'xsec_x_half','xsec_x_half_val','Y=','Z','X','X(m)','Z(m)',i,rotate=False ).items():
#                fig_dictionary.update({'fig_xsec_x_half'+str(i)+key:value})
#    if op_xsec_X_user  == True:
#        for a in list(range(len(xsec_user_xvals))):
#            for i in list(params):
##                 for key,value in plotting(faces,'xsec_x_user_'+str(xsec_user_xvals[a]),
##                                        'xsec_x_user_val'+str(xsec_user_xvals[a]),
##                                   'Y=','Z','X','X(m)','Z(m)',i,rotate=False ).items():
##                    fig_dictionary.update({'xsec_x_user_val'+str(xsec_user_xvals[a])+str(i)+key:value})
##    if op_xsec_Y_user  == True:
##        for a in list(range(len(xsec_user_yvals))):
##            for i in list(params):
##                for key,value in plotting(faces,'xsec_y_user_'+str(xsec_user_yvals[a]),
##                                    'xsec_y_user_val'+str(xsec_user_yvals[a]),
##                                    'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).items():
#                    fig_dictionary.update({'xsec_y_user_val'+str(xsec_user_yvals[a])+str(i)+key:value})
#    return fig_dictionary
