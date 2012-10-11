
procedure doall (filename)
string filename
begin
#ccdproc(filename, ccdtype="", zerocor=no, darkcor=no, flatcor=no, fixfile="echmask.pl", biassec="[2100:2128,2:2027]", trimsec="[21:2048,1:2048]", order=3, niterate=3, int-)
hedit(filename,"DISPAXIS",1,add=yes,verify=no) 
#magnify(filename, filename+".rs", xmag=1, ymag=4)
hedit(filename+".rs","DISPAXIS",1,add=yes,verify=no) 
apall(filename+".rs", references="JBrefspec.fits", interactive-, find-, recenter+, resize+, edit-, trace-, fittrace-, extract+, extras-, lower=-2, upper=2, b_sample="-6:-3,3:6", b_naverage=1, width=12, radius=15, shift-, ylevel=.05, t_order=5, t_sample="200:1850,*", t_naverage=3, t_niterate=3)
imarith( filename+".rs.ec", "/", "echelle_flat_scatsub_nolow.ec", filename+".rs.ec.flat")
refspectra(filename+".rs.ec.flat", answer="yes", references="JBtharspec.ec", sort="", group="")
dispcor(filename+".rs.ec.flat", filename+".rs.ec.dispcor")


#imarith(filename+".rs.ec.dispcor", "/", "echelle_blueflat_combine.rs.ec.fits", filename+".rs.ec.dispcor.blueflat")
#imarith(filename+".rs.ec.dispcor", "/", "echelle_redflat_combine.rs.ec.fits", filename+".rs.ec.dispcor.redflat")
#apscatter(filename+".rs", filename+".rs.scatsub", scatter="scatter_"+filename, find-, recenter-, resize-, edit-, trace-, fittrace-, nsum=-10, inter+, references=filename+".rs", smooth+)
#apall(filename+".rs.scatsub", references="JBrefspec.fits", interactive-, find-, recenter+, resize+, edit-, trace-, fittrace-, extract+, extras-, lower=-2, upper=2, b_sample="-6:-3,3:6", b_naverage=1, width=12, radius=15, shift-, ylevel=.05, t_order=5, t_sample="200:1850,*", t_naverage=3, t_niterate=3)
#refspectra(filename+".rs.scatsub.ec", answer="yes", references="JBtharspec.ec", sort="", group="")
#dispcor(filename+".rs.scatsub.ec", filename+".rs.scatsub.ec.dispcor")
#imarith(filename+".rs.scatsub.ec.dispcor", "/", "echelle_blueflat_combine.rs.scatsub.ec.fits", filename+".rs.scatsub.ec.dispcor.blueflat")
#imarith(filename+".rs.scatsub.ec.dispcor", "/", "echelle_redflat_combine.rs.scatsub.ec.fits", filename+".rs.scatsub.ec.dispcor.redflat")
end

