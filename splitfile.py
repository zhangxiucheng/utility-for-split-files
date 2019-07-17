import os, sys

buffersize = 1024 * 1024  #split a file (1MB per package) by default
filesep = '\n'

def split(fromfile, todir, buffersize=buffersize):
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
