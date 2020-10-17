import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.lines as mlines
import matplotlib.cm as cm

###############################################################################
#-----------------------------Variables--------------------------------------#
lambda1=350 #nm
lambda2=500
lambda3=920
T=10 #C
P=775 #hPa
f=2.7 #hPa
r_0=15*10**7 #nm
long_0=550 #nm
##############################################################################
lambd=[]
print('This code run the Alexei V.Filippenko\'s model for atmospheric differential refraction adding the seeing efect in case of a split of 1.8 arcsec in diameter.\n The atmospheric differential refraction as a function of wavelenght is calculated for the condictions typical of major optical observatories. ')
print('See: THE IMPORTANCE OF ATMOSPHERIC DIFFERENTIAL REFRACTION IN SPECTROPHOTOMETRY. 1982 ')

KEY=input('\n->Type Ex for run an example or  press \'any key\' to introduce wavelenghts in [nm] ...')
if KEY=='Ex':
	lambd=[lambda1,lambda2,lambda3]
else:
	KEY2=False
	while KEY2!=True:
		wavelenght=float(input('Insert wavelenght in nm: '))
		lambd.append(wavelenght)
		KEY2=input('Do you want another? (any key/no) ')
		if KEY2=='no':
			KEY2=True
print('Wavelenghts :' + str(lambd))

def vapor(long_onda,f,T):
	'''
	The presence of water vapor in the atmosphere reduces (n-1)10^6 by "return()"
	'''
	return( (0.0624-0.000680/long_onda**2)/(1+0.003661*T)*f )

def n_sealevelfun(long_onda,f,T):
	'''
	The index of refraction at sea level.
	'''
	H2O=vapor(long_onda,f,15)
	print('The water vapour factor-lambda[microns]= '+ str(round(long_onda,3))+
		' f[mmHG]='+str(round(f,3))+' T[ºC]='+str(round(T,3))+' is : '+
		 str(round(H2O,3)) )
	return( (64.328+29498.1/(146-(1/long_onda)**2)
		+255.4/(41-(1/long_onda)**2)-H2O)/10**6 +1)

def n(long_onda,T,P,f):
	'''
	The index of refractrion with the parameters of interest.
	'''
	n_sealevel=n_sealevelfun(long_onda,f,15)
	print('Value of n at sea level:'+ str(round(n_sealevel,3)))
	H2O_2=vapor(long_onda,f,T)
	print('The water vapour factor-lambda[microns]= '+ str(round(long_onda,3))+
		' f[mmHG]='+str(round(f,3))+' T[ºC]='+str(round(T,3))+' is : '+ 
		str(round(H2O_2,3)) )
	return( ((n_sealevel-1)*( P*(1+(1.049-0.0157*T)*10**(-6)*P)/
		(720.883*(1+0.003661*T))-H2O_2/10**6))+1 )

def Deltar(long_onda,ang,T,P,f):
	'''
	The atmospheric diferential refraction relative to 500nm calculated for an object at zenith angle ang.
	'''
	n450=n(450*0.001,T,P,f)
	print('Reference n value at 450nm: '+str(round(n450,6)))
	print('The index of refraction for lambda[microns]= '+
	 str(round(long_onda,3))+' f[mmHG]='+str(round(f,3))+' T[ºC]='+
	 str(round(T,3))+' P[mmHg]='+str(round(P,3)) +' :'+ 
	 str(round(n(long_onda,T,P,f),6)))
	return(206265*(n(long_onda,T,P,f)-n450)*np.tan(ang))


def r0(long_onda,r_0,long_0,ang):
	'''
	The coherence length.
	'''
	return( r_0*((long_onda/long_0)**(1.2))*(np.cos(ang*np.pi/180))**0.6 )
def alpha(long_onda,r_0,long_0,ang):
	'''
	Seeing disk. Angular size. 
	'''
	return( 1.2*206265*long_onda/r0(long_onda,r_0,long_0,ang)  )


ang=np.linspace(0,60,5) #distancia cenital. No vale para 80
Buf=[]
buf=0
print('Zenith distance values in degrees')
print(str(np.round(ang,3))+'\n')

for i in lambd:
	Buf.append([])
	Valores=np.round(Deltar(i*0.001,ang*np.pi/180,T,P*0.750,f*0.750),3) 
	#Convertimos a micras,rad,C,mmHg,mmHg en la entrada
	print('For a value of lambda'+ str(i) +
		' microns, a desviation is obtained [arcsec]:')
	print(Valores); print('\n-----------------------------------\n')
	Buf[buf]=Valores ; buf=buf+1

ax=plt.figure().add_subplot(111)
colors = cm.rainbow(np.linspace(0, 1, len(lambd)))
for i in range(len(lambd)):
	c=[colors[i]]
	plt.scatter(ang,Buf[i],c=c,label= str(lambd[i])+ 'nm')
plt.legend(); plt.legend(shadow=True); ax.set_ylabel('$\Delta R (arcsec)$')
ax.set_xlabel('Z [deg]')
plt.title('Relative positions of the different beams')
plt.grid(True)
plt.show() ; plt.close()



Buf2=[]
buf=0
for i in lambd:
	Buf2.append([])
	Buf2[buf]=alpha(i,r_0,long_0,ang)
	buf=buf+1
print('Seeing values in order of lambda:')
for i in range(len(Buf2)):
	print(Buf2[i])


input('\n ||WARNING|| \n'+
	'It is possible that for resolution reasons the graphics may not scale properly.'+ 
	'The dotted line of the first wavelength serves as a reference for the diameters\n You can adjust the plot changing SCALE value after close the plot. \n See the Ex case\n'+
	'||PRESS ANY KEY||')
scaleSTOP='yes'
SCALE=110
print('SCALE = 110 [plot units]')

while scaleSTOP!='no':
	print('\nPloting...')
	angulo=np.linspace(0,2*np.pi,100)
	ax=plt.figure().add_subplot(111)
	cmap = plt.get_cmap('gnuplot')
	colors = [cmap(i) for i in np.linspace(0, 1, (len(lambd)+1)*2)]
	for i in range(len(lambd)):
		c=colors[i+2]
		plt.scatter(ang,Buf[i],c=c,label= str(lambd[i])+ 'nm')
	plt.legend(prop={'size': 20},shadow=True); 
	for k in range(len(lambd)):
		c=colors[k+2]
		for j in range(len(Buf[0])):
			for i in angulo:
				plt.plot(ang[j],Buf[k][j]+Buf2[k][j]/2*np.sin(i), marker='.',
					c=c,markersize=0.5)
				plt.plot(ang[j],1.8/2*np.sin(i), marker='.',
					c='black',markersize=0.5)
			plt.plot(ang[j],Buf[k][j],markersize=np.abs(Buf2[k][j])*SCALE,marker='o',
				c=c,alpha=0.2)
			plt.plot(ang[j], 0, markersize=1.8*SCALE,fillstyle='none',marker='o',c='black',label='Split')
	ax.set_ylabel('$\Delta R (arcsec)$',fontsize=30); ax.set_xlabel('Z [deg]',fontsize=30)
	plt.title('Atmospheric dispersion on different $\lambda$',fontsize=30)
	plt.grid(True);
	plt.text(0,1,'Split (D=1.8 arsec)',fontsize=20)
	mng = plt.get_current_fig_manager();mng.resize(*mng.window.maxsize())
	plt.show() ; plt.close()
	scaleSTOP='Reset'
	while scaleSTOP !='yes' and scaleSTOP!='no':
		scaleSTOP=str(input('Do you want to change SCALE value? (yes/no):' ))
	if scaleSTOP=='yes':
		SCALE=float(input('New SCALE value, previus ->'+str(SCALE)+' : '))




