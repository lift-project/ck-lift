#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    return {'return':0}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j=q.find('This is sbt ')
           if j>=0:
              ver=q[j+12:]
              break

    return {'return':0, 'version':ver}

##############################################################################
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    fp=cus['full_path']
    ep=cus['env_prefix']

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)

    env[ep]=p2
    env[ep+'_BIN']=p1
    env[ep+'_TOOL']='sbt'

    return {'return':0, 'bat':s}
