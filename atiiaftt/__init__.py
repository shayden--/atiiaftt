"""
Force-Torque transform library for ATI-IA FT Sensors.

This module uses cffi to wrap the MIT licensed c library released by
ATI-IA for force-torque sensors.

The tranform functions may be called by importing the cffi module and 
calling the application interfaces directly, or the wrapper classes 
may be used to call the functions with more pythonic methods.

Usage examples are found in 'ftconvert.py'

This module does not provide any access to hardware, a module such as 
'NI-DAQmx', matching the ADC, must be used to aquire data first.

Copyright (c) 2018 Tyson Boer

The MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

name = "atiiaftt"

__all__ = ['FTUnit','FTSensor']

from .ft_interface import FTUnit
from .ft_interface import FTSensor

