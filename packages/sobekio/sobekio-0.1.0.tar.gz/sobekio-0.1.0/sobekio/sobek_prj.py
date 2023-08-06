# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 18:00:52 2018

SobekPrj and SobekCase classes

@author: quang
"""

import os
import pandas as pd
from warnings import warn
from his_file import HisFile


class SobekPrj:
    """Sobek Project class
    
    This class holds information for one sobek project and provide functions
    that users can get data from one or more cases of the project
    
    Methods
    -------
        get_case_number : int
            get folder storing case files
            
        his_from_case : pd.DataFrame
            get output data from one or more cases
    """
    
    def __init__(self, path=None):
    
        self.path = path
        self.name = os.path.basename(path)
        file_list = [f for f in os.listdir(path) if \
                    os.path.isfile(os.path.join(path,f))]
        file_list_lc = [f.lower() for f in file_list]
        # find the index of the caselist.cmt in all lower case file list
        # this should raise an error if there is one - meaning that the
        # caselist.cmt is not in the project folder.
        case_list_idx = file_list_lc.index('caselist.cmt')
        # returns the real file name, this way allows working with file system
        # that supports case-sensitive naming
        case_list_f = os.path.join(path, file_list[case_list_idx])
        self.case_cmt = case_list_f
        self.case_df = pd.read_csv(case_list_f, sep=' ',
                               header=None,
                               quotechar="'",
                               names=['number', 'name']
                               )
        
    def get_case_number(self, name=None):
        """Search for case number from case name"""
        
        case_search = self.case_df['name'] == name
        if case_search.any():
            if case_search.cumsum().to_list()[-1] > 1:
                raise KeyError('Duplicated case name in the caselist.cmt file')
            case_nr = self.case_df.loc[self.case_df['name'] == name,
                                'number'].iloc[0]
        else:
            case_nr = -1
            warn('Case: ' + name + ' does not exists')
        return case_nr
    
    def his_from_case(self, names=[],
                 his_type='calcpnt',
                 id_list=[],
                 param=1):
        """Read sobek output (.HIS) from cases.
    
        Parameters
        ----------
            names : list
                list of case names
            his_type : str 
                type of HIS file: \n
                    'wid': 'calcpnt.his' \n
                    'qid': 'reachseg.his' \n
                    'sid': 'struc.his' \n
                    'mid': 'measstat.his' \n
                    'latid': 'qlat.his' \n
                    'lid': 'qlat.his' \n
                    'pid': 'pump.his' \n
                    'fmid': 'flowmap.his' \n
                    'moid': 'morpmap.his' \n
                    'smid': 'gsedmap.his' \n
                    'shid': 'gsedhis.his' \n
                    or simply input full file names (ex. 'calcpnt.his')
            id_list : list
                list of IDs to get results
            param : str
                indexes, or names of the parameters. Can be a part of the names,
                but must be unique for searching.
        Raises
        ------
        IOError
            if HIS file was not found
        Return
        ------
        pandas.DataFrame
            ts: datetime \n
            case: name of cases \n
            parameter: name of parameters if more than one parameter were given
                
        """
        
        if isinstance(names, str):
            names = [names]
        case_nrs = [self.get_case_number(i) for i in names if \
                    self.get_case_number(i) != -1]
        case_names = [i for i in names if \
            self.get_case_number(i) != -1]
        if len(case_nrs) == 0:
            df_out = None
        else:
            case_paths = [os.path.join(self.path, str(i)) for i in case_nrs]
            cases = [SobekCase(i) for i in case_paths]
            df_list = []
            for k, s_case in enumerate(cases):
                s_case.set_wk_file(his_type)
                if not s_case.wk_file:
                    raise IOError('HIS file not found for ' + his_type)
                his = HisFile(s_case.wk_file)
                i_df = his.get_data_by_id(id_list, param)
                i_df = i_df.assign(case=case_names[k])
                df_list.append(i_df)
            df_out = pd.concat(df_list, axis=0)
        return df_out


class SobekCase():
    """Sobek Case class.

    for processing files within a case
    
    Parameters
    ----------
        path: str
            path to case folder
    Attributes
    ----------
        path: str
            path to case folder
        case_nr: str
            case number
        files: list
            list of all files in the case folder
        files_lc: list
            list of all files in the case folder converted to lower case strings
        wk_file: str
            current working file
    """

    def __init__(self, path):
        
        assert(os.path.exists(path))
        self.path = path
        self.files = os.listdir(self.path)
        self.files_lc = [f.lower() for f in self.files]
        self.wk_file = None
    
    def get_file_path(self, lc_name):
        
        if lc_name in self.files_lc:
            f_path = self.files[self.files_lc.index(lc_name)]
            f_path = os.path.join(self.case_folder, f_path)
        else:
            f_path = None
        return f_path

    def set_wk_file(self, ftype):
        """Set working file"""
        
        assert(isinstance(ftype, str))
        ftype = ftype.lower()
        self.wk_file = None
        ftypes = {'wid': 'calcpnt.his',
                  'qid': 'reachseg.his',
                  'sid': 'struc.his',
                  'mid': 'measstat.his',
                  'latid': 'qlat.his',
                  'lid': 'qlat.his',
                  'pid': 'pump.his',
                  'fmid': 'flowmap.his',
                  'moid': 'morpmap.his',
                  'smid': 'gsedmap.his',
                  'shid': 'gsedhis.his',
                  'bnd': 'boundary.dat',
                  'lat': 'lateral.dat',
                  'tg': 'trigger.def',
                  'init': 'initial.dat',
                  'pdat': 'profile.dat',
                  'pdef': 'profile.def',
                  'sdat': 'struct.dat',
                  'sdef': 'struct.def',
                  'cdef': 'control.def',
                  'cdesc': 'casedesc.cmt',
                  'setting': 'settings.dat'
                  }
        ftype_file = ftypes.get(ftype)
        if not ftype_file:
            # in this case, working file is not one of the above
            # set direct with file name given by ftype
            ftype_file = self.get_file_path(ftype)
        if ftype_file:
            self.wk_file = os.path.join(self.path, ftype_file)



