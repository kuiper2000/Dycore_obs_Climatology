#!/usr/bin/env python
# coding: utf-8

# In[43]:


with open("day_label.txt", "r") as file:
     start_day, end_day = map(int, file.read().split())
with open("iteration.txt", "r") as file:
     iteration = int(file.read())
with open("iteration.txt", "r") as file:
     iteration = int(file.read())    


# In[38]:


# iteration = 1
# start_day = 0
# end_day   = 500


# In[44]:


import h5py

## load T_obs climatology (doesn't change with iteration)
#  file_path = '/home/kaichiht/Colab/2025_research/Dycore_obs_Climatology/IdealizeSpetral.jl/exp/HSt42/obs_theta/'
file_name = 'grid_t_obs.dat'

# Open the HDF5 file in read mode
with h5py.File(file_name, "r") as file:
    # List all datasets and groups
    # print("Keys:", list(file.keys()))

    # Access a specific dataset (assuming the key is 'dataset_name')
    dataset = file["T"]
    
    # Read dataset into a NumPy array
    temp_Dycore = dataset[:]

## load Q1_obs climatology (change with iteration)
# file_path = '/home/kaichiht/Colab/2025_research/Dycore_obs_Climatology/IdealizeSpetral.jl/exp/HSt42/obs_theta/'
#file_name = 'grid_Q1'+str(iteration)+'.dat'
file_name = 'grid_Q1_'+str(iteration-1)+'.dat'


import os
if os.path.exists(file_name):
    print("File exists")
    # Open the HDF5 file in read mode
    with h5py.File(file_name, "r") as file:
        # List all datasets and groups
        # print("Keys:", list(file.keys()))
    
        # Access a specific dataset (assuming the key is 'dataset_name')
        dataset   = file["Q1"]
        
        # Read dataset into a NumPy array
        Q1_Dycore = dataset[:]
else:
    # if the iterated Q1 files doesn't exist, use the original one
    file_name = 'grid_Q1.dat'

    # Open the HDF5 file in read mode
    with h5py.File(file_name, "r") as file:
        # List all datasets and groups
        # print("Keys:", list(file.keys()))
    
        # Access a specific dataset (assuming the key is 'dataset_name')
        dataset   = file["Q1"]
        
        # Read dataset into a NumPy array
        Q1_Dycore = dataset[:] #(use a small first guess)


# In[40]:


# load previous iteration 

import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import matplotlib.cm as cm
import datetime 
import time
from Load_File import Load_File

#del tmp
# start_day = 0
# end_day   = 500

def load_file(PR, start_day, end_day, path, load_variable='none'):
    tmp = []
    for i in range(start_day, end_day+25, 25):
        #path          = '/work/kaichiht/Colab/2025_research/Dycore_obs_Climatology/IdealizeSpetral.jl/exp/HSt42/HSt42_0/'
        
        file_path     = path+'RH80_PR'+str(PR)+'_'+str(end_day)+'day_startfrom_'+str(i)+'day_final.dat'
        f             = Load_File(load_variable)
        if i == start_day:
            with h5py.File(file_path, "r") as file:
                print(file.keys())
        print(i)
        if os.path.exists(file_path):
            if i==0:
                tmp = np.array(f.load_data(file_path))
            else:
                tmp = np.concatenate((tmp,np.array(f.load_data(file_path))))
    
    return tmp

if iteration >1:
    # load previous iteration to generate the following iteration 
    path              = '/work/kaichiht/Colab/2025_research/Dycore_obs_Climatology/IdealizeSpetral.jl/exp/HSt42/HSt42_0_'+str(iteration-1)+'/'
    grid_t_c_xyzt     = load_file(0, start_day, end_day, path, 'grid_t_c_xyzt')
    grid_p_full_xyzt  = load_file(0, start_day, end_day, path, 'grid_p_full_xyzt')
    # calculate Q_{N} = Q_{N-1}-2/3 (\bar{T}-T_obs)/\tau
    lat = np.linspace(-90, 90, 64)
    p     = grid_p_full_xyzt[:,:,:,:].mean(axis=(0,3))
    sigma = grid_p_full_xyzt[:,:,:,:].mean(axis=(0))/grid_p_full_xyzt[:,19,:,:].mean(axis=(0))
    
    k_a = 1/40
    k_s = 1/4
    k_t = k_a + (k_s-k_a)*np.maximum(0,(sigma.mean(axis=2)-0.7)/(1-0.7))*np.cos(lat/180*np.pi)**4
    k_t_3D = np.tile(k_t[..., np.newaxis],(1,1,128))
    
    Q_N = (Q1_Dycore - 1/5*(grid_t_c_xyzt[1600:,:,:,:].mean(axis=0)-temp_Dycore)*k_t_3D)
else:
    Q_N = Q1_Dycore


# In[33]:


# import h5py
# import numpy as np

# ## Write Regrid File into and HDF5 file 
# file_path = '/home/kaichiht/Colab/2025_research/Dycore_obs_Climatology/IdealizeSpetral.jl/exp/HSt42/obs_theta/'
# file_name = 'grid_t_obs.dat'


# # Create a new HDF5 file
# with h5py.File(file_path+file_name, "w") as hdf:
#     # Define data for variable T
#     #T = np.random.rand(10, 10)  # Example: 10x10 array with random values

#     # Create a dataset in the HDF5 file
#     hdf.create_dataset("T", data=temp_Dycore)

#     # Optionally, add attributes (metadata)
#     hdf["T"].attrs["units"] = "Kelvin"
#     hdf["T"].attrs["description"] = "Temperature data"

## Write Regrid File into and HDF5 file 
# file_path = '/home/kaichiht/Colab/2025_research/Dycore_obs_Climatology/IdealizeSpetral.jl/exp/HSt42/obs_theta/'
file_name = 'grid_Q1_'+str(iteration)+'.dat'


# Create a new HDF5 file
with h5py.File(file_name, "w") as hdf:
    # Define data for variable T
    #T = np.random.rand(10, 10)  # Example: 10x10 array with random values

    # Create a dataset in the HDF5 file
    hdf.create_dataset("Q1", data=Q_N)

    # Optionally, add attributes (metadata)
    hdf["Q1"].attrs["units"] = "Kelvin/s"
    hdf["Q1"].attrs["description"] = "Heating data"
    

