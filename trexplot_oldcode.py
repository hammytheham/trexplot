
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
from matplotlib.backends.backend_pdf import PdfPages
import sys
from trexoptions import *     #import the option file

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
    '"SatGas"':"SatGas",'"SatLiq"':"SatLiq",'"X1"':"X1", '"X2"':"X2", '"Pcap(Pa)"':"Pcap", '"DGas_kg/m3"':"DGas_kg/m3",
    '"DLiq_kg/m3"':"DLiq_kg/m3", '"Porosity"':"Porosity", '"Perm_X(m2)"':"Perm_X(m2)", '"Perm_Y(m2)"':"Perm_Y(m2)",
    '"Perm_Z(m2)"':"Perm_Z(m2)", '"Krel_Gas"':"Krel_Gas", '"Krel_Liq"':"Krel_Liq", '"HGas(J/kg)"':"HGas(J/kg)",
    '"HLiq(J/kg)"':"HLiq(J/kg)", '"Cp(J/kg/C)"':"Cp(J/kg/C)", '"TC(W/m/C)"':"TC(W/m/C)", '"DBlk_kg/m3"':"DBlk_kg/m3",
    '"Tdif(m2/s)"':"Tdif(m2/s)"})


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
        vals=zone.xyz.values.reshape(len(zone.X.unique()),len(zone.Y.unique()),len(zone.Z.unique()))

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
    if rotate == True:
        axis2,axis1 = np.meshgrid(axis1,axis2)
    else:
        axis1,axis2 = np.meshgrid(axis1,axis2)
    fig,ax=plt.subplots(1,1,figsize=(10,10))
    ax.set_title(label=('%(name)s surface (%(surlabel)s %(name2).1f) - %(data)s - min/max/mean (%(min).4e /%(max).4e / %(mean).2e) '
                        %{'name':name,'surlabel':surlabel,'name2':name2,'data':data,'min':np.min(facedata),
                          'max':np.max(facedata),'mean':np.mean(facedata) }),pad=15)
    print ("axis1",axis1.size,"axis2",axis2.size,"facedata",facedata.size)
    c=ax.pcolormesh(axis1,axis2,facedata,edgecolors='k',cmap='jet', vmin=np.min(facedata), vmax=np.max(facedata))
    ax.set_xlabel('%(xlabel)s'%{'xlabel':xlabel})
    ax.set_ylabel('%(ylabel)s'%{'ylabel':ylabel})
    cbar=fig.colorbar(c, ax=ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('%(data)s'%{'data':data}, rotation=270)
    return fig

def plot_contour(axis1,axis2,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Plots contours of the parameter values. Uses the centre of cell cordinates.
    Optionally, easily could overlay this output ontop of plot_colormesh
    """

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
    return fig


def plot_flowvectors_no_cont(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Following based on this: https://stackoverflow.com/questions/25342072/computing-and-drawing-vector-fields
    Uses both the centre (or corner for displacement) values (graident function) and the corner values (plotting) for constructing the quiver plot
    """
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
    return fig

def plot_flowvectors_cont(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
    """
    Following based on this: https://stackoverflow.com/questions/25342072/computing-and-drawing-vector-fields
    Uses both the centre (or corner for displacement) values (graident function) and the corner values (plotting) for constructing the quiver plot
    Overlay of contours of the parameter data. Not of the gradient.
    """

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
    return fig



flowdata_params=[]
flowvector_params=[]
displacement_params=[]
stress_strain_params=[]

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
if op_DGas					== True:flowdata_params.append('DGas_kg/m3')
if op_DLiq					== True:flowdata_params.append('DLiq_kg/m3')
if op_Krel_Gas				== True:flowdata_params.append('Krel_Gas')
if op_Krel_Liq				== True:flowdata_params.append('Krel_Liq')
if op_HGas					== True:flowdata_params.append('HGas(J/kg)')
if op_HLiq					== True:flowdata_params.append('HLiq(J/kg)')
if op_Cp					== True:flowdata_params.append('Cp(J/kg/C)')
if op_TC					== True:flowdata_params.append('TC(W/m/C)')
if op_DBlk					== True:flowdata_params.append('DBlk_kg/m3')
if op_Tdif					== True:flowdata_params.append('Tdif(m2/s)')

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
        pcolor=plot_pcolormesh(f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    if contour_plot==True:
        contour=plot_contour(j,h,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    if flow_vectors_no_cont==True:
        vectors_no_cont=plot_flowvectors_no_cont(j,h,f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    if flow_vectors_cont==True:
        vectors_cont=plot_flowvectors_cont(j,h,f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
    figdict={pcolor:'pcolor',contour:'contour',vectors_no_cont:'vectors_no_cont',vectors_cont:'vectors_cont'}
    return figdict

def pdfplotting(faces,params,file_name):
    """
    Pdf plotting - opens a pdf file, loops through parameters for selected faces and calls plotting() function
    Writes the resulting figure to the pdf file.
    """
    pp=PdfPages(filename=file_name)
    if op_Top == True:
        for i in list(params):
            for b in plotting(faces      ,'Top'  ,'tpval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False):
                pp.savefig(b)
                plt.close('all')
    if op_Bot == True:
        for i in list(params):
            for b in plotting(faces      ,'Bot'  ,'btval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False):
                pp.savefig(b)
                plt.close('all')
    if op_Max_Y== True:
        for i in list(params):
            for b in plotting(faces      ,'Max-Y','MxYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False):
                pp.savefig(b)
                plt.close('all')
    if op_Min_Y== True:
        for i in list(params):
            for b in plotting(faces      ,'Min-Y','MnYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False):
                pp.savefig(b)
                plt.close('all')
    if op_Max_X== True:
        for i in list(params):
            for b in plotting(faces      ,'Max-X','MxXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                pp.savefig(b)
                plt.close('all')
    if op_Min_X== True:
        for i in list(params):
            for b in plotting(faces      ,'Min-X','MnXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                pp.savefig(b)
                plt.close('all')
    if op_xsec_Y_half == True:
        for i in list(params):
            for a in plotting(faces      ,'xsec_y_half','xsec_y_val_half','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ) :
                pp.savefig(a)
                plt.close('all')
    if op_xsec_X_half == True:
        for i in list(params):
            for a in plotting(faces      ,'xsec_x_half','xsec_x_half_val','Y=','Z','X','X(m)','Z(m)',i,rotate=False ):
                pp.savefig(a)
                plt.close('all')
    if op_xsec_X_user  == True:
        for a in list(range(len(xsec_user_xvals))):
            for i in list(params):
                for b in plotting(faces,'xsec_x_user_'+str(xsec_user_xvals[a]),
                                'xsec_x_user_val'+str(xsec_user_xvals[a]),
                                'Y=','Z','X','X(m)','Z(m)',i,rotate=False ):
                    pp.savefig(b)
                    plt.close('all')
    if op_xsec_Y_user  == True:
        for a in list(range(len(xsec_user_yvals))):
            for i in list(params):
                for b in plotting(faces,'xsec_y_user_'+str(xsec_user_yvals[a]),
                                    'xsec_y_user_val'+str(xsec_user_yvals[a]),
                                    'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                    pp.savefig(b)
                    plt.close('all')
    pp.close()


def pngplotting(faces,params):
    """
    Save the figure output to a png file in a sub folder called 'trexplot_output_pngs' in the current working directory.
    """
    if op_Top == True:
        for i in list(params):
            for b in plotting(faces      ,'Top'  ,'tpval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False):
                b.savefig(cwd+'/trexplot_output_pngs/'+'Top'+str(i))
                plt.close('all')
    if op_Bot == True:
        for i in list(params):
            for b in plotting(faces      ,'Bot'  ,'btval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False):
                b.savefig(cwd+'/trexplot_output_pngs/'+'Bot'+str(i))
                plt.close('all')
    if op_Max_Y== True:
        for i in list(params):
            for b in plotting(faces      ,'Max-Y','MxYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False):
                b.savefig(cwd+'/trexplot_output_pngs/'+'Max-Y'+str(i))
                plt.close('all')
    if op_Min_Y== True:
        for i in list(params):
            for b in plotting(faces      ,'Min-Y','MnYval','Y=','Z','X','X(m)','Z(m)',i,rotate=False):
                b.savefig(cwd+'/trexplot_output_pngs/'+'Min-Y'+str(i))
                plt.close('all')
    if op_Max_X== True:
        for i in list(params):
            for b in plotting(faces      ,'Max-X','MxXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                b.savefig(cwd+'/trexplot_output_pngs/'+'Max-X'+str(i))
                plt.close('all')
    if op_Min_X== True:
        for i in list(params):
            for b in plotting(faces      ,'Min-X','MnXval','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                b.savefig(cwd+'/trexplot_output_pngs/'+'Min-X'+str(i))
                plt.close('all')
    if op_xsec_Y_half == True:
        for i in list(params):
            for b in plotting(faces      ,'xsec_y_half','xsec_y_val_half','X=','Y','Z','Y(m)','Z(m)',i,rotate=True ).savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_y_half'+str(i)):
                b.savefig(cwd+'/trexplot_output_pngs/'+'xsec_y_half'+str(i))
                plt.close('all')
    if op_xsec_X_half == True:
        for i in list(params):
            for b in plotting(faces      ,'xsec_x_half','xsec_x_half_val','Y=','Z','X','X(m)','Z(m)',i,rotate=False ).savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_x_half'+str(i)):
                b.savefig(cwd+'/trexplot_output_pngs/'+'xsec_x_half'+str(i))
                plt.close('all')
    if op_xsec_X_user  == True:
        for a in list(range(len(xsec_user_xvals))):
            for i in list(params):
                for b in plotting(faces,'xsec_x_user_'+str(xsec_user_xvals[a]),
                                    'xsec_x_user_val'+str(xsec_user_xvals[a]),
                                   'Y=','Z','X','X(m)','Z(m)',i,rotate=False ):
                    b.savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_x_user_val'+str(xsec_user_xvals[a])+str(i))
                plt.close('all')
    if op_xsec_Y_user  == True:
        for a in list(range(len(xsec_user_yvals))):
            for i in list(params):
                for b in plotting(faces,'xsec_y_user_'+str(xsec_user_yvals[a]),
                                    'xsec_y_user_val'+str(xsec_user_yvals[a]),
                                    'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                    b.savefig(cwd+'/trexplot_output_pngs/'+ 'xsec_y_user_val'+str(xsec_user_yvals[a])+str(i))
                plt.close('all')

def fig_return():
    """
    Return a dictionary containing figures from which they can be modified in other programs
    """
    fig_dictionary={}
    if op_Top == True:
        for i in list(params):
            for b in plotting(faces      ,'Top'        ,'tpval'          ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False):
                fig_dictionary.update({'fig_Top'+str(i)+b.key():b})
    if op_Bot == True:
        for i in list(params):
             for b in plotting(faces      ,'Bot'        ,'btval'          ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False):
                fig_dictionary.update({'fig_Bot'+str(i)+b.key():b})
    if op_Max_Y== True:
        for i in list(params):
             for b in plotting(faces      ,'Max-Y'      ,'MxYval'         ,'Y=','Z','X','X(m)','Z(m)',i,rotate=False):
                fig_dictionary.update({'fig_Max-Y'+str(i)})
    if op_Min_Y== True:
        for i in list(params):
             for b in plotting(faces      ,'Min-Y'      ,'MnYval'         ,'Y=','Z','X','X(m)','Z(m)',i,rotate=False):
                fig_dictionary.update({'fig_Min-Y'+str(i)})
    if op_Max_X== True:
        for i in list(params):
             for b in plotting(faces      ,'Max-X'      ,'MxXval'         ,'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                fig_dictionary.update({'fig_Max-X'+str(i)})
    if op_Min_X== True:
        for i in list(params):
             for b in plotting(faces      ,'Min-X'      ,'MnXval'         ,'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                fig_dictionary.update({'fig_Min-X'+str(i)})
    if op_xsec_Y_half == True:
        for i in list(params):
             for b in plotting(faces      ,'xsec_y_half','xsec_y_val_half','X=','Y','Z','Y(m)','Z(m)',i,rotate=True):
                fig_dictionary.update({'fig_xsec_y_half'+str(i)})
    if op_xsec_X_half == True:
        for i in list(params):
             for b in plotting(faces      ,'xsec_x_half','xsec_x_half_val','Y=','Z','X','X(m)','Z(m)',i,rotate=False ):
                fig_dictionary.update({'fig_xsec_x_half'+str(i)})
    if op_xsec_X_user  == True:
        for a in list(range(len(xsec_user_xvals))):
            for i in list(params):
                 for b in plotting(faces,'xsec_x_user_'+str(xsec_user_xvals[a]),
                                        'xsec_x_user_val'+str(xsec_user_xvals[a]),
                                   'Y=','Z','X','X(m)','Z(m)',i,rotate=False ):
                    fig_dictionary.update({'xsec_x_user_val'+str(xsec_user_xvals[a])+str(i)})
    if op_xsec_Y_user  == True:
        for a in list(range(len(xsec_user_yvals))):
            for i in list(params):
                for b in plotting(faces,'xsec_y_user_'+str(xsec_user_yvals[a]),
                                    'xsec_y_user_val'+str(xsec_user_yvals[a]),
                                    'X=','Y','Z','Y(m)','Z(m)',i,rotate=True ):
                    fig_dictionary.update({'xsec_y_user_val'+str(xsec_user_yvals[a])+str(i)})
    return fig_dictionary

def main():
    if op_Flowdata==True:
        flowfaces=flowdata_import()
        if op_png==True:
            pngplotting(flowfaces,flowdata_params)
        if op_pdf==True:
            pdfplotting(flowfaces,flowdata_params,cwd+"/flow_data.pdf")
        if op_fig==True:
            fig_return(flowfaces,flowdata_params)
    if op_Flowvector==True:
        flowvecfaces=flowvector_import()
        if op_png==True:
            pngplotting(flowvecfaces,flowvector_params)
        if op_pdf==True:
            pdfplotting(flowvecfaces,flowvector_params,cwd+"/flow_vector.pdf")
#        if op_fig==True:
#            fig_return(flowvecfaces,flowvector_params)
    if op_Displacement==True:
        dispfaces=displace_import()
        if op_png==True:
            pngplotting(dispfaces,displacement_params)
        if op_pdf==True:
            pdfplotting(dispfaces,displacement_params,cwd+"/displacement.pdf")
#        if op_fig==True:
#            fig_return(dispfaces,displacement_params)
    if op_Stress_Strain==True:
        stressfaces=stress_strain_import()
        if op_png==True:
            pngplotting(stressfaces,stress_strain_params)
        if op_pdf==True:
            pdfplotting(stressfaces,stress_strain_params,cwd+"/stress_strain.pdf")
#        if op_fig==True:
#            fig_return(stressfaces,stress_strain_params)
#    if op_fig==True:
#        return fig_dictionary



if __name__ == "__main__":
    main()


# In[ ]:


#Old code


#corner_val_import()[3] #returns all the x and z values for the 3rd value of op_corner_z i.e. 6 or -900 - the reshape order above i dont get but works
#corner_val_import()[:,:,[1]].flatten() #how to select[z,y,x] and then flatten


##face and data choosing


#def corner_points(cpvs,emptylist):
#    #function makes a crude iumperfect mesh
#    B=cpvs
#    A=emptylist
#    for i in range(len(B)):
#        if i == 0:
#            A[0]=B[i]-((B[i+1]-B[i])/2)
#            A[i+1]=B[i+1]-((B[i+1]-B[i])/2)
#        if (i+1)==len(B):
#            break
#        else:
#            A[i+1]=B[i+1]-((B[i+1]-B[i])/2)
#    print("cp script",A)
#    return A
#
#
#
#def corner_point_vals(axis):
#    last=np.array(float(axis.unique()[-1])+(float(axis.unique()[-1])-float(axis.unique()[-2])))
#    cpvs=np.append(axis.unique(),last)
#    print(cpvs)
#    emptylist=np.zeros(len(cpvs))
#    return cpvs,emptylist



#corner_val_import()[:,:,[1]].flatten()  #how to select[z,y,x]
#stressfaces.update({'xsec_x_user_'+str(xsec_user_xvals[i]):xsec_x_user,


#def plotting(faces,name,name2,surlabel,dim1,dim2,xlabel,ylabel,data,rotate):
#    a=face_choose(faces[name][dim1],faces[name][dim2],faces[name][data])
#    b=corner_point_vals(faces[name][dim1])
#    print("B",b[0],"B1",b[1]) #return the corner points and empty list same size
#    c=corner_points(b[0],b[1]) # returns an array of the correct size filled with correct corners
#    print("C",c)
#    e=corner_point_vals(faces[name][dim2])
#    f=corner_points(e[0],e[1])
#    fig=plot_pcolormesh(f,c,a,data,name,faces[name2],surlabel,xlabel,ylabel,rotate)
#    return fig

#def axes_values():
#   #By default the corner values from the displacement output are used.
#   #google read in xyz coordinate file and make a resulting 3D mesh out of it.
#   #might aswell do it properly!! Future proof plus eric has more complex meshes.
#
#    if op_corner == True:
#        xvals=op_corner_x
#        yvals=op_corner_y
#        zvals=op_corner_z
#    else:
#        xvals=displace_import()['Top']['X'].unique()
#        yvals=displace_import()['Top']['X'].unique()
#        zvals=displace_import()['Top']['X'].unique()

#
#        #difa=np.diff(axis1[:])
#        #print('difa=',difa)
#        #difb=np.diff(axis2[:])
#        #print('difb=',difb)
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis2,axis1 = np.meshgrid(axis1,axis2)
#
#        #dy[np.isinf(dy)]=np.nan
#        #dx[np.isinf(dx)]=np.nan
#        print(dy,dx)


# In[ ]:


array=[[5.327318e-08, 5.302213e-08, 5.264198e-08, 5.232477e-08, 5.226435e-08
  ,5.258210e-08, 5.325536e-08, 5.410714e-08, 5.487324e-08, 5.532210e-08],
 [4.953998e-08, 4.913573e-08, 4.851350e-08, 4.795346e-08, 4.774013e-08,
  4.807313e-08, 4.894058e-08, 5.009330e-08, 5.113477e-08, 5.174467e-08],
 [4.280405e-08, 4.201194e-08, 4.078997e-08, 3.962570e-08, 3.900056e-08,
  3.931232e-08, 4.059173e-08, 4.244279e-08, 4.411359e-08, 4.509325e-08],
 [3.548336e-08, 3.381851e-08, 3.131880e-08, 2.888704e-08, 2.730930e-08,
  2.739829e-08, 2.930735e-08, 3.251616e-08, 3.536279e-08, 3.705464e-08],
 [3.500417e-08, 3.167505e-08, 2.698106e-08, 2.250465e-08, 1.925050e-08,
  1.868078e-08, 2.108715e-08, 2.641765e-08, 3.093883e-08, 3.376233e-08],
 [3.829746e-08, 3.372373e-08, 2.752396e-08, 2.174541e-08, 1.738411e-08,
  1.632301e-08, 1.880493e-08, 2.553067e-08, 3.106102e-08, 3.467288e-08],
 [3.978388e-08, 3.471880e-08, 2.794453e-08, 2.168303e-08, 1.691082e-08,
  1.566582e-08, 1.815470e-08, 2.540173e-08, 3.130537e-08, 3.522191e-08],
 [4.169603e-08, 3.606093e-08, 2.863494e-08, 2.183823e-08, 1.660694e-08,
  1.515640e-08, 1.763109e-08, 2.546118e-08, 3.177640e-08, 3.604230e-08],
 [4.410161e-08, 3.780208e-08, 2.963374e-08, 2.224080e-08, 1.649566e-08,
  1.481601e-08, 1.725275e-08, 2.573638e-08, 3.250728e-08, 3.717480e-08],
 [6.536926e-07, 5.937457e-07, 5.085931e-07, 4.250558e-07, 3.587753e-07,
  3.242687e-07, 3.190302e-07, 2.625842e-08, 3.353554e-08, 3.866824e-08],
 [9.520179e-05, 1.094854e-04, 1.194284e-04, 1.099747e-04, 8.360293e-05,
  4.614698e-05, 5.924715e-06, 4.173997e-08, 3.490613e-08, 4.058102e-08],
 [3.640606e-05, 9.214843e-05, 1.146954e-04, 1.063602e-04, 7.358278e-05,
  3.175129e-05, 5.873365e-06, 4.257781e-08, 3.667121e-08, 4.298280e-08],
 [6.332070e-07, 5.813288e-07, 5.036060e-07, 4.240752e-07, 3.599401e-07,
  3.255439e-07, 3.182350e-07, 2.993201e-08, 3.889183e-08, 4.595719e-08],
 [3.944654e-08, 3.513427e-08, 2.901323e-08, 2.219682e-08, 3.109058e-07,
  3.500287e-07, 4.238882e-07, 5.178232e-07, 6.159438e-07, 6.885575e-07],
 [3.861711e-08, 3.470954e-08, 2.903090e-08, 3.828296e-08, 8.048252e-05,
  1.259718e-04, 1.641670e-04, 1.778327e-04, 1.617571e-04, 1.398119e-04],
 [3.809521e-08, 3.453472e-08, 2.924624e-08, 3.887079e-08, 3.825505e-05,
  1.088375e-04, 1.580838e-04, 1.710754e-04, 1.385573e-04, 5.521310e-05],
 [3.783447e-08, 3.457314e-08, 2.963125e-08, 2.365725e-08, 3.137766e-07,
  3.520025e-07, 4.232712e-07, 5.124309e-07, 6.007149e-07, 6.616466e-07],
 [3.779601e-08, 3.479368e-08, 3.016164e-08, 2.447899e-08, 1.688958e-08,
  1.840337e-08, 2.337519e-08, 2.980264e-08, 3.612878e-08, 4.082953e-08],
 [3.794715e-08, 3.516983e-08, 3.081637e-08, 2.541763e-08, 1.846540e-08,
  1.961266e-08, 2.407896e-08, 2.992447e-08, 3.567364e-08, 3.988821e-08],
 [3.826045e-08, 3.567910e-08, 3.157718e-08, 2.645390e-08, 2.005500e-08,
  2.090930e-08, 2.492847e-08, 3.026053e-08, 3.550527e-08, 3.930720e-08],
 [4.079975e-08, 3.913685e-08, 3.626867e-08, 3.260099e-08, 2.884180e-08,
  2.843189e-08, 3.028694e-08, 3.316273e-08, 3.604072e-08, 3.798938e-08],
 [4.907877e-08, 4.811656e-08, 4.639948e-08, 4.425569e-08, 4.228165e-08,
  4.159599e-08, 4.209853e-08, 4.325655e-08, 4.450283e-08, 4.532603e-08],
 [5.567425e-08, 5.506284e-08, 5.397009e-08, 5.263876e-08, 5.144292e-08,
  5.083017e-08, 5.085334e-08, 5.129416e-08, 5.184568e-08, 5.221874e-08],
 [5.914666e-08, 5.868727e-08, 5.787003e-08, 5.688669e-08, 5.599869e-08,
  5.545781e-08, 5.533023e-08, 5.550704e-08, 5.579456e-08, 5.599997e-08]]

#array= np.multiply(array,1000000)


# In[ ]:


difa= [0 ,100 ,200 ,300 ,400, 500, 600, 700, 800, 900]
difb= [1 ,1 ,1 ,1, 1, 1,  1,  1,  1, 1 , 1,  1,  1 , 1
  ,1  ,1  ,1  ,1  ,1  ,1 ,1 ,1 ,1 ,1]

#difb= [100. ,100. ,100. ,100. , 50.,  10.,  10.,  10.,  10. , 10. , 10.,  10.,  10. , 10.
#  ,10.  ,10.  ,10.  ,10.  ,10.  ,10. ,100. ,100. ,100. ,100.]


# In[ ]:


dy,dx=np.gradient(array,difb,difa)
dx


# In[ ]:


x = np.linspace(-90000000,9000000, 30)
x


# In[ ]:


#def plot_flowvectors(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
#    if rotate == True:
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis4,axis3 = np.meshgrid(axis3,axis4)
#    else:
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis3,axis4 = np.meshgrid(axis4,axis3)
#
#    fig, ax = plt.subplots()
#    ax.quiver(axis3, axis4, dx, dy,facedata)
#    ax.set(aspect=1, title='Quiver Plot')
#    plt.show()
#    return fig

#def plot_flowvectors(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
#    if rotate == True:
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis4,axis3 = np.meshgrid(axis3,axis4)
#    else:
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis3,axis4 = np.meshgrid(axis4,axis3)
#
#    fig, ax = plt.subplots()
#    im=ax.imshow(facedata, extent=[axis3.min(), axis3.max(), axis4.min(), axis4.max()])
#    ax.quiver(axis3, axis4, dx, dy,facedata)
#    ax.set(aspect=1, title='Quiver Plot')
#    fig.colorbar(im)
#    plt.show()
#    return fig


#def plot_flowvectors_no_cont(axis1,axis2,axis3,axis4,facedata,data,name,name2,surlabel,xlabel,ylabel,rotate):
#    """
#    Following based on this: https://stackoverflow.com/questions/25342072/computing-and-drawing-vector-fields
#    Uses
#
#    """
#    if rotate == True:
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis4,axis3 = np.meshgrid(axis3,axis4)
#        #axis2,axis1 = np.meshgrid(axis1,axis2)
#
#    else:
#        dy,dx=np.gradient(facedata, axis2, axis1)
#        axis3,axis4 = np.meshgrid(axis3,axis4)
#        #axis1,axis2 = np.meshgrid(axis1,axis2)



#
#    if op_Bot == True:
#        for i in list(params):
#            b in plotting(faces      ,'Bot'  ,'btval' ,'Z=','Y','X','X(m)','Y(m)',i,rotate=False).savefig(cwd+'/trexplot_output_pngs/'+'Bot'+str(i))
#                b.savefig(cwd+'/trexplot_output_pngs/'+'Bot'+str(i))
#                plt.close('all')
#
