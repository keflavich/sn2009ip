import pyspeckit
import pyspeckitmodels
import ref_index
import pylab
import numpy as np
from pyspeckit.spectrum.models.inherited_voigtfitter import voigt
from pyspeckit.spectrum.models import model
from DISfunctions import *

sp = sp4w = pyspeckit.Spectrum('UT120830_DIS.final.txt',skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
sp4w.specname="UT120830"
sp4w.xarr.units='angstroms'
sp4w.xarr.xtype='wavelength'
sp4w.units = 'erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
sp4w.plotter(xmin=5725,xmax=6025)
#sp4w.baseline(xmin=5725,xmax=5993,exclude=[5832,5931],subtract=False)
#sp4w.baseline.highlight_fitregion()
#sp4w.specfit(guesses=[0.3136687151432469, 5876.202442972989, 4.4120216889139092, 0.095548263897897501, 5896.9814771973188, 10.294717274131941], show_components=False)
#sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
#sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.39,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_5875AA.png")
#print " ".join(["%15s" % s for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
#print " ".join(["%15g" % s for s in sp.specfit.parinfo.values])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])

sp4w.plotter(xmin=4900,xmax=5150,ymin=0.01,ymax=0.08)
sp4w.baseline(xmin=4900,xmax=5200,exclude=[5008,5026],subtract=False,reset_selection=True)
sp4w.baseline.highlight_fitregion()
sp4w.specfit(guesses=[0.22937395770033309, 5018.4176853603767, 6.1407554649053635])
#sp4w.specfit.parinfo.tableprint()
#sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.03,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_5015AA.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])


sp4w.plotter(xmin=4600,xmax=5100,ymax=0.13,ymin=0.00)
sp4w.baseline(xmin=4700,xmax=5000,exclude=[4790,4920],subtract=False,reset_selection=True,order=2)
sp4w.baseline.highlight_fitregion()
#sp4w.specfit(guesses=[2.216496266988826, 4861.8069815195076,
#    4.5006123086073542, 0.1873849277344477, 2, 4862, 20, 5, 0.1, 4922, 5,
#    1],
#    fittype='voigt')
sp4w.specfit(guesses=[2.216496266988826, 4861.8069815195076, 4.5006123086073542,
                      2, 4862, 20, 
                      0.1, 4922, 5],
    fittype='gaussian')
#sp4w.specfit.parinfo.tableprint()
sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.02)
sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.02,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_hbeta.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp4hbeta = hbeta(sp4w)

sp4w.plotter(xmin=4200,xmax=4750,ymin=0.00)
#sp4w.baseline(xmin=4400,xmax=4600,exclude=[4460,4482],subtract=False,reset_selection=True)
#sp4w.specfit(guesses=[0.22937395770033309, 4471.4176853603767, 6.1407554649053635])
#sp4w.baseline.highlight_fitregion()
#sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.8,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_4471A.png")
#print " ".join(["%15s" % s for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
#print " ".join(["%15g" % s for s in sp.specfit.parinfo.values])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])

sp4w.plotter(xmin=4000,xmax=4700,ymin=-0.02)
sp4w.baseline(xmin=4120,xmax=4700,exclude=[4230,4396,4460,4482],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp4w.specfit(guesses=[1.0392979045557098, 4340.9883608224227, 2.7300612843256729,
                     0.26780350719313301, 4343.5025329855362, 15.104260071803573,
                     -0.14419907828636985, 4274.030329372441, 47.614614312455721])
#sp4w.specfit.parinfo.tableprint()
sp4w.baseline.highlight_fitregion()
sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.03)
sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.00,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_Hgamma.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp4hgamma = hgamma(sp4w)


sp4w.plotter(xmin=3600,xmax=4200)#,ymin=0.80,ymax=1.405)
#sp4w.baseline(xmin=3800,xmax=4080,exclude=[3869.37, 3842, 3878, 3827.96, 3984.59, 4013.4, 4045.81, 4081.81, 4117.82],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
#sp4w.specfit(guesses=[0.17678816359414271, 3836.2891489490876, 2.3292524690269341,
#        0.58790225628388193, 3889.6980403298326, 3.1921500773523186,
#        -0.14490959654871732, 3937.1710595457921, 16.194584370845611, 
#         0.34109668314543307, 3969.7732056762652, 3.207456982280704], show_components=True)
#sp4w.baseline.highlight_fitregion()
#sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
#sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.90,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_4300AA.png")
#print " ".join(["%15s" % s for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
#print " ".join(["%15g" % s for s in sp.specfit.parinfo.values])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])


sp4w.plotter(xmin=6800,xmax=7500)
#sp4w.baseline(xmin=6900,xmax=7500,exclude=[7000,7100],subtract=False,reset_selection=True,highlight_fitregion=True)
#sp4w.specfit(guesses=[0.15398474751230004, 7065.783123452833, 3.4814939453680830,
#                     0.057402044667803014, 7062.9233595429278, 25.94673682027123], show_components=True)
#sp4w.baseline.highlight_fitregion()
#sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.05)
#sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=0.20,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_7060AA.png")
#print " ".join(["%15s" % s for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
#print " ".join(["%15g" % s for s in sp.specfit.parinfo.values])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])

sp4w.plotter(xmin=6100,xmax=7000,ymax=0.27,ymin=-0.04)
sp4w.baseline(xmin=6100,xmax=7000,exclude=[6360,6746,6815,6884,7003,7126,7506,7674,8142,8231],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp4w.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314, 1,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,  1,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672,  1,],
                    fittype='voigt')
#sp4w.specfit.parinfo.tableprint()
sp4w.baseline.highlight_fitregion()
sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.02)
sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=-0.02,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_Halpha_voigt_zoom.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp4w.plotter.axis.set_xlim(6562-150,6562+150)
sp4w.plotter.savefig("SN2009ip_UT120830_Halpha_voigt_zoomzoom.png")

sp4w.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672])
#sp4w.specfit.parinfo.tableprint()
sp4w.baseline.highlight_fitregion()
sp4w.specfit.plot_components(add_baseline=True,component_yoffset=-0.02)
sp4w.specfit.plotresiduals(axis=sp4w.plotter.axis,clear=False,yoffset=-0.02,label=False)
sp4w.plotter.savefig("SN2009ip_UT120830_Halpha_zoom.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp4w.plotter.axis.set_xlim(6562-150,6562+150)
sp4w.plotter.savefig("SN2009ip_UT120830_Halpha_zoomzoom.png")
sp4w.plotter.axis.set_xlim(6000,8500)
sp4w.plotter.savefig("SN2009ip_UT120830_Halpha.png")
sp4halpha = halpha(sp4w)

sp4halpha.data -= sp4halpha.baseline.basespec
sp4halpha.baseline.subtracted=True
sp4hbeta.data -= sp4hbeta.baseline.basespec
sp4hbeta.baseline.subtracted=True
sp4hgamma.data -= sp4hgamma.baseline.basespec
sp4hgamma.baseline.subtracted=True

sp4halpha.plotter(xmin=-20000,xmax=20000,ymin=-0.02,ymax=0.25)
sp4hbeta.plotter(xmin=-20000,xmax=20000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='b')
sp4hgamma.plotter(xmin=-20000,xmax=20000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='r')
sp4halpha.plotter.axis.legend(sp4halpha.plotter.axis.lines,
        ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
        loc='upper left')

oldaxis4 = sp4halpha.plotter.axis
import mpl_toolkits.axes_grid.inset_locator
sp4halpha.plotter.axis = mpl_toolkits.axes_grid.inset_locator.inset_axes(sp4halpha.plotter.axis,
        width="40%", height="40%",loc=1)
sp4halpha.plotter(xmin=-3000,xmax=3000,ymin=-0.02,ymax=0.25)
sp4halpha.plotter.axis.set_title("")
sp4hbeta.plotter(xmin=-3000,xmax=3000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='b')
sp4hgamma.plotter(xmin=-3000,xmax=3000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='r')
sp4halpha.plotter.axis.set_title("")

sp4halpha.plotter.savefig('SN2009ip_UT120830_Habg_compare.png')

sp4hbetaM = sp4hbeta * pyspeckitmodels.hydrogen.r_to_hbeta['balmera'][1]
sp4hgammaM = sp4hgamma * pyspeckitmodels.hydrogen.r_to_hbeta['balmera'][1] / pyspeckitmodels.hydrogen.r_to_hbeta['balmerg'][1]

oldaxis4.clear()
sp4halpha.plotter.axis=oldaxis4
sp4halpha.plotter(xmin=-20000,xmax=20000,ymin=-0.02,ymax=0.25)
sp4hbetaM.plotter(xmin=-20000,xmax=20000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='b')
sp4hgammaM.plotter(xmin=-20000,xmax=20000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='r')
sp4halpha.plotter.axis.legend(sp4halpha.plotter.axis.lines,
        ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
        loc='upper left')

sp4halpha.plotter.axis = mpl_toolkits.axes_grid.inset_locator.inset_axes(sp4halpha.plotter.axis,
        width="40%", height="40%",loc=1)
sp4halpha.plotter(xmin=-3000,xmax=3000,ymin=-0.02,ymax=0.25)
sp4halpha.plotter.axis.set_title("")
sp4hbetaM.plotter(xmin=-3000,xmax=3000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='b')
sp4hgammaM.plotter(xmin=-3000,xmax=3000,ymin=-0.02,ymax=0.25,clear=False,axis=sp4halpha.plotter.axis,color='r')
sp4halpha.plotter.axis.set_title("")

sp4halpha.plotter.savefig('SN2009ip_UT120830_Habg_compare_scaled10000K.png')
