import pyspeckit
import pyspeckitmodels
import ref_index
import pylab
import numpy as np
from pyspeckit.spectrum.models.inherited_voigtfitter import voigt
from pyspeckit.spectrum.models import model
from DISfunctions import *

sp = sp2w = pyspeckit.Spectrum('UT121009_DIS.final.txt',skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
sp2w.specname="UT121009"
sp2w.units = 'erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
sp2w.xarr.units='angstroms'
sp2w.xarr.xtype='wavelength'
sp2w.plotter(xmin=5625,xmax=6125,ymax=1.2,ymin=0.7)
sp2w.baseline(xmin=5725,xmax=5993,exclude=[5832,5931],subtract=False,reset_selection=True)
sp2w.baseline.highlight_fitregion()
sp2w.specfit(guesses=[0.3136687151432469, 5876.202442972989, 4.4120216889139092, 0.095548263897897501, 5896.9814771973188, 10.294717274131941], show_components=False)
#sp2w.specfit.parinfo.tableprint()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.8,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_5875AA.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])

sp2w.plotter(xmin=4900,xmax=5150,ymin=1.10,ymax=1.65)
sp2w.baseline(xmin=4900,xmax=5200,exclude=[5008,5026],subtract=False,reset_selection=True)
sp2w.baseline.highlight_fitregion()
sp2w.specfit(guesses=[0.22937395770033309, 5018.4176853603767, 6.1407554649053635])
#sp2w.specfit.parinfo.tableprint()
#sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=1.2,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_5015AA.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])


sp2w.plotter(xmin=4600,xmax=5100,ymax=3.75,ymin=1.0)
sp2w.baseline(xmin=4700,xmax=5000,exclude=[4800,4940],subtract=False,reset_selection=True,order=2)
sp2w.baseline.highlight_fitregion()
#sp2w.specfit(guesses=[2.216496266988826, 4861.8069815195076,
#    4.5006123086073542, 0.1873849277344477, 2, 4862, 20, 5, 0.1, 4922, 5,
#    1],
#    fittype='voigt')
sp2w.specfit(guesses=[2.216496266988826, 4861.8069815195076, 4.5006123086073542,
                      2, 4862, 20, 
                      0.1, 4922, 5],
    fittype='gaussian')
#sp2w.specfit.parinfo.tableprint()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=1.1,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_hbeta.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp2hbeta = hbeta(sp2w)

just_hbeta = sp.copy()
just_hbeta.data -= sp.specfit.modelcomponents[2,:]
just_hbeta.plotter(xmin=4600,xmax=5100,ymax=2.50,ymin=-0.3)
just_hbeta.baseline(xmin=4700,xmax=5000,exclude=[4800,4940],subtract=True,reset_selection=True,highlight_fitregion=True,order=2)
just_hbeta.specfit(guesses=[2.216496266988826, 4861.8069815195076, 4.5006123086073542, 1,
                      2, 4862, 20, 1,
                      0.1, 4922, 5, 1],
                    fittype='voigt')
just_hbeta.baseline.highlight_fitregion()
just_hbeta.specfit.plot_components(add_baseline=False,component_yoffset=-0.1)
just_hbeta.specfit.plotresiduals(axis=just_hbeta.plotter.axis,clear=False,yoffset=-0.20,label=False)
just_hbeta.specfit.annotate(chi2='optimal')
just_hbeta.plotter.savefig("SN2009ip_UT121009_hbeta_voigt_threecomp.png")
just_hbeta.specfit.fitleg.set_visible(False)
pylab.plot([4600,5100],[-0.2,-0.2],'y--')
pylab.gca().set_ylim(-0.3,0.3)
pylab.draw()
just_hbeta.plotter.savefig("SN2009ip_UT121009_hbeta_voigt_threecomp_zoom.png")

just_hbeta.plotter(xmin=4600,xmax=5100,ymax=2.50,ymin=-0.3)
just_hbeta.specfit(guesses=[2.216496266988826, 4861.8069815195076, 4.5006123086073542, 1,
                      2, 4862, 20, 1],
                    fittype='voigt')
just_hbeta.baseline.highlight_fitregion()
just_hbeta.specfit.plot_components(add_baseline=False,component_yoffset=-0.1)
just_hbeta.specfit.plotresiduals(axis=just_hbeta.plotter.axis,clear=False,yoffset=-0.20,label=False)
just_hbeta.specfit.annotate(chi2='optimal')
just_hbeta.plotter.savefig("SN2009ip_UT121009_hbeta_voigt_twocomp.png")
just_hbeta.specfit.fitleg.set_visible(False)
pylab.plot([4600,5100],[-0.2,-0.2],'y--')
pylab.gca().set_ylim(-0.3,0.3)
pylab.draw()
just_hbeta.plotter.savefig("SN2009ip_UT121009_hbeta_voigt_twocomp_zoom.png")


sp2w.plotter(xmin=4400,xmax=4550,ymin=1.5)
sp2w.baseline(xmin=4400,xmax=4600,exclude=[4460,4482],subtract=False,reset_selection=True)
sp2w.specfit(guesses=[0.22937395770033309, 4471.4176853603767, 6.1407554649053635])
#sp2w.specfit.parinfo.tableprint()
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=1.6,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_4471A.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])

sp2w.plotter(xmin=4000,xmax=4700,ymin=1.25,ymax=3.25)
sp2w.baseline(xmin=4120,xmax=4700,exclude=[4230,4396,4460,4482],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[1.0392979045557098, 4340.9883608224227, 2.7300612843256729,
                     0.26780350719313301, 4343.5025329855362, 15.104260071803573,
                     -0.14419907828636985, 4274.030329372441, 47.614614312455721])
#sp2w.specfit.parinfo.tableprint()
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=1.50,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_Hgamma.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp2hgamma = hgamma(sp2w)


sp2w.plotter(xmin=3600,xmax=4200,ymin=0.80,ymax=1.405)
sp2w.baseline(xmin=3800,xmax=4080,exclude=[3869.37, 3842, 3878, 3827.96, 3984.59, 4013.4, 4045.81, 4081.81, 4117.82],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[0.17678816359414271, 3836.2891489490876, 2.3292524690269341,
        0.58790225628388193, 3889.6980403298326, 3.1921500773523186,
        -0.14490959654871732, 3937.1710595457921, 16.194584370845611, 
         0.34109668314543307, 3969.7732056762652, 3.207456982280704])
#sp2w.specfit.parinfo.tableprint()
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.90,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_4300AA.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])


sp2w.plotter(xmin=6800,xmax=7500,ymin=0.4,ymax=0.8)
sp2w.baseline(xmin=6900,xmax=7500,exclude=[7000,7100],subtract=False,reset_selection=True,highlight_fitregion=True)
sp2w.specfit(guesses=[0.15398474751230004, 7065.783123452833, 3.4814939453681009,
                     0.057402044667803014, 7062.9233595429278, 25.94673682027123])
#sp2w.specfit.parinfo.tableprint()
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.05)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.45,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_7060AA.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])

sp2w.plotter(xmin=6100,xmax=7000,ymax=4.00,ymin=0)
sp2w.baseline(xmin=6100,xmax=7000,exclude=[6450,6746,6815,6884,7003,7126,7506,7674,8142,8231],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314, 1,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,  1,
                    0.11957267912208754, 6678.3853431367716, 4.1892742162283181,  1,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672,  1,],
                    fittype='voigt')
#sp2w.specfit.parinfo.tableprint()
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.20,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_zoom.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
sp2w.plotter.axis.set_xlim(6562-150,6562+150)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_zoomzoom.png")

just_halpha = sp2w.copy()
just_halpha.data -= sp2w.specfit.modelcomponents[2,:]
just_halpha.plotter(xmin=6100,xmax=7000,ymax=4.00,ymin=0)
just_halpha.baseline(xmin=6100,xmax=7000,exclude=[6450,6746,6815,6884,7003,7126,7506,7674,8142,8231],subtract=True,reset_selection=True,highlight_fitregion=True,order=2)
just_halpha.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314, 1,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,  1,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672,  1,],
                    fittype='voigt')
just_halpha.baseline.highlight_fitregion()
just_halpha.specfit.plot_components(add_baseline=False,component_yoffset=-0.1)
just_halpha.specfit.plotresiduals(axis=just_halpha.plotter.axis,clear=False,yoffset=-0.20,label=False)
just_halpha.specfit.annotate(chi2='optimal')
pylab.gca().set_ylim(-0.3,3.2)
just_halpha.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_threecomp.png")
just_halpha.specfit.fitleg.set_visible(False)
pylab.plot([6100,7000],[-0.2,-0.2],'y--')
pylab.gca().set_ylim(-0.3,0.3)
pylab.draw()
just_halpha.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_threecomp_zoom.png")

just_halpha.plotter(xmin=6100,xmax=7000,ymax=4.00,ymin=0)
just_halpha.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314, 1,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,  1],
                    fittype='voigt')
just_halpha.baseline.highlight_fitregion()
just_halpha.specfit.plot_components(add_baseline=False,component_yoffset=-0.1)
just_halpha.specfit.plotresiduals(axis=just_halpha.plotter.axis,clear=False,yoffset=-0.20,label=False)
just_halpha.specfit.annotate(chi2='optimal')
pylab.gca().set_ylim(-0.3,3.2)
just_halpha.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_twocomp.png")
just_halpha.specfit.fitleg.set_visible(False)
pylab.plot([6100,7000],[-0.2,-0.2],'y--')
pylab.gca().set_ylim(-0.3,0.3)
pylab.draw()
just_halpha.plotter.savefig("SN2009ip_UT121009_Halpha_voigt_twocomp_zoom.png")

sp2w.plotter(xmin=6100,xmax=7000,ymax=4.00,ymin=0)
sp2w.baseline(xmin=6100,xmax=7000,exclude=[6450,6746,6815,6884,7003,7126,7506,7674,8142,8231],subtract=False,reset_selection=True,highlight_fitregion=True,order=2)
sp2w.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314,
                    0.53985149324131965, 6564.3460908526877, 19.443226155616617,
                    0.11957267912208754, 6678.3853431367716, 4.1892742162283181,
                    0.10506431180136294, 6589.9310414408683, 72.378997529374672])
#sp2w.specfit.parinfo.tableprint()
sp2w.baseline.highlight_fitregion()
sp2w.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
sp2w.specfit.plotresiduals(axis=sp2w.plotter.axis,clear=False,yoffset=0.20,label=False)
sp2w.plotter.savefig("SN2009ip_UT121009_Halpha_zoom.png")
print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
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

sp2halpha.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=3.5)
sp2hbeta.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=3.5,clear=False,axis=sp2halpha.plotter.axis,color='b')
sp2hgamma.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=3.5,clear=False,axis=sp2halpha.plotter.axis,color='r')
sp2halpha.plotter.axis.legend(sp2halpha.plotter.axis.lines,
        ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
        loc='upper left')

oldaxis2 = sp2halpha.plotter.axis
import mpl_toolkits.axes_grid.inset_locator
sp2halpha.plotter.axis = mpl_toolkits.axes_grid.inset_locator.inset_axes(sp2halpha.plotter.axis,
        width="40%", height="40%",loc=1)
sp2halpha.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=3.5)
sp2halpha.plotter.axis.set_title("")
sp2hbeta.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=3.5,clear=False,axis=sp2halpha.plotter.axis,color='b')
sp2hgamma.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=3.5,clear=False,axis=sp2halpha.plotter.axis,color='r')
sp2halpha.plotter.axis.set_title("")

sp2halpha.plotter.savefig('SN2009ip_UT121009_Habg_compare.png')

sp2hbetaM = sp2hbeta * pyspeckitmodels.hydrogen.r_to_hbeta['balmera'][1]
sp2hgammaM = sp2hgamma * pyspeckitmodels.hydrogen.r_to_hbeta['balmera'][1] / pyspeckitmodels.hydrogen.r_to_hbeta['balmerg'][1]

oldaxis2.clear()
sp2halpha.plotter.axis=oldaxis2
sp2halpha.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=8.0)
sp2hbetaM.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=8.0,clear=False,axis=sp2halpha.plotter.axis,color='b')
sp2hgammaM.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=8.0,clear=False,axis=sp2halpha.plotter.axis,color='r')
sp2halpha.plotter.axis.legend(sp2halpha.plotter.axis.lines,
        ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
        loc='upper left')

sp2halpha.plotter.axis = mpl_toolkits.axes_grid.inset_locator.inset_axes(sp2halpha.plotter.axis,
        width="40%", height="40%",loc=1)
sp2halpha.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=8.0)
sp2halpha.plotter.axis.set_title("")
sp2hbetaM.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=8.0,clear=False,axis=sp2halpha.plotter.axis,color='b')
sp2hgammaM.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=8.0,clear=False,axis=sp2halpha.plotter.axis,color='r')
sp2halpha.plotter.axis.set_title("")

sp2halpha.plotter.savefig('SN2009ip_UT121009_Habg_compare_scaled10000K.png')
