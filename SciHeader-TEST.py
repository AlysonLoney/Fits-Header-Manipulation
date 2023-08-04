
""" 
    Runs fits files with multiple headers (this case 2) and saves the file again with 
    only the scientific header.  
"""

import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.io import fits
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy.visualization import LogStretch, SqrtStretch, ZScaleInterval, LinearStretch, PowerStretch


Fits1 = fits.open('     pathway to the fits file here    ') 

#NOTE usually for accessing the scientific header youd use 0 but because this file has the scientific header second - I put 1 and it seemed to work well
data_Fits1 = Fits1[1].data #Accessing the data 
hdr1 = Fits1[1].header #Accessing the header
wcs1 = WCS(hdr1) #defining the world coordinate system


def Norms(norm):

    """ 
        not neccesary, just for visualization. 
        (for another program of mine)
    """

    Sqrt_Stretch = ImageNormalize(stretch = SqrtStretch()) #Best for far UV 
    Log_Stretch = ImageNormalize(stretch = LogStretch()) #Works for all types (best bet usually)
    ZScaleLog = ImageNormalize(interval = ZScaleInterval(), stretch = LogStretch()) #Best for far IR 
    ZscaleLin = ImageNormalize(interval = ZScaleInterval(), stretch = LinearStretch()) #Best for Optical
    ZscalePow = ImageNormalize(interval = ZScaleInterval(), stretch = PowerStretch(a = 0.40)) #Another option for far IR (can be tricky)

    if norm == 'norm 1': 
        return Sqrt_Stretch
    
    if norm == 'norm 2':
        return Log_Stretch
    
    if norm == 'norm 3': 
        return ZScaleLog
    
    if norm == 'norm 4': 
        return ZscaleLin
    
    if norm == 'norm 5': 
        return ZscalePow


#test plot (once again for fun)
fig = plt.figure(figsize = (8, 5))
fig.add_subplot(projection = wcs1)
plt.imshow(data_Fits1, origin = 'lower', norm = Norms('norm 3'), cmap = 'Greys_r')
plt.xlabel('RA')
plt.ylabel('Dec')
plt.title('Test Plot')
plt.show()


#saving the file with ONLY the scientific header information
prihdr = wcs1.to_header() 
prihdu = fits.PrimaryHDU(header = prihdr, data = data_Fits1)
hdulist = fits.HDUList([prihdu])

hdulist.writeto('   pathway to where you want the new file saved .fits    ', overwrite = True)
