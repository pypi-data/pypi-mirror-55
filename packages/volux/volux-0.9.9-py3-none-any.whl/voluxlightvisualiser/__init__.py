from volux import VoluxModule
import threading
import numpy as np
import pyaudio
from time import process_time


class VoluxLightVisualiser(VoluxModule):
    def __init__(self, mode, packetHz, hueHz,  hue_cycle_duration,
    shared_modules=[], pollrate=100, initial_input_value=0, hue_min=0,
    hue_max=65535, colortemp=6500, *args, **kwargs):
        super().__init__(
            module_name="Volux Light Visualiser",
            module_attr="vis",
            module_get=self.get,
            get_type=tuple,
            get_min=(0,0,0,0),
            get_max=(65535,65535,65535,9000),
            module_set=self.set,
            set_type=float,
            set_min=0,
            set_max=100,
            shared_modules=shared_modules,
            pollrate=pollrate
        )
        self.input_value = initial_input_value
        self.colortemp = colortemp

        self.mode = mode
        self.packetHz = packetHz  # how often to send network packets to devices
        self.hueHz = hueHz  # how often to increment the hue
        self.hue_min = hue_min
        self.hue_max = hue_max
        self.hue_cycle_duration = hue_cycle_duration

        self._enabled = False  # initial value for _enabled
        self._hue = 0  # initial value for _hue

        self.threads = [
            threading.Thread(
                target=self._hue_cycle_func,
                args=(
                    self._get_hue_increment(),
                    1 / self.hueHz
                )
            )
        ]

    def get(self):

        return self.mode.get_vis_color(
            input_hue=self._hue,
            input_colortemp=self.colortemp,
            input_value=self.input_value,
            minsat=0,
            maxsat=65535,
            minbri=0,
            maxbri=65535
        )

    def set(self, new_val):

        self.input_value = new_val  # 0 .. 100

    def start(self):

        if self._enabled == True:

            raise Exception("already enabled!")

        elif self._enabled == False:

            self._enabled = True
            self._start_threads()

        else:

            raise Exception("'enabled' should be bool")

    def stop(self):

        self._enabled = False

    def _start_threads(self):

        for thread in self.threads:
            thread.start()

    def _get_hue_increment(self):

        return (self.hue_max / self.hueHz) / self.hue_cycle_duration

    def _hue_cycle_func(self,hue_increment,time_per_hue_step):

        while self._enabled == True:

            t1 = process_time()
            new_val = self._hue + hue_increment  # add increment to current value
            self._hue = new_val % self.hue_max  # limit the value to hue_max
            t2 = process_time()

            while (t2 - t1 < time_per_hue_step):
                t2 = process_time()

    def _get_rel_hue(self):

        pass

class VisMode:
    def __init__(self,vis_color_method,*args,**kwargs):
        self.get_vis_color = vis_color_method

class IntenseMode(VisMode):
    def __init__(self,*args,**kwargs):
        super().__init__(
            vis_color_method=self.get_color_method,
        )

    def get_color_method(self,input_hue,input_colortemp,input_value,minsat,maxsat,minbri,maxbri):

        # print("---get vis color wip---")
        # print("input_hue:",input_hue)
        # print("input_colortemp:",input_colortemp)
        # print("input_value:",input_value)
        # print("input_value/100:",input_value/100)

        # h = 0
        # s = 0
        # b = 65535 * (input_value/100)
        # k = 6500

        h = input_hue
        s = maxsat * (input_value/100)  # regular saturation - higher levels = higher saturation
        b = maxbri * (input_value/100)
        k = input_colortemp

        # print((h,s,b,k))

        return (h, s, b, k)

INTENSE_MODE = IntenseMode()
