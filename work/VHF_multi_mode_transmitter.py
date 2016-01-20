#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: V/HF mult-imode transmitter
# Author: Alex Stewart
# Description: basic multimode transmitter
# Generated: Wed Jan 20 16:16:07 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class VHF_multi_mode_transmitter(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="V/HF mult-imode transmitter")

        ##################################################
        # Variables
        ##################################################
        self.var_1 = var_1 = 145100000
        self.var_text = var_text = var_1
        self.tx_mode = tx_mode = 0,0,1
        self.tx_freq = tx_freq = 1500,-1500,-1500
        self.tune = tune = 0
        self.side_band = side_band = 2
        self.samp_rate = samp_rate = 1.515152e6
        self.pwr = pwr = .11,.11,.11,.11,.11,.11,.0,0,.11
        self.lo_freq_Hz = lo_freq_Hz = (145.1e6,145.11e6,14.070e6,14.236e6,28.720e6,10.0e6,15.0e6,var_1)
        self.hi_lo = hi_lo = 1
        self.freq_chooser = freq_chooser = 0
        self.fine_tune = fine_tune = 0
        self.chooser = chooser = 1

        ##################################################
        # Blocks
        ##################################################
        _tune_sizer = wx.BoxSizer(wx.VERTICAL)
        self._tune_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_tune_sizer,
        	value=self.tune,
        	callback=self.set_tune,
        	label="Coarse Tune",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._tune_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_tune_sizer,
        	value=self.tune,
        	callback=self.set_tune,
        	minimum=-61000,
        	maximum=61000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_tune_sizer, 3, 1, 1, 1)
        self._side_band_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.side_band,
        	callback=self.set_side_band,
        	label="  Sideband",
        	choices=[0,1,2],
        	labels=['LSB','USB','CW'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._side_band_chooser, 3, 2, 1, 1)
        self._hi_lo_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.hi_lo,
        	callback=self.set_hi_lo,
        	label="Power Level",
        	choices=[1,2],
        	labels=['Low','High'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._hi_lo_chooser, 4, 2, 1, 1)
        self._freq_chooser_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.freq_chooser,
        	callback=self.set_freq_chooser,
        	label="FREQUENCY SELECT",
        	choices=[0,1,2,3,4,5,6,7],
        	labels=['145.100','145.110','14.070','14.236','28.720','10','15','PRESET'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._freq_chooser_chooser, 1, 1, 1, 1)
        _fine_tune_sizer = wx.BoxSizer(wx.VERTICAL)
        self._fine_tune_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_fine_tune_sizer,
        	value=self.fine_tune,
        	callback=self.set_fine_tune,
        	label="Fine Tune",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._fine_tune_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_fine_tune_sizer,
        	value=self.fine_tune,
        	callback=self.set_fine_tune,
        	minimum=-5000/2,
        	maximum=5000/2,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_fine_tune_sizer, 4, 1, 1, 1)
        self._chooser_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.chooser,
        	callback=self.set_chooser,
        	label="TX-RX Selector",
        	choices=[1,0],
        	labels=["Receive","Transmit"],
        )
        self.GridAdd(self._chooser_chooser, 6, 1, 2, 1)
        self._var_text_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.var_text,
        	callback=self.set_var_text,
        	label="PRESET FREQUENCY",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._var_text_static_text, 1, 2, 1, 1)
        self.pfb_interpolator_ccf_0 = pfb.interpolator_ccf(
        	  8,
        	  (),
        	  100)
        self.pfb_interpolator_ccf_0.declare_sample_delay(0)
        	
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate/4)
        self.osmosdr_sink_0.set_center_freq(lo_freq_Hz[freq_chooser]+tune+fine_tune-(tx_freq[side_band]), 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.fft_filter_xxx_0_0_0_0_0 = filter.fft_filter_fff(1, (firdes.band_pass(1,samp_rate/32, 250, 3500, 400)), 1)
        self.fft_filter_xxx_0_0_0_0_0.declare_sample_delay(0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate/32,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_vcc(((pwr[freq_chooser]*hi_lo), ))
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_vff((40*10, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blks2_valve_1 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(chooser))
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=tx_mode[side_band],
        	output_index=0,
        )
        self.band_pass_filter_0 = filter.interp_fir_filter_ccf(1, firdes.band_pass(
        	1, 47348, 150, 1500, 300, firdes.WIN_HAMMING, 6.76))
        self.audio_source_0_0 = audio.source(47348, "", True)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate/32, analog.GR_COS_WAVE, tx_freq[side_band], 1, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, (0.070)*9)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.audio_source_0_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.blks2_selector_0, 0), (self.blocks_multiply_const_vxx_1_0_0_0, 0))    
        self.connect((self.blks2_valve_1, 0), (self.pfb_interpolator_ccf_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.fft_filter_xxx_0_0_0_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blks2_valve_1, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blks2_selector_0, 1))    
        self.connect((self.fft_filter_xxx_0_0_0_0_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.pfb_interpolator_ccf_0, 0), (self.osmosdr_sink_0, 0))    

    def get_var_1(self):
        return self.var_1

    def set_var_1(self, var_1):
        self.var_1 = var_1
        self.set_var_text(self.var_1)
        self.set_lo_freq_Hz((145.1e6,145.11e6,14.070e6,14.236e6,28.720e6,10.0e6,15.0e6,self.var_1))

    def get_var_text(self):
        return self.var_text

    def set_var_text(self, var_text):
        self.var_text = var_text
        self._var_text_static_text.set_value(self.var_text)

    def get_tx_mode(self):
        return self.tx_mode

    def set_tx_mode(self, tx_mode):
        self.tx_mode = tx_mode
        self.blks2_selector_0.set_input_index(int(self.tx_mode[self.side_band]))

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.analog_sig_source_x_0_0.set_frequency(self.tx_freq[self.side_band])
        self.osmosdr_sink_0.set_center_freq(self.lo_freq_Hz[self.freq_chooser]+self.tune+self.fine_tune-(self.tx_freq[self.side_band]), 0)

    def get_tune(self):
        return self.tune

    def set_tune(self, tune):
        self.tune = tune
        self._tune_slider.set_value(self.tune)
        self._tune_text_box.set_value(self.tune)
        self.osmosdr_sink_0.set_center_freq(self.lo_freq_Hz[self.freq_chooser]+self.tune+self.fine_tune-(self.tx_freq[self.side_band]), 0)

    def get_side_band(self):
        return self.side_band

    def set_side_band(self, side_band):
        self.side_band = side_band
        self._side_band_chooser.set_value(self.side_band)
        self.analog_sig_source_x_0_0.set_frequency(self.tx_freq[self.side_band])
        self.blks2_selector_0.set_input_index(int(self.tx_mode[self.side_band]))
        self.osmosdr_sink_0.set_center_freq(self.lo_freq_Hz[self.freq_chooser]+self.tune+self.fine_tune-(self.tx_freq[self.side_band]), 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate/32)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate/32)
        self.fft_filter_xxx_0_0_0_0_0.set_taps((firdes.band_pass(1,self.samp_rate/32, 250, 3500, 400)))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate/4)

    def get_pwr(self):
        return self.pwr

    def set_pwr(self, pwr):
        self.pwr = pwr
        self.blocks_multiply_const_vxx_1_0_0_0.set_k(((self.pwr[self.freq_chooser]*self.hi_lo), ))

    def get_lo_freq_Hz(self):
        return self.lo_freq_Hz

    def set_lo_freq_Hz(self, lo_freq_Hz):
        self.lo_freq_Hz = lo_freq_Hz
        self.osmosdr_sink_0.set_center_freq(self.lo_freq_Hz[self.freq_chooser]+self.tune+self.fine_tune-(self.tx_freq[self.side_band]), 0)

    def get_hi_lo(self):
        return self.hi_lo

    def set_hi_lo(self, hi_lo):
        self.hi_lo = hi_lo
        self._hi_lo_chooser.set_value(self.hi_lo)
        self.blocks_multiply_const_vxx_1_0_0_0.set_k(((self.pwr[self.freq_chooser]*self.hi_lo), ))

    def get_freq_chooser(self):
        return self.freq_chooser

    def set_freq_chooser(self, freq_chooser):
        self.freq_chooser = freq_chooser
        self.blocks_multiply_const_vxx_1_0_0_0.set_k(((self.pwr[self.freq_chooser]*self.hi_lo), ))
        self.osmosdr_sink_0.set_center_freq(self.lo_freq_Hz[self.freq_chooser]+self.tune+self.fine_tune-(self.tx_freq[self.side_band]), 0)
        self._freq_chooser_chooser.set_value(self.freq_chooser)

    def get_fine_tune(self):
        return self.fine_tune

    def set_fine_tune(self, fine_tune):
        self.fine_tune = fine_tune
        self._fine_tune_slider.set_value(self.fine_tune)
        self._fine_tune_text_box.set_value(self.fine_tune)
        self.osmosdr_sink_0.set_center_freq(self.lo_freq_Hz[self.freq_chooser]+self.tune+self.fine_tune-(self.tx_freq[self.side_band]), 0)

    def get_chooser(self):
        return self.chooser

    def set_chooser(self, chooser):
        self.chooser = chooser
        self._chooser_chooser.set_value(self.chooser)
        self.blks2_valve_1.set_open(bool(self.chooser))


def main(top_block_cls=VHF_multi_mode_transmitter, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
