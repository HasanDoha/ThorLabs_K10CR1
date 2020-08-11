#!/usr/bin/env python



import InstrumentDriver

import thorlabs_apt as apt

import thorlabs_apt.core as apt_core

from collections import Counter

import ctypes
import os, time


class Driver(InstrumentDriver.InstrumentWorker):

    """ This class implements the Ocean Optics Spectrometer"""

    

    def performOpen(self, options={}):

        """Perform the operation of opening the instrument connection"""

        # init object

        self.motor = None

        try:

            # open connection

            #devices = sb.list_devices()
            devices = apt.list_available_devices()

            # check if devices available

            if len(devices) == 0:

                # no devices found

                raise Exception('No motor found')

            elif len(devices) == 1:

                # one device, use

                #self.spec = sb.Spectrometer(devices[0])
                self.motor = apt.Motor(55000409)
                self.motor.move_home()

            else:

                # many devices, look for serial

                #self.spec = sb.Spectrometer.from_serial_number(self.comCfg.address)
                self.motor = apt.Motor(55000409)
                self.motor.move_home()

        except Exception as e:

            # re-cast errors as a generic communication error

            raise InstrumentDriver.CommunicationError(str(e))





    def performClose(self, bError=False, options={}):

        """Perform the close instrument connection operation"""

        # check if digitizer object exists

        try:

            if self.motor is None:

                # do nothing, object doesn't exist (probably was never opened)

                return

        except:

            # never return error here, do nothing, object doesn't exist

            return

        try:

            # close and remove object

            self.motor._cleanup()

            del self.motor

        except:

            # never return error here

            pass





    def performSetValue(self, quant, value, sweepRate=0.0, options={}):

        """Perform the Set Value instrument operation. This function should

        return the actual value set by the instrument"""

        # check quantity
        ##======================================================##
        ##  loading the rotator motor to rotate the polarizer   ##
        ##  motor serial number ::  55000409                    ##
        ##  minimum velocity    ::  0.000 degree/second         ##
        ##  accleration         ::  9.999 degrees/second^2      ##
        ##  maximum velocity    ::  10.000 degrees/second       ##
        ##======================================================##

        if quant.name == 'Velocity':

            # conversion from s -> us

            #self.spec.integration_time_micros(int(value*1E6))
            #self.motor.integration_time_micros(int(value*1E6))
            self.motor.set_velocity_parameters(0.000, 9.999, value)

        elif quant.name == 'Move To':

            # temperature set point

            #self.spec.tec_set_temperature_C(value)
            
            self.motor.move_to(value,blocking=True)
            #current_position = self.motor.position()
            #if abs(self.motor.position() - value)>.5:
            #    self.motor.move_home()
            #self.motor.move_to(value,blocking=True)
        return value





    def performGetValue(self, quant, options={}):

        """Perform the Get Value instrument operation"""

        # check type of quantity

        if quant.name == 'Current Position':

            # temperature

            value = self.motor.position

        """elif quant.name == 'Intensity':

		    # get number of averages
            numavgs = self.getValue('Navgs')
		
            # get wavelength and intensity

            vX = self.spec.wavelengths()
            vY = self.spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
            
            for i in range(int(numavgs)-1):				                
                vY += self.spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
                
            vY /= numavgs
            
			# assume equally-spaced waveform values
			
            value = quant.getTraceDict(vY, dt=vX[1]-vX[0], t0=vX[0])

			
        elif quant.name == 'DeltaR':
		
			 # get number of averages
            numavgs = self.getValue('Navgs')
		
            # get wavelength and intensity

            vX = self.spec.wavelengths()

            vY1 = self.spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
            
            for i in range(int(numavgs)-1):				                
                vY1 += self.spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
       
	        # write down the value on the sample.  assume equally-spaced waveform values

            vY1 /= numavgs
            			
			#move the stage
            ctypes.windll.user32.MessageBoxA(0, "Move the stage!", "Stage Move Time", 1)

			
            vY2 = self.spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
            
            for i in range(int(numavgs)-1):				                
                vY2 += self.spec.intensities(correct_dark_counts=False, correct_nonlinearity=False)
 
			# write down the value off of the sample.  assume equally-spaced waveform values        
            vY2 /= numavgs
            
			#calculate deltaR / R
            vY = 1 - vY1/vY2
			
            value = Counter(quant.getTraceDict(vY, dt=vX[1]-vX[0], t0=vX[0]))"""
			
        return value

        



if __name__ == '__main__':

    pass

