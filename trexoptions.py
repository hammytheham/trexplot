#trexoptions.py
#Config (option) file for trexplotting options - Hamish Robertson

#By default (op_corner=False) the corner values from the displacement output are used.
#Set op_corner =True and input into arrays to override/if no displacement.tec
#Check treactmech version to make sure displacement output is constant
op_corner=False
op_corner_x=[1,2,3,6,8]
op_corner_y=[2,4,10]
op_corner_z=[1,2,3.4,3.6,3.8,4,7,8]

#Output
op_png					= True   #output  png files
op_pdf					= True  #output pdfs
op_fig					= True   #return figure files

#Plot types
colored_cells			=True
contour_plot			=True
flow_vectors_no_cont	=True
flow_vectors_cont		=True

#log plot option - choose True to set the plot data to log
colored_cells_log_plot  =True  #coloured cells log plot


#Files
op_Flowdata				= True	 #readin flowdata files
op_Flowvector			= False	 #readin flowvector files
op_Displacement			= False	 #note the xsection half values
								 #are one 'ahead' as extra value. User no addition
op_Stress_Strain		= False	 #readin stress_strain files
op_aqconc               = True
op_gas_volfrac          = True
op_min_si               = True
op_min_ab               = True



#Faces
op_Top					= True   #output top surface
op_Bot					= True  #output bottom surface
op_Max_Y				= False  #output y-plane along the maximum value of x surface
op_Min_Y				= False	 #output y-plane along the minimum value of x surface
op_Max_X				= False	 #output x-plane along the maximum value of y surface
op_Min_X				= False	 #output x-plane along the minimum value of y surface
op_xsec_Y_half			= True   #output x-plane along the medium value of y
op_xsec_X_half			= False	 #output y-plane along the medium value of x
op_xsec_Y_user			= False   #User specified x-planes from y values
op_xsec_X_user			= False	 #User specified y-planes from x values

#Specify cross sections
xsec_user_yvals =[1,2,5] #insert y vals for x-plane starting locations
xsec_user_xvals =[1,3,6] #insert x vals for y-plane starting locations


#Flowdata Variables
op_Porosity				= True
op_Perm_X				= True	# add log, add min + max,
op_Perm_Y				= False
op_Perm_Z				= False
op_Pressure				= False
op_Temperature			= True
op_SatGas				= False
op_SatLiq				= False
op_X1					= False
op_X2					= False
op_Pcap					= False
op_DGas					= False
op_DLiq					= False
op_Krel_Gas				= False
op_Krel_Liq				= False
op_HGas					= False
op_HLiq					= False
op_Cp					= False
op_TC					= False
op_DBlk					= False
op_Tdif					= False

#Flowvector Variables
op_FluxLiq				= False
op_FluxLiq_X			= False
op_FluxLiq_Y			= False
op_FluxLiq_Z			= False
op_PorVelLiq			= False
op_PorVelLiqX			= False
op_PorVelLiqY			= False
op_PorVelLiqZ			= False
op_FluxGas				= False
op_FluxGas_X			= False
op_FluxGas_Y			= False
op_FluxGas_Z			= False
op_PorVelGas			= False
op_PorVelGasX			= False
op_PorVelGasY			= False
op_PorVelGasZ			= False
op_HeatFlux				= False
op_HeatFlux_X			= False
op_HeatFlux_Y			= False
op_HeatFlux_Z			= False

#Displacement variables
op_Disp_x				= False
op_Disp_y				= False
op_Disp_z				= False

#Stress Strain variables
op_Sigma_xx				= False
op_Sigma_yy				= False
op_Sigma_zz				= False
op_Sigma_yz				= False
op_Sigma_xz				= False
op_Sigma_xy				= False
op_Strain_xx			= False
op_Strain_yy			= False
op_Strain_zz			= False
op_Strain_yz			= False
op_Strain_xz			= False
op_Strain_xy			= False
op_Vol_Strain			= False
op_E_fail_xx			= False
op_E_fail_yy			= False
op_E_fail_zz			= False
op_E_fail_yz2			= False
op_E_fail_xz2			= False
op_E_fail_xy2			= False
op_E_fail_vol			= False

#Aqueous Species for aqconc.tec
#Check and add to the dictionary bellow to input all of your solution species
#left is name as it appears in the aqconc file, right is renamed version for pandas
#only thing that matters is the X,Y,Z names. Generally try and keep the rest the same
#The dictionary bellow the names is where you turn them on or off just expand as needed
#This section is a little different to the above as when you add in new minerals or output
#You need to modify this. The other files you dont tend to get variations in output

aqconc_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"P(Pa)"':"Pressure(Pa)", '"T(C)"':"Temperature(C)",
            '"SatGas"':"SatGas",'"SatLiq"':"SatLiq",'"aH2O"':"aH2O",'"pH"':"pH",'"t_na+"':"t_na+",'"t_cl-"':"t_cl-",
            '"t_hco3-"':"t_hco3-",'"t_ca+2"':"t_ca+2",'"t_so4-2"':"t_so4-2",'"t_mg+2"':"t_mg+2",'"t_ba+2"':"t_ba+2",
            '"t_al+3"':"t_al+3",'"t_h4sio4"':"t_h4sio4",'"t_k+"':"t_k+"}

aqconc_variable={'Pressure(Pa)':True,
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

# Import params and variable print settings for gas_volfrac.tec
gas_volfrac_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"P(bar)"':"Pressure(bar)", '"T(C)"':"Temperature(C)",
                 '"SatGas"':"SatGas",'"RH"':"RH"}
gas_volfrac_names=["X", "Y", "Z", "Pressure(bar)", "Temperature(C)",
                 "SatGas","RH"]

gas_volfrac_variable={'Pressure(Pa)':True,
            'Temperature(C)':True,
            'SatGas':True,
            'RH':True}

#Import params and variable print settings for min_SI.tec
min_si_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"T(C)"':"Temperature(C)",
                 '"dolomite"':"dolomite",'"calcite"':"calcite"}

min_si_variable={'Temperature(C)':True,
            'dolomite':True,
            'calcite':True}

#Import params and variable print settings for mineral.tec
min_ab_name={'"X(m)"':"X", '"Y(m)"':"Y", '"Z(m)"':"Z", '"Porosity"':"Porosity",
            '"Poros_Chg"':"Poros_Chg",'"Permx(m^2)"':"Permx(m^2)",'"Kx/Kx0"':"Kx/Kx0", '"Permz(m^2)"':"Permz(m^2)",
            '"Kz/Kz0"':"Kz/Kz0",'"dolomite"':"dolomite",'"calcite"':"calcite"}

min_ab_variable={'Porosity':True,
            'Poros_Chg':True,
            'Permx(m^2)':True,
            'Kx/Kx0':True,
            'Permz(m^2)':True,
            'Kz/Kz0':True,
            'dolomite':True,
            'calcite':True}
