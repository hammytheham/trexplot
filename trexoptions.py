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
op_png					= False   #output  png files
op_pdf					= False  #output pdfs
op_fig					= True   #return figure files

#Plot types
colored_cells			=True
contour_plot			=True
flow_vectors_no_cont	=True
flow_vectors_cont		=True



#Files
op_Flowdata				= True	 #readin flowdata files
op_Flowvector			= False	 #readin flowvector files
op_Displacement			= False	 #note the xsection half values
								 #are one 'ahead' as extra value. User no addition
op_Stress_Strain		= False	 #readin stress_strain files

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

#Specify cross sections
xsec_user_yvals =[1,2,5] #insert y vals for x-plane starting locations
xsec_user_xvals =[1,3,6] #insert x vals for y-plane starting locations


#Flowdata Variables
op_Porosity				= True
op_Perm_X				= False	# add log, add min + max,
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
