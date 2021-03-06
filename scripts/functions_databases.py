'''
'''

from tasks_v2 import Task
import os
from os.path import join, exists
import sys
import functions_general as fg
from external_tools import TOOLS_DICT
import re

''' static db variables '''
PATH_PFAM_DATABASE = '{0!s}/pfam/Pfam-A.hmm'.format(fg.PATH_DATABASES)
PATH_NR = join(fg.PATH_DATABASES, 'nr', 'nr')
PATH_SWISS_PROT = join(fg.PATH_DATABASES, 'uniprot_sprot', 'uniprot_sprot')
PATH_UNIREF90 = join(fg.PATH_DATABASES, 'uniref90', 'uniref90')
PATH_NOG_CATEGORIES = join(fg.PATH_DATABASES, 'nog_categories')

def db2stitle_task(db, tasks, log_flag=True):
    base_db = os.path.basename(db)
    trgs = ['{0!s}/{1!s}.stitle'.format(fg.PATH_DATABASES, base_db)]
    cmd = 'python {0!s}/fastaID2names.py --fasta {1!s} > {2!s}'.format(
           fg.PATH_SCRIPTS, db, trgs[0])
    name = 'db2stitle_'+base_db
    out, err = fg.GEN_LOGS(name) if(log_flag) else (None, None)
    return Task(command=cmd, dependencies=tasks, targets=trgs, name=name, stdout=out, stderr=err)

def build_blast_task(path_db,out_dir,dbtype,tasks,log_flag=True):
    trgs = []
    #title doesn't seem to change the out name .. it's still xx.gz.psq, etc? CHECK.
    title = os.path.basename(path_assembly).split('.')[0]
    cmd = 'gunzip -c {0!s} | {1!s} -in - -dbtype {2!s} -title {3!s} -out {4!s}'.format(
    path_assembly, fg.tool_path_check(TOOLS_DICT['blast'].full_exe[0]),dbtype,title,out_dir)
    name = 'build_blastplus_db_' + title
    out, err = fg.GEN_LOGS(name) if(log_flag) else (None, None)
    return Task(command=cmd,dependencies=tasks,targets=trgs,name=name,stdout=out,stderr=err)

def build_diamond_task(path_db_fasta,out_path,tasks,log_flag=True):
    title = os.path.basename(out_path)
    trgs = ['{0!s}'.format(out_path + '.dmnd')] 
    cmd = '{0!s} makedb --in {1!s} --db {2!s}'.format(TOOLS_DICT['diamond'].full_exe[0], path_db_fasta, out_path)
    name = 'build_diamond_'+ title
    out, err = fg.GEN_LOGS(name) if(log_flag) else (None, None)
    return Task(command=cmd, dependencies=tasks, targets=trgs, name=name, stdout=out, stderr=err)
 
def pfam_build_task(source, tasks, log_flag=True):
    trgs = [PATH_PFAM_DATABASE+'.h3f']
    cmd = 'cd {0!s} ; {1!s} -f {2!s};'.format(fg.PATH_DATABASES, fg.tool_path_check(TOOLS_DICT['hmmer'].full_exe[1]), source)
    name = 'hmmpress'
    out, err = fg.GEN_LOGS(name) if(log_flag) else (None, None)
    return Task(command=cmd, dependencies=tasks, targets=trgs, name=name, stdout=out, stderr=err)


