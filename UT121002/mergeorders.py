import pyspeckit
#import pyfits
import numpy as np

def loadplot(fn, axis=None, norm=False, midorder=33, scale=None,offset=0.0):
    tempthing = pyspeckit.wrappers.load_IRAF_multispec(fn)
    if scale is not None:
        for sp in tempthing:
            sp.data *= scale
    if axis is not None: 
        clear=False
    else: 
        clear=True
    if norm:
        plort = (tempthing[midorder]/tempthing[midorder].data.max())
        plort.plotter(axis=axis,clear=clear,offset=offset)
        tempthing[midorder].plotter.axis = plort.plotter.axis
        (tempthing[midorder+1]/tempthing[midorder+1].data.max()).plotter(axis=plort.plotter.axis,clear=False,color='blue',offset=offset)
        (tempthing[midorder-1]/tempthing[midorder-1].data.max()).plotter(axis=plort.plotter.axis,clear=False,color='red' ,offset=offset)
    else:
        tempthing[midorder].plotter(axis=axis,clear=clear,offset=offset)
        tempthing[midorder+1].plotter(axis=tempthing[midorder].plotter.axis,clear=False,color='blue',offset=offset)
        tempthing[midorder-1].plotter(axis=tempthing[midorder].plotter.axis,clear=False,color='red' ,offset=offset)
    sp = pyspeckit.Spectra(tempthing,xunits='angstroms')
    sp.plotter.axis = tempthing[midorder].plotter.axis
    return sp

def mergespec(fn):
    tempthing = pyspeckit.wrappers.load_IRAF_multispec(fn)
    for x in tempthing:
        x.crop(250,1150,units='pixels')
    return pyspeckit.Spectra(tempthing,xunits=x.xarr.units)

def mergeorders(splist):
    bigxarr = np.arange(float(splist[-1].xarr.min()),float(splist[0].xarr.max()),splist[-1].xarr.cdelt())
    bigspec = pyspeckit.Spectrum(data=np.zeros(bigxarr.shape), xarr=bigxarr,
            xarrkwargs={'units':'angstroms'})
    weights = bigspec.copy()
    
    for sp in (splist):
        spint = pyspeckit.arithmetic.interp(sp,bigspec)
        bigspec += spint
        flint = spint.data > 0
        weights.data += flint
    
    wspec = bigspec/weights

    return wspec
    
dis = pyspeckit.Spectrum('/Users/adam/work/sn2009ip/UT121002_DIS.final.txt',filetype='txt',skiplines=1)
dis.xarr.units = 'angstroms'
dis.xarr.xtype='wavelength'
dis.xarr *= 1.005715
dis.redshift = 0.005715

#nocal = loadplot('SN2009ip_comb.rs.ec.dispcor.fits')
#ec   = loadplot('SN2009ip_comb.rs.ec.dispcor.cal.fits')
eccr = loadplot('SN2009ip_comb.rs.ec.dispcor.crop.cal.fits')
eccrhi = loadplot('SN2009ip_comb.rs.ec.dispcor.crop.cal_hi.fits')
eccr.specname="SN2009ip"
eccrhi.specname="SN2009ip"
HR =  loadplot('HR7596_comb.rs.ec.dispcor.crop.cal.fits')
HRhi =  loadplot('HR7596_comb.rs.ec.dispcor.crop.cal_hi.fits')
HR.specname="HR7596"
HRhi.specname="HR7596"
import pylab
pylab.show()

ec = mergeorders(eccr)
hr = mergeorders(HR)
echi = mergeorders(eccrhi)
hrhi = mergeorders(HRhi)

hr.plotter(ymin=-1e-14,ymax=5e-11)
hrhi.plotter(axis=hr.plotter.axis,clear=False,color='r',ymin=-1e-14,ymax=4e-11)

eccr.plotter(ymax=1e-13,ymin=-1e-14)
echi.plotter(axis=eccr.plotter.axis,clear=False,color='r',ymin=-1e-14,ymax=5e-13)
dis_erg = dis * 1e-14
dis_erg.plotter(axis=eccr.plotter.axis,clear=False,color='orange')
ec.plotter(axis=eccr.plotter.axis,clear=False,color='g',ymin=-1e-14,ymax=5e-13)

ecsm = ec.copy()
ecsm.smooth(5)
ecsm.plotter()
dis_erg.plotter(axis=ecsm.plotter.axis,clear=False,color='orange')

pylab.show()

hrcal = pyspeckit.Spectrum('/Volumes/disk5/usr/stsci/iraf/iraf/noao/lib/onedstds/spec16cal/hr7596.dat')

sn_nocal = loadplot('SN2009ip_comb.rs.ec.dispcor.crop.fits')
sn_nocal.plotter(ymin=-0.001,ymax=0.015,xmin=6000,xmax=7200)
hr_nocal = loadplot('HR7596_comb.rs.ec.dispcor.crop.fits',axis=sn_nocal.plotter.axis,scale=1e-1,offset=-0.001)
hr_nocal.plotter(ymin=-0.001,ymax=0.015,xmin=6000,xmax=7200,axis=sn_nocal.plotter.axis,clear=False,color='r')
dis_lowscale = dis * 0.01/2.2
dis_lowscale.plotter(axis=sn_nocal.plotter.axis,clear=False,color='orange',ymax=0.015)


#ecbc = loadplot('SN2009ip_comb.rs.ec.dispcor.blueflat.cal.fits')
#ecsp = pyspeckit.Spectra(ec,xunits='angstroms')

# blueflatwithscat = loadplot('echelle_blueflat_combine.rs.ec.dispcor.fits', norm=True)
# blueflatec = loadplot('echelle_blueflat_combine.rs.scatsub.ec.dispcor.fits',axis=blueflatwithscat[30].plotter.axis, norm=True)
# flatwithscat = loadplot('echelle_redflat_combine.rs.ec.dispcor.fits', norm=True,axis=blueflatwithscat[30].plotter.axis)
# flatec = loadplot('echelle_redflat_combine.rs.scatsub.ec.dispcor.fits',axis=flatwithscat[30].plotter.axis, norm=True)
# flat = pyfits.getdata('echelle_redflat_combine.rs.scatsub.ec.dispcor.fits')
# flatnorm = flat / flat.max(axis=1)[:,np.newaxis]
# flatfits = pyfits.open('echelle_redflat_combine.rs.scatsub.ec.dispcor.fits')
# flatfits[0].data = flatnorm
# flatfits.writeto('flatnorm_weight.fits',clobber=True)

#flatspec = pyspeckit.wrappers.load_IRAF_multispec('flatnorm_weight.fits')

#HRraw = pyspeckit.wrappers.load_IRAF_multispec('HR7596_flat_combine.fits')
#HRsp = pyspeckit.Spectra(HR,xunits='angstroms')

sens = [pyspeckit.Spectrum('sens.%04i.fits' % ii) for ii in xrange(1,107)]
#senssp = pyspeckit.Spectra(sens,xunits='angstroms')

#bigxarr = np.arange(float(ec[-1].xarr.min()),float(ec[0].xarr.max()),ec[-1].xarr.cdelt())
#bigspec = pyspeckit.Spectrum(data=np.zeros(bigxarr.shape), xarr=bigxarr,
#        xarrkwargs={'units':'angstroms'})
#weights = bigspec.copy()

# for sp,sn in zip(eccr,sens):
#     #sp.data.mask = (sn.data < 20) + (sn.data > 35)
#     spint = pyspeckit.arithmetic.interp(sp,bigspec)
#     #flint = pyspeckit.arithmetic.interp(fl,bigspec)
#     #flint.data[flint.data<0.20] = 0
#     #bigspec += spint*flint
#     weights += flint
# 
# wspec = bigspec/weights
# wspec.data.mask = (wspec.data < 0) + (wspec.data > 2e-8)
# wspec.data[weights == 0] = 0

#bigspec.plotter(xmin=6300,xmax=6900)
#wspec.plotter(xmin=6500,xmax=6700,axis=bigspec.plotter.axis,clear=False,color='b')
#ecsp2 = pyspeckit.Spectra(ec,xunits='angstroms')

#sens[30].plotter()
#sens[31].plotter(axis=sens[30].plotter.axis,clear=False,color='blue')
#sens[29].plotter(axis=sens[30].plotter.axis,clear=False,color='red' )

# flatspec[30].plotter()
# flatspec[31].plotter(axis=flatspec[30].plotter.axis,clear=False,color='blue')
# flatspec[29].plotter(axis=flatspec[30].plotter.axis,clear=False,color='red' )

#nocal_norm = [n/n.data.max() for n in nocal]
#nocal_norm[30].plotter(color='green',clear=False)
#nocal_norm[31].plotter(axis=nocal_norm[30].plotter.axis,clear=False,color='blue')
#nocal_norm[29].plotter(axis=nocal_norm[30].plotter.axis,clear=False,color='red' )

##flatted = [(nc/fs)*(fs>0.2) for nc,fs in zip(nocal,flatspec)]
#for fl,fs in zip(flatted,flatspec):
#    fl.data.mask = fs.data < 0.2

#flatted[30].plotter()
#flatted[31].plotter(axis=flatted[30].plotter.axis,clear=False,color='blue')
#flatted[29].plotter(axis=flatted[30].plotter.axis,clear=False,color='red' )

#flattedHR = [(nc/fs)*(fs>0.2) for nc,fs in zip(HR,flatspec)]
#for fl,fs in zip(flattedHR,flatspec):
#    fl.data.mask = fs.data < 0.2

#flattedHR[30].plotter()
#flattedHR[31].plotter(axis=flattedHR[30].plotter.axis,clear=False,color='blue')
#flattedHR[29].plotter(axis=flattedHR[30].plotter.axis,clear=False,color='red' )



##for nc,fs,sn in zip(nocal,flatspec,sens):
#    spfl = (nc / fs) * (fs > 0.2)
#    pass
