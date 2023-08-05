import numpy
from matplotlib import re
from .atominfo import isfloat,atom_info,atom_mass
from .constants import *

def read_fort13(fortfile,lastchtied,atom,head_path=None):
    '''
    Read fort.13 and store fitted parameters in array.
    '''
    # Read fort.13
    fort = open(fortfile,'r')
    line13 = []
    for line in fort:
        if len(line.split())==0: break
        elif line[0]!='!': line13.append(line.replace('\n',''))
    # Set up header file
    if head_path!=None:
        headlist = numpy.loadtxt(head_path,dtype='str',comments='!',delimiter='\n',ndmin=1)
    # Prepare table1, initialise atomic header array, and get mid redshift of the system
    # Info sorted as followed: filename - position - lambinit - lambfina - sigvalue
    header  = numpy.empty((0,9)) # [element,wavelength,oscillator,gammavalue,qcoeff,chisq,chisqnu,npix,ndf]
    comment = numpy.empty((0,3)) # [headerline,comment,wamid]
    table1  = []
    i = 1
    while line13[i].split()[0]!='*':
        l = line13[i].split()
        headline = line13[i].split('!')[-1] if head_path==None else headlist[i-1]
        header  = numpy.vstack([header,atom_info(headline.split()[0],atom)+[0,0,0,0]])
        comment = numpy.vstack([comment,[headline,'-',0]])
        dv  = l[4].split('=')[1].split('!')[0]
        dv  = dv if isfloat(dv)==False else float(dv) if 'vsig' in l[4] else float(dv)/(2*numpy.sqrt(2*numpy.log(2)))
        table1.append([l[0],float(l[1]),float(l[2]),float(l[3]),dv])
        i=i+1
    # Prepare table2 listing all the components
    table2 = []
    idx = 1
    for i in range(i+1,len(line13)):
        l = line13[i].split('!')[0].split()
        species  = l[0] if len(l[0])>1 else l[0]+l[1]
        coldens  = l[1] if len(l[0])>1 else l[2]
        redshift = l[2] if len(l[0])>1 else l[3]
        doppler  = l[3] if len(l[0])>1 else l[4]
        alpha    = l[4] if len(l)==8 else l[5] if len(l)==9 else 0
        region   = int(l[-1])
        if type(alpha)==str:
            if 'E-' in alpha:
                expon = re.compile(r'[^\d.-]+').sub('',alpha.split('E-')[-1])
                alpha = float(alpha.split('E-')[0])*10**-float(expon)
            elif 'E+' in alpha:
                expon = re.compile(r'[^\d.-]+').sub('',alpha.split('E+')[-1])
                alpha = float(alpha.split('E+')[0])*10**float(expon)
            else:
                alpha = float(re.compile(r'[^\d.-]+').sub('',alpha))
        mode = 'thermal' if float(l[-3])==float(l[-2])==0 else 'turbulent'
        table2.append([species,coldens,redshift,doppler,region,idx,alpha,mode])
        idx=idx+1
    # Modify column density to summed column densities if necessary
    for k in range(len(table2)):
        N   = re.compile(r'[^\d.-]+').sub('',table2[k][1])
        tie = ''.join(re.findall('[a-zA-Z%]+',table2[k][1][-2:]))
        if table2[k][0] not in ['<>','>>','__','<<'] and table2[k][1][-1].isdigit()==False:
            N    = 10**float(N)
            tie0 = ''.join(re.findall('[a-zA-Z%]+',table2[k-1][1][-2:]))
            tie1 = ''.join(re.findall('[a-zA-Z%]+',table2[k][1][-2:]))
            if '%' in tie1:
                for l in range(k+1,len(table2)):
                    tie2 = ''.join(re.findall('[a-zA-Z%]+',table2[l][1][-2:]))
                    if tie2==tie0.upper() and ord(tie2[0].lower())>=ord(lastchtied):
                        N = N - 10**float(re.compile(r'[^\d.-]+').sub('',table2[l][1]))
                    else:
                        break
            elif '%' not in tie0 and tie1!=tie0 and ord(tie1[0].lower())>=ord(lastchtied):
                for l in range(k+1,len(table2)):
                    tie2 = ''.join(re.findall('[a-zA-Z%]+',table2[l][1][-2:]))
                    if tie2==tie1:
                        N = N - 10**float(re.compile(r'[^\d.-]+').sub('',table2[l][1]))
                    else:
                        break
            N = '%.6f'%numpy.log10(N)
        table2[k][1] = N+tie
    # Modify Doppler parameter if thermally tied
    for k in range(len(table2)):
        id0   = table2[k][0]
        b0    = table2[k][3]
        mode  = table2[k][-1]
        val0  = re.compile(r'[^\d.-]+').sub('',b0)
        tie0  = ''.join(re.findall('[a-zA-Z%]+',b0[-2:]))
        if tie0.islower()==True and id0 not in ['<>','>>','__','<<']:
            mass0 = atom_mass(id0)
            for l in range(len(table2)):
                id1   = table2[l][0]
                b1    = table2[l][3]
                val1  = re.compile(r'[^\d.-]+').sub('',b1)
                tie1  = ''.join(re.findall('[a-zA-Z%]+',b1[-2:]))
                if tie1==tie0.upper() and mode=='thermal':
                    mass1 = atom_mass(id1)
                    val1  = '%.6f'%(numpy.sqrt(mass0/mass1)*float(val0))
                    table2[l][3] = val1+tie1
                if tie1==tie0.upper() and mode=='turbulent':
                    table2[l][3] = val0+tie1
    # Modify Redshift parameter if tied
    for k in range(len(table2)):
        id0   = table2[k][0]
        z0    = table2[k][2]
        val0  = re.compile(r'[^\d.-]+').sub('',z0)
        tie0  = ''.join(re.findall('[a-zA-Z%]+',z0[-2:]))
        if tie0.islower()==True and id0 not in ['<>','>>','__','<<']:
            for l in range(len(table2)):
                id1   = table2[l][0]
                z1    = table2[l][2]
                val1  = re.compile(r'[^\d.-]+').sub('',z1)
                tie1  = ''.join(re.findall('[a-zA-Z%]+',z1[-2:]))
                if tie1==tie0.upper():
                    table2[l][2] = val0+tie1
    return header,comment,table1,table2
                    
def read_fort26(fortfile,lastchtied,atom,head_path=None):
    '''
    Read fort.26 and store fitted parameters in array.
    '''
    # Read fort.26
    fort = open(fortfile,'r')
    line26 = []
    for line in fort:
        if len(line.split())==0: break
        elif line[0]!='!': line26.append(line.replace('\n',''))
    # Set up header file
    if head_path!=None:
        headlist = numpy.loadtxt(head_path,dtype='str',comments='!',delimiter='\n',ndmin=1)
    # Prepare table1, initialise atomic header array, and get mid redshift of the system
    # Info sorted as followed: filename - position - lambinit - lambfina - sigvalue
    header  = numpy.empty((0,9))                # [element,wavelength,oscillator,gammavalue,qcoeff,chisq,chisqnu,npix,ndf]
    comment = numpy.empty((0,3))                # [headerline,comment,wamid]
    table1  = []
    i = 0
    while line26[i][0:3]=='%% ':
        l = line26[i].replace('%% ','').split()
        headline = line26[i].split('!')[-1] if head_path==None else headlist[i]
        header  = numpy.vstack([header,atom_info(headline.split()[0],atom)+[0,0,0,0]])
        comment = numpy.vstack([comment,[headline,'-',0]])
        dv  = l[4].split('=')[1].split('!')[0]
        dv  = dv if isfloat(dv)==False else float(dv) if 'vsig' in l[4] else float(dv)/(2*numpy.sqrt(2*numpy.log(2)))
        table1.append([l[0],float(l[1]),float(l[2]),float(l[3]),dv])
        i=i+1
    # Prepare table2 listing all the components
    tempest = numpy.empty((0,3),dtype=object)
    table2 = []
    idx=1
    for i in range(i,len(line26)):
        l = line26[i].split('[')[0].split('!')[0].split()
        species  = l[0] if len(l[0])>1 else l[0]+l[1]
        coldens  = l[5] if len(l[0])>1 else l[6]
        redshift = l[1] if len(l[0])>1 else l[2]
        doppler  = l[3] if len(l[0])>1 else l[4]
        alpha    = l[8] if len(l)==11 else l[7] if len(l)==10 else 0
        region   = int(l[-1])
        if type(alpha)==str:
            if 'E-' in alpha:
                expon = re.compile(r'[^\d.-]+').sub('',alpha.split('E-')[-1])
                alpha = float(alpha.split('E-')[0])*10**-float(expon)
            elif 'E+' in alpha:
                expon = re.compile(r'[^\d.-]+').sub('',alpha.split('E+')[-1])
                alpha = float(alpha.split('E+')[0])*10**float(expon)
            else:
                alpha = float( re.compile(r'[^\d.-]+').sub('',alpha))
        mode = 'thermal'
        if '[' in line26[i]:
            val0 = float(line26[i].split('[')[1].split()[0])
            val1 = float(line26[i].split('[')[1].split()[1])
            val2 = float(line26[i].split('[')[1].split()[2])
            val3 = float(line26[i].split('[')[1].split()[3])
            mode = 'thermal' if val0==val1==val2==val3==0 else 'turbulent'
        if mode=='turbulent':
            tie  = ''.join(re.findall('[a-zA-Z%]+',doppler[-2:]))
            tempest = numpy.vstack((tempest,numpy.array([tie,val0,val2],dtype=object)))
        table2.append([species,coldens,redshift,doppler,region,idx,alpha,mode])
        idx=idx+1
    # Modify column density to summed column densities if necessary
    for k in range(len(table2)):
        N   = re.compile(r'[^\d.-]+').sub('',table2[k][1])
        tie = ''.join(re.findall('[a-zA-Z%]+',table2[k][1][-2:]))
        if table2[k][0] not in ['<>','>>','__','<<'] and table2[k][1][-1].isdigit()==False:
            N    = 10**float(N)
            tie0 = ''.join(re.findall('[a-zA-Z%]+',table2[k-1][1][-2:]))
            tie1 = ''.join(re.findall('[a-zA-Z%]+',table2[k][1][-2:]))
            if '%' in tie1:
                for l in range(k+1,len(table2)):
                    tie2 = ''.join(re.findall('[a-zA-Z%]+',table2[l][1][-2:]))
                    if tie2==tie0.upper() and ord(tie2[0].lower())>=ord(lastchtied):
                        N = N - 10**float(re.compile(r'[^\d.-]+').sub('',table2[l][1]))
                    else:
                        break
            elif '%' not in tie0 and tie1!=tie0 and ord(tie1[0].lower())>=ord(lastchtied):
                for l in range(k+1,len(table2)):
                    tie2 = ''.join(re.findall('[a-zA-Z%]+',table2[l][1][-2:]))
                    if tie2==tie1:
                        N = N - 10**float(re.compile(r'[^\d.-]+').sub('',table2[l][1]))
                    else:
                        break
            N = '%.6f'%numpy.log10(N)
        table2[k][1] = N+tie
    # Modify Doppler parameter if thermally tied
    for k in range(len(table2)):
        id0   = table2[k][0]
        b0    = table2[k][3]
        mode  = table2[k][-1]
        val0  = re.compile(r'[^\d.-]+').sub('',b0)
        tie0  = ''.join(re.findall('[a-zA-Z%]+',b0[-2:]))
        if id0 not in ['<>','>>','__','<<']:
            if tie0.islower()==True and ord(tie0[0].lower())<ord(lastchtied):
                mass0 = atommass(id0)
                for l in range(len(table2)):
                    id1   = table2[l][0]
                    b1    = table2[l][3]
                    val1  = re.compile(r'[^\d.-]+').sub('',b1)
                    tie1  = ''.join(re.findall('[a-zA-Z%]+',b1[-2:]))
                    if tie1==tie0.upper() and mode=='thermal':
                        mass1 = atommass(id1)
                        val1  = '%.6f'%(numpy.sqrt(mass0/mass1)*float(val0))
                        table2[l][3] = val1+tie1
                    if tie1==tie0.upper() and mode=='turbulent':
                        table2[l][3] = val0+tie1
    # Modify Redshift parameter if tied
    for k in range(len(table2)):
        id0   = table2[k][0]
        z0    = table2[k][2]
        val0  = re.compile(r'[^\d.-]+').sub('',z0)
        tie0  = ''.join(re.findall('[a-zA-Z%]+',z0[-2:]))
        if tie0.islower()==True and id0 not in ['<>','>>','__','<<']:
            for l in range(len(table2)):
                id1   = table2[l][0]
                z1    = table2[l][2]
                val1  = re.compile(r'[^\d.-]+').sub('',z1)
                tie1  = ''.join(re.findall('[a-zA-Z%]+',z1[-2:]))
                if tie1==tie0.upper():
                    table2[l][2] = val0+tie1
    return header,comment,table1,table2

def get_dv(header,table1,comment,atom,dvplot=None,zmid=None):
    '''
    Calculate central redshift and velocity dispersion.
    '''
    # Calculate mid-redshift among all fitting regions
    if zmid==None:
        zreg = numpy.empty((0,2))
        for j in range (len(table1)):
            text_comment = comment[j,0].split()
            if 'external' not in text_comment:
                zmin = float(table1[j][2])/float(header[j,1])-1
                zmax = float(table1[j][3])/float(header[j,1])-1
            else:
                # Get redshit edges of the external fitting region
                wref = float(atom_info(text_comment[0],atom)[1])
                wmin = table1[j][2]
                wmax = table1[j][3]
                zmin = float(wmin)/wref-1
                zmax = float(wmax)/wref-1
                # Get wavelength edges of the associated tied region
                wref = float(atom_info(text_comment[2],atom)[1])
                wmin = wref*(zmin+1)
                wmax = wref*(zmax+1)
                # Get redshift edges of the corresponding overlapping region
                wref = float(atom_info(get_trans(comment,text_comment[2]),atom)[1])
                zmin = float(wmin)/wref-1
                zmax = float(wmax)/wref-1
            zreg = numpy.vstack([zreg,[zmin,zmax]])
        zmid = (min(zreg[:,0])+max(zreg[:,1]))/2.
    # Calculate maximum velocity dispersions
    dv = 0
    for j in range (len(header)):
        text_comment = comment[j,0].split()
        if 'external' in text_comment:
            wref  = float(header[j,1])
            # Wavelength at zmid in the overlapping region
            reg   = float(atom_info(get_trans(comment,text_comment[2]),atom)[1])*(zmid+1)
            # Transition wavelength of the overlapping element
            wion  = float(atom_info(text_comment[2],atom)[1])
            # Central wavelength of external tied transition for the overlapped system
            wamid = wref*(reg/wion)
            text  = text_comment[0]+' at z='+str(round(wamid/float(header[j,1])-1,6))
            dvmin = abs(2*(table1[j][2]-wamid)/(table1[j][2]+wamid))*c
            dvmax = abs(2*(table1[j][3]-wamid)/(table1[j][3]+wamid))*c
            dv    = max(dv,dvmin,dvmax)
        elif 'overlap' in text_comment:
            wamid = float(header[j,1])*(zmid+1)
            text  = text_comment[2]+' at z='+str(round(wamid/float(atom_info(text_comment[2],atom)[1])-1,6))
            dvmin = abs(2*(table1[j][2]-wamid)/(table1[j][2]+wamid))*c
            dvmax = abs(2*(table1[j][3]-wamid)/(table1[j][3]+wamid))*c
            dv    = max(dv,dvmin,dvmax)
        else:
            wamid = float(header[j,1])*(zmid+1)
            text  = '-'
            dvmin = abs(2*(table1[j][2]-wamid)/(table1[j][2]+wamid))*c
            dvmax = abs(2*(table1[j][3]-wamid)/(table1[j][3]+wamid))*c
            dv    = max(dv,dvmin,dvmax)
        comment[j,1:] = [text,wamid]
    if dvplot!=None:
        dvmin = -dvplot[0] if len(dvplot)==1 else dvplot[0]
        dvmax = +dvplot[0] if len(dvplot)==1 else dvplot[1]
    elif dv<150:
        dvmin,dvmax = -150,150
    else:
        dvmin,dvmax = -dv,+dv
    return dvmin,dvmax,zmid

def get_trans(comment,overlaptrans):
    '''
    Find transition part of overlap system, if existing.
    '''
    for k in range(len(comment)):
        headline = comment[k,0].split()
        if 'overlap' in headline and headline[2]==overlaptrans:
            break
    return headline[0]
