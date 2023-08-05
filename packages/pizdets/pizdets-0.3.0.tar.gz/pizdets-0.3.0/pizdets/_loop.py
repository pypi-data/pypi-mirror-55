import schedule
import time, os
import pandas as pd, numpy as np

#%%
def pause_mixers_and_measure_OD(self):
    self.mix(0)
    time.sleep(3)
    self.record()
    self.mix(1)

def make_dilution(self,tube,death_volume=0, peace_volume=0,extra_vacuum=5):
    self.mix(1)
    if death_volume>0:
        self.pump_death(tube, death_volume)
    if peace_volume>0:
        self.pump_peace(tube, peace_volume)
    self.vacuum(tube, death_volume+peace_volume)
    self.mix(0)
    self.vacuum(tube, extra_vacuum)
    self.mix(1)

def read_thresholds_from_file(self):
    thresholds = pd.read_csv(os.path.join(self.files.main_folder, "thresholds.csv"), header=None).values[0]
    thresholds = np.array(thresholds.ravel()).astype(int)
    return thresholds


def read_last_OD_values(self):
    self.df_update()
    lastvals = np.array(self.df.iloc[-1, 1::4])
    return lastvals

def read_death_volumes():
    dv = pd.read_csv(os.path.join(self.files.main_folder, "death_volumes.csv"), header=None).values[0]
    new_death_volumes = np.array(dv.ravel()).astype(float)
    assert len(new_death_volumes) == 7
    assert all(new_death_volumes < 10)
    return new_death_volumes

def dilute_if_necessary(self,tube, total_dilution_volume=10):
    thresholds = read_thresholds_from_file()  # 7 OD thresholds
    ODvalues = read_last_OD_values()  # 7 OD values
    death_volumes = read_death_volumes()  # 7 death volumes
    peace_volumes = total_dilution_volume - death_volumes

    if ODvalues[tube] < thresholds[tube]:
        make_dilution(death_volume = death_volumes[tube],
                      peace_volume = peace_volumes[tube],
                      extra_vacuum = 5)


def experiment_loop(self):

    schedule.every().minute.at(":00").do(pause_mixers_and_measure_OD)
    schedule.every().minute.at(":05").do(dilute_if_necessary, total_dilution_volume=10)
    schedule.every().minute.at(":30").do(pause_mixers_and_measure_OD, total_dilution_volume=10)
    schedule.every().minute.at(":35").do(dilute_if_necessary)

    for t in range(7): # wash peace and vacuum tubes to prevent drying out
        schedule.every().day.at("9:30").do(make_dilution, tube=t, peace_volume=1)


    while True:
        schedule.run_pending()
        time.sleep(1)


