import pyspeckit
import pyfits
import numpy as np

def loadplot(fn, axis=None, norm=False):
    tempthing = pyspeckit.wrappers.load_IRAF_multispec(fn)
    if axis is not None: 
        clear=False
    else: 
        clear=True
    if norm:
        plort = (tempthing[30]/tempthing[30].data.max())
        plort.plotter(axis=axis,clear=clear)
        tempthing[30].plotter.axis = plort.plotter.axis
        (tempthing[31]/tempthing[31].data.max()).plotter(axis=plort.plotter.axis,clear=False,color='blue')
        (tempthing[29]/tempthing[29].data.max()).plotter(axis=plort.plotter.axis,clear=False,color='red' )
    else:
        tempthing[30].plotter(axis=axis,clear=clear)
        tempthing[31].plotter(axis=tempthing[30].plotter.axis,clear=False,color='blue')
        tempthing[29].plotter(axis=tempthing[30].plotter.axis,clear=False,color='red' )
    return tempthing

def mergespec(fn):
    tempthing = pyspeckit.wrappers.load_IRAF_multispec(fn)
    for x in tempthing:
        x.crop(250,1150,units='pixels')
    return pyspeckit.Spectra(tempthing,xunits=x.xarr.units)
    

nocal = loadplot('SN2009ip.comb.rs.ec.dispcor.fits')
ec   = loadplot('SN2009ip.comb.rs.ec.dispcor.cal.fits')
ecrc = loadplot('SN2009ip.comb.rs.ec.dispcor.redflat.cal.fits')
ecbc = loadplot('SN2009ip.comb.rs.ec.dispcor.blueflat.cal.fits')
#ecsp = pyspeckit.Spectra(ec,xunits='angstroms')

blueflatwithscat = loadplot('echelle_blueflat_combine.rs.ec.dispcor.fits', norm=True)
blueflatec = loadplot('echelle_blueflat_combine.rs.scatsub.ec.dispcor.fits',axis=blueflatwithscat[30].plotter.axis, norm=True)
flatwithscat = loadplot('echelle_redflat_combine.rs.ec.dispcor.fits', norm=True,axis=blueflatwithscat[30].plotter.axis)
flatec = loadplot('echelle_redflat_combine.rs.scatsub.ec.dispcor.fits',axis=flatwithscat[30].plotter.axis, norm=True)
flat = pyfits.getdata('echelle_redflat_combine.rs.scatsub.ec.dispcor.fits')
flatnorm = flat / flat.max(axis=1)[:,np.newaxis]
flatfits = pyfits.open('echelle_redflat_combine.rs.scatsub.ec.dispcor.fits')
flatfits[0].data = flatnorm
flatfits.writeto('flatnorm_weight.fits',clobber=True)

flatspec = pyspeckit.wrappers.load_IRAF_multispec('flatnorm_weight.fits')

HR = pyspeckit.wrappers.load_IRAF_multispec('HR7596_flat_combine.fits')
#HRsp = pyspeckit.Spectra(HR,xunits='angstroms')

sens = [pyspeckit.Spectrum('sens.%04i.fits' % ii) for ii in xrange(1,107)]
#senssp = pyspeckit.Spectra(sens,xunits='angstroms')

bigxarr = np.arange(float(ec[-1].xarr.min()),float(ec[0].xarr.max()),ec[-1].xarr.cdelt())
bigspec = pyspeckit.Spectrum(data=np.zeros(bigxarr.shape), xarr=bigxarr,
        xarrkwargs={'units':'angstroms'})
weights = bigspec.copy()

for sp,fl,sn in zip(ecrc,flatspec,sens):
    #sp.data.mask = (sn.data < 20) + (sn.data > 35)
    spint = pyspeckit.arithmetic.interp(sp,bigspec)
    flint = pyspeckit.arithmetic.interp(fl,bigspec)
    flint.data[flint.data<0.20] = 0
    bigspec += spint*flint
    weights += flint

wspec = bigspec/weights
wspec.data.mask = (wspec.data < 0) + (wspec.data > 2e-8)
wspec.data[weights == 0] = 0

bigspec.plotter(xmin=6300,xmax=6900)
wspec.plotter(xmin=6500,xmax=6700,axis=bigspec.plotter.axis,clear=False,color='b')
#ecsp2 = pyspeckit.Spectra(ec,xunits='angstroms')

sens[30].plotter()
sens[31].plotter(axis=sens[30].plotter.axis,clear=False,color='blue')
sens[29].plotter(axis=sens[30].plotter.axis,clear=False,color='red' )

flatspec[30].plotter()
flatspec[31].plotter(axis=flatspec[30].plotter.axis,clear=False,color='blue')
flatspec[29].plotter(axis=flatspec[30].plotter.axis,clear=False,color='red' )

nocal_norm = [n/n.data.max() for n in nocal]
nocal_norm[30].plotter(axis=flatspec[30].plotter.axis,color='green',clear=False)
nocal_norm[31].plotter(axis=nocal_norm[30].plotter.axis,clear=False,color='blue')
nocal_norm[29].plotter(axis=nocal_norm[30].plotter.axis,clear=False,color='red' )

flatted = [(nc/fs)*(fs>0.2) for nc,fs in zip(nocal,flatspec)]
for fl,fs in zip(flatted,flatspec):
    fl.data.mask = fs.data < 0.2

flatted[30].plotter()
flatted[31].plotter(axis=flatted[30].plotter.axis,clear=False,color='blue')
flatted[29].plotter(axis=flatted[30].plotter.axis,clear=False,color='red' )

flattedHR = [(nc/fs)*(fs>0.2) for nc,fs in zip(HR,flatspec)]
for fl,fs in zip(flattedHR,flatspec):
    fl.data.mask = fs.data < 0.2

flattedHR[30].plotter()
flattedHR[31].plotter(axis=flattedHR[30].plotter.axis,clear=False,color='blue')
flattedHR[29].plotter(axis=flattedHR[30].plotter.axis,clear=False,color='red' )

hrcal = pyspeckit.Spectrum('/Volumes/disk5/usr/stsci/iraf/iraf/noao/lib/onedstds/spec16cal/hr7596.dat')


for nc,fs,sn in zip(nocal,flatspec,sens):
    spfl = (nc / fs) * (fs > 0.2)
    pass
