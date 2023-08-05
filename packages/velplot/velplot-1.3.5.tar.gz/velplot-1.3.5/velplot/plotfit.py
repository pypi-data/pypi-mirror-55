import numpy,sys
import matplotlib.pyplot as plt
from matplotlib import re
from scipy.ndimage import gaussian_filter1d
from .constants import *
from .voigt import voigt_model
from .readspec import read_spec

def check_shift(i,dvmin,dvmax,table1,table2,header,comment,pubstyle=False):
    '''
    Check applied shifts, zero or continuum levels in input model.
    '''
    # Calculate velocity at center position of the plots
    vcent = (dvmin+dvmax)/2
    vhalf = (dvmax-dvmin)/2
    
    left  = table1[i][2]
    right = table1[i][3]
    
    shift,cont,slope,loc,zero = 0,1,0,0,0

    for j in range(len(table2)):

        val = table2[j][0]
        N   = float(re.compile(r'[^\d.-]+').sub('',table2[j][1]))
        z   = float(re.compile(r'[^\d.-]+').sub('',table2[j][2]))
        b   = float(re.compile(r'[^\d.-]+').sub('',table2[j][3]))
        reg = table2[j][4]
        if val==">>" and (reg==i+1 or (reg==0 and left<1215.6701*(z+1)<right)):
            if pubstyle==False:
                t = plt.text(vcent-.5*vhalf,-.43,'>> %.5f km/s'%b,color='blue',fontsize=5)
                t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
            shift = -b
        if val=="<>" and (reg==i+1 or (reg==0 and left<1215.6701*(z+1)<right)):
            if pubstyle==False:
                t = plt.text(vcent-.5*vhalf,-.28,'<> %.5f'%N,color='blue',fontsize=5)
                t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
            cont  = N
            slope = b
            loc   = z
        if val=="__" and (reg==i+1 or (reg==0 and left<1215.6701*(z+1)<right)):
            if pubstyle==False:
                t = plt.text(vcent-.27*vhalf,-.28,'__ %.5f'%N,color='blue',fontsize=5)
                t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
            zero = -N

    ''' Insert comments in figure '''

    if pubstyle==False:
        
        t1 = plt.text(vcent-.97*vhalf,-.4,
                      str(header[i,0])+' '+str('%.2f'%float(header[i,1])),
                      color='blue',fontsize=10,ha='left')
        t2 = plt.text(vcent-.1*vhalf,-.28,
                      ' f = %.4f'%float(header[i,2]),
                      color='blue',fontsize=5,ha='left')
        t3 = plt.text(vcent+.1*vhalf,-.28,
                      ' $\chi^2_{\mathrm{abs}}$ = '+header[i,-4],
                      color='blue',fontsize=5,ha='left')
        t5 = plt.text(vcent+.1*vhalf,-.43,
                      'npix = '+header[i,-2],
                      color='blue',fontsize=5,ha='left')
        t4 = plt.text(vcent+.35*vhalf,-.28,
                      ' $\chi^2_{\mathrm{red}}$ = '+header[i,-3],
                      color='blue',fontsize=5,ha='left')
        t6 = plt.text(vcent+.35*vhalf,-.43,
                      'ndf  = '+header[i,-1],
                      color='blue',fontsize=5,ha='left')
        t7 = plt.text(vcent+.97*vhalf,-.4,
                      str(i+1)+' - '+str(table1[i][0].split('/')[-1]),
                      color='blue',fontsize=7,ha='right')
        for t in [t1,t2,t3,t4,t5,t6,t7]:
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))

        if header[i,4]!='0':
            t = plt.text(vcent-.1*vhalf,-.43,
                         'q = %.0f'%float(header[i,4]),
                         color='blue',fontsize=5,ha='left')
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
        if 'overlap' in comment[i,0]:
            t = plt.text(vcent+.97*vhalf,.3,
                         'Overlapping system:\n'+comment[i,1],
                         color='darkorange',weight='bold',fontsize=6,horizontalalignment='right')
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
        if 'external' in comment[i,0]:
            t = plt.text(vcent+.97*vhalf,.3,
                         'External system:\n'+comment[i,1],
                         color='darkorange',weight='bold',fontsize=6,horizontalalignment='right')
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
    return shift,cont,slope,loc,zero

def plot_fit(i,table1,table2,header,atom,comment,shift,cont,slope,loc,zero,dvmin,dvmax,zmid,
             dispersion=0.01,daoaun=0,nores=False,unscale=False,getwave=False,details=False,
             pubstyle=False):
    '''
    Plot system and model.
    
    Parameters
    ----------
    i : int
      Index of the fitting region.
    daoaun : float
      Unit of da/a value in VPFIT.
    nores : bool
      Flag to not plot residuals
    unscale : bool
      Flag to not correct the data and distort the models
    getwave : bool
      Flag to get wavelength array from the spectrum
    details : bool
      Flag to plot individual Voigt profiles
    '''
    if pubstyle:
        plt.text(-5,-0.175,header[i,0]+' %.2f'%float(header[i,1]),fontsize=10,color='black',ha='center',va='center')    
    # Load data and model
    chunk = numpy.loadtxt('chunks/vpfit_chunk'+'%03d'%(i+1)+'.txt',comments='!')
    ibeg    = abs(chunk[:,0]-table1[i][2]).argmin()+1 if table1[i][2]!=table1[i][3] else 0
    iend    = abs(chunk[:,0]-table1[i][3]).argmin()-1 if table1[i][2]!=table1[i][3] else -1
    wa = chunk[ibeg:iend,0]
    fl = chunk[ibeg:iend,1]
    er = chunk[ibeg:iend,2]
    mo = chunk[ibeg:iend,3]
    wamid   = float(comment[i,2])
    pos     = abs(wa-wamid).argmin()
    vel     = 2*(wa-wamid)/(wa+wamid)*c
    # Estimate the half-pixel size to shift the steps of the flux array when plotting
    pos    = abs(wa-(table1[i][2]+table1[i][3])/2).argmin()
    pix1   = wa[pos]
    pix2   = (wa[pos]+wa[pos-1])/2
    dempix = 2*(pix1-pix2)/(pix1+pix2)*c
    # Plot residuals based on the flux, error, and model from the chunks
    rescol = 'black' if pubstyle else 'magenta'
    plt.axhline(y=1.6,color=rescol,zorder=2,lw=0.3)
    plt.axhline(y=1.7,color=rescol,ls='dotted',zorder=2,lw=0.3)
    plt.axhline(y=1.8,color=rescol,zorder=2,lw=0.3)
    if nores==False and table1[i][2]!=table1[i][3]:
        velo = vel if unscale else vel+shift
        res  = (fl-mo)/er/10+1.7
        plt.plot(velo+dempix,res,lw=.4,drawstyle='steps',color=rescol,zorder=3)
    # Plot model corrected for floating zero and continuum and velocity shift

    if table1[i][2]!=table1[i][3]:
        corr   = cont+slope*(wa/((1+loc)*1215.6701)-1)
        model  = mo/corr+zero
        model  = model / (1+zero)
        model  = mo if unscale else model
        velo   = vel if unscale else vel+shift
        velcol = 'red' if pubstyle else 'lime'
        plt.plot(velo,model,lw=1.,color=velcol,alpha=0.8,zorder=1)
        if pubstyle==False:
            plt.plot(velo+dempix,er,lw=.2,drawstyle='steps',color='cyan')
    # Plot data
    if getwave:
        specwa,specfl = read_spec(i,table1)
        wabeg   = wamid * (2*c+dvmin) / (2*c-dvmin)
        waend   = wamid * (2*c+dvmax) / (2*c-dvmax)
        ibeg    = abs(specwa-wabeg).argmin()
        iend    = abs(specwa-waend).argmin()
        ibeg    = ibeg-1 if ibeg>0 else ibeg
        iend    = iend+1 if iend<len(specwa)-1 else iend
        wa = specwa[ibeg:iend]
        fl = specfl[ibeg:iend]
        pos     = abs(wa-wamid).argmin()
        vel     = 2*(wa-wamid)/(wa+wamid)*c
    corr   = cont+slope*(wa/((1+loc)*1215.6701)-1)
    flux   = fl/corr + zero
    flux   = flux / (1+zero)
    flux   = fl if unscale else flux
    velo   = vel if unscale else vel+shift
    plt.plot(velo+dempix,flux,drawstyle='steps',lw=0.3,color='black',zorder=2)
    # Prepare high dispersion wavelength array
    start  = wamid * (2*c+dvmin) / (2*c-dvmin)
    end    = wamid * (2*c+dvmax) / (2*c-dvmax)
    val    = 1
    wave   = [start-2]
    dv     = dispersion
    while wave[-1]<end+2:
        wave.append(wave[-1]*(2*c+dv)/(2*c-dv))
    wave   = numpy.array(wave)
    vel    = 2*(wave-wamid)/(wave+wamid)*c
    vel    = vel-shift if unscale else vel
    model  = [1]*len(vel)
    show   = []
    for k in range(len(table2)):
        complist = numpy.empty((0,2))
        z = float(re.compile(r'[^\d.-]+').sub('',table2[k][2]))
        N = float(re.compile(r'[^\d.-]+').sub('',table2[k][1]))
        b = float(re.compile(r'[^\d.-]+').sub('',table2[k][3]))
        
        ''' Plot high dispersion Voigt profiles, lines, and labels for each component '''
                
        for p in range(len(atom)):
            
            alpha = table2[k][-2]*daoaun
            cond1 = table2[k][0]==atom[p,0]
            cond2 = table2[k][0] not in ['<>','>>','__','<<']
            cond3 = wa[0] < (1+z)*float(atom[p,1]) < wa[-1]

            if cond1 and cond2 and cond3:

                lambda0 = float(atom[p,1])

                if details:

                    q       = float(atom[p,5])
                    wavenum = 1./(lambda0*10**(-8))
                    wavenum = wavenum - q*(alpha**2-2*alpha)
                    lambda0 = 1/wavenum*10**(8)
                    f       = float(atom[p,2])
                    gamma   = float(atom[p,3])
                    profile = voigt_model(N,b,wave/(z+1),lambda0,gamma,f)
                    model   = model*profile
                    vsig    = table1[i][4]/dv
                    conv    = gaussian_filter1d(profile,vsig)
                    if unscale:
                        corr = cont+slope*(wave/((1+z)*1215.6701)-1)
                        conv = conv*corr-zero
                        conv = conv/(1-zero)
                    plt.plot(vel,conv,lw=0.2,color='orange')
                if atom[p,1]==header[i][1] or abs(float(atom[p,1])-float(header[i][1])) > 0.1:
                    lobs  = lambda0*(z+1)
                    vobs  = 2*(lobs-wamid)/(lobs+wamid)*c
                    vobs  = vobs - shift if unscale else vobs
                    if pubstyle:
                        plt.plot([vobs,vobs],[1.1,1.2],color='red',lw=0.5)
                    else:
                        pos   = 1.08 if val%2==0 else 1.25
                        zdiff = abs(2*(z-zmid)/(z+zmid))
                        color = '#FF4D4D' if zdiff < 0.003 and atom[p,0]==header[i][0] and atom[p,1]==header[i][1] \
                                else '#9370db' if zdiff < 0.003\
                                else '#ba55d3' if zdiff > 0.003 and atom[p,0] in ['HI','??'] \
                                else 'darkorange'
                        plt.axvline(x=vobs,ls='dashed',color=color,lw=.5,zorder=1,alpha=0.7)
                        lab1 = table2[k][-3]
                        lab2 = ''.join(re.findall('[a-zA-Z]+',table2[k][2][-2:]))
                        if table2[k][2][-1].isdigit()==True and str(lab1)+color not in show:
                            t = plt.text(vobs,pos,lab1,color=color,weight='bold',fontsize=7,horizontalalignment='center')
                            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))
                            show.append(str(lab1)+color)
                            val = val + 1
                        elif table2[k][2][-1].isdigit()==False and lab2+color not in show:
                            t = plt.text(vobs,pos,lab2,color=color,weight='bold',fontsize=5, horizontalalignment='center')
                            #t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))
                            show.append(lab2+color)
                            val = val + 1                         
    if details:
        vsig  = table1[i][4]/dv
        model = gaussian_filter1d(model,vsig)
        if unscale:
            corr  = cont+slope*(wave/((1+z)*1215.6701)-1)
            model = model*corr-zero
            model = model/(1-zero)
        plt.plot(vel,model,lw=1.,color='orange',alpha=.5,zorder=1)
    plt.axhline(y=1,color='black',ls='dotted',lw=0.3)
    plt.axhline(y=0,color='black',ls='dotted',lw=0.3)
    
