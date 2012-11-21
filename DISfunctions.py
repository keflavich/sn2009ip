import ref_index 
import pyspeckit
import pyspeckitmodels 
import pylab as pl

def halpha(sp):
    #return pyspeckitmodels.hydrogen.hydrogen.wavelength['balmera'] * 1e4
    HA = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmera']*1e3)
    return line(sp, 6562.7715) # NIST
    return line(sp, HA)

def he5876(sp):
    return line(sp, 5876.621  ) # NIST

def hbeta(sp):
    #return pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerb'] * 1e4
    HB = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerb']*1e3)
    return line(sp, 4861.128) # NIST
    return line(sp, HB)

def hgamma(sp):
    #return pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerg'] * 1e4
    HG = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerg']*1e3)
    return line(sp, 4340.471)
    return line(sp, HG)

def padelta(sp):
    #return pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerg'] * 1e4
    HG = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['paschend']*1e3)
    #return line(sp, 4340.471)
    return line(sp, HG)

def pagamma(sp):
    #return pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerg'] * 1e4
    HG = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['pascheng']*1e3)
    #return line(sp, 4340.471)
    return line(sp, HG)

def brgamma(sp):
    #return pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerg'] * 1e4
    HG = ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['brackettg']*1e3)
    #return line(sp, 4340.471)
    return line(sp, HG)

def line(sp, refX):
    sp = sp.copy()
    sp.xarr.units = 'angstroms'
    sp.xarr.refX = refX
    sp.xarr.refX_units = 'angstroms'
    sp.xarr.xtype='wavelength'
    sp.xarr.convert_to_unit('km/s')
    return sp


def fit_hdelta(sp, date, xmin=3900,xmax=4300,ymin=0.8,ymax=1.405,
        #exclude=[3601,3846,3869.37,3913,3956,3984.59,4013.4,4045.81,4081.81,4117.82,4230,4396,4460,4482],
        exclude=[3600,4035,4089,4114,4150,4600],
        guesses=[0.1,ref_index.vac2air(pyspeckitmodels.hydrogen.hydrogen.wavelength['balmerd']*1e3)*10,5,2],
        fittype='voigt'):

    sp.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    sp.baseline(xmin=xmin, xmax=xmax, exclude=exclude, subtract=False,
        reset_selection=True, highlight_fitregion=True, order=1)
    sp.specfit(guesses=guesses,
            fittype=fittype)
    sp.specfit.xmin, sp.specfit.xmax = sp.specfit.get_model_xlimits()
    sp.specfit.parinfo.tableprint()
    sp.baseline.highlight_fitregion()
    sp.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=ymin+0.1,label=False)
    sp.plotter.savefig("SN2009ip_UT"+str(date)+"_hdelta.png")
    print " ".join(["%15s" % x for x in ('Center Wavelength','Peak','Integral','FWHM')])
    print " ".join(["%15g" % x for x in (sp.specfit.parinfo.SHIFT0.value, (sp.data-sp.baseline.basespec)[sp.specfit.get_full_model(add_baseline=False) > sp.error].max(),sp.specfit.integral(direct=True),sp.specfit.measure_approximate_fwhm(plot=True,interpolate_factor=100)) ])


import mpl_toolkits.axes_grid.inset_locator

def plot_hydrogens(date, xmin=-20, xmax=25, ymin=-0.75, ymax=2.0,
        beta_off=-0.25, gamma_off=-0.5):

    pl.rcParams['font.size']=18

    sphalpha = pyspeckit.Spectrum('UT12%s_Halpha.fits' % date)
    sphbeta = pyspeckit.Spectrum('UT12%s_Hbeta.fits' % date)
    sphgamma = pyspeckit.Spectrum('UT12%s_Hgamma.fits' % date)
    for sp in [sphalpha,sphbeta,sphgamma]:
        sp.units = '$10^{-14}$ erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
        sp.xarr.convert_to_unit("Mm/s")
    pl.clf()
    axis1 = pl.gca()

    sphalpha.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,axis=axis1)
    sphbeta.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,clear=False,axis=sphalpha.plotter.axis,color='b',offset=beta_off)
    sphgamma.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,clear=False,axis=sphalpha.plotter.axis,color='r',offset=gamma_off)
    sphalpha.plotter.axis.legend(sphalpha.plotter.axis.lines,
            ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
            loc='upper left')
    axis1.set_ylim(ymin,ymax)
    axis1.set_xlabel("Velocity (1000 km s$^{-1}$)")

    axis2 = mpl_toolkits.axes_grid.inset_locator.inset_axes(sphalpha.plotter.axis,
            width="40%", height="40%",loc=1)
    sphalpha.plotter(xmin=-3,xmax=3,ymin=ymin,ymax=ymax,axis=axis2)
    sphalpha.plotter.axis.set_title("")
    sphbeta.plotter(xmin=-3,xmax=3,ymin=ymin,ymax=ymax,clear=False,axis=axis2,color='b',offset=beta_off)
    sphgamma.plotter(xmin=-3,xmax=3,ymin=ymin,ymax=ymax,clear=False,axis=axis2,color='r',offset=gamma_off)
    sphalpha.plotter.axis.set_title("")

    axis2.set_ylim(ymin,ymax)
    axis2.set_xlabel("Velocity (1000 km s$^{-1}$)")

    pl.draw()
    sphalpha.plotter.savefig('SN2009ip_UT12%s_Habg_compare.png' % (date))

    # sphbetaM = sphbeta * pyspeckitmodels.hydrogen.r_to_hbeta['balmera'][1]
    # sphgammaM = sphgamma * pyspeckitmodels.hydrogen.r_to_hbeta['balmera'][1] / pyspeckitmodels.hydrogen.r_to_hbeta['balmerg'][1]

    # oldaxis3.clear()
    # sphalpha.plotter.axis=oldaxis3
    # sphalpha.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=4.0)
    # sphbetaM.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=4.0,clear=False,axis=sphalpha.plotter.axis,color='b')
    # sphgammaM.plotter(xmin=-20000,xmax=20000,ymin=-0.2,ymax=4.0,clear=False,axis=sphalpha.plotter.axis,color='r')
    # sphalpha.plotter.axis.legend(sphalpha.plotter.axis.lines,
    #         ['H$\\alpha$','H$\\beta$','H$\\gamma$'], 
    #         loc='upper left')

    # sphalpha.plotter.axis = mpl_toolkits.axes_grid.inset_locator.inset_axes(sphalpha.plotter.axis,
    #         width="40%", height="40%",loc=1)
    # sphalpha.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=4.0)
    # sphalpha.plotter.axis.set_title("")
    # sphbetaM.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=4.0,clear=False,axis=sphalpha.plotter.axis,color='b')
    # sphgammaM.plotter(xmin=-3000,xmax=3000,ymin=-0.2,ymax=4.0,clear=False,axis=sphalpha.plotter.axis,color='r')
    # sphalpha.plotter.axis.set_title("")


    # sphalpha.plotter.savefig('SN2009ip_UT121002_Habg_compare_scaled10000K.png')
    
def plot_dates(line, xmin=-20, xmax=25, ymin=-0.75, ymax=2.0,
        rel_offs=-0.1):

    pl.rcParams['font.size']=18

    sp0830 = pyspeckit.Spectrum('UT120830_H%s.fits' % line)*5
    sp1002 = pyspeckit.Spectrum('UT121002_H%s.fits' % line)
    sp1009 = pyspeckit.Spectrum('UT121009_H%s.fits' % line)
    for sp in [sp0830,sp1002,sp1009]:
        sp.units = '$10^{-14}$ erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
        sp.xarr.convert_to_unit("Mm/s")
        sp.baseline(xmin=-20,xmax=20,exclude=[-5,5])
    pl.clf()
    axis1 = pl.gca()

    sp1002.specfit(xmin=xmin,xmax=xmax,guesses=[1,0,1])
    sp1009.specfit(xmin=xmin,xmax=xmax,guesses=[1,0,1])
    sp0830.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,axis=axis1,offset=rel_offs*2,color='b')
    sp1002.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,clear=False,axis=sp0830.plotter.axis,color='k',offset=rel_offs*1)
    sp1009.plotter(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,clear=False,axis=sp0830.plotter.axis,color='r',offset=rel_offs*0)
    #sp1009.specfit.measure_approximate_fwhm(plot=True,color='r',linestyle='dotted')
    #sp1002.specfit.measure_approximate_fwhm(plot=True,color='k',linestyle='dotted')
    leg = sp0830.plotter.axis.legend(sp0830.plotter.axis.lines,
            ['UT120830 $\\times5$','UT121002','UT121009'], 
            loc='upper left')
    for txt,ln in zip(leg.get_texts(),leg.get_lines()):
        txt.set_color(ln.get_color())
    
    axis1.set_ylim(ymin,ymax)
    axis1.set_xlabel("Velocity (1000 km s$^{-1}$)")
    if line == 'e5876':
        axis1.set_title("He 5876 $\\AA$")
    else:
        axis1.set_title("H$\\%s$" % line)
    axis1.set_ylabel(axis1.get_ylabel()+" + const")

    axis2 = mpl_toolkits.axes_grid.inset_locator.inset_axes(sp0830.plotter.axis,
            width="40%", height="40%",loc=1)
    sp0830.plotter(xmin=-3,xmax=3,ymin=ymin,ymax=ymax,axis=axis2,offset=rel_offs*2, color='b')
    sp0830.plotter.axis.set_title("")
    sp1002.plotter(xmin=-3,xmax=3,ymin=ymin,ymax=ymax,clear=False,axis=axis2,color='k',offset=rel_offs*1)
    sp1009.plotter(xmin=-3,xmax=3,ymin=ymin,ymax=ymax,clear=False,axis=axis2,color='r',offset=rel_offs*0)
    sp1009.specfit.measure_approximate_fwhm(plot=True,color='r',linestyle='dotted')
    sp1002.specfit.measure_approximate_fwhm(plot=True,color='k',linestyle='dotted')
    sp0830.plotter.axis.set_title("")

    axis2.set_ylim(ymin,ymax)
    axis2.set_xlabel("") #"Velocity (1000 km s$^{-1}$)")
    axis2.set_ylabel("") #axis2.get_ylabel()+" + const")

    pl.draw()
    sp0830.plotter.savefig('SN2009ip_H%s_date_compare.png' % (line))
    sp0830.plotter.savefig('SN2009ip_H%s_date_compare.eps' % (line))

    return axis1,axis2,sp0830,sp1002,sp1009
