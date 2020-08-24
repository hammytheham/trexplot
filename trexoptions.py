#trexoptions.py
#Config (option) file for trexplotting options - Hamish Robertson

#By default (op_corner=True) the corner values from the displacement output are used.
#Set op_corner =True and input into arrays to override/if no displacement.tec
#Check treactmech version to make sure displacement output is constant
op_corner=False
op_corner_x=[1,2,3,6,8]
op_corner_y=[2,4,10]
op_corner_z=[1,2,3.4,3.6,3.8,4,7,8]

info                    =True #Runtime progress info for user. Warnings on negative log plots are not included

#Output
op_png					= False   #output  png files
op_pdf					= True  #output pdfs
op_fig					= False   #return figure files

#Plot types
colored_cells			=True
colored_cells_log_plot  =False  #log the coloured cells plot
contour_plot			=True
flow_vectors_no_cont	=True
flow_vectors_cont		=False


#Files
op_Flowdata				= False	 #readin flowdata files
op_Flowvector			= False	 #readin flowvector files
op_Displacement			= False	 #note the xsection half values are one 'ahead' as extra value. User no addition
op_Stress_Strain		= True	 #readin stress_strain files
op_aqconc               = False   #readin aqconc file
op_gas_volfrac          = False  #readin gas_volfrac file
op_min_ab               = False  #readin mineral saturation
op_min_si               = False  #readin absolute values of minerals
# op_Plasticity           = True # not currently used

#Faces
op_Top					= True   #output top surface
op_Bot					= False  #output bottom surface
op_Max_Y				= False  #output y-plane along the maximum value of x surface
op_Min_Y				= False	 #output y-plane along the minimum value of x surface
op_Max_X				= False	 #output x-plane along the maximum value of y surface
op_Min_X				= False	 #output x-plane along the minimum value of y surface
op_xsec_Y_half			= False   #output x-plane along the medium value of y
op_xsec_X_half			= False	 #output y-plane along the medium value of x
op_xsec_Y_user			= False   #User specified x-planes from y values
op_xsec_X_user			= False	 #User specified y-planes from x values
op_xsec_Z_user			= True	 #User specified z-planes from z values

#Specify cross sections
xsec_user_yvals =[1,2,5] #insert y vals for x-plane starting locations
xsec_user_xvals =[1,3,6] #insert x vals for y-plane starting locations
xsec_user_zvals =[1,3,5]   #plan view crosssections

#Flowdata Variables
op_Porosity				= True
op_Perm_X				= True	# add log, add min + max,
op_Perm_Y				= True
op_Perm_Z				= True
op_Pressure				= True
op_Temperature			= True
op_SatGas				= True
op_SatLiq				= True
op_X1					= True
op_X2					= True
op_Pcap					= True
op_DGas					= True
op_DLiq					= True
op_Krel_Gas				= True
op_Krel_Liq				= True
op_HGas					= True
op_HLiq					= True
op_Cp					= True
op_TC					= True
op_DBlk					= True
op_Tdif					= True

#Flowvector Variables
op_FluxLiq				= True
op_FluxLiq_X			= True
op_FluxLiq_Y			= True
op_FluxLiq_Z			= True
op_PorVelLiq			= True
op_PorVelLiqX			= True
op_PorVelLiqY			= True
op_PorVelLiqZ			= True
op_FluxGas				= True
op_FluxGas_X			= True
op_FluxGas_Y			= True
op_FluxGas_Z			= True
op_PorVelGas			= True
op_PorVelGasX			= True
op_PorVelGasY			= True
op_PorVelGasZ			= True
op_HeatFlux				= True
op_HeatFlux_X			= True
op_HeatFlux_Y			= True
op_HeatFlux_Z			= True

#Displacement variables
op_Disp_x				= True
op_Disp_y				= True
op_Disp_z				= True

#Stress Strain variables
op_Sigma_xx				= True
op_Sigma_yy				= True
op_Sigma_zz				= True
op_Sigma_yz				= True
op_Sigma_xz				= True
op_Sigma_xy				= True
op_Strain_xx			= True
op_Strain_yy			= True
op_Strain_zz			= True
op_Strain_yz			= True
op_Strain_xz			= True
op_Strain_xy			= True
op_Vol_Strain			= True
op_E_fail_xx			= True
op_E_fail_yy			= True
op_E_fail_zz			= True
op_E_fail_yz2			= True
op_E_fail_xz2			= True
op_E_fail_xy2			= True
op_E_fail_vol			= True

#Plasticity variables - I started writing a plasticity import file
#pretty sure its all in stress strain file

#Aqueous Species for aqconc.tec
#Check and add to the dictionary bellow to input all of your solution species
#left is name as it appears in the aqconc file, right is renamed version for pandas
#only thing that matters is the X,Y,Z names. Generally try and keep the rest the same
#The dictionary bellow the names is where you turn them on or off just expand as needed
#This section is a little different to the above as when you add in new minerals or output
#You need to modify this. The other files you dont tend to get variations in output
#Order matters
aqconc_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"P(bar)"':"Pressure(bar)", '"T(C)"':"Temperature(C)",
            '"SatGas"':"SatGas",'"SatLiq"':"SatLiq",'"aH2O"':"aH2O",'"pH"':"pH",'"t_na+"':"t_na+",'"t_cl-"':"t_cl-",
            '"t_hco3-"':"t_hco3-",'"t_ca+2"':"t_ca+2",'"t_so4-2"':"t_so4-2",'"t_mg+2"':"t_mg+2",'"t_ba+2"':"t_ba+2",
            '"t_al+3"':"t_al+3",'"t_h4sio4"':"t_h4sio4",'"t_k+"':"t_k+"}

#Order doesn't matter
aqconc_variable={'Pressure(bar)':True,
            'Temperature(C)':True,
            'SatGas':True,
            'SatLiq':True,
            'aH2O':True,
            'pH':True,
            't_na+':True,
            't_cl-':True,
            't_hco3-':True,
            't_ca+2':True,
            't_so4-2':True,
            't_mg+2':True,
            't_ba+2':True,
            't_al+3':True,
            't_h4sio4':True,
            't_k+':True}

# Import params and variable print settings for gas_volfrac.tec.Func inserts values in before as too small a dataset for normal use.
# Note the setting that the dict key is "'X'" format rather than '"X"' in others. The script writes a header of the dict keys to the top of the
# .tec file which is then re-read back in. Why? See futher discussion in the function gas_volfrac_import. If you need extra then just remove the blanks.
# Order matters
gas_volfrac_name={"'X'":'X', "'Y'":'Y', "'Z'":'Z', "'Pressure(bar)'":'Pressure(bar)', "'Temperature(C)'":'Temperature(C)',
                 "'SatGas'":'SatGas',"'RH'":'RH',"'blank1'":'blank1',"'blank2'":'blank2',"'blank3'":'blank3',"'blank4'":'blank4'}

#Order doesnt matter
gas_volfrac_variable={'Pressure(bar)':True,
            'Temperature(C)':True,
            'SatGas':True,
            'RH':True}

#Import params and variable print settings for mineral.tec.
# Order matters
min_ab_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"Porosity"':"Porosity",
            '"Poros_Chg"':"Poros_Chg",'"Permx(m^2)"':"Permx(m^2)",'"Kx/Kx0"':"Kx_Kx0", '"Permz(m^2)"':"Permz(m^2)",
            '"Kz/Kz0"':"Kz_Kz0",'"dolomite"':"dolomite",'"calcite"':"calcite"}

#Order doesnt matter
min_ab_variable={'Porosity':True,
            'Poros_Chg':True,
            'Permx(m^2)':True,
            'Kx_Kx0':True,
            'Permz(m^2)':True,
            'Kz_Kz0':True,
            'dolomite':True,
            'calcite':True}


#Import params and variable print settings for min_SI.tec
# Order matters
min_si_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"T(C)"':"Temperature(C)",
                 '"dolomite"':"dolomite",'"calcite"':"calcite"}

#Order doesnt matter
min_si_variable={'Temperature(C)':True,
            'dolomite':True,
            'calcite':True}
