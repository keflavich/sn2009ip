import pyfits
import difflib

def do_nods(filelist):
    """
    """

    headers = [pyfits.getheader(fn) for fn in filelist]

    for ii,fn in (enumerate(filelist)):
        if ii==len(filelist)-1:
            break

        try:
            if headers[ii]['BOREOFFX'] == 0 and headers[ii+1]['BOREOFFX'] == -5.9220000000000E-03:
                fitsfile = pyfits.open(fn)
                fitsfile[0].data -= pyfits.getdata(filelist[ii+1])

                matches = difflib.SequenceMatcher(None,fn,filelist[ii+1]).get_matching_blocks()
                outfilename = fn[matches[0].a:matches[0].size] + fn[matches[0].size:matches[1].a] + "-" + filelist[ii+1][matches[0].size:matches[1].b] + fn[matches[1].a:matches[1].size+matches[1].a]
                fitsfile.writeto(outfilename)
                print matches, outfilename

            elif headers[ii+1]['BOREOFFX'] == 0 and headers[ii]['BOREOFFX'] == -5.9220000000000E-03:
                fitsfile = pyfits.open(fn)
                fitsfile[0].data = pyfits.getdata(filelist[ii+1]) - fitsfile[0].data

                matches = difflib.SequenceMatcher(None,fn,filelist[ii+1]).get_matching_blocks()
                outfilename = fn[matches[0].a:matches[0].size] + filelist[ii+1][matches[0].size:matches[1].b] + "-" + fn[matches[0].size:matches[1].a] + fn[matches[1].a:matches[1].size+matches[1].a]
                fitsfile.writeto(outfilename)
                print matches, outfilename
        except IOError:
            pass



if __name__ == "__main__":

    import optparse
    parser=optparse.OptionParser()
    #parser.add_option("--verbose","-v",help="Be loud? Default True",default=False,action='store_true')

    options,args = parser.parse_args()

    do_nods(args)
