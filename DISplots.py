import pyspeckit
import ref_index
import pyspeckitmodels
import mpl_toolkits
from pylab import *

def overlay():
    spectra = ['UT120830_DIS.final.txt','UT121002_DIS.final.txt','UT121009_DIS.final.txt']

    figure(1); clf();

    colors = ['b','k','r']

    rcParams['font.size']=18

    for ii,spname in enumerate(spectra):
        sp = pyspeckit.Spectrum(spname,skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
        sp.xarr.units='angstroms'
        sp.xarr.xtype='wavelength'
        sp.units = '10$^{-14}$ erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'
        sp.plotter(figure=figure(1),color=colors[ii],clear=False,ymin=-0.1,ymax=4)
        UTD = spname[:8]
        sp.plotter.axis.lines[-1].set_label(UTD)

    leg=legend(loc='best')
    for txt,ln in zip(leg.get_texts(),leg.get_lines()):
        txt.set_color(ln.get_color())
    savefig('SN2009ip_AllThree.png')
    savefig('SN2009ip_AllThree.eps')

overlay()

def makemyplots(errstyle=None,units=None,xRange=200):
    spectra = ['UT120830_DIS.final.txt','UT120830_DIS.final.txt','UT121002_DIS.final.txt','UT121009_DIS.final.txt']

    eng_to_grk = {'g':'gamma',
            'a':'alpha',
            'b':'beta',
            'd':'delta'}

    figure(0); clf();

    rcParams['font.size']=18

    nx = len(spectra)
    ny = len(eng_to_grk)

    for ii,spname in enumerate(spectra):
        sp = pyspeckit.Spectrum(spname,skiplines=1,xarrkwargs={'xtype':'wavelength','unit':'angstroms'})
        if ii == 1:
            sp.data *= 10
            sp.error *= 10

        sp.baseline(order=5,highlight_fitregion=False, 
                exclude=[a  for x in [4101,4340,4863,5879,6562.8,6850,7067,7575] 
                    for a in [x-50,x+50]])

        sp.specname=spname[:8]
        if ii==1: sp.specname+="$\\times$10"
        sp.xarr.units='angstroms'
        sp.xarr.xtype='wavelength'
        sp.units = '10$^{-14}$ erg s$^{-1}$ cm$^{-2}$ $\\AA^{-1}$'

        for jj,line in enumerate(['a','b','g','d']):
            name = 'balmer'+line
            wavelength = pyspeckitmodels.hydrogen.wavelength[name]
            airwave = ref_index.vac2air(wavelength*1e3)*10

            sp.xarr.refX = airwave
            sp.xarr.refX_units = 'angstroms'
            if units is not None:
                sp.xarr.convert_to_unit(units)

            ax = subplot(ny,nx,ii+jj*ny+1)
            sp.plotter.axis=ax
            if units is None:
                sp.plotter(axis=ax,xmin=airwave-xRange/2, xmax=airwave+xRange/2,
                        offset=0.1*(jj==0), ymin=-0.1, errstyle=errstyle)
            elif units == 'Mm/s':
                sp.plotter(axis=ax,xmin=-xRange/2, xmax=+xRange/2,
                        offset=0.1*(jj==0), ymin=-0.1, errstyle=errstyle)

            print name,"y limits: ",sp.plotter.ymin,sp.plotter.ymax

            ax.set_ylabel('')
            ax.set_xlabel('')
            ax.yaxis.set_major_locator(MaxNLocator(5))
            ax.yaxis.set_tick_params(labelsize=14)
            ax.xaxis.set_major_locator(MaxNLocator(5))
            ax.xaxis.set_tick_params(labelsize=14)
            if ii != 0:
                ax.set_yticklabels([])
            else:
                ax.set_ylabel('H$\\'+eng_to_grk[line]+"$")
            if jj == 0:
                pass
                #sp.plotter.axis.set_ylabel('H$\\'+eng_to_grk[line]+"$\\n"+sp.units)
            else:
                sp.plotter.axis.set_title("")
            #if ii != 2:
            #    sp.plotter.axis.set_xticklabels([])

            if units is not None:
                sp.xarr.convert_to_unit('angstroms')
            
    for ii,spname in enumerate(spectra):
        for jj,line in enumerate(['a','b','g','d']):
            ax = subplot(ny,nx,ii+jj*nx+1)
            yl = subplot(ny,nx,(nx-1)+jj*nx+1).get_ylim()
            ax.set_ylim(-0.1,yl[1])

    tight_layout(pad=2.2,h_pad=0.175,w_pad=0)
    #subplots_adjust(hspace=0.175,wspace=0)
    figtext(0.03,0.5,sp.units,rotation='vertical',va='center',ha='center')
    if units is None:
        figtext(0.5,0.03,"Wavelength ($\\AA$)")
    elif units == 'Mm/s':
        figtext(0.5,0.03,"Velocity (1000 km s$^{-1}$)")


    if errstyle is not None:
        if units is not None:
            savefig('SN2009ip_hlines_grid_errbar_velocity.png')
            savefig('SN2009ip_hlines_grid_errbar_velocity.eps')
        else:
            savefig('SN2009ip_hlines_grid_errbar.png')
            savefig('SN2009ip_hlines_grid_errbar.eps')
    elif units is not None:
        savefig('SN2009ip_hlines_grid_velocity.png')
        savefig('SN2009ip_hlines_grid_velocity.eps')
    else:
        savefig('SN2009ip_hlines_grid.png')
        savefig('SN2009ip_hlines_grid.eps')
    show()


makemyplots(errstyle='fill',units='Mm/s',xRange=20)
makemyplots(errstyle=None,units='Mm/s',xRange=20)
makemyplots(errstyle=None,units=None,xRange=200)
makemyplots(errstyle='fill',units=None,xRange=200)

from DISfunctions import *

plot_hydrogens('1002')
plot_hydrogens('0830',ymax=0.3, beta_off=-0.05,gamma_off=-0.1,ymin=-0.15)
plot_hydrogens('1009',ymax=3.5)
plot_dates('alpha',ymax=3.5,ymin=-0.3,rel_offs=-0.1)
plot_dates('beta',ymax=2.5,ymin=-0.3,rel_offs=-0.1)
plot_dates('gamma',ymax=1.5,ymin=-0.4,rel_offs=-0.125)
plot_dates('e5876',ymax=0.5,ymin=-0.2,rel_offs=-0.05)


def doitall(sp, xmin, xmax, exclude=None, border=2, guesses=None, fittype='gaussian'):
    sp.plotter(xmin=xmin,xmax=xmax)
    sp.baseline(xmin=xmin, xmax=xmax, exclude=exclude, subtract=False,
            reset_selection=True, highlight_fitregion=True, order=border)
    sp.specfit(guesses=[2.4007096541802202, 6563.2307968382256, 3.5653446153950314, 1,
                        0.53985149324131965, 6564.3460908526877, 19.443226155616617,  1,
                        0.11957267912208754, 6678.3853431367716, 4.1892742162283181,  1,
                        0.10506431180136294, 6589.9310414408683, 72.378997529374672,  1,],
                        fittype='voigt')
    #sp.specfit.parinfo.tableprint()
    sp.baseline.highlight_fitregion()
    sp.specfit.plot_components(add_baseline=True,component_yoffset=-0.1)
    sp.specfit.plotresiduals(axis=sp.plotter.axis,clear=False,yoffset=0.20,label=False)
    sp.plotter.savefig("SN2009ip_UT121002_Halpha_voigt_zoom.png")
    print " ".join(["%15s %15s" % (s,s+"err") for s in sp.specfit.parinfo.parnames])," ".join(["%15s" % ("EQW"+str(i)) for i,w in enumerate(sp.specfit.EQW(components=True))])
    print " ".join(["%15g %15g" % (par.value,par.error) for par in sp.specfit.parinfo])," ".join(["%15g" % w for w in sp.specfit.EQW(components=True)])
    sp.plotter.axis.set_xlim(6562-150,6562+150)



