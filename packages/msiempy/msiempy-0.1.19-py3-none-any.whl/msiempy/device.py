"""Provide ESM, ERC and data source management.
"""

import logging
log = logging.getLogger('msiempy')

import csv
import ipaddress
import inspect
import json
import logging
import re
import sys
from itertools import chain
from io import StringIO
from functools import partial, lru_cache

from . import NitroDict, NitroList, NitroError, NitroObject
from .__utils__ import dehexify

class Device(NitroObject):
    pass

class ERC(Device):
    pass

class ESM(Device):
    """
    ESM class
    
    Public Methods:
    
        version()       Returns simple version string, '10.1.0'
        
        buildstamp()    Returns buildstamp string, '10.0.2 20170516001031'
        
        time()          Returns ESM time (GMT)
        
        disks()         Returns string of disk status
        
        ram()           Returns string of disk status
        
        backup_status()     Returns dict with keys:
                             - autoBackupEnabled: bool
                             - autoBackupDay: int
                             - backupLastTime: str (timestamp)
                             - backupNextTime: str (timestamp)
        
        callhome()      Returns True/False if callhome is active/not active
        
        rulestatus()    Returns dict with keys:
                        - rulesAndSoftwareCheckEnabled: bool
                        - rulesAndSoftLastCheck: str (timestamp)
                        - rulesAndSoftNextCheck: str (timestamp)

        status()        Returns dict with the status outputs above plus a few
                        other less interesting details.
               
        timezones()     Returns dict (str, str)
                            timezone_id: timezone_name
        
        tz_name_to_id(id)         Returns timezone name matching given timezone ID.
        
        tz_id_to_name(tz_name)    Returns timezone ID matching given timezone name.
        
        tz_offsets()    Returns list of timezone tuples. 
                        (tz_id, tz_name, tz_offset)
                        [(1, 'Midway Island, Samoa', '-11:00'),
                         (2, 'Hawaii', '-10:00'),
            
        type_id_to_venmod(type_id)     Returns tuple. (vendor, model) matching
                                       provided type_id.
        
        venmod_to_type_id(vendor, model)    Returns string of matching type_id
        
    """
    def __init__(self, *args, **kwargs):
        """
        Returns:
            obj. ESM object
        """
        super().__init__(*args, **kwargs)
        
    def refresh(self):
        super().refresh()

    @property
    def text(self):
        return str('ESM object')

    @property
    def json(self):
        return (dict(self))

    def time(self):
        """
        Returns:
            str. ESM time (GMT).

        Example:
            '2017-07-06T12:21:59.0+0000'
        """
        return self.nitro.request("get_esm_time")['value']

    def buildstamp(self):
        return self.nitro.buildstamp()
    
    def version(self):
        return self.nitro.version

    def status(self):
        """
        Returns:
            dict. ESM stats.
            including:
                - processor status
                - hdd status
                - ram status
                - rule update status
                - backup status
                - list of top level devices
        Other functions exist to return subsets of this data also.
        """
        status = self.nitro.request("get_sys_info")
        return self.map_status_int_fields(status)

    def map_status_int_fields(self, status):
        new_status = {}
        new_status['cpu'] = status['HDW'].split('\n')[0][6:]
        new_status['hdd'] = status['HDW'].split('\n')[1][6:]
        new_status['ram'] = status['HDW'].split('\n')[2][6:]
        new_status['autoBackupEnabled'] = status['ABENABLED']
        new_status['autoBackupHour'] = status['ABHOUR']
        new_status['autoBackupDay'] = status['ABDAY']
        new_status['backupNextTime'] = status['BUNEXT']
        new_status['backupLastTime'] = status['BULAST']
        new_status['rulesAndSoftwareCheckEnabled'] = status['RSCENABLED']
        new_status['rulesAndSoftNextCheck'] = status['RSNEXT']
        if status['RSLAST'] == 'RSLAST':
            new_status['rulesAndSoftLastCheck'] = None
        else:
            new_status['rulesAndSoftLastCheck'] = status['RSLAST']
        if status['CHIP'] == 'CHIP':
            new_status['callHomeIp'] = None
        else:
            new_status['callHomeIp'] = status['CHIP']
        return new_status


    def disks(self):
        """
        Returns:
            str. ESM disks and utilization.

        Example:
            'sda3     Size:  491GB, Used:   55GB(12%), Available:  413GB, Mount: /'
        """
        return self.status()['hdd']

    def ram(self):
        """
        Returns:
            str. ESM ram and utilization.

        Example:
            'Avail: 7977MB, Used: 7857MB, Free: 119MB'
        """
        return self.status()['ram']

    def backup_status(self):
        """
        Returns:
            dict. Backup status and timestamps.

            {'autoBackupEnabled': True,
                'autoBackupDay': 7,
                'autoBackupHour': 0,
                'backupLastTime': '07/03/2017 08:59:36',
                'backupNextTime': '07/10/2017 08:59'}
        """
        fields = ['autoBackupEnabled',
                   'autoBackupDay',
                   'autoBackupHour',
                   'autoBackupHour',
                   'backupNextTime']

        return {key: val for key, val in self.status().items()
                if key in fields}

    def callhome(self):
        """
        Returns:
            bool. True/False if there is currently a callhome connection
        """
        if self.status()['callHomeIp']:
            return True

    def rules_status(self):
        """
        Returns:
            dict. Rules autocheck status and timestamps.

        Example:
        { 'rulesAndSoftwareCheckEnabled': True
          'rulesAndSoftLastCheck': '07/06/2017 10:28:43',
          'rulesAndSoftNextCheck': '07/06/2017 22:28:43',}

        """
        self._fields = ['rulesAndSoftwareCheckEnabled',
                        'rulesAndSoftLastCheck',
                        'rulesAndSoftNextCheck']
        return {self.key: self.val for self.key, self.val in self.status().items()
                if self.key in self._fields}

    def get_alerts(self, ds_id, flows=False):
        """Tells the ESM to retrieve alerts from the provided device ID.
        
        Arguments:
            ds_id (str): IPSID for the device, e.g. 144116287587483648
            flows (bool): Also get flows from the device (default: False)
        
        Returns:
            None
        """
        self.nitro.request('get_alerts_now', ds_id=ds_id)
        if flows:
            self.nitro.request('get_flows_now', ds_id=ds_id)

    @lru_cache(maxsize=None)    
    def recs(self):
        """
        Returns: 
            
        """
        rec_list = self.nitro.request('get_recs')
        return [(rec['name'], rec['id']['id'])for rec in rec_list]
                
    @lru_cache(maxsize=None)   
    def _get_timezones(self):
        """
        Gets list of timezones from the ESM.
        
        Returns:
            str. Raw return string from ESM including 
        """
        return self.nitro.request('time_zones')
        
    def tz_offsets(self):
        """
        Builds table of ESM timezones including offsets.
        
        Returns:
            list. List of timezone tuples (name, id, offset)
            
        Example:
            [(1, 'Midway Island, Samoa', '-11:00'),
             (2, 'Hawaii', '-10:00'),
             ...
            ]
        """
        return [(tz['id']['value'], tz['name'], tz['offset']) 
                  for tz in self._get_timezones()]
                   
        
    def timezones(self):
        """
        Builds table of ESM timezones and names only. No offsets.
        
        Returns:
            dict. {timezone_id, timezone_name}
        """
        return {str(tz['id']['value']): tz['name']
                            for tz in self._get_timezones()}

    def tz_name_to_id(self, tz_name):
        """
        Args:
            tz_name (str): Case sensitive, exact match timezone name
            
        Returns:
            str. Timezone id or None if there is no match
        """
        tz_reverse = {tz_name.lower(): tz_id 
                        for tz_id, tz_name in self.timezones().items()}
        try:
            return tz_reverse[tz_name.lower()]
        except KeyError:
            return None
    
    def tz_id_to_name(self, tz_id):
        """
        Args:
            td_id (str): Numerical string (Currently 1-74)
        
        Returns:
            str. Timezone name or None if there is no match
        """
        try:
            return self.timezones()[tz_id]
        except KeyError:
            return None
    
    def type_id_to_venmod(self, type_id):
        """
        Args:
            type_id (str): Numerical string 
        
        Returns:
            tuple. (vendor, model) or None if there is no match
        """
        ds_types = self._get_ds_types()
        for venmod in ds_types:
            if str(venmod[0]) == str(type_id):
                return (venmod[1], venmod[2])
        return(('Unkown vendor for type_id {}'.format(type_id),'Unkown vendor'))

    def venmod_to_type_id(self, vendor, model):
        """
        Args:
            vendor (str): Exact vendor string including puncuation
            model (str): Exact vendor string including puncuation
        
        Returns:
            str. Matching type_id or None if there is no match
        """
        for venmod in self._get_ds_types():
            if vendor == venmod[1]:
                if model == venmod[2]:
                    return str(venmod[0])

    def rules_history(self):
        """
        Returns: 
            Policy Editor rule history.
        """
        file = self.nitro.request('get_rule_history')['TK']
        return self.nitro.get_internal_file(file)

    @lru_cache(maxsize=None)   
    def _get_ds_types(self):
        """
        Retrieves device table from ESM
                    
        Returns:
            list. of tuples output from callback: _format_ds_types()

        Note:
            rec_id (str): self.rec_id assigned in method
        """
        rec_id = self.recs()[0][1]
        return  self.nitro.request('get_dstypes', rec_id=rec_id)
                    
    def _format_ds_types(self, venmods):
        """
        Callback to create type_id/vendor/model table
        
        Args:
            venmods (obj): request object from _get_ds_types
        
        Returns:
            list. of tuples 
                
           [(542, 'McAfee', 'SaaS Email Protection')
            (326, 'McAfee', 'Web Gateway')
            (406, 'Microsoft', 'ACS - SQL Pull')
            (491, 'Microsoft', 'Endpoint Protection - SQL Pull')
            (348, 'Microsoft', 'Exchange')]

        Note: 
            This is a callback for _get_ds_types.

        """
        return [(mod['id']['id'], ven['name'], mod['name'],)
                    for ven in venmods['vendors']
                    for mod in ven['models']]

class DevTree(NitroList):
    """
    Interface to the ESM device tree.
    
    Public Methods:
    
        search('term')      Returns a DataSource object matching the name,
                        IPv4/IPv6 address, hostname or device ID.

        search_group(field='term')    Returns a list of DataSource objects that match 
                                  the given term for the given field. 
                                  Valid field options include:
                                    - parent_id = '144119615532826624'
                                    - type_id = '65'
                                    - vendor = 'Intersect Alliance'
                                    - model = 'Snare for Windows'
                                    - require_tls = 'T'
                                    - port = '514'
                                    - tz_id = '51'
                                    - tz_name = 'Darwin'
                                    - zone_id = '7'
                                                            
        last_times(days=,       Returns a list of DataSource objects that 
                   hours=,      the ESM has NOT heard from since the
                   minutes=)    provided timeframe.
                                  args are cummulative, 
                               e.g. (days=30, hours=5) will added together


        refresh()   Rebuilds the tree
                            
        __len__     Returns the total number of devices in the tree
        
        __iter__    Interates through each DataSource object in the tree. 
        
        __contains__    Returns bool as to whether a datasource name, IP,
                        hostname or ds_id exist in the device tree.
                        
    """
    def __init__(self, *args, **kwargs):
        """
        Initalize the DevTree object
        """
        super().__init__(*args, **kwargs)
        self.devtree = self.build_devtree()
        self._cast_datasources()
        
    def __len__(self):
        """
        Returns the count of devices in the device tree.
        """
        return len(self.devtree)
        
    def __iter__(self):
        """
        Returns:
            Generator with datasource objects.
        """
        for ds in self.devtree:
            yield ds

    def __str__(self):
        return json.dumps(self.devtree)


    def __repr__(self):
        return json.dumps(self.devtree)

    def __contains__(self, term):
        """
        Returns:
            bool: True/False the name or IP matches the provided search term.
        """
        if self.search(term):
            return True
        else:
            return None

    def __getitem__(self, key):
        return self.devtree[key]

    def search(self, term, zone_id='0'):
        """
        Args:
            term (str): Datasource name, IP, hostname or ds_id
            
            zone_id (int): Provide zone_id to limit search to a specific zone

        Returns:
            Datasource object that matches the provided search term or None

        """
        search_fields = ['ds_ip', 'name', 'hostname', 'ds_id']

        found = [ds for ds in self.devtree
                    for field in search_fields 
                    if str(term).lower() == str(ds[field]).lower()
                    if ds['zone_id'] == zone_id]
        
        if found:
            return found[0]        

    def search_ds_group(self, field, term, zone_id='0'):
        """
        Args:
            field (str): Valid DS config field to search
            term (str): Data to search for in specified field
            
        Returns:
            Generator containing any matching DataSource objects or None
            Result must be iterated through.
            
        Raises:
            ValueError: if field or term are None
        """
        return (DataSource(adict=ds) for ds in self.devtree
                        if ds.get(field) == term)
                       
    def refresh(self):
        """
        Rebuilds the devtree
        """
        self.devtree = self.build_devtree()
        self._cast_datasources()
        
    def get_ds_times(self):
        """
        """
        last_times = self._get_last_event_times()
        self._insert_ds_last_times()
        return last_times
        
    def recs(self):
        """
        Returns:
            list of Receiver dicts (str:str)
        """
        return [self._rec for self._rec in self.devtree
                    if self._rec['desc_id'] in ['2','13']]
    
    def build_devtree(self):
        """
        Coordinates assembly of the devtree object
        """
        devtree = self._get_devtree()
        if devtree == 'ITEMS':
            print('Device tree is empty. Must add at least one datasource for this to work.')
            self.devicetree = []
            return
        devtree = self._format_devtree(devtree)
        devtree = self._insert_rec_info(devtree)        
        containers = self._get_client_containers(devtree)
        devtree = self._merge_clients(containers, devtree)
        devtree = [self._normalize_bool_vals(ds) for ds in devtree if ds]
        zonetree = self._get_zonetree()
        devtree = self._insert_zone_names(zonetree, devtree)
        zone_map = self._get_zone_map()
        devtree = self._insert_zone_ids(zone_map, devtree)            
        last_times = self._get_last_times()
        last_times = self._format_times(last_times)
        devtree = self._insert_ds_last_times(last_times, devtree)
        devtree = self._filter_bogus_ds(devtree)
        return devtree

    def _get_devtree(self):
        """
        Returns:
            ESM device tree; raw, but ordered, string.
            Does not include client datasources.
        """
        resp = self.nitro.request('get_devtree')
        return dehexify(resp['ITEMS'])

    def _format_devtree(self, devtree):
        """
        Parse key fields from raw device strings into datasource dicts

        Returns:
            List of datasource dicts
        """
        devtree = StringIO(devtree)
        devtree = csv.reader(devtree, delimiter=',')
        devtree_lod = []
        _ignore_remote_ds = False

        for idx, row in enumerate(devtree, start=1):
            if len(row) == 0:
                continue

            # Get rid of duplicate 'asset' devices
            if row[0] == '16':  
                continue

            # Filter out distributed ESMs                
            if row[0] == '9':  
                _ignore_remote_ds = True
                continue
            
            # Filter out distributed ESM data sources
            if _ignore_remote_ds:  
                if row[0] != '14':
                    continue
                else:
                    _ignore_remote_ds = False
            
            if row[2] == "3":  # Client group datasource group containers
                row.pop(0)     # are fake datasources that seemingly have
                row.pop(0)     # two uneeded fields at the beginning.
            if row[16] == 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT':
                row[16] = '0'  # Get rid of weird type-id for N/A devices
            
            if len(row) < 29:
                continue
            
            ds_fields = {'idx': idx,
                            'desc_id': row[0],
                            'name': row[1],
                            'ds_id': row[2],
                            'enabled': row[15],
                            'ds_ip': row[27],
                            'hostname': row[28],
                            'type_id': row[16],
                            'vendor': '',
                            'model': '',
                            'tz_id': '',
                            'date_order': '',
                            'port': '',
                            'require_tls': '',
                            'client_groups': row[29],
                            'zone_name': '',
                            'zone_id': '',
                            'client': False
                            }
            devtree_lod.append(ds_fields)
        return devtree_lod

    def _insert_rec_info(self, devtree):
        """
        Adds parent_ids to datasources in the tree based upon the
        ordered list provided by the ESM. All the datasources below
        a Receiver row have it's id set as their parent ID.

        Returns:
            List of datasource dicts
        """
        _pid = '0'
        esm_dev_id = ['14']
        esm_mfe_dev_id = ['19', '21', '22', '24']
        nitro_dev_id = ['2', '4', '10', '12', '13', '15']
        datasource_dev_id = ['3', '5', '7', '17', '20', '23', '256']
        
                   
        for device in devtree:
            if device['desc_id'] in esm_dev_id:
                esm_name = device['name']
                esm_id = device['ds_id']
                device['parent_name'] = 'n/a'
                device['parent_id'] = '0'
                continue

            if device['desc_id'] in esm_mfe_dev_id:
                parent_name = device['name']
                parent_id = device['ds_id']
                device['parent_name'] = 'n/a'
                device['parent_id'] = '0'
                continue
            
            if device['desc_id'] in nitro_dev_id:
                device['parent_name'] = esm_name
                device['parent_id'] = esm_id
                parent_name = device['name']
                pid = device['ds_id']
                continue

            if device['desc_id'] in datasource_dev_id:
                device['parent_name'] = parent_name
                device['parent_id'] = pid
            else:
                device['parent_name'] = 'n/a'
                device['parent_id'] = 'n/a'

        return devtree

    def _get_client_containers(self, devtree):
        """
        Filters DevTree for datasources that have client datasources.
        
        Returns:
            List of datasource dicts that have clients
        """
        return [ds for ds in devtree
                if ds['desc_id'] == "3"
                if int(ds['client_groups']) > 0]

    def _merge_clients(self, containers, devtree):
        ds_idx = 0
        merged_tree = []
        for ds in devtree:
            
            # These are client group folders. No way to associate to the clients.
            if ds['desc_id'] == '254': continue
            
            ds['idx'] = ds_idx
            merged_tree.append(ds)
            ds_idx += 1

            if ds in containers:
                clients = self._get_clients(ds['ds_id'])
                clients = self._format_clients(clients)
                for client in clients:
                    client['idx'] = ds_idx
                    ds_idx += 1
                    client['parent_id'] = ds['ds_id']
                    merged_tree.append(client)
        return merged_tree

    def _get_clients(self, ds_id):
        """
        Get list of raw client strings.

        Args:
            ds_id (str): Parent ds_id(s) are collected on init
            ftoken (str): Set and used after requesting clients for ds_id

        Returns:
            List of strings representing unparsed client datasources
        """

        file = self.nitro.request('req_client_str', ds_id=ds_id)['FTOKEN']
        return dehexify(self.nitro.get_internal_file(file))

    def _format_clients(self, clients):
        """
        Parse key fields from _get_clients() output.

        Returns:
            list of dicts
        """
        clients = StringIO(clients)
        clients = csv.reader(clients, delimiter=',')

        clients_lod = []
        for row in clients:
            if len(row) < 13:
                continue

            ds_fields = {'desc_id': "256",
                          'name': row[1],
                          'ds_id': row[0],
                          'enabled': row[2],
                          'ds_ip': row[3],
                          'hostname': row[4],
                          'type_id': row[5],
                          'vendor': row[6],
                          'model': row[7],
                          'tz_id': row[8],
                          'date_order': row[9],
                          'port': row[11],
                          'require_tls': row[12],
                          'zone_name': '',
                          'zone_id': '',
                          'client': True
                               }
            clients_lod.append(ds_fields)
        return clients_lod        

    def _get_zonetree(self):
        """
        Retrieve zone data.
        
        Returns:
            str: device tree string sorted by zones
        """        
        resp = self.nitro.request('get_zones_devtree')
        return dehexify(resp['ITEMS'])
        
    def _insert_zone_names(self, zonetree, devtree):
        """
        Args:
            zonetree (str): Built by self._get_zonetree
        
        Returns:
            List of dicts (str: str) devices by zone
        """
        zone_name = None
        zonetree = StringIO(zonetree)
        zonetree = csv.reader(zonetree, delimiter=',')

        for row in zonetree:
            if row[0] == '1':
                zone_name = row[1]
                if zone_name == 'Undefined':
                    zone_name = ''
                continue
            for device in devtree:
                if device['ds_id'] == row[2]:
                    device['zone_name'] = zone_name
        return devtree

    def _get_zone_map(self):
        """
        Builds a table of zone names to zone ids.
        
        Returns:
            dict (str: str) zone name : zone ids
        """
        zone_map = {}
        resp = self.nitro.request('zonetree')

        if not resp:
            return zone_map
        for zone in resp:
            zone_map[zone['name']] = zone['id']['value']
            for szone in zone['subZones']:
                zone_map[szone['name']] = szone['id']['value']
        return zone_map
        
    def _insert_zone_ids(self, zone_map, devtree):
        """
        """
        for device in devtree:
            if device['zone_name'] in zone_map.keys():
                device['zone_id'] = zone_map.get(device['zone_name'])
            else:
                device['zone_id'] = '0'
        return devtree
        
    def _insert_venmods(self):
        """
        Populates vendor/model fields for any datasources 
        
        Returns:
            List of datasource dicts - devtree
        """
        for self._ds in self._devtree:
            if not self._ds['vendor'] and self._ds['desc_id'] == '3': 
                self._ds['vendor'], self._ds['model'] = ESM().type_id_to_venmod(self._ds['type_id'])
        return self._devtree_lod
    
    def _insert_desc_names(self):
        """
        Populates the devtree with desc_names matching the desc_ids
        
        Returns:
            List of datasource dicts - devtree
        
        """
        self._type_map = {'1': 'zone',
                        '2': 'ERC',
                        '3': 'datasource',
                        '4': 'Database Event Monitor (DBM)',
                        '5': 'DBM Database',
                        '7': 'Policy Auditor',
                        '10': 'Application Data Monitor (ADM)',
                        '12': 'ELM',
                        '13': 'McAfee Event Receiver/ELM',
                        '14': 'Local ESM',
                        '15': 'Advanced Correlation Engine (ACE)',
                        '16': 'Asset datasource',
                        '17': 'Score-based Correlation',
                        '19': 'McAfee ePolicy Orchestrator (ePO)',
                        '20': 'EPO',
                        '21': 'McAfee Network Security Manager (NSM)',
                        '22': 'McAfee Network Security Platform (NSP)',
                        '23': 'NSP Port',
                        '24': 'McAfee Vulnerability Manager (MVM)',
                        '25': 'Enterprise Log Search (ELS)',
                        '254': 'client_group',
                        '256': 'client'}

        for self._ds in self._devtree:
            if self._ds['desc_id'] in self._type_map:
                self._ds['desc'] = self._type_map[self._ds['desc_id']]
        return self._devtree
        
                        
    def _get_last_times(self):
        """
        Returns:
            string with datasource names and last event times.
        """
        resp = self.nitro.request('ds_last_times')
        return dehexify(resp['ITEMS'])

    def _format_times(self, last_times):
        """
        Formats the output of _get_last_times

        Args:
            last_times (str): string output from _get_last_times()

        Returns:
            list of dicts - [{'name', 'model', 'last_time'}]
        """
            
        last_times = StringIO(last_times)
        last_times = csv.reader(last_times, delimiter=',')
        last_times_lod = []
        for row in last_times:
            if len(row) == 5:
                time_d = {}
                time_d['name'] = row[0]
                time_d['model'] = row[2]
                if row[3]:
                    time_d['last_time'] = row[3]
                else:
                    time_d['last_time'] = 'never'
                last_times_lod.append(time_d)
        return last_times_lod

    def _insert_ds_last_times(self, last_times, devtree):
        """
        Parse event times str and insert it into the _devtree

        Returns:
            List of datasource dicts - the devtree
        """
        for device in devtree:
            for d_time in last_times:
                if device['name'] == d_time['name']:
                    device['model'] = d_time['model']
                    device['last_time'] = d_time['last_time']
        return devtree

    def _filter_bogus_ds(self, devtree):
        """Filters objects that inaccurately show up as datasources sometimes.
        
        Arguments:
            devtree (list) -- the devtree
        """
        type_filter = ['1', '16', '254']
        return [ds for ds in devtree if ds['desc_id'] not in type_filter]

    def _cast_datasources(self):
        for dev in self.devtree:
            if dev['desc_id'] in ['3','256']:
                self.devtree[int(dev['idx'])] = DataSource(dev)
                
    def duplicate_datasource(self, p):
        """Check for duplicate dataname name or IP address.
        
        Arguments:
            p (dict) -- datasource params 

        Parameters:
            name (str): datasource name
            ds_ip (str): datasource IP
            zone_id (str): optional zone_id
        """
        
        if p.get('zone_id'):
            result = self.search(p['name'], zone_id=['zone_id'])
            if not result:
                result = self.search(p['ds_ip'], zone_id=['zone_id'])
        else:
            result = self.search(p['name'])
            if not result:
                result = self.search(p['ds_ip'])
        return result

    def add(self, kwargs):
            """
            Adds a datasource. 

            Args:
                **kwargs: datasource attributes
            
            Attributes:
                client (bool): designate a client datasource (not child)
                name (str): name of datasource (req)
                parent_id (str): id of parent device (req)
                ds_ip (str): ip of datasource (ip or hostname required)
                hostname (str): hostname of datasource 
                type_id (str): type of datasource (req)
                enabled (bool): enabled or not (default: True)
                tz_id (str): timezone of datasource (default UTC: 8)
                zone_id (str): numberic ESM id for zone (default: 0)
                    Examples (tz_id only): PST: 27, MST: 12, CST: 11, EST: 32 
                require_tls (bool): datasource uses syslog tls
            
            Returns:
                result id (str): id of the result. Not the ds_id as of 11.2.1
                    or None on Error            
            """
            p = self._validate_ds_params(kwargs)
            dd = self.duplicate_datasource(p)
            if dd:
                print('Error: Cannot add Datasource. Duplicate name: {} or IP Address: {}'
                    .format(dd['name'], dd['ds_ip']))
                return

            if p.get('client'):
                self.add_client(p)
                return

            if self.nitro.api_v == 1:
                result_id = self.nitro.request('add_ds_11_1_3', 
                                                parent_id=p['parent_id'],
                                                name=p['name'],
                                                ds_ip=p['ds_ip'],
                                                type_id=p['type_id'],
                                                zone_id=p['zone_id'],
                                                enabled=p['enabled'],
                                                url=p['url'],
                                                ds_id=0,
                                                child_enabled='false',
                                                child_count=0,
                                                child_type=0,
                                                idm_id=0,
                                                parameters=p['parameters'])
            else:
                result_id = self.nitro.request('add_ds_11_2_1', 
                                               parent_id=p['parent_id'],
                                                name=p['name'],
                                                ds_ip=p['ds_ip'],
                                                type_id=p['type_id'],
                                                zone_id=p['zone_id'],
                                                enabled=p['enabled'],
                                                url=p['url'],
                                                parameters=p['parameters'])
            self.devtree.append(p)
            return result_id

    def add_client(self, p):
        """Add a datasource client
        
        Arguments:
            p (dict)) -- datasource parameters
        
        Parameters:
            parent_id (str): datasource id of the client group datasource
            name (str): name of the client
            enabled (bool): enabled or not (default: True
            ds_ip (str): IP address for client 
            hostname (str): hostname for client
            type_id (str): numeric ESM type-id
            tz_id (str): numeric ESM timezone id or GMT
            dorder (str): Date order
            maskflag (str): 
            port (str): IP port to use
            require_tls (bool): use syslog-TLS (default: False)
        """
        for ds in self.devtree:
            if ds['ds_id'] == p['parent_id']:
                if ds['desc_id'] != '3':
                    print('Error: Client parent must be matching datasource'
                           'not "{}".'.format(ds['name']))
                    return


        result_id = self.nitro.request('add_client1',
                            parent_id=p['parent_id'],
                            name=p['name'],
                            enabled=p['enabled'] or 'T',
                            ds_ip=p['ds_ip'],
                            hostname=p['hostname'],
                            type_id=p['type_id'],
                            tz_id=p['tz_id'],
                            dorder=p['dorder'],
                            maskflag=p['maskflag'],
                            port=p['port'],
                            require_tls=['require_tls'])
        return


    def _validate_ds_params(self, p):
        """Validate parameters for new datasource.
        
        Arguments:
            p (dict) -- datasource parameters
        
        Returns:
            datasource dict with normalized values
        
            or False if something is invalid.
        """
        # Common for all datasources
        if not p.get('name'):
            logging.error('Error: New datasource requires "name".')
            return

        if not p.get('ds_ip'):
             if p.get('ip'):
                 p['ds_ip'] = p['ip']
             else:
                if not p.get('hostname'):
                    logging.error('Error: New datasource requires "ip" or "hostname".')
                    return
        
        if not p.get('hostname'):
            p['hostname'] = ''

        if not p.get('parent_id'):
            p['parent_id'] = 0

        p = self._validate_ds_tz_id(p)

        if p.get('enabled') == False:
            p['enabled'] = 'false'
        else:
            p['enabled'] = 'true'

        if p.get('client'):
            if not p.get('dorder'):
                p['dorder'] = 0

            if not p.get('maskflag'):
                p['maskflag'] = 'true'

            if not p.get('port'):
                p['port'] = 0

            if not p.get('require_tls'):
                p['require_tls'] = 'F'

            if not p.get('type_id'):
                p['type_id'] = 0

        else:
            if not p.get('type_id'):
                logging.error('Error: New datasource requires "type_id".')
                return

            if not p.get('zone_id'):
                p['zone_id'] = 0

            if not p.get('url'):
                p['url'] = ''

            _v2_base_vars = ['client', 'parent_id', 'name', 'ds_ip', 'type_id', 
                                'zone_id', 'enabled', 'url', 'parameters']
            
            _v1_base_vars = _v2_base_vars + ['ds_id', 'childEnabled', 
                                                'childCount', 'childType', 'idmId']

            p['parameters'] = []
            popme = []
            for key, val in p.items():
                if self.nitro.api_v == 1:
                    if key not in _v1_base_vars:
                        p['parameters'].append({'key': key,
                                                'value': val})
                        popme.append(key)  
                elif self.nitro.api_v == 2:
                    if key not in _v2_base_vars:
                        p['parameters'].append({'key': key,
                                                'value': val})
                        popme.append(key)  
            for key in popme:
                p.pop(key)              
        return p

    def _validate_ds_tz_id(self, p):
        """Validates datasource time zone id.
        
        Arguments:
            p (dict): datasource param
        
        Returns:
            dict of datasource params or None if invalid
        """
        if p.get('tz_id'):
            if p['tz_id'] == 'GMT':
                return p
            try:
                if not 0 <= int(p.get('tz_id')) <= 75:
                    logging.error('Error: New datasource "tz_id" must be int between 1-74 or GMT.')
                    return
            except ValueError:
                logging.error('Error: New datasource "tz_id" must be int between 1-74 or GMT.')
                return
        else:
            p['tz_id'] = 26
        return p

    @staticmethod
    def _normalize_bool_vals(d):
        """Recursively changes strings 'T', 'F' to bool
        
        Arguments:
            d (dict) -- nested dicts and lists okay
        """
        for k, v in d.items():
            if isinstance(v, dict):
                DevTree._normalize_bool_vals(v)
            if isinstance(v, list):
                for items in v:
                    DevTree._normalize_bool_vals(items)
            elif v in ['T', 'F']:
                if v == 'T':
                    d[k] = True
                else:
                    d[k] = False
        return d

class DataSource(NitroDict):
    """DataSource class
    
    Arguments:
        adict (dict): datasource parameters
        
    Best instantiated from DevTree():
        >>> dt = DevTree()
        >>> ds = dt[25]
        or
        >>> ds = dt.search('10.10.1.1')

    Parameters:
        name (str): name of the datasource
        ds_ip (str): IP of the datasource
        hostname (str): hostname for the datasource
        ds_id (str): internal datasource ID (e.g 144234544545444)
        type_id (str): numeric internal datasource type id
        desc_id (str): always '3' a datasource or '254' for a client
        parent_id (str): internal ds_id for the parent device
        parent_name (str): name of the parent device
        enabled (str): 'T' or 'F'
        client (bool): Client datasource or not
        zone_id (str): numeric zone_id
        zone_name (str): name of the zone
        tz_id (str): internal numeric timezone ID
        vendor (str): vendor of datasource (e.g. Microsoft)
        model (str): model of datasource (e.g. Windows)
        require_tls (str): Use syslog over TLS
        url (str): URL of the datasource

    """
    def __init__(self, *args, **kwargs):
        """
        Initalize the DataSource object
        """
        super().__init__(*args, **kwargs)

    def data_from_id(self):
        pass

    def load_details(self):
        """DataSource object is lazy. This gets the rest of the parameters."""
        if self.nitro.api_v == 1:
            details = self.nitro.request('ds_details1', ds_id=self.data['ds_id'])
        else:
            details = self.nitro.request('ds_details2', ds_id=self.data['ds_id'])
        self._map_parameters(details)

    def delete(self):
        """This deletes the datasource and all the data. Be careful.
        """
        if self.data['desc_id'] not in ['3','256']:
            print('Only a DataSource can be deleted with this method.')
            return

        if self.data['desc_id'] == '256':
            self.delete_client()
        else:
            if self.nitro.api_v == 1:
                self.nitro.request('del_ds1', parent_id=self.data['parent_id'], ds_id=self.data['ds_id'])
            elif self.nitro.api_v == 2:
                self.nitro.request('del_ds2', parent_id=self.data['parent_id'], ds_id=self.data['ds_id'])
    
    def delete_client(self):
        file = self.nitro.request('get_wfile', ds_id=self.data['ds_id'])['TK']
        job_id = self.nitro.request('del_client', 
                                        parent_id=self.data['parent_id'], ftoken=file)['JID']
        status = self.nitro.request('get_job_status', job_id=job_id)['JS']
        while status == 0:
            status = self.nitro.request('get_job_status', job_id=job_id)['JS']

    def _map_parameters(self, p):
        """Map the internal ESM field names to msiempy style
        
        Arguments:
            p (dict): datasource parameters
        """
        p = DevTree._normalize_bool_vals(p)
        self.data['name'] = p.get('name')
        self.data['ds_ip'] = p.get('ipAddress')
        self.data['zone_id'] = p.get('zoneId')
        self.data['enabled'] = p.get('enabled')

        if self.nitro.api_v == 1:
            self.data['ds_id'] = p.get('pdsId')
            self.data['parent_id'] = p.get('parentId').get('id')
        elif self.nitro.api_v == 2:
            self.data['ds_id'] = p.get('pdsId').get('value')
            self.data['parent_id'] = p.get('parentId').get('value')

        if self.data['desc_id'] == '256':
           self.data['tz_id'] = p.get('tz_id')
        else:
            self.data['child_enabled'] = p.get('childEnabled')
            self.data['idm_id'] = p.get('idmId')
            self.data['child_count'] = p.get('childCount')
            self.data['child_type'] = p.get('childType')
            self.data['type_id'] = p.get('typeId').get('id')
            if p.get('parameters'):
                for d in p['parameters']:
                    # The key is called "key" and the value is the key. 
                    # The value is called value and the value is the value.
                    self.data[d.get('key')] = d.get('value')
