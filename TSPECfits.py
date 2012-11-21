import pyspeckit
from DISfunctions import *

tsp1 = pyspeckit.Spectrum('UT120831_TSpec.final.txt',skiplines=1)
tsp1.specname="UT120831"
tsp1.xarr.units='angstroms'
tsp1.xarr.xtype='wavelength'
tsp1 = tsp1 * 10
tsp1.units = '$10^{-15}$ erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
tsp1.data.mask[tsp1.data>0.1] = 0
tsp1.data.mask[(tsp1.xarr > 11100)*(tsp1.xarr < 11300)] = True
tsp2 = pyspeckit.Spectrum('UT121002_TSpec.final.txt',skiplines=1)
tsp2.specname="UT121002"
tsp2.xarr.units='angstroms'
tsp2.xarr.xtype='wavelength'
tsp2.data.mask = tsp2.data<0
tsp2.units = '$10^{-14}$ erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
tsp2.data.mask[(tsp2.xarr > 11100)*(tsp2.xarr < 11300)] = True

for sp in [tsp1,tsp2]:
    print sp.specname
    sp.plotter(xmin=12400,xmax=13300)
    sp.baseline(xmin=12400,xmax=13300,exclude=[12770,12866],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(12821)]-0.05
    sp.plotter(xmin=12400,xmax=13300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    # single version sp.specfit(guesses=[0.2,12821,3])
    sp.specfit(guesses=[0.2,12821,6,0.05,12821.2,12])
    sp.specfit.plot_components(add_baseline=True,component_yoffset=-0.01)
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    # single version sp.plotter.savefig(sp.specname+"_TSPEC_PaB_fit.png")
    sp.plotter.savefig(sp.specname+"_TSPEC_PaB_multi_fit.png")
    print " ".join(["%15s" % x for x in ('Center Wavelength','Center Err','Peak','Integral','FWHM')])
    print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    print sp.specfit.integral()

    sp.plotter(xmin=12400,xmax=13300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,12821,3,2],fittype='voigt')
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_PaB_voigt_fit.png")
    print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    print sp.specfit.integral()

    sp.plotter(xmin=21360,xmax=21960)
    sp.baseline(xmin=21360,xmax=21960,exclude=[21630,21690],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(21661)]-0.02
    sp.plotter(xmin=21360,xmax=21960,ymin=yoffset-0.02)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,21661,3],fittype='gaussian')
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_BrG_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass

    wl = 20580
    sp.plotter(xmin=wl-300,xmax=wl+300)
    sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.02
    sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.02)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,wl,3])
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_HeI2.06_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass

    try:
        wl = 23037
        sp.plotter(xmin=wl-300,xmax=wl+300)
        sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
        yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.02
        sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.02)
        sp.baseline.highlight_fitregion()
        sp.specfit(guesses=[0.2,wl,3])
        sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
        sp.plotter.savefig(sp.specname+"_TSPEC_23038A_fit.png")
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        wl = 23047
        sp.plotter(xmin=wl-300,xmax=wl+300)
        sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
        yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.02
        sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.02)
        sp.baseline.highlight_fitregion()
        sp.specfit(guesses=[0.2,wl,3])
        sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
        sp.plotter.savefig(sp.specname+"_TSPEC_23038A_fit.png")
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])

    wl = 10830
    sp.plotter(xmin=wl-300,xmax=wl+300)
    sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30,10911,10971],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.05
    sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,wl,3])
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_He10830_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass

    wl = 10941
    sp.plotter(xmin=wl-300,xmax=wl+300)
    sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[10800,10860,wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.05
    sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,wl,3])
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_PaG_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass

    wl = 10052
    sp.plotter(xmin=wl-300,xmax=wl+300)
    sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.05
    sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,wl,3])
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_PaD_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass

    wl = 17006
    sp.plotter(xmin=wl-300,xmax=wl+300)
    sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.05
    sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,wl,3])
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_HeI17006_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass

    wl = 12158
    sp.plotter(xmin=wl-300,xmax=wl+300)
    sp.baseline(xmin=wl-300,xmax=wl+300,exclude=[wl-30,wl+30],powerlaw=True,subtract=False,reset_selection=True)
    yoffset = sp.baseline.basespec[sp.xarr.x_to_pix(wl)]-0.05
    sp.plotter(xmin=wl-300,xmax=wl+300,ymin=yoffset-0.05)
    sp.baseline.highlight_fitregion()
    sp.specfit(guesses=[0.2,wl,3])
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=yoffset,label=False)
    sp.plotter.savefig(sp.specname+"_TSPEC_12158_fit.png")
    try:
        print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, sp.specfit.parinfo.SHIFT0.error, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])
    except:
        pass



import pylab
pylab.show()
