import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree


#Reading the input file

f = open('input.dat','r')
content = f.read()
lines = content.split('\n')
for i in lines:
    file_name= lines[1] 
    start   = lines[2] 
    start = int(start)

# Definition of the block average function

def blockAverage(data, maxBlockSize=None):
	"""Computes the block average of a timeseries "x", and 
	provides error bounds for the estimated mean <x>. 

	Parameters
	--------------------
	`data`  : Time series array of an observable X
	`maxBlocksize` : Maximum number of observations/block

	Returns
	--------------------
	`m_points` : Points used (observations/block) for computing averages
	`blockVar` : Variances for each blocksize array 
	`blockMean` : Variances for each blocksize array 	
	"""
 
	Nobs = len(data)           # total number of observations in data
	minBlockSize = 1           # min 1 observation/block
 
	if maxBlockSize is None: maxBlockSize = int(Nobs/4)   # max: 4 blocks (otherwise can't calc variance)
  
	# m_points = 2**n until being less of the inputed maxblocksize
	power = np.arange(int(np.log(maxBlockSize)/np.log(2)))
	m_points = 2**power

	NumBlocks = len(m_points)   				# total number of block sizes

	blockMean = np.zeros(NumBlocks)             # mean for each blocksize
	blockVar  = np.zeros(NumBlocks)             # variance associated with each blockSize


	# Loop for all considered blocksizes (m)
	for k,m in enumerate(m_points):

		Nblock    = int(Nobs/m)               # Number of blocks
		obsProp   = np.zeros(Nblock)          # Container for parcelling block 

		# Loop to chop datastream into blocks and take average
		for i in range(1,Nblock+1):
			
			i1 = (i-1) * m
			i2 =  i1 + m
			obsProp[i-1] = np.mean(data[i1:i2])

		blockMean[k] = np.mean(obsProp)
		blockVar[k]  = np.var(obsProp)/(Nblock - 1)
	
	return m_points, blockVar, blockMean

# Reading output file


Raw_data = np.loadtxt('results/'+file_name,skiprows=1)

data = Raw_data.T

time,uener,kinener,etotal,temp,mom,press = data

# Computing the averages from the data arrays

data_entrance = ["Potential energy (KJ/mol)","Kinetic Energy (KJ/mol)" , "Total Energy (KJ/mol)" , "Temperature (K)" ,"Momentum (Kg · m /s)" , "Pressure (Pa)"]
# start = 932 # (Number of points that take the system to equilibrium) We should do that this variable should be an input !!!!
averages , errors = [] , []

for i ,xi in enumerate(data[1:]) :  #for each array of data avoiding time
	n_tot = len(xi)
	# Computing the block averages
	m_points_i,block_variance_i,block_mean_val_i = blockAverage(xi[start:],maxBlockSize=int(n_tot/100))
	blockSTD_i = np.sqrt(block_variance_i)
	mean_val =  block_mean_val_i.mean()
	std = (blockSTD_i[-5:]).mean()
	averages.append(mean_val)
	errors.append(std)
	# print results 
	print(f"Average : <{data_entrance[i]}> = {mean_val:15.5e} +/- {std:.5e} ")

with open("final_results.dat","w") as outFile :
	outFile.write("# Mean values and errors for the studied thermodynamic properties.\n")
	for i,label in enumerate(data_entrance):
		outFile.write(f"{label:>15} {averages[i]} +/- {errors[i]} \n")

# plotting the results

#plotting the energies
start2=932
plt.figure().set_figwidth(10)
plt.plot(time[start:],uener[start:],label=f'Epot = {averages[0]:.4e} +/- {errors[0]:.4e}')
plt.plot(time[start:],kinener[start:],label=f'Ekin = {averages[1]:.4e} +/- {errors[1]:.4e}')
plt.plot(time[start:],etotal[start:],label=f'Etotal = {averages[2]:.4e} +/- {errors[2]:.4e}')
plt.ylabel('Energy (KJ/mol)')
plt.xlabel('Time (s)')
plt.legend(bbox_to_anchor=(1.1, 1.05),fancybox=True, shadow=True, ncol=5)

# Shrink current axis by 20%


# Put a legend to the right of the current axis
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(fname='plots/energies.pdf',dpi=1000)
plt.clf()
#plotting temperatures
plt.plot(time[start:],temp[start:],label=f'Temp = {averages[3]:.4e} +/- {errors[3]:.4e} ')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.legend(bbox_to_anchor=(1.1, 1.05),fancybox=True, shadow=True, ncol=5)

# Shrink current axis by 20%


# Put a legend to the right of the current axis
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(fname='plots/Temperature.pdf',dpi=1000)
plt.clf()

# Plotting the momentum vs the time
plt.plot(time[start:],mom[start:],label=f'Momentum = {averages[4]:.4e} +/- {errors[4]:.4e} ')
plt.xlabel('Time (s)')
plt.ylabel('Momentum (Kg · m /s)')
plt.legend(bbox_to_anchor=(1.1, 1.05),fancybox=True, shadow=True, ncol=5)

# Shrink current axis by 20%


# Put a legend to the right of the current axis
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(fname='plots/Momentum.pdf',dpi=1000)
plt.clf()

# Plotting the momentum vs the time
plt.plot(time[start:],press[start:],label=f'Pressure = {averages[5]:.4e} +/- {errors[5]:.4e} ')
plt.xlabel('Time (s)')
plt.ylabel('Pressure (Pa)')
plt.legend(bbox_to_anchor=(1.1, 1.05),fancybox=True, shadow=True, ncol=5)

# Shrink current axis by 20%


# Put a legend to the right of the current axis
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(fname='plots/Pressure.pdf',dpi=1000)
plt.clf()

		
		