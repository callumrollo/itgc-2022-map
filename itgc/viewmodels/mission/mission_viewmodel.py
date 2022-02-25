import os
import sys
import json
import glob
import datetime
import pandas as pd
import numpy as np

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)

from itgc.viewmodels.shared.viewmodelbase import ViewModelBase

blank_json_dict = {"type": "FeatureCollection", "features": []}


def track_to_json(df, today=False) -> dict:
    """ converts a dataframe of track points to geojson format"""
    loc_list = []
    for i, row in df.iterrows():
        if not np.isnan(row.lon) and not np.isnan(row.lat):
            loc = [row.lon, row.lat]
            loc_list.append(loc)
    start_time = df.loc[df.index[0], 'datetime']
    end_time = df.loc[df.index[-1], 'datetime']
    jul = df.loc[df.index[0]].julian_day
    if today:
        glider_order = 4
    else:
        glider_order = int(jul) % 4
    target_item = {
        "type": "Feature",
        "properties": {"popupContent": f"Julian day {int(jul)}",
                       "gliderOrder": glider_order},
        "start": start_time,
        "end": end_time,
        "geometry": {
            "type": "LineString",
            "coordinates": loc_list
        }}
    return target_item


class MissionViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.mission_list = []
        self.targets = blank_json_dict
        self.lon, self.lat = 1.236, 52.624
        self.waypoints = blank_json_dict
        self.waypointdict = blank_json_dict
        self.targetdict = blank_json_dict
        self.start = self.request_dict.start
        self.end = self.request_dict.end
        self.start_time = self.request_dict.start_time
        self.end_time = self.request_dict.end_time
        if self.start_time or self.end_time:
            self.hidef_ship_track = True
        else:
            self.hidef_ship_track = False
        if not self.start:
            self.start_dt = datetime.datetime(2000, 1, 1)
        else:
            if not self.start_time:
                start_hour = 0
                start_min = 0
            else:
                start_hour = int(self.start_time[:2])
                start_min = int(self.start_time[3:])
            self.start_dt = datetime.datetime(int(self.start[:4]), int(self.start[5:7]), int(self.start[8:]),
                                              start_hour, start_min)
        if not self.end:
            self.end_dt = datetime.datetime(2100, 1, 1)
        else:
            if not self.end_time:
                end_hour = 23
                end_min = 59
            else:
                end_hour = int(self.end_time[:2])
                end_min = int(self.end_time[3:])
            self.end_dt = datetime.datetime(int(self.end[:4]), int(self.end[5:7]), int(self.end[8:]),
                                            end_hour, end_min)

    def check_dives(self):
        # dives, mission_gliders, dives_by_glider, most_recent_dives = blank_json_dict, blank_json_dict, blank_json_dict, blank_json_dict
        dives_by_glider = []
        if not dives_by_glider:
            self.zoom = 'No dives yet for this mission'
            self.dive_page_links = []
            self.recentdivesdict = blank_json_dict
            self.dives_by_glider_json = blank_json_dict
            self.dives_by_glider_json_dupe = []
            self.lines_by_glider_json = blank_json_dict
        isobath_dict = {}
        mission_folder = folder + '/static/json/isobaths'
        for depth in [50, 200, 500, 1000]:
            with open(mission_folder + '/isobaths_' + str(depth) + 'm.json', 'r') as myfile:
                json_in = json.load(myfile)
            isobath_dict['depth_' + str(depth) + '_m'] = json.loads(json_in)
        self.isobath_dict = isobath_dict

    def add_events(self):
        event_dir = folder + '/static/nbp_data/'
        for dataset in ['ctd', 'tmc', 'core', 'thor', 'hugin', 'alr', 'vmp', 'ship', 'wp', 'points', 'ship_days',
                        'hugin_bottle', 'fish']:
            try:
                if self.hidef_ship_track and dataset == 'ship':
                    df = pd.read_csv(f"{event_dir}1_min_nrt.csv", parse_dates=['datetime'])
                    df_a = df[df.datetime > self.start_dt]
                    df_cut = df_a[df_a.datetime < self.end_dt]
                    today = df.julian_day.values[-1]
                    jul_days = np.unique(df_cut.julian_day)
                    items = []
                    for day in jul_days:
                        if day == today:
                            last_day = True
                        else:
                            last_day = False
                        df_sub = df_cut[df_cut.julian_day == day]
                        items.append(track_to_json(df_sub, today=last_day))
                    tgtdict = {
                        "type": "FeatureCollection",
                        "features": items
                    }
                    self.__setattr__(f"{dataset}_dict", tgtdict)
                    continue
                with open(f"{event_dir}{dataset}.json") as json_to_load:
                    json_dict = json.load(json_to_load)
                features = json_dict['features']
                features_in_time = []
                for feature in features:
                    try:
                        start = datetime.datetime.fromisoformat(feature['start'])
                    except:
                        try:
                            start = datetime.datetime.fromisoformat(feature['end'])
                        except:
                            features_in_time.append(feature)
                            continue
                    try:
                        end = datetime.datetime.fromisoformat(feature['end'])
                    except:
                        end = start
                    if self.start_dt <= start <= self.end_dt or self.start_dt <= end <= self.end_dt:
                        features_in_time.append(feature)
                    json_dict['features'] = features_in_time
                self.__setattr__(f"{dataset}_dict", json_dict)
            except:
                self.__setattr__(f"{dataset}_dict", blank_json_dict)
        try:
            amsr_dirs = glob.glob(f'{folder}/static/img/tiles/AMSR*')
            amsr_dirs.sort()
            amsr_dict = {}
            for amsr in amsr_dirs:
                amsr_date = amsr.split('/')[-1][-10:]
                date_str = amsr_date.replace('_', '-')
                amsr_dict[date_str] = amsr[-32:]
            self.amsr_dict = amsr_dict
        except:
            self.amsr_dict = {}

        try:
            modis_dirs = glob.glob(f'{folder}/static/img/tiles/MODIS*')
            modis_dirs.sort()
            modis_dict = {}
            for modis in modis_dirs:
                modis_date = modis.split('/')[-1][-8:]
                date_str = f"{modis_date[:4]}-{modis_date[4:6]}-{modis_date[6:]}"
                modis_dict[date_str] = modis[-32:]
            self.modis_dict = modis_dict
        except:
            self.modis_dict = {}

        try:
            polar_dirs = glob.glob(f'{folder}/static/img/tiles/polarview/*')
            polar_dirs.sort()
            polar_dict = {}
            for amsr in polar_dirs:
                amsr_date = amsr.split('/')[-1]
                date_str = f"{amsr_date[:4]}-{amsr_date[4:6]}-{amsr_date[6:8]} {amsr_date[9:11]}:{amsr_date[11:13]}:{amsr_date[13:15]}"
                polar_dict[date_str] = amsr[-42:]
            self.polar_dict = polar_dict
        except:
            self.polar_dict = {}
        self.pre_start_time = self.start_time
        self.pre_end_time = self.end_time
        self.start_time = None
        self.end_time = None
