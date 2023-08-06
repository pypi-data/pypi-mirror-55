#
# This file is distributed as part of the Wannier19 code     #
# under the terms of the GNU General Public License. See the #
# file `LICENSE' in the root directory of the Wannier19      #
# distribution, or http://www.gnu.org/copyleft/gpl.txt       #
#                                                            #
# The Wannier19 code is hosted on GitHub:                    #
# https://github.com/stepan-tsirkin/wannier19                #
#                     written by                             #
#           Stepan Tsirkin, University ofZurich              #
#                                                            #
#------------------------------------------------------------
#
#  This is the main file of the library, and the user is suposed 
#  to import only it. 

import functools as __functools

try:
    from .integrate import eval_integral_BZ as __eval_integral_BZ
    from .utility import smoother as __smoother
    from . import integrateXnk  as __integrateXnk
    from . import tabulateXnk   as __tabulateXnk 
## Public part: 
    from . import symmetry
    from .get_data import Data
except ImportError:
    from integrate import eval_integral_BZ as __eval_integral_BZ
    from utility import smoother as __smoother
    import integrateXnk  as __integrateXnk
    import tabulateXnk   as __tabulateXnk 
## Public part: 
    import symmetry
    from get_data import Data
    

integrate_options=__integrateXnk.calculators.keys()
tabulate_options =__tabulateXnk.calculators.keys()





import sys


def __figlet(text,font='cosmike',col='yellow'):
    from colorama import init
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    from termcolor import cprint 
    from pyfiglet import figlet_format
    letters=[figlet_format(X, font=font).rstrip("\n").split("\n") for X in text]
#    print (letters)
    logo=[]
    for i in range(len(letters[0])):
        logo.append("".join(L[i] for L in letters))
    cprint("\n".join(logo),col, attrs=['bold'])



__figlet("Wannier 19",font='speed')
__figlet("    by Stepan Tsirkin",font='straight',col='green')

#for font in ['twopoint','contessa','tombstone','thin','straight','stampatello','slscript','short','pepper']:
#    __figlet("by Stepan Tsirkin",font=font,col='green')


def __check_option(quantities,avail,tp):
    for opt in quantities:
      if opt not in avail:
        raise RuntimeError("Quantity {} is not available for {}. Available options are : \n{}\n".format(opt,tp,avail) )


def integrate(Data,NKdiv=None,NKFFT=None,Efermi=None,omega=None, Ef0=0,smearEf=10,smearW=10,quantities=[],adpt_num_iter=0,fout_name="w19",symmetry_gen=[],
                GammaCentered=True,restart=False,numproc=0):
    __check_option(quantities,integrate_options,"integrate")
    smooth=__smoother(Efermi,10)
    eval_func=__functools.partial(  __integrateXnk.intProperty, Efermi=Efermi, smootherEf=smooth,quantities=quantities )
    res=__eval_integral_BZ(eval_func,Data,NKdiv,NKFFT=NKFFT,nproc=numproc,
            adpt_num_iter=adpt_num_iter,adpt_nk=1,
                fout_name=fout_name,symmetry_gen=symmetry_gen,
                GammaCentered=GammaCentered,restart=restart)
    return res



def tabulate(Data,NKdiv=None,NKFFT=None,omega=None, quantities=[],symmetry_gen=[],ibands=None,
                      restart=False,numproc=0):
    __check_option(quantities,tabulate_options,"tabulate")
    eval_func=__functools.partial(  __tabulateXnk.tabXnk, ibands=ibands,quantities=quantities )
    res=__eval_integral_BZ(eval_func,Data,NKdiv,NKFFT=NKFFT,nproc=numproc,
            adpt_num_iter=0 ,symmetry_gen=symmetry_gen,  GammaCentered=True ,restart=restart)
    return res



