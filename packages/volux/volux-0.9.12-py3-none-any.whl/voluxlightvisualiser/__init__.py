from volux import VoluxModule
import threading
import numpy as np
import pyaudio
from time import process_time, sleep
import tkinter as tk
from tkinter import ttk


class VoluxLightVisualiser(VoluxModule):
    def __init__(self, mode, packetHz, hueHz,  hue_cycle_duration,
    shared_modules=[], pollrate=100, initial_input_value=0, hue_min=0,
    hue_max=65535, colortemp=6500, min_saturation=0, max_saturation=65535,
    *args, **kwargs):
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
        self.tk_frame = VoluxLightVisualiser_TkFrame
        self.frame_attr = 'vis_frame'
        # self.gui = None  # must be set via _set_gui_instace once self.tk_frame has been initialised elsewhere
        self.input_value = initial_input_value
        self.colortemp = colortemp

        self.minsat = min_saturation
        self.maxsat = max_saturation

        self.mode = mode
        self.packetHz = packetHz  # how often to send network packets to devices
        self.hueHz = hueHz  # how often to increment the hue
        self.hue_min = hue_min
        self.hue_max = hue_max
        self.hue_cycle_duration = hue_cycle_duration

        self._enabled = False  # initial value for _enabled
        self._hue = 0  # initial value for _hue
        self._rel_hue = self._hue  # initial value for _rel_hue

        self.threads = [
            threading.Thread(
                target=self._hue_cycle_func,
                args=(
                    self._get_hue_increment(),
                    1 / self.hueHz,
                    65535/2
                )
            )
        ]

    def get(self):

        return self.mode.get_vis_color(
            input_hue=self._rel_hue,
            input_colortemp=self.colortemp,
            input_value=self.input_value,
            minsat=self.minsat,
            maxsat=self.maxsat,
            minbri=0,
            maxbri=65535
        )

    def get_from_gui(self):

        return self.mode.get_vis_color(
            input_hue=self._rel_hue,
            input_colortemp=self.colortemp,
            input_value=self.input_value,
            minsat=self.gui.mainApp.vis_frame.minsat.get(),
            maxsat=self.gui.mainApp.vis_frame.maxsat.get(),
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

    def _hue_cycle_func(self,hue_increment,time_per_hue_step,input_value_impact):

        while self._enabled == True:

            new_val = self._hue + hue_increment

            rel_input_multiplier = (self.input_value/100)*input_value_impact
            rel_hue = self._hue + rel_input_multiplier

            self._hue = new_val % self.hue_max  # limit the value to hue_max
            self._rel_hue = rel_hue % self.hue_max

            # print("_hue:",self._hue)
            cli_bar_raw_perc = int((self._hue / self.hue_max) * 100)
            cli_bar_rel_perc = int((self._rel_hue / self.hue_max) * 100)
            cli_bar_diff = cli_bar_rel_perc - cli_bar_raw_perc
            full_bar = "#"*cli_bar_raw_perc + "@"*cli_bar_diff
            print("[{:<100}]".format(full_bar))
            # print("[{:<100}]".format("#"*cli_bar_perc))
            # print("_rel_hue:",self._rel_hue)


            sleep(time_per_hue_step)

    def _get_rel_hue(self):

        pass

    def _set_gui_instance(self, gui):

        setattr(self,'gui',gui)

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
        # print("minsat:",minsat)
        # print("maxsat:",maxsat)
        # print("minbri:",minbri)
        # print("maxbri:",maxbri)

        satrange = (maxsat - minsat)
        brirange = (maxbri - minbri)

        # print("satrange:",satrange)
        # print("brirange:",brirange)

        h = input_hue
        s = minsat + (satrange * (input_value/100))  # regular saturation - higher levels = higher saturation
        b = minbri + (brirange * (input_value/100))
        k = input_colortemp

        # print((h,s,b,k))

        return (h, s, b, k)

INTENSE_MODE = IntenseMode()

class VoluxLightVisualiser_TkFrame(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.parent = parent
        self.vis_on = tk.BooleanVar()
        self.minsat = tk.DoubleVar()
        self.maxsat = tk.DoubleVar()

        self.visualiser_title = ttk.Label(self, text="VISUALISER")
        self.visualiser_title.pack()

        self.visualiser_checkbox = ttk.Checkbutton(self, text="Enable", variable=self.vis_on)
        self.visualiser_checkbox.pack()

        self.visualiser_minsat = ttk.Scale(self, from_=0, to=65535, command=self.onScale_minsat)
        self.visualiser_minsat.pack()

        self.visualiser_minsat_label = ttk.Label(self, text=0, textvariable=self.minsat)
        self.visualiser_minsat_label.pack()

        self.visualiser_maxsat = ttk.Scale(self, from_=0, to=65535, command=self.onScale_maxsat)
        self.visualiser_maxsat.pack()

        self.visualiser_maxsat_label = ttk.Label(self, text=0, textvariable=self.maxsat)
        self.visualiser_maxsat_label.pack()

    def onScale_minsat(self, val):

        v = int(float(val))
        self.minsat.set(v)

    def onScale_maxsat(self, val):

        v = int(float(val))
        self.maxsat.set(v)
