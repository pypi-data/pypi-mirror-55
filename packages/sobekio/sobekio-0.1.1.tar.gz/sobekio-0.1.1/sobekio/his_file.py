# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 18:00:52 2018

HisFile Class

@author: quang
"""
import os
import re
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import configparser as cp

class HisFile():
    """HIS file class, for processing sobek output (.HIS).
    
    Attributes
    ----------
    path : str
        path to the file
    ids: dict
        dict of Sobek-IDs stored in HIS and its HIA file (if any)
    n_ids: int
        total ids
    n_params: int
        total parameters
    n_ts: int
        total time steps
    t0: str
        starting time
    title: str
        title of the file
    his_path: str
        path to his file
    hia_path: str
        path to hia file (if any)
        
    Raises
    ------
    IOError
        if HIS file was not found
    
    Methods
    -------
    id_to_loc
    get_param
    get_time_df

    """
    
    
    def __init__(self, path):
        """
        Parameters
        ----------
            path: path to the directory containing .HIS file (and .HIA file)
        """
        
        assert(os.path.exists(path))
        assert(os.path.isfile(path))
        self.dname = os.path.dirname(path)
        self.fname = os.path.basename(path)
        self.his_path = path
        all_files = os.listdir(self.dname)
        all_files_lc = [f.lower() for f in all_files]
        hia_file = self.fname.lower().replace('.his', '.hia')
        if hia_file in all_files_lc:
            self.hia_path = os.path.join(
                                self.dname, 
                                all_files[all_files_lc.index(hia_file)]
                            )
        else:
            self.hia_path = None
        self.get_info()

    def get_info(self):
        """reading basic information of the HIS file"""

        title = []
        try:
            f = open(self.his_path, 'rb')
            file_size = os.stat(self.his_path).st_size
            self.file_size = file_size
            for i in range(4):
                title.append(f.read(40).decode('windows-1252'))
            n_par = np.fromfile(f, np.int, 1)[0]
            n_loc = np.fromfile(f, np.int, 1)[0]
            self.n_params = n_par
            self.n_ids = n_loc
            t0 = re.search(
                    '[0-9]{4}.[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2}',
                    title[3]).group(0)
            self.t0 = datetime.strptime(t0, '%Y.%m.%d %H:%M:%S')
            scu = re.search('scu=\ *([0-9]{1,})([a-zA-Z]*)', title[3])
            self.sc = int(scu.group(1))
            self.sc_unit = scu.group(2)
            self.title = title[1]
            ts_pos = 168 + 20 * self.n_params + 24 * self.n_ids
            n_ts = int((file_size - ts_pos) / (4 * n_loc * n_par + 4))
            self.n_ts = n_ts
            par_id = [i + 1 for i in range(n_par)]
            short_par = []
            # reading parameter
            # it is better to seperate short- and long-parameters
            # Otherwise, searching for a parameter could give two results and cause error
            for i in range(n_par):
                s_par = f.read(20).decode('windows-1252')
                # correcting this in measstat.his
                s_par = s_par.replace('Water Level', 'Waterlevel')
                short_par.append(s_par)
            par_df = pd.DataFrame({'short_par': short_par}, index=par_id)
            if self.hia_path:
                his_cp = cp.ConfigParser()
                his_cp.read(self.hia_path, encoding='windows-1252')
                if 'Long Parameters' in his_cp.sections():
                    if his_cp.items('Long Parameters'):
                        long_par_df = pd.DataFrame(
                                his_cp.items('Long Parameters'),
                                columns=['par_id', 'long_par'])
                        long_par_df.par_id = long_par_df.par_id.astype(int)
                        long_par_df = long_par_df.set_index('par_id')
                        par_df = pd.merge(par_df, long_par_df, left_index=True,
                                         right_index=True, how='outer')
                        par_df.long_par[par_df.long_par.isnull()] = ''
            if 'long_par' not in par_df.columns:
                par_df['long_par'] = ['Long ' + i for i in par_df.short_par]
            self.par_df = par_df
            # reading id - location
            sid = []
            location = [i + 1 for i in range(n_loc)]
            for i in range(n_loc):
                # for moving cursor
                np.fromfile(f, np.int, 1)
                sid.append(f.read(20).decode('windows-1252').rstrip())
            if self.hia_path:
                his_cp = cp.ConfigParser()
                his_cp.read(self.hia_path, encoding='windows-1252')
                if 'Long Locations' in his_cp.sections():
                    if his_cp.items('Long Locations'):
                        long_id = [i[1] for i in his_cp.items('Long Locations')]
                        long_loc = [int(i[0]) for i in
                                        his_cp.items('Long Locations')]
                        sid = sid + long_id
                        location = location + long_loc
            self.ids = dict(zip(sid, location))
            f.close()
        except IOError:
            raise IOError('Error reading file: ' + self.his_path)


    def id_to_loc(self, s_id):
        """Convert ID to its position in the data array
        
        Parameters
        ----------
            s_id : str
                Long or short ID
        Return
        -------
        int
            None if the s_id is not found in the location table
        """
    
        loc = None
        try:
            loc = self.ids.get(s_id)
        except KeyError:
            loc = None
        return loc
    
    def param_str_to_int(self, param):
        """convert param string to index
        
        Paramters
        ----------
            param: str
                single parameter given as string
                
        Return
        ------
            int
        """
        par_id = None
        assert(isinstance(param, int) or isinstance(param, str))
        try:
            par_id = int(param)
            if par_id not in range(1, self.n_params + 1):
                raise ValueError('param must be in between 1 and ', self.n_params)
        except ValueError:
            params = [s for s in self.par_df.short_par if param.lower()
                     in s.lower()]
            if len(params) == 1:
                par_id = self.par_df.index[self.par_df.short_par == params[0]][0]
            else:
                params = [s for s in self.par_df.long_par if param.lower()
                         in s.lower()]
                if len(params) == 1:
                    par_id = self.par_df.index[self.par_df.long_par == params[0]][0]
                else:
                    raise ValueError('parameter does not exist or ambiguous: ', param)
        return par_id
    
    def param_to_list(self, param):
        """convert input parameters to list of param indexes
        
        Paramters
        ----------
            param: int, str, or iterable object
            
        Return
        ------
        list
        """
        
        # param was given as a string, could be param name or 'all'
        if isinstance(param, str) or isinstance(param, int):
            if param == 'all':
                ret = [i for i, p in enumerate(self.par_df.short_par)]
            else:
                ret = [self.param_str_to_int(param)]
        else:
            ret = [self.param_str_to_int(par) for par in param]
        return ret
        
    def get_time_df(self):
        """Get data.frame of time series"""
        
        ts_pos = 168 + 20 * self.n_params + 24 * self.n_ids
        timeSteps = []
        f = open(self.his_path, 'rb')
        f.seek(ts_pos)
        for i in range(self.n_ts):
            step = np.fromfile(f, np.int, 1)[0]
            if self.sc_unit == 's':
                timeSteps.append(self.t0 +
                                 timedelta(seconds=(float(step) * self.sc)))
            elif self.sc_unit == 'm':
                timeSteps.append(self.t0 +
                                 timedelta(minutes=(float(step) * self.sc)))
            elif self.sc_unit == 'h':
                timeSteps.append(self.t0 +
                                 timedelta(hours=(float(step) * self.sc)))
            elif self.sc_unit == 'd':
                timeSteps.append(self.t0 +
                                 timedelta(days=(float(step) * self.sc)))
            f.seek(4 * self.n_ids * self.n_params, 1)
        f.close()
        timeDF = pd.DataFrame({'ts': timeSteps})
        return timeDF

    def _get_data_by_loc(self, locations=[], param=[1]):
        """Return pd.DataFrame contain data of the parameter
        for the locations

        Parameters
        ----------
        locations: list
            list of locations (int)
        param: int
            index of the parameter in .HIS file
        """
        
        if isinstance(param, int):
            param = [param]
        f = open(self.his_path, 'rb')
        his_df_pos = 168 + 20 * self.n_params + 24 * self.n_ids
        f.seek(his_df_pos)
        # all_data is a matrix
        # first column is time
        # next columns are values for parameters at locations, grouping by 
        # locations and sorting from left to right by parameter indexes
        # like: loc1(par1, par2,...,parN), loc2(par1, par2,...,parN)...
        all_data = np.fromfile(f, np.float32, -1)
        all_data = np.reshape(all_data, (self.n_ts,
                               self.n_params * self.n_ids + 1))
        param_data = []
        for i, p in enumerate(param):
            cols = list(map(lambda x: p + self.n_params * (x - 1) ,
                            locations))
            param_data.append(all_data[:, cols])
        f.close()
        ret = np.concatenate(param_data)
        return ret

    def get_data_by_id(self, id_list=[], param=1):
        """Return data of the parameter for the IDs as pd.DataFrame
        
        Parameters
        ----------
        IDs: list
            list of IDs (short of long)
            
        param: int/str
            parameter as Index or Name. Param can be given as a single value or
            a list, or 'all' for getting data for all parameters
        Return
        ------
        a pandas.DataFrame
            if there are more than parameters, one more column named 'parameter' 
            to indicate the parameters
        """
        # checking id_list
        if isinstance(id_list, str):
            id_list = [id_list]
        if not isinstance(id_list, list):
            try:
                id_list = [i for i in id_list]
            except TypeError:
                TypeError('id_list must be given as a string for single ID or as an \
                      iterable object for many IDs')
                raise
        par_id = self.param_to_list(param)
        locs = [self.id_to_loc(i) for i in id_list if self.id_to_loc(i)]
        col_names = [i for i in id_list if self.id_to_loc(i)]
        data_df = self._get_data_by_loc(locs, par_id)
        data_df = pd.DataFrame(data_df)
        data_df.columns = col_names
        ts_df = self.get_time_df()
        n_pars = len(par_id)
        ts_df_out = []
        if n_pars > 1:
            for i in range(n_pars):
                ts_df_out.append(ts_df.assign(parameter = self.par_df.short_par[i+1]))
            ts_df = pd.concat(ts_df_out, ignore_index=True)
        df_out = ts_df.join(data_df, rsuffix='R')
        none_ids = [i for i in id_list if not self.id_to_loc(i)]
        if len(none_ids) > 0:
            for i in none_ids:
                arg = {i: np.nan}
                df_out = df_out.assign(**arg)
            all_names = id_list.copy()
            all_names.insert(0, 'ts')
            if n_pars > 1:
                all_names.insert(1, 'parameter')
                df_out = df_out.reindex(all_names, axis=1)
        return df_out