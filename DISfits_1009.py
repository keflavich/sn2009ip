import pyspeckit
import pyspeckitmodels
import ref_index
import pylab
import numpy as np
from pyspeckit.spectrum.models.inherited_voigtfitter import voigt
from pyspeckit.spectrum.models import model

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

sp2w = pyspeckit.Spectrum('UT121009_DIS.final.txt',skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
sp2w.specname="UT121009"
sp2w.units = 'erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
sp2w.xarr.units='angstroms'
sp2w.xarr.xtype='wavelength'
sp2w.plotter(xmin=5725,xmax=6025,ymax=0.71,ymin=0.35)
sp2w.baseline(xmin=5725,xmax=5993,exclude=[5832,5931],subtract=False)
sp2w.baseline.highlight_fitregion()
sp2w.specfit(guesses=[0.3136687151432469, 5876.202442972989, 4.4120216889139092, 0.095548263897897501, 5896.9814771973188, 10.294717274131941], show_components=False)
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.39,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_5875AA.png")

sp2w.plotter(xmin=4900,xmax=5150,ymin=0.60,ymax=0.85)
sp2w.baseline(xmin=4900,xmax=5200,exclude=[5008,5026],subtract=False,reset_selection=True)
sp2w.baseline.highlight_fitregion()
sp2w.specfit(guesses=[0.22937395770033309, 5018.4176853603767, 6.1407554649053635])
#sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.65,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_5015AA.png")


sp2w.plotter(xmin=4600,xmax=5100,ymax=2.1,ymin=0.5)
sp2w.baseline(xmin=4700,xmax=5000,exclude=[4790,4920],subtract=False,reset_selection=True,order=2)
sp2w.baseline.highlight_fitregion()
#sp2w.specfit(guesses=[2.216496266988826, 4861.8069815195076,
#    4.5006123086073542, 0.1873849277344477, 2, 4862, 20, 5, 0.1, 4922, 5,
#    1],
#    fittype='voigt')
sp2w.specfit(guesses=[2.216496266988826, 4861.8069815195076, 4.5006123086073542,
                      2, 4862, 20, 
                      0.1, 4922, 5],
    fittype='gaussian')
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.6,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_hbeta.png")
sp2hbeta = hbeta(sp2w)

sp2w.plotter(xmin=4400,xmax=4550,ymin=0.75)
sp2w.baseline(xmin=4400,xmax=4600,exclude=[4460,4482],subtract=False,reset_selection=True)
sp2w.specfit(guesses=[0.22937395770033309, 4471.4176853603767, 6.1407554649053635])
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.8,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_4471A.png")

sp2w.plotter(xmin=4000,xmax=4700,ymin=0.70)
sp2w.baseline(xmin=4120,xmax=4700,exclude=[4230,4396,4460,4482],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[1.0392979045557098, 4340.9883608224227, 2.7300612843256729,
                     0.26780350719313301, 4343.5025329855362, 15.104260071803573,
                     -0.14419907828636985, 4274.030329372441, 47.614614312455721])
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.75,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_Hgamma.png")
sp2hgamma = hgamma(sp2w)


sp2w.plotter(xmin=3600,xmax=4200,ymin=0.80,ymax=1.405)
sp2w.baseline(xmin=3800,xmax=4080,exclude=[3869.37, 3842, 3878, 3827.96, 3984.59, 4013.4, 4045.81, 4081.81, 4117.82],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[0.17678816359414271, 3836.2891489490876, 2.3292524690269341,
        0.58790225628388193, 3889.6980403298326, 3.1921500773523186,
        -0.14490959654871732, 3937.1710595457921, 16.194584370845611, 
         0.34109668314543307, 3969.7732056762652, 3.207456982280704])
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.90,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_4300AA.png")


sp2w.plotter(xmin=6800,xmax=7500,ymin=0.1,ymax=0.5)
sp2w.baseline(xmin=6900,xmax=7500,exclude=[7000,7100],subtract=False,reset_selection=True,highlight_fitregion=True)
sp2w.specfit(guesses=[0.15398474751230004, 7065.783123452833, 3.4814939453681009,
                     0.057402044667803014, 7062.9233595429278, 25.94673682027123])
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.05)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.20,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_7060AA.png")

sp2w.plotter(xmin=6100,xmax=7000,ymax=2.23,ymin=0)
sp2w.baseline(xmin=6100,xmax=7000,exclude=[6450,6746,6815,6884,7003,7126,7506,7674,8142,8231],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314, 1,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,  1,
                    0.11957267912208754, 6678.3853431367716, 4.1892742162283181,  1,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672,  1,],
                    fittype='voigt')
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.20,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_zoom.png")
sp2w.plotter.axis.set_xlim(6562-150,6562+150)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_zoomzoom.png")

sp2w.plotter(xmin=6100,xmax=7000,ymax=2.23,ymin=0)
sp2w.baseline(xmin=6100,xmax=7000,exclude=[6450,6746,6815,6884,7003,7126,7506,7674,8142,8231],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,
                    0.11957267912208754, 6678.3853431367716, 4.1892742162283181,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672])
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.20,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_zoom.png")
sp2w.plotter.axis.set_xlim(6562-150,6562+150)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_zoomzoom.png")
sp2w.plotter.axis.set_xlim(6000,8500)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha.png")
sp2halpha = halpha(sp2w)

sp2halpha.data -= sp2halpha.baseline.basespec
sp2halpha.baseline.subtracted=True
sp2hbeta.data -= sp2hbeta.baseline.basespec
sp2hbeta.baseline.subtracted=True
sp2hgamma.data -= sp2hgamma.baseline.basespec
sp2hgamma.baseline.subtracted=True

sp2halpha.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=2.0)
sp2hbeta.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=2.0,clear=False,axis=sp2halpha.plotter.axis,color='b')
sp2hgamma.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=2.0,clear=False,axis=sp2halpha.plotter.axis,color='r')
sp2halpha.plotter.axis.legend(sp2halpha.plotter.axis.lines,
        ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
        loc='upper left')

import mpl_toolkits.axes_grid.inset_locator
sp2halpha.plotter.axis = mpl_toolkits.axes_grid.inset_locator.inset_axes(sp2halpha.plotter.axis,
        width="40%", height="40%",loc=1)
sp2halpha.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=2.0)
sp2halpha.plotter.axis.set_title("")
sp2halpha.plotter.axis.set_title("")
sp2hbeta.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=2.0,clear=False,axis=sp2halpha.plotter.axis,color='b')
sp2hgamma.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=2.0,clear=False,axis=sp2halpha.plotter.axis,color='r')

sp2halpha.plotter.savefig('SN2009ip_UT121009_Habg_compare.png')
