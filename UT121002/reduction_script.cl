noao
imred
ccdred
echelle
proto
set imclobber=yes

#    ccdproc blueflat*.fits ccdtype="" zerocor=no darkcor=no flatcor=no fixfile="echmask.pl" biassec="[2100:2128,2:2027]" trimsec="[21:2048,1:2048]" order=3 niterate=3 int- 
#    imcombine blueflat*fits echelle_blueflat_combine.fits combine=median
#    ccdproc redflat*.fits ccdtype="" zerocor=no darkcor=no flatcor=no fixfile="echmask.pl" biassec="[2100:2128,2:2027]" trimsec="[21:2048,1:2048]" order=3 niterate=3 int- 
#    imcombine redflat*fits echelle_redflat_combine.fits combine=median
#    
#    # imarith blueflat.0033.fits / 200 blueflatBLUEdiv200.fits
#    # imarith blueflatBLUEdiv200.fits + eQUARTZ_OPEN.0030.fits blueflatSUM.fits
#    # hedit blueflatSUM.fits FILTER "Blue+Open" and the header updated
#    
#    # INTERACTIVE!
#    apscat1 order=35 low_rej=6. high_rej=1.5
#    apscat2 order=7 niter=2 high_rej=5
#    
#    hedit echelle_blueflat_combine.fits DISPAXIS 1 add+ verify-
#    magnify echelle_blueflat_combine.fits echelle_blueflat_combine.rs.fits xmag=1 ymag=4 
#    apall echelle_blueflat_combine.rs.fits references=JBrefspec interactive- find- recenter+ resize- edit+ trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
#    apscatter echelle_blueflat_combine.rs.fits echelle_blueflat_combine.rs.scatsub.fits scatter=scatter_blueflat find- recenter- resize- edit- trace- fittrace- nsum=-10 inter+ references=echelle_blueflat_combine.rs smooth+
#    apall echelle_blueflat_combine.rs.scatsub.fits references=JBrefspec interactive- find- recenter+ resize- edit+ trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
#    refspectra echelle_blueflat_combine.rs.scatsub.ec.fits answer="yes" references="JBtharspec.ec" sort="" group=""
#    dispcor echelle_blueflat_combine.rs.scatsub.ec echelle_blueflat_combine.rs.scatsub.ec.dispcor
#    
#    hedit echelle_redflat_combine.fits DISPAXIS 1 add+ verify-
#    magnify echelle_redflat_combine.fits echelle_redflat_combine.rs.fits xmag=1 ymag=4 
#    apall echelle_redflat_combine.rs.fits references=JBrefspec interactive- find- recenter+ resize- edit+ trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
#    apscatter echelle_redflat_combine.rs.fits echelle_redflat_combine.rs.scatsub.fits scatter=scatter_redflat find- recenter- resize- edit- trace- fittrace- nsum=-10 inter+ references=echelle_redflat_combine.rs smooth+
#    apall echelle_redflat_combine.rs.scatsub.fits references=JBrefspec interactive- find- recenter+ resize- edit+ trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
#    refspectra echelle_redflat_combine.rs.scatsub.ec.fits answer="yes" references="JBtharspec.ec" sort="" group=""
#    dispcor echelle_redflat_combine.rs.scatsub.ec echelle_redflat_combine.rs.scatsub.ec.dispcor
#    
#    imarith echelle_redflat_combine.rs.scatsub.fits + echelle_blueflat_combine.rs.scatsub.fits echelle_flat_scatsub.fits
#    apnormalize echelle_flat_scatsub.fits echelle_flat_scatsub_norm.fits references=JBrefspec find- recenter- resize- edit- trace- fittrace- nsum=-10 inter+
#    
#    ccdproc SN2009ip.0160.fits ccdtype="" zerocor=no darkcor=no flatcor=no fixfile="echmask.pl" biassec="[2100:2128,2:2027]" trimsec="[21:2048,1:2048]" order=3 niterate=3 int-
#    ccdproc SN2009ip.0161.fits ccdtype="" zerocor=no darkcor=no flatcor=no fixfile="echmask.pl" biassec="[2100:2128,2:2027]" trimsec="[21:2048,1:2048]" order=3 niterate=3 int-
#    ccdproc SN2009ip.0162.fits ccdtype="" zerocor=no darkcor=no flatcor=no fixfile="echmask.pl" biassec="[2100:2128,2:2027]" trimsec="[21:2048,1:2048]" order=3 niterate=3 int-
#    imcombine SN2009ip.0160.fits,SN2009ip.0161.fits,SN2009ip.0162.fits SN2009ip.comb.fits combine=median
#    imcombine HR7596.0163,HR7596.0164 HR7596_comb.fits combine=median
#    
#    #imcopy echelle_flat_scatsub echelle_flat_scatsub_nolow
#    #imreplace echelle_flat_scatsub_nolow 100000000 lower=INDEF upper=1
#    #!python -c "import astropy.io.fits as pyfits; f=pyfits.open('echelle_flat_scatsub_nolow.fits'); f[0].data[:,:73]=1e8; f[0].data[:,1964:]=1e8; f.writeto('echelle_flat_scatsub_nolow.fits',clobber=True)"
#    
#    !python -c "import astropy.io.fits as pyfits; f=pyfits.open('echelle_flat_scatsub.fits'); f[0].data[:,:200]=1e8; f[0].data[:,1800:]=1e8; f.writeto('echelle_flat_scatsub_nolow.fits',clobber=True)"
#    apall echelle_flat_scatsub_nolow references=JBrefspec interactive- find- recenter+ resize- edit+ trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
#    
#    
#    task doall=doall.cl
#    doall HR7596_comb
#    doall SN2009ip_comb
#    
magnify HR7596_comb HR7596_comb.rs xmag=1 ymag=4 
hedit HR7596_comb.rs "DISPAXIS" 1 add=yes verify=no  
apall HR7596_comb.rs  references="echelle_flat_scatsub_nolow"  interactive-  find-  recenter+  resize+  edit-  trace-  fittrace-  extract+  extras-  lower=-2  upper=2  b_sample="-6:-3 3:6"  b_naverage=1  width=12  radius=15  shift-  ylevel=.05  t_order=5  t_sample="200:1850 *"  t_naverage=3  t_niterate=3 
imarith HR7596_comb.rs.ec / echelle_flat_scatsub_nolow.ec HR7596_comb.rs.ec.flat
refspectra HR7596_comb.rs.ec.flat  answer="yes"  references="JBtharspec.ec"  sort=""  group=""
dispcor HR7596_comb.rs.ec.flat   HR7596_comb.rs.ec.dispcor
!rm HR7596_comb.rs.ec.dispcor.crop.fits	
scopy HR7596_comb.rs.ec.dispcor[250:1750,*] HR7596_comb.rs.ec.dispcor.crop

magnify SN2009ip.comb SN2009ip_comb.rs xmag=1 ymag=4 
hedit SN2009ip_comb.rs "DISPAXIS" 1 add=yes verify=no  
apall SN2009ip_comb.rs  references="echelle_flat_scatsub_nolow"  interactive-  find-  recenter+  resize+  edit-  trace-  fittrace-  extract+  extras-  lower=-2  upper=2  b_sample="-6:-3 3:6"  b_naverage=1  width=12  radius=15  shift-  ylevel=.05  t_order=5  t_sample="200:1850 *"  t_naverage=3  t_niterate=3 
imarith SN2009ip_comb.rs.ec / echelle_flat_scatsub_nolow.ec SN2009ip_comb.rs.ec.flat
refspectra SN2009ip_comb.rs.ec.flat  answer="yes"  references="JBtharspec.ec"  sort=""  group=""
dispcor SN2009ip_comb.rs.ec.flat   SN2009ip_comb.rs.ec.dispcor
!rm SN2009ip_comb.rs.ec.dispcor.crop.fits
scopy SN2009ip_comb.rs.ec.dispcor[250:1750,*] SN2009ip_comb.rs.ec.dispcor.crop

!rm std
standard HR7596_comb.rs.ec.dispcor.crop.fits caldir=./ star_name=hr7596 output=std answer="NO!" bandwidth=2 bandsep=2
!rm sens.*fits
sensfunc standards="std" sensitivity="sens" answer="NO" order=20 func="spline3"
imreplace sens*fits 10 lower=INDEF upper=10 
imreplace sens*fits 35 lower=35 upper=INDEF
!rm SN2009ip_comb.rs.ec.dispcor.crop.cal.fits
calibrate SN2009ip_comb.rs.ec.dispcor.crop SN2009ip_comb.rs.ec.dispcor.crop.cal 

#imarith HR7596_comb.rs / echelle_flat_scatsub_nolow HR7596_comb_flat.rs
#imarith SN2009ip.comb.rs / echelle_flat_scatsub_nolow SN2009ip_comb_flat.rs
#doall HR7596.0163
#doall HR7596.0164
#imcombine HR7596.016*.rs.ec.dispcor.fits HR7596_combine.fits combine=median
#imcombine HR7596.016*.rs.ec.dispcor.blueflat.fits HR7596_combine_blueflat.fits combine=median
#imcombine HR7596.016*.rs.ec.dispcor.redflat.fits HR7596_combine_redflat.fits combine=median
#doall SN2009ip.0160
#doall SN2009ip.0161
#doall SN2009ip.0162
#imcombine SN2009ip.0160.rs.ec.dispcor.fits,SN2009ip.0161.rs.ec.dispcor.fits,SN2009ip.0162.rs.ec.dispcor.fits SN2009ip.comb.rs.ec.dispcor.fits combine=median
#imcombine SN2009ip.0160.rs.ec.dispcor.blueflat.fits,SN2009ip.0161.rs.ec.dispcor.blueflat.fits,SN2009ip.0162.rs.ec.dispcor.blueflat.fits SN2009ip.comb.rs.ec.dispcor.blueflat.fits combine=median
#imcombine SN2009ip.0160.rs.ec.dispcor.redflat.fits,SN2009ip.0161.rs.ec.dispcor.redflat.fits,SN2009ip.0162.rs.ec.dispcor.redflat.fits SN2009ip.comb.rs.ec.dispcor.redflat.fits combine=median


# already divided by flats above
# standard HR7596_comb.rs.scatsub.ec.dispcor.blueflat.fits caldir=onedstds$spec16cal/ star_name=hr7596 output=stdblue answer="NO!"
# !rm sens.blue*fits
# sensfunc standards="stdblue" sensitivity="sensblue" answer="NO"
# imreplace sens*fits 35 lower=INDEF upper=35 
# imreplace sens*fits 10 lower=10 upper=INDEF
# !rm SN2009ip.comb.rs.ec.dispcor.blueflat.cal.fits
# calibrate SN2009ip.comb.rs.ec.dispcor.blueflat SN2009ip.comb.rs.ec.dispcor.blueflat.cal 
# 
# standard HR7596_comb.rs.scatsub.ec.dispcor.redflat.fits caldir=onedstds$spec16cal/ star_name=hr7596 output=stdred answer="NO!"
# !rm sens.red*fits
# sensfunc standards="stdred" sensitivity="sensred" answer="NO"
# imreplace sens*fits 35 lower=INDEF upper=35 
# imreplace sens*fits 10 lower=10 upper=INDEF
# !rm SN2009ip.comb.rs.ec.dispcor.redflat.cal.fits
# calibrate SN2009ip.comb.rs.ec.dispcor.redflat SN2009ip.comb.rs.ec.dispcor.redflat.cal 



# # HR7596.0163.fits
# # HR7596.0164.fits
# 
# hedit SN2009ip.0160.fits,SN2009ip.0161.fits,SN2009ip.0162.fits DISPAXIS 1 add+
# magnify SN2009ip.0160.fits SN2009ip.0160.rs.fits xmag=1 ymag=4
# magnify SN2009ip.0161.fits SN2009ip.0161.rs.fits xmag=1 ymag=4
# magnify SN2009ip.0162.fits SN2009ip.0162.rs.fits xmag=1 ymag=4
# 
# apall SN2009ip.0160.rs.fits references=JBrefspec.fits interactive- find- recenter+ resize+ edit- trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
# apall SN2009ip.0161.rs.fits references=JBrefspec.fits interactive- find- recenter+ resize+ edit- trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
# apall SN2009ip.0162.rs.fits references=JBrefspec.fits interactive- find- recenter+ resize+ edit- trace- fittrace- extract+ extras- lower=-2 upper=2 b_sample="-6:-3,3:6" b_naverage=1 width=12 radius=15 shift- ylevel=.05 t_order=5 t_sample="200:1850,*" t_naverage=3 t_niterate=3
# 
# imarith SN2009ip.0160.rs.ec.fits / echelle_blueflat_combine.rs.ec.fits SN2009ip.0160.rs.ec.flat.fits
# imarith SN2009ip.0161.rs.ec.fits / echelle_blueflat_combine.rs.ec.fits SN2009ip.0161.rs.ec.flat.fits
# imarith SN2009ip.0162.rs.ec.fits / echelle_blueflat_combine.rs.ec.fits SN2009ip.0162.rs.ec.flat.fits
# refspectra SN2009ip.0160.rs.ec.flat.fits answer="yes" references="JBtharspec.ec" sort="" group=""
# refspectra SN2009ip.0161.rs.ec.flat.fits answer="yes" references="JBtharspec.ec" sort="" group=""
# refspectra SN2009ip.0162.rs.ec.flat.fits answer="yes" references="JBtharspec.ec" sort="" group=""
# dispcor SN2009ip.0160.rs.ec.flat.fits SN2009ip.0160.rs.ec.dispcor.fits
# dispcor SN2009ip.0161.rs.ec.flat.fits SN2009ip.0161.rs.ec.dispcor.fits
# dispcor SN2009ip.0162.rs.ec.flat.fits SN2009ip.0162.rs.ec.dispcor.fits
# imcombine SN2009ip.016*.rs.ec.dispcor.fits SN2009ip.comb.rs.ec.dispcor.fits combine=median


# make flatnorm in pylab.... sigh....
# flat = pyfits.getdata('echelle_blueflat_combine.rs.ec.fits')
# flatnorm = flat / flat.max(axis=1)[:,newaxis]
# flatfits = pyfits.open('echelle_blueflat_combine.rs.ec.fits')
# flatfits[0].data = flatnorm
# flatfits.writeto('flatnorm_weight.fits')
# bigxarr = np.arange(float(ec[-1].xarr.min()),float(ec[0].xarr.max()),ec[-1].xarr.cdelt())
# bigspec = pyspeckit.Spectrum(data=np.zeros(bigxarr.shape), xarr=bigxarr, xarrkwargs={'units':'angstroms'})
# 
# imarith SN2009ip.comb.rs.ec.dispcor.cal * flatnorm_weight.fits SN2009ip.comb.rs.ec.dispcor.cal.weighted.fits
# scombine SN2009ip.comb.rs.ec.dispcor.cal.weighted.fits SN2009ip_merged.fits  combine=sum
# scombine flatnorm_weight.fits flatnorm_weight_merged.fits  combine=sum
# imarith SN2009ip_merged.fits / flatnorm_weight_merged.fits SN2009ip_merged_flat.fits



