# ATMOSPHERIC-DIFFERENTIAL-REFRACTION-
Alexei V.Filippenko\'s model for atmospheric differential refraction adding the seeing efect in case of a split of 1.8 arcsec in diameter.
Link: http://adsabs.harvard.edu/full/1982PASP...94..715F

This code shows the relative positions of the images of a astronomical source at 350 nm, 500 nm and 920 nm. You can also enter the wavelengths you want in nm and change (inside the code) the value of the parameters.
In the second plot, the hollow circle represents the entrance of a 1.8 arsec diameter slit.

## CODE INFORMATION
I have created several functions to modulate the different sections of Alexei V. FIlippenko's article. 
The parameters must be entered : wavelength in nm, pressure in hPa, f (the water vapor pressure ) in hPa, r_0(the coherence length, reflects the turbulent state of the atmosphere) in nm, temperature in degrees Celsius. 
The program is responsible for entering it in the appropriate units for the equations.  

Instead of using 500 nm as a reference in equation 4, 450 nm was used.

An expected result is:
![Example](/images/logo.png)
Format: ![Alt Text](url)
