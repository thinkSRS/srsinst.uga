##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import time
import numpy as np
from srsgui import Task
from srsgui import InstrumentInput, IntegerInput
from srsinst.rga.plots.timeplot import TimePlot

from srsinst.uga import get_uga


class UGAStateMonitorTask(Task):
    """Monitor UGA pressure and temperature 
    """
    InstrumentName = 'uga to monitor'
    UpdatePeriod = 'update period'
    input_parameters = {
        InstrumentName: InstrumentInput(),
        UpdatePeriod: IntegerInput(2, ' s', 1, 60, 1)
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.uga = get_uga(self, self.params[self.InstrumentName])

        self.ax = self.figure.subplots(nrows=1, ncols=2, sharex=True)

        self.pressure_plot = TimePlot(self, self.ax[0], 'Pressure',
            ['Ion Gauge', 'Pirani Gauge', 'CM Gauge'])
        self.pressure_plot.ax.set_yscale('log')

        self.temperature_plot = TimePlot(self, self.ax[1], 'Temperature',
            ['Chamber', 'Elbow', 'Sample Inlet',
             'Capillary', 'Turbo Pump'])

    def test(self):
        while True:
            if not self.is_running():
                break

            self.display_device_info(device_name=self.params[self.InstrumentName], update=True)

            self.pressure_plot.add_data([self.uga.ig.get_pressure(), self.uga.rp.get_pressure(),
                         self.uga.bp.get_pressure()], True)

            self.temperature_plot.add_data([self.uga.temperature.chamber, self.uga.temperature.elbow,
                         self.uga.temperature.sample_inlet, self.uga.temperature.capillary,
                         self.uga.temperature.turbo_pump], True)

            time.sleep(self.params[self.UpdatePeriod])

    def cleanup(self):
        pass
