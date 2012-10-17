import pyspeckit
import pyspeckitmodels
import ref_index
import pylab
import numpy as np
from pyspeckit.spectrum.models.inherited_voigtfitter import voigt
from pyspeckit.spectrum.models import model

def mymodel(xarr, b0, b1,
        amp1, xcen1, gw1, lw1,
        amp2, xcen2, gw2, lw2,
        amp3, xcen3, gw3, lw3,
        amp4, xcen4, gw4, lw4,
        return_components=False,
        normalized=False,
        **kwargs):
    """ docstring """

    base = xarr*b1+b0
    v1 = voigt(xarr,amp1,xcen1,gw1,lw1, normalized=normalized)
    v2 = voigt(xarr,amp2,xcen2,gw2,lw2, normalized=normalized)
    v3 = voigt(xarr,amp3,xcen3,gw3,lw3, normalized=normalized)
    v4 = voigt(xarr,amp4,xcen4,gw4,lw4, normalized=normalized)

    if return_components:
        return np.array([base,v1,v2,v3,v4])
    else:
        mod = base+v1+v2+v3+v4
        return mod

ModelClass =  model.SpectralModel(mymodel, 18,
        parnames=['b0','b1']+\
            [a+str(ii) 
            for ii in xrange(4)
            for a in ['amplitude','shift','gwidth','lwidth']], 
        parlimited=[(False,False)]*2 + [(False,False),(False,False),(True,False),(True,False)]*4, 
        parlimits=[(0,0)]*2 + [(0,0), (0,0), (0,0), (0,0)]*4,
        shortvarnames=('b0','b1') + ('A',r'\Delta x',r'\sigma_G',r'\sigma_L')*4,
        multisingle='multi',
        )

ModelClass.components = lambda xarr,pars: mymodel(xarr, *pars, return_components=True)

def pcygni(xarr, b0, b1,
        amp1, xcen1, gw1, lw1,
        amp2, xcen2, gw2, lw2,
        amp3, xcen3, gw3, lw3,
        amp4, xcen4, gw4, lw4,
        amp5, xcen5, gw5, lw5,
        return_components=False,
        normalized=False,
        **kwargs):
    """ docstring """

    base = xarr*b1+b0
    v1 = voigt(xarr,amp1,xcen1,gw1,lw1, normalized=normalized)
    v2 = voigt(xarr,amp2,xcen2,gw2,lw2, normalized=normalized)
    v3 = voigt(xarr,amp3,xcen3,gw3,lw3, normalized=normalized)
    v4 = voigt(xarr,amp4,xcen4,gw4,lw4, normalized=normalized)
    v5 = voigt(xarr,amp5,xcen5,gw5,lw5, normalized=normalized)

    if return_components:
        return np.array([base,v1,v2,v3,v4,v5])
    else:
        mod = base+v1+v2+v3+v4+v5
        return mod

PCygni =  model.SpectralModel(pcygni, 22,
        parnames=['b0','b1']+\
            [a+str(ii) 
            for ii in xrange(5)
            for a in ['amplitude','shift','gwidth','lwidth']], 
        parlimited=[(False,False)]*2 + [(False,False),(False,False),(True,False),(True,False)]*5, 
        parlimits=[(0,0)]*2 + [(0,0), (0,0), (0,0), (0,0)]*5,
        shortvarnames=('b0','b1') + ('A',r'\Delta x',r'\sigma_G',r'\sigma_L')*5,
        multisingle='multi',
        )

PCygni.components = lambda xarr,pars: pcygni(xarr, *pars, return_components=True)


def halpha(sp):
    HA = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmera']*1e3)
    return line(sp, 6562.7715) # NIST
    return line(sp, HA)

def hbeta(sp):
    HB = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerb']*1e3)
    return line(sp, 4861.128) # NIST
    return line(sp, HB)

def hgamma(sp):
    HG = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerg']*1e3)
    return line(sp, 4340.471)
    return line(sp, HG)

def line(sp, refX):
    sp = sp.copy()
    sp.xarr.units = 'angstroms'
    sp.xarr.refX = refX
    sp.xarr.refX_units = 'angstroms'
    sp.xarr.xtype='wavelength'
    sp.xarr.convert_to_unit('km/s')
    return sp

sp2 = pyspeckit.Spectrum('UT121009_DIS.txt',skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
sp2.units = 'erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
sp2.specfit.register_fitter('mymodel',ModelClass,18,multisingle='multi')
sp2.specfit.register_fitter('pcygni',PCygni,22,multisingle='multi')
sp3 = pyspeckit.Spectrum('UT121002_DIS.txt',skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
sp3.units = 'erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
sp3.specfit.register_fitter('mymodel',ModelClass,18,multisingle='multi')
sp3.specfit.register_fitter('pcygni',PCygni,22,multisingle='multi')
sp4 = pyspeckit.Spectrum('UT120830_DIS.txt',skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
sp4.units = 'erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
sp4.specfit.register_fitter('mymodel',ModelClass,18,multisingle='multi')
sp4.specfit.register_fitter('pcygni',PCygni,22,multisingle='multi')

for sp in [sp2,sp3,sp4]:
    sp.xarr.units = 'angstroms'
    sp.xarr.refX = 6562.80
    sp.xarr.refX_units = 'angstroms'
    sp.xarr.xtype='wavelength'
    sp.xarr.convert_to_unit('km/s')

parlimits = [(0,0)]*2 + [(0,0), (0,0), (0,0), (0,0)]*4
parlimits[15] = (5000,5300)
parlimits[16] = (0,300)
parlimits[17] = (0,300)
parlimited =[(False,False)]*2 + [(False,False),(False,False),(True,False),(True,False)]*4
for xx in (15,16,17): parlimited[xx] = (True,True)
for xx in [2,6,10,14]:
    parlimits[xx] = (0,0)
    parlimited[xx] = (True,False)
parlimits[11] = (600,7800)
parlimited[11] = (True,True)
parlimits[12] = (0,2500)
parlimited[12] = (True,True)
parlimits[13] = (0,2500)
parlimited[13] = (True,True)
guesses = ([0.674,-4.63e-6]+
        [2.4,19,162,20]+
        [0.54,25,900,400]+
        [0.1,5000,85,200]+
        [0.11,5188,184,10]
        )
test = mymodel(sp2.xarr, *guesses, return_components=True)
#sp2.plotter.axis.plot(sp2.xarr,test.T,color='g')
pylab.show()
sp2.specname="UT121009"
sp2.plotter(xmin=-50000,xmax=50000,ymin=-0.1)
sp2.specfit.selectregion(xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000],highlight_fitregion=True)
sp2.specfit(fittype='mymodel',guesses=guesses, parlimits=parlimits,
        parlimited=parlimited, show_components=True,
        xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000], 
        highlight_fitregion=True)
sp2.specfit.plotresiduals()
pylab.figure(2); pylab.title('Residuals UT121009'); pylab.gca().set_ylim(-0.1,0.1)
sp2.specfit.highlight_fitregion(color='orange',linewidth=0.5)
sp2.plotter.savefig('UT121009_halpha_4compfit.png')

sp3.specname="UT121002"
sp3.plotter(xmin=-50000,xmax=50000,ymin=-0.1)
sp3.specfit(fittype='mymodel',guesses=guesses, parlimits=parlimits,
        parlimited=parlimited, show_components=True,
        xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000], 
        highlight_fitregion=True)
sp3.specfit.plotresiduals(fig=12)
pylab.figure(12); pylab.title('Residuals UT121002'); pylab.gca().set_ylim(-0.1,0.1)
sp3.specfit.highlight_fitregion(color='orange',linewidth=0.5)
pylab.show()
sp3.plotter.savefig('UT121002_halpha_4compfit.png')

sp4.specname="UT120830"
sp4.plotter(xmin=-50000,xmax=50000,ymin=-0.1)
sp4.specfit(fittype='mymodel',guesses=guesses, parlimits=parlimits,
        parlimited=parlimited, show_components=True,
        xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000], 
        highlight_fitregion=True)
sp4.specfit.plotresiduals(fig=14)
pylab.figure(14); pylab.title('Residuals UT120830'); pylab.gca().set_ylim(-0.1,0.1)
sp4.specfit.highlight_fitregion(color='orange',linewidth=0.5)
pylab.show()
sp4.plotter.savefig('UT120830_halpha_4compfit.png')

parlimits = [(0,0)]*2 + [(0,0), (0,0), (0,0), (0,0)]*5
parlimits[15] = (5000,5300)
parlimits[16] = (0,300)
parlimits[17] = (0,300)
parfixed =[False]*22
parlimited =[(False,False)]*2 + [(False,False),(False,False),(True,False),(True,False)]*5
for xx in (15,16,17): parlimited[xx] = (True,True)
for xx in [2,6,10,14]:
    parlimits[xx] = (0,0)
    parlimited[xx] = (True,False)
parlimits[11] = (-200,200)
parlimited[11] = (True,True)
parlimits[12] = (0,25000)
parlimited[12] = (True,True)
parlimits[13] = (0,25000)
parlimited[13] = (True,True)
parlimited[18] = (True,True)
parlimits[18] = (-0.1,0)
parlimited[19] = (True,True)
parlimits[19] = (-15000,-1000)
parlimited[10] = (True,True)
parlimits[10] = (0,0.1)
parfixed[0]=True
parfixed[1]=True
guesses = ([0.674,-4.63e-6]+
        [2.4,19,162,20]+
        [0.54,25,900,400]+
        [0.05,0,2000,2000]+
        [0.11,5188,184,10]+
        [-0.05,-5000,300,300]
        )

sp2.specname="UT121009"
sp2.plotter(xmin=-50000,xmax=50000,ymin=-0.1)
sp2.specfit.selectregion(xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000],highlight_fitregion=True)
sp2.specfit(fittype='pcygni',guesses=guesses, parlimits=parlimits,
        parlimited=parlimited, show_components=True,
        xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000], 
        parfixed=parfixed,
        highlight_fitregion=True)
sp2.specfit.plotresiduals(fig=25)
pylab.figure(25); pylab.title('Residuals UT121009'); pylab.gca().set_ylim(-0.1,0.1)
sp2.specfit.highlight_fitregion(color='orange',linewidth=0.5)

sp3.specname="UT121002"
sp3.plotter(xmin=-50000,xmax=50000,ymin=-0.1)
sp3.specfit(fittype='pcygni',guesses=guesses, parlimits=parlimits,
        parlimited=parlimited, show_components=True,
        xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000], 
        parfixed=parfixed,
        highlight_fitregion=True)
sp3.specfit.plotresiduals(fig=26)
pylab.figure(26); pylab.title('Residuals UT121002'); pylab.gca().set_ylim(-0.1,0.1)
sp3.specfit.highlight_fitregion(color='orange',linewidth=0.5)
pylab.show()

sp4.specname="UT120830"
sp4.plotter(xmin=-50000,xmax=50000,ymin=-0.1)
sp4.specfit(fittype='pcygni',guesses=guesses, parlimits=parlimits,
        parlimited=parlimited, show_components=True,
        xmin=-25000,xmax=37000,exclude=[10800,14400,18750,24000], 
        parfixed=parfixed,
        highlight_fitregion=True)
sp4.specfit.plotresiduals(fig=27)
pylab.figure(27); pylab.title('Residuals UT120830'); pylab.gca().set_ylim(-0.1,0.1)
sp4.specfit.highlight_fitregion(color='orange',linewidth=0.5)
pylab.show()


"""
    
pre = sp4*15

from pylab import *
sp2.plotter(xmin=-20000,xmax=5000,ymin=0,figure=figure(0))
sp3.plotter(xmin=-20000,xmax=5000,ymin=0,axis=sp2.plotter.axis,clear=False,color='b')
pre.plotter(xmin=-20000,xmax=5000,ymin=0,axis=sp2.plotter.axis,clear=False,color='g')
"""

