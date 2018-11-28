# coding: utf-8
#Debuging efforts go in here. This file is not useful for the end user
#Note to self - if issues with the grid     print(a[[0],[0],:].flatten()) in corner_point_vals
#Error was in corner_val_import for line vals=zone.xyz.values.reshape - debug commands bellow
#print(zone['xyz'])
#print(vals.shape)
#print (len(zone.X.unique()),len(zone.Y.unique()),len(zone.Z.unique()))
# in plotting print(len(f),len(c),a,a.shape)


import trexplot as tp

def main():
    #tp.gas_volfrac_import()
    #print('dispfaces',len(tp.displace_import()['Top']['X'].unique()))
    #print('flowdatafaces',len(tp.flowdata_import()['Top']['X'].unique()))

#    print(tp.corner_point_vals()['Top_X'])
#    print (tp.corner_val_import()[0])
    #print(tp.aqconc_name[])
    print(tp.gas_volfrac_import()['Top']['Z'])
    #print(tp.aq_conc_import())

    #print([i for i in tp.gas_volfrac_name.values()])

if __name__ == "__main__":
    main()
