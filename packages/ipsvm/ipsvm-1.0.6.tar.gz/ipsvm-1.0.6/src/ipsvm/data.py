import calendar
import os.path
from datetime import datetime, timedelta

import ai.cdas as cdas
import numpy as np
import pandas as pd
import pyprind
from astropy.io import ascii
from dateutil.relativedelta import relativedelta


GAP = -1e31


def trim_data(data, data_min, data_max):
    return data if data.size == 0 else data.loc[(data > data_min) & (data < data_max)]


def drop_duplicates(data):
    return data.loc[~data.index.duplicated(keep="first")]


class Data:
    def __init__(self, field, density, speed):
        self._field = field
        self._density = density
        self._speed = speed

    @property
    def field(self):
        return self._field

    @property
    def density(self):
        return self._density

    @property
    def speed(self):
        return self._speed

    def filter(self, config):
        self._field = drop_duplicates(trim_data(self._field, config["MIN_FIELD"], config["MAX_FIELD"]))
        self._density = drop_duplicates(trim_data(self._density, config["MIN_DENSITY"], config["MAX_DENSITY"]))
        self._speed = drop_duplicates(trim_data(self._speed, config["MIN_SPEED"], config["MAX_SPEED"]))

    def range(self, min_timestamp, max_timestamp):
        return Data(
            self.field.loc[(self.field.index >= min_timestamp) & (self.field.index <= max_timestamp)],
            self.density.loc[(self.density.index >= min_timestamp) & (self.density.index <= max_timestamp)],
            self.speed.loc[(self.speed.index >= min_timestamp) & (self.speed.index <= max_timestamp)],
        )

    @staticmethod
    def get_spacecraft_data(spacecraft, start, end, config):
        spacecraft = config.spacecraft_from_alias(spacecraft)
        if spacecraft == "ACE":
            data = Data.get_ace_data(start, end, config)
        elif spacecraft == "DSCOVR":
            data = Data.get_dscovr_data(start, end, config)
        elif spacecraft == "HELIOSA":
            data = Data.get_heliosa_data(start, end, config)
        elif spacecraft == "HELIOSB":
            data = Data.get_heliosb_data(start, end, config)
        elif spacecraft == "OMNI":
            data = Data.get_omni_data(start, end, config)
        elif spacecraft == "STEREOA":
            data = Data.get_stereoa_data(start, end, config)
        elif spacecraft == "STEREOB":
            data = Data.get_stereob_data(start, end, config)
        elif spacecraft == "ULYSSES":
            data = Data.get_ulysses_data(start, end, config)
        elif spacecraft == "VOYAGER1":
            data = Data.get_voyager1_data(start, end, config)
        elif spacecraft == "VOYAGER2":
            data = Data.get_voyager2_data(start, end, config)
        elif spacecraft == "WIND":
            data = Data.get_wind_data(start, end, config)
        return data

    @staticmethod
    def get_ace_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "AC_H0_MFI",
                start,
                end,
                ["Magnitude"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            field_key = "Magnitude" if config["DOWNLOAD_CDF"] else "<|B|>"
            mask = field_data[field_key] != GAP
            field = pd.Series(
                field_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "AC_H0_SWE",
                start,
                end,
                ["Vp", "Np"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "Np" if config["DOWNLOAD_CDF"] else "H_DENSITY"
            speed_key = "Vp" if config["DOWNLOAD_CDF"] else "SW_H_SPEED"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_dscovr_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "DSCOVR_H0_MAG",
                start,
                end,
                ["B1F1"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch1" if config["DOWNLOAD_CDF"] else "EPOCH"
            field_key = "B1F1" if config["DOWNLOAD_CDF"] else "B"
            mask = field_data[field_key] != GAP
            field = pd.Series(
                field_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "DSCOVR_H1_FC",
                start,
                end,
                ["V_GSE", "Np"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "Np" if config["DOWNLOAD_CDF"] else "ION_N"
            if config["DOWNLOAD_CDF"]:
                if plasma_data[epoch_key].size == 1:
                    plasma_data["V_GSE"] = np.array([plasma_data["V_GSE"]])
                mask = np.all(plasma_data["V_GSE"] != GAP, axis=1)
                speed = pd.Series(
                    np.sqrt(
                        plasma_data["V_GSE"][mask, 0] ** 2
                        + plasma_data["V_GSE"][mask, 1] ** 2
                        + plasma_data["V_GSE"][mask, 2] ** 2
                    ),
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
                )
            else:
                mask = (
                    (plasma_data["VX_(GSE)"] != GAP)
                    & (plasma_data["VY_(GSE)"] != GAP)
                    & (plasma_data["VZ_(GSE)"] != GAP)
                )
                speed = pd.Series(
                    np.sqrt(
                        plasma_data["VX_(GSE)"][mask] ** 2
                        + plasma_data["VY_(GSE)"][mask] ** 2
                        + plasma_data["VZ_(GSE)"][mask] ** 2
                    ),
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
                )
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()

        return Data(field, density, speed)

    @staticmethod
    def get_heliosa_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "HELIOS1_40SEC_MAG-PLASMA",
                start,
                end,
                ["Vp", "Np", "B_R", "B_T", "B_N"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "Np" if config["DOWNLOAD_CDF"] else "N_P"
            speed_key = "Vp" if config["DOWNLOAD_CDF"] else "V_P"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "HEL1_6SEC_NESSMAG",
                start,
                end,
                ["B"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            mask = field_data["B"] != GAP
            field = pd.Series(
                field_data["B"][mask], index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]]
            )
        except:
            try:
                epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
                mask = (plasma_data["B_R"] != GAP) & (plasma_data["B_T"] != GAP) & (plasma_data["B_N"] != GAP)
                field = pd.Series(
                    np.sqrt(
                        plasma_data["B_R"][mask] ** 2 + plasma_data["B_T"][mask] ** 2 + plasma_data["B_N"][mask] ** 2
                    ),
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
                )
            except:
                field = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_heliosb_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "HELIOS2_40SEC_MAG-PLASMA",
                start,
                end,
                ["Vp", "Np", "B_R", "B_T", "B_N"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "Np" if config["DOWNLOAD_CDF"] else "N_P"
            speed_key = "Vp" if config["DOWNLOAD_CDF"] else "V_P"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "HEL2_6SEC_NESSMAG",
                start,
                end,
                ["B"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            mask = field_data["B"] != GAP
            field = pd.Series(
                field_data["B"][mask], index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]]
            )
        except:
            try:
                epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
                mask = (plasma_data["B_R"] != GAP) & (plasma_data["B_T"] != GAP) & (plasma_data["B_N"] != GAP)
                field = pd.Series(
                    np.sqrt(
                        plasma_data["B_R"][mask] ** 2 + plasma_data["B_T"][mask] ** 2 + plasma_data["B_N"][mask] ** 2
                    ),
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
                )
            except:
                field = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_omni_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_plasma_data = cdas.get_data(
                "sp_phys",
                "OMNI_HRO_1MIN",
                start,
                end,
                ["F", "flow_speed", "proton_density"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH_TIME"
            field_key = "F" if config["DOWNLOAD_CDF"] else "MAG_AVG_B-VECTOR"
            density_key = "proton_density" if config["DOWNLOAD_CDF"] else "PROTON_DENSITY"
            speed_key = "flow_speed" if config["DOWNLOAD_CDF"] else "FLOW_SPEED,_GSE"
            mask = field_plasma_data[field_key] != GAP
            field = pd.Series(
                field_plasma_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_plasma_data[epoch_key][mask]],
            )
            mask = field_plasma_data[speed_key] != GAP
            speed = pd.Series(
                field_plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_plasma_data[epoch_key][mask]],
            )
            mask = field_plasma_data[density_key] != GAP
            density = pd.Series(
                field_plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_plasma_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
            speed = pd.Series()
            density = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_stereoa_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "STA_L1_MAG_RTN",
                start,
                end,
                ["BFIELD"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            if config["DOWNLOAD_CDF"]:
                if field_data["Epoch"].size == 1:
                    field_data["BFIELD"] = np.array([field_data["BFIELD"]])
                mask = field_data["BFIELD"][:, 3] != GAP
                field = pd.Series(
                    field_data["BFIELD"][mask, 3],
                    index=[calendar.timegm(dt.timetuple()) for dt in field_data["Epoch"][mask]],
                )
            else:
                mask = field_data["BTOTAL"] != GAP
                field = pd.Series(
                    field_data["BTOTAL"][mask],
                    index=[calendar.timegm(dt.timetuple()) for dt in field_data["EPOCH"][mask]],
                )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "STA_L2_PLA_1DMAX_1MIN",
                start,
                end,
                ["proton_bulk_speed", "proton_number_density"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "proton_number_density" if config["DOWNLOAD_CDF"] else "DENSITY"
            speed_key = "proton_bulk_speed" if config["DOWNLOAD_CDF"] else "SPEED"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_stereob_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "STB_L1_MAG_RTN",
                start,
                end,
                ["BFIELD"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            if config["DOWNLOAD_CDF"]:
                if field_data["Epoch"].size == 1:
                    field_data["BFIELD"] = np.array([field_data["BFIELD"]])
                mask = field_data["BFIELD"][:, 3] != GAP
                field = pd.Series(
                    field_data["BFIELD"][mask, 3],
                    index=[calendar.timegm(dt.timetuple()) for dt in field_data["Epoch"][mask]],
                )
            else:
                mask = field_data["BTOTAL"] != GAP
                field = pd.Series(
                    field_data["BTOTAL"][mask],
                    index=[calendar.timegm(dt.timetuple()) for dt in field_data["EPOCH"][mask]],
                )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "STB_L2_PLA_1DMAX_1MIN",
                start,
                end,
                ["proton_bulk_speed", "proton_number_density"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "proton_number_density" if config["DOWNLOAD_CDF"] else "DENSITY"
            speed_key = "proton_bulk_speed" if config["DOWNLOAD_CDF"] else "SPEED"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_ulysses_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "UY_1SEC_VHM",
                start,
                end,
                ["B_MAG"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH_TIME"
            field_key = "B_MAG" if config["DOWNLOAD_CDF"] else "MAGNETIC_FIELD_MAGNITUDE"
            mask = field_data[field_key] != GAP
            field = pd.Series(
                field_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "UY_M0_BAI",
                start,
                end,
                ["Velocity", "Density"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            if config["DOWNLOAD_CDF"]:
                if plasma_data["Epoch"].size == 1:
                    plasma_data["Density"] = np.array([plasma_data["Density"]])
                    plasma_data["Velocity"] = np.array([plasma_data["Velocity"]])
                mask = plasma_data["Density"][:, 0] != GAP
                density = pd.Series(
                    plasma_data["Density"][mask, 0],
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["Epoch"][mask]],
                )
                mask = np.all(plasma_data["Velocity"] != GAP, axis=1)
                speed = pd.Series(
                    np.sqrt(
                        plasma_data["Velocity"][mask, 0] ** 2
                        + plasma_data["Velocity"][mask, 1] ** 2
                        + plasma_data["Velocity"][mask, 2] ** 2
                    ),
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["Epoch"][mask]],
                )
            else:
                mask = plasma_data["PROTON"] != GAP
                density = pd.Series(
                    plasma_data["PROTON"][mask],
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["TIME"][mask]],
                )
                mask = (plasma_data["VEL_R"] != GAP) & (plasma_data["VEL_T"] != GAP) & (plasma_data["VEL_N"] != GAP)
                speed = pd.Series(
                    np.sqrt(
                        plasma_data["VEL_R"][mask] ** 2
                        + plasma_data["VEL_T"][mask] ** 2
                        + plasma_data["VEL_N"][mask] ** 2
                    ),
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["TIME"][mask]],
                )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_voyager1_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "VOYAGER1_2S_MAG",
                start,
                end,
                ["F1"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch2" if config["DOWNLOAD_CDF"] else "EPOCH"
            field_key = "F1" if config["DOWNLOAD_CDF"] else "B-MAGNITUDE_(F1)"
            mask = field_data[field_key] != GAP
            field = pd.Series(
                field_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "VOYAGER1_PLS_HIRES_PLASMA_DATA",
                start,
                end,
                ["V", "dens"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "dens" if config["DOWNLOAD_CDF"] else "PROTON_DENSITY"
            speed_key = "V" if config["DOWNLOAD_CDF"] else "VP"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_voyager2_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "VOYAGER2_2S_MAG",
                start,
                end,
                ["F1"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch2" if config["DOWNLOAD_CDF"] else "EPOCH"
            field_key = "F1" if config["DOWNLOAD_CDF"] else "B-MAGNITUDE_(F1)"
            mask = field_data[field_key] != GAP
            field = pd.Series(
                field_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "VOYAGER2_PLS_HIRES_PLASMA_DATA",
                start,
                end,
                ["V", "dens"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch" if config["DOWNLOAD_CDF"] else "EPOCH"
            density_key = "dens" if config["DOWNLOAD_CDF"] else "PROTON_DENSITY"
            speed_key = "V" if config["DOWNLOAD_CDF"] else "VP"
            mask = plasma_data[density_key] != GAP
            density = pd.Series(
                plasma_data[density_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
            mask = plasma_data[speed_key] != GAP
            speed = pd.Series(
                plasma_data[speed_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in plasma_data[epoch_key][mask]],
            )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def get_wind_data(start, end, config):
        if config["CACHE"] is not None and os.path.isdir(config["CACHE"]):
            cdas.set_cache(True, config["CACHE"])
        else:
            cdas.set_cache(False)
        try:
            field_data = cdas.get_data(
                "sp_phys",
                "WI_H0_MFI",
                start,
                end,
                ["B3F1"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            epoch_key = "Epoch3" if config["DOWNLOAD_CDF"] else "EPOCH"
            field_key = "B3F1" if config["DOWNLOAD_CDF"] else "B"
            mask = field_data[field_key] != GAP
            field = pd.Series(
                field_data[field_key][mask],
                index=[calendar.timegm(dt.timetuple()) for dt in field_data[epoch_key][mask]],
            )
        except:
            field = pd.Series()
        try:
            plasma_data = cdas.get_data(
                "sp_phys",
                "WI_K0_SWE",
                start,
                end,
                ["V_GSE_plog", "Np"],
                cdf=config["DOWNLOAD_CDF"],
                progress=config["DOWNLOAD_PROGRESS"],
            )
            if config["DOWNLOAD_CDF"]:
                mask = plasma_data["Np"] != GAP
                density = pd.Series(
                    plasma_data["Np"][mask], index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["Epoch"][mask]]
                )
                if plasma_data["Epoch"].size == 1:
                    plasma_data["V_GSE_p"] = np.array([plasma_data["V_GSE_p"]])
                mask = plasma_data["V_GSE_p"][:, 0] != GAP
                speed = pd.Series(
                    plasma_data["V_GSE_p"][mask, 0],
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["Epoch"][mask]],
                )
            else:
                mask = plasma_data["ION_NP"] != GAP
                density = pd.Series(
                    plasma_data["ION_NP"][mask], index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["EPOCH"][mask]]
                )
                mask = plasma_data["FLOW_SPEED"] != GAP
                speed = pd.Series(
                    plasma_data["FLOW_SPEED"][mask],
                    index=[calendar.timegm(dt.timetuple()) for dt in plasma_data["EPOCH"][mask]],
                )
        except:
            density = pd.Series()
            speed = pd.Series()
        return Data(field, density, speed)

    @staticmethod
    def download_monthly_data(spacecraft, config):
        spacecraft = config.spacecraft_from_alias(spacecraft)
        shocks = ascii.read(config["SPACECRAFT"][spacecraft]["TRUE_POSITIVES_LIST"])
        shock_datetimes = np.array(
            [datetime(row["col1"], row["col2"], row["col3"], row["col4"], row["col5"], row["col6"]) for row in shocks]
        )
        shock_datetimes.sort()
        first_shock_datetime = np.amin(shock_datetimes)
        last_shock_datetime = np.amax(shock_datetimes)

        start = datetime(first_shock_datetime.year, first_shock_datetime.month, 1)
        end = start + relativedelta(months=1)

        bar = pyprind.ProgPercent(
            (last_shock_datetime.year - first_shock_datetime.year - 1) * 12
            + last_shock_datetime.month
            + (12 - first_shock_datetime.month + 1),
            track_time=True,
        )

        while start - timedelta(minutes=config["MAX_SCAN_WINDOW"] + config["SCAN_STEP"]) < last_shock_datetime:
            Data.get_spacecraft_data(
                spacecraft,
                start - timedelta(minutes=config["MAX_SCAN_WINDOW"] + config["SCAN_STEP"]),
                end + timedelta(minutes=config["MAX_SCAN_WINDOW"] + config["SCAN_STEP"]),
                config,
            )
            start += relativedelta(months=1)
            end += relativedelta(months=1)
            bar.update()
