import splitfile
import os
if __name__ =='__main__':
    fromfile = input('input the location of the file to be split:')
    todir = input('input filter to save parts(empety filter is needed):')
    buffersize = int(input('input size of the parts:'), 10)
    splitfile.split(fromfile, todir, buffersize)
    frompackage = todir
    todir = input('input filter to save joined file:')
    objfile = splitfile.join(frompackage, todir)
