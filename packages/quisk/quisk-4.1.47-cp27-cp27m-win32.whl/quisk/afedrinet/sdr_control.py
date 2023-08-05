#!/usr/bin/python           # This is client.py file
import os,sys
os.environ['PATH'] = os.path.dirname(__file__) + ';' + os.environ['PATH']

#import array
#import socket               # Import socket module
from afedri import *
#import afedri

class Control:
  def __init__(self, sdr_address="192.168.0.8", sdr_port=50000):
	self.hw = afedri(sdr_address, sdr_port)
	if self.hw.s is None:	# Failure to find the hardware
		self.hw = None
  def OpenHW(self):
	if not self.hw: return
	data  = self.hw.get_sdr_name()
	print data[4:]
	self.hw.start_capture()
  def CloseHW(self):
	if not self.hw: return
	self.hw.stop_capture()
	self.hw.close                     # Close the socket when done
  def SetHWLO(self, vfo):
	if not self.hw: return
	self.hw.set_center_freq(vfo)
  def SetHWSR(self, sample_rate):
	if not self.hw: return
	self.hw.set_samp_rate(sample_rate)
	print "Sample Rate %i" % sample_rate
  def SetAttenuator(self, indx):
	if not self.hw: return
	self.hw.set_gain_indx(indx)


