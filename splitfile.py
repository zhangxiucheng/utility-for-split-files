import os, sys

buffersize = 1024 * 1024  #split a file (1MB per package) by default
filesep = '\n'

def split(fromfile, todir, buffersize=buffersize):
    """
    help text:
        fromfile is the abs path to the file you want to process

    todir:
        the directory to store your package
        supposed to be empty
        if not files in todir will be deleted

    buffersize:
        max size of one split part of your aim file
        buffersize = 1 means 1 bit is the max size of one split part file
    
    an extra config.in file will be craeted to store package config info
    this file will be used when func join(frompackage, todir, ifclean=False) is called
    """
    if not os.path.exists(todir):
        os.mkdir(todir)
    else:
        print('warning: files that already exit will be deleted!!!')
        for filename in os.listdir(todir):
            os.remove(os.path.join(todir, filename))
    
    partnum = 0
    input = open(fromfile, 'rb')
    fromfilename = os.path.basename(fromfile)
    configfile = open(os.path.join(todir, 'config.in'), 'w')
    configfile.write(fromfilename + filesep)
    configfile.write(str(buffersize) + filesep)
    print(fromfilename)
    while True:
        buffer = input.read(buffersize)
        if not buffer: break
        partnum += 1
        filename = os.path.join(todir, ('part%04d' % partnum))
        configfile.write('part%04d\n' % partnum)
        fileobj = open(filename, 'wb')
        fileobj.write(buffer)
        fileobj.close()
    input.close()
    configfile.close()
    assert partnum <= 9999
    return partnum

def join(frompackage, todir, ifclean=False):
    """
    recover your split files from packages

    frompackage:
        abs directory to packages

    todir:
        location where to store your file

    ifclean:
        wether you want to keep part files
    """
    configobj = open(os.path.join(frompackage, 'config.in'), 'r')
    tofilename = configobj.readline()[:-1]
    buffersize = int(configobj.readline(), 10)
    tofileobj = open(os.path.join(todir, tofilename), 'wb')
    for line in configobj.readlines():
        partname = line[:-1]
        if not partname: break
        partfile = open(os.path.join(frompackage, partname), 'rb')
        buffer = partfile.read(buffersize)
        tofileobj.write(buffer)
        partfile.close()
        if ifclean: os.remove(os.path.join(frompackage, partname))
        print(partname, 'joined successfully!')
    tofileobj.close()
    configobj.close()
