# Copyright (c) 2019, NewAE Technology Inc
# All rights reserved.
#
#
# Find this and more at newae.com - this file is part of the PhyWhisperer-USB
# project, https://github.com/newaetech/phywhispererusb
#
#    This file is part of PhyWhisperer-USB.
#
#    PhyWhisperer-USB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PhyWhisperer-USB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PhyWhisperer-USB.  If not, see <http://www.gnu.org/licenses/>.
#=================================================

import phywhisperer.interface.naeusb as NAE
import phywhisperer.interface.program_fpga as LLINT
import sys
import os
import re
import logging
import pkg_resources
import threading
import time
from phywhisperer.interface.bootloader_sam3u import Samba
from phywhisperer.sniffer import USBSniffer, USBSimplePrintSink
from phywhisperer.protocol import PWPacketDispatcher, PWPacketHandler, IncompletePacket
from zipfile import ZipFile
import pdb

#include once implemented
# from phywhisperer.firmware.phywhisperer import getsome

class Usb(PWPacketDispatcher):
    """PhyWhisperer-USB Interface"""


    MAX_PATTERN_LENGTH = 64

    def __init__ (self, viewsb=False):
        """ Set up PhyWhisperer-USB device.
        
        Args:
            viewsb: Should only be set to 'True' when this is called by ViewSB.
        """
        self.viewsb = viewsb
        self.addpattern = False
        self.short_timestamps = [0] * 2**3
        self.long_timestamps = [0] * 2**16
        self.stat_pattern_match_value = 0
        self.capture_size = 8188 # default to FIFO size
        self.usb_trigger_freq = 240E6 #internal frequency used for trigger ticks
        self.slurp_defines()
        # Set up the PW device to handle packets in ViewSB:
        if viewsb:
            super().__init__(verbose=False)
            self.sniffer = USBSniffer()
            self.register_packet_handler(self.sniffer)


    def slurp_defines(self):
        """ Parse Verilog defines file so we can access register and bit
        definitions by name and avoid 'magic numbers'.
        """
        self.verilog_define_matches = 0
        defines_file = pkg_resources.resource_filename('phywhisperer', 'firmware/defines.v')
        defines = open(defines_file, 'r')
        define_regex_base  =   re.compile(r'`define')
        define_regex_radix =   re.compile(r'`define\s+?(\w+).+?\'([bdh])([0-9a-fA-F]+)')
        define_regex_noradix = re.compile(r'`define\s+?(\w+?)\s+?(\d+?)')
        for define in defines:
            if define_regex_base.search(define):
                match = define_regex_radix.search(define)
                if match:
                    self.verilog_define_matches += 1
                    if match.group(2) == 'b':
                        radix = 2
                    elif match.group(2) == 'h':
                        radix = 16
                    else:
                        radix = 10
                    setattr(self, match.group(1), int(match.group(3),radix))
                else:
                    match = define_regex_noradix.search(define)
                    if match:
                        self.verilog_define_matches += 1
                        setattr(self, match.group(1), int(match.group(2),10))
                    else:
                        logging.warning("Couldn't parse line: %s", define)
        # make sure everything is cool:
        assert self.verilog_define_matches == 49, "Trouble parsing Verilog defines file (%s): didn't find the right number of defines." % defines_file
        defines.close()


    def con(self, PID=0xC610, sn=None, program_fpga=True):
        """Connect to PhyWhisperer-USB. Raises error if multiple detected

        Args:
            PID (int, optional): USB PID of PhyWhisperer, defaults to 0xC610 (NewAE standard).
            sn (int, option):  Serial Number of PhyWhisperer, required when multiple
                PhyWhisperers are connected.
            program_fpga (bool, option): Specifies whether or not to program the FPGA with
                the default firmware when we connect. Set to False if using custom bitstream.
        """

        self.usb = NAE.NAEUSB()
        self.usb.con(idProduct=[PID], serial_number=sn)
        self._llint = LLINT.PhyWhispererUSB(self.usb)

        if program_fpga:
            from phywhisperer.firmware.phywhisperer import getsome
            with ZipFile(getsome("phywhisperer-firmware.zip")) as myzip:
                with myzip.open('phywhisperer_top.bit') as bitstream:
                    self._llint.FPGAProgram(bitstream)
            pass
        pass


    def set_power_source(self, src):
        """Set power source for target.

        Args:
            src (str):
              * "5V" for power from this computer (via 'Control' USB port).
              * "host" for power from the host of the connection we're sniffing.
              * "off" for no power.
        """
        if src == "5V":
            self._llint.changePowerSource(self._llint.PWR_SRC_5V)
            pass
        elif src == "host":
            self._llint.changePowerSource(self._llint.PWR_SRC_HOST)
            pass
        elif src == "off" or src is None or src == False:
            self._llint.changePowerSource(self._llint.PWR_SRC_OFF)
            pass
        else:
            raise AttributeError("Unknown source %s, valid sources: '5V', 'host', 'off'")


    def reset_fpga(self):
        """ Reset FPGA registers to defaults, use liberally to clear incorrect states.
        """
        self._llint.resetFPGA()

    def load_bitstream(self, bitfile):
        """Load bitstream onto FPGA"""
        if not os.path.isfile(bitfile):
            raise ValueError("Cannot find specified bitfile {}".format(bitfile))

        bitstream = open(bitfile, "rb")
        self._llint.FPGAProgram(bitstream)
        pass


    def erase_sam3u(self):
        """Erase the SAM3U Firmware, which forces it into bootloader mode."""
        self._llint.eraseFW(confirm=True)

    def program_sam3u(self, port, fw_path=None):
        """Program the SAM3U Firmware assuming device is in bootloader mode.
        
        Args:
            port (str): Serial port name, such as 'COM36' or '/dev/ttyACM0'.        
        """

        fw_data = None
        print("Opening firmware...")

        if fw_path is None:
            print("Firmware not specified. Using firmware/phywhisperer.py")
            from phywhisperer.firmware.phywhisperer import getsome
            fw_data = getsome("phywhisperer-SAM3U1C.bin").read()
        else:
            if not os.path.isfile(fw_path):
                raise ValueError("Cannot find specified firmware file {}".format(fw_path))
            fw_data = open(fw_path, "rb").read()

        sam = Samba()
        print("Opened!\nConnecting...")
        sam.con(port)
        print("Connected!\nErasing...")
        sam.erase()
        print("Erased!\nProgramming file {}...".format(fw_path))
        sam.write(fw_data)
        print("Programmed!\nVerifying...")
        if sam.verify(fw_data):
            print("Verify OK!")
            sam.flash.setBootFlash(True)
            print("Bootloader disabled. Please power cycle device.")
        else:
            print("Verify FAILED!")

        sam.ser.close()


    def set_usb_mode(self, mode='auto'):
        """Set USB PHY speed.
        
        Args:
            mode (str):
                 * "LS": manually set the PHY to low speed.
                 * "FS": manually set the PHY to full speed.
                 * "HS": manually set the PHY to high speed.
                 * "auto": Default. PW will attempt to automatically determine the
                       speed when the target is connected. Mode must be set to
                       'auto' prior to connecting the target, otherwise speed
                       cannot be determined correctly. Setting the mode to
                       'auto' actively causes PW to try to determine the speed.
        """
        if mode == 'auto':
           self.usb.cmdWriteMem(self.REG_USB_SPEED, [self.USB_SPEED_AUTO])
        elif mode == 'LS':
           self.usb.cmdWriteMem(self.REG_USB_SPEED, [self.USB_SPEED_LS])
        elif mode == 'FS':
           self.usb.cmdWriteMem(self.REG_USB_SPEED, [self.USB_SPEED_FS])
        elif mode == 'HS':
           self.usb.cmdWriteMem(self.REG_USB_SPEED, [self.USB_SPEED_HS])
        else:
           raise ValueError('Invalid mode %s; specify auto, LS, FS, or HS.' % mode)
        pass


    def get_usb_mode(self):
        """Returns USB PHY speed.
           A return value of 'auto' means that the speed has not been
           determined yet (was the mode set to 'auto' _before_ the target was
           connected or powered up?).
        """
        value = self.usb.cmdReadMem(self.REG_USB_SPEED, 1)[0]
        if value == self.USB_SPEED_AUTO:
            return 'auto'
        elif value == self.USB_SPEED_LS:
            return 'LS'
        elif value == self.USB_SPEED_FS:
            return 'FS'
        elif value == self.USB_SPEED_HS:
            return 'HS'
        else:
            raise ValueError('Internal error: REG_USB_SPEED register contains invalid value %d.' % value)


    def read_capture_data(self, entries=0, verbose=False, blocking=False, burst_size=8192, timeout=10):
        """Read from USB capture memory.
        
        Args:
            blocking (bool, optional):
                * True: wait for data to be available before reading (slower).
                * False: read immediately, with underflow protection, all of the captured
                  data, until PW tells us we've read everything ('entries' is ignored).
            entries (int, optional): When blocking=True, number of capture entries to read. If not specified, 
                 read all the captured data. Cannot be greater than capture size, as set 
                 by set_capture_size().
            burst_size (int, optional): When blocking=False, size of burst FIFO reads, defaults to 8192.
            timeout (int, optional): timeout in seconds (ignored if 0, defaults to 10)
            verbose (bool, optional): Print extra debug info.
        
        Returns: List of captured entries. Each list element is itself a 3-element list,
        containing the 3 bytes that make up a capture entry. Can be parsed by split_packets()
        or split_data().
        """
        data = []
        starttime = time.time()

        if blocking:
            entries_read = 0

            if not entries:
                entries = self.capture_size
            elif entries > self.capture_size:
                raise ValueError('Error: requested to read %d entries but only %d were captured.' % (entries, self.capture_size))

            while entries_read < entries:
                while self.fifo_empty():
                    if time.time() - starttime > timeout:
                        logging.warning("Capture timed out!")
                        break
                data.append(self.usb.cmdReadMem(self.REG_SNIFF_FIFO_RD, 4)[0:3])
                entries_read += 1

        else:
            notdone = True
            raw = []
            while notdone:
                raw.extend(self.usb.cmdReadMem(self.REG_SNIFF_FIFO_RD, 4*burst_size))
                if raw[-2] & (128 + 4) == (128 + 4):
                    notdone = False
                if time.time() - starttime > timeout:
                    logging.warning("Capture timed out!")
                    notdone = False
            # reformat the return array and at the same time, filter out the (possibly numerous) empty FIFO reads:
            for i in range(int(len(raw)/4)):
                if raw[i*4+2] & 3 != self.FE_FIFO_CMD_STRM:
                    data.append(raw[i*4:i*4+3])

        if len(data): # maybe we only got empty reads
            if data[-1][2] & 8:
                logging.warning("Capture FIFO underflowed!")
            if data[-1][2] & 64:
                logging.warning("Capture FIFO overflow. Capture stopped when overflow detected.")

        return data


    def split_data(self, rawdata, verbose=False):
        """Split raw USB capture data into data events and times, stat events and times.
        
        Returns:
            4-tuple of lists:
                0. data event times
                1. data bytes corresponding to data event times
                2. USB status update times
                3. USB status bytes corresponding to status update times
        """
        timestep = 0
        data_bytes = []
        data_times = []
        stat_bytes = []
        stat_times = []
        data_commands = 0
        stat_commands = 0
        time_commands = 0

        for raw in rawdata:
            command = raw[2] & 0x3
            if (command == self.FE_FIFO_CMD_DATA):
                data = raw[1]
                ts = raw[0] & 0x7
                self.short_timestamps[ts] += 1
                #hardware reports the number of cycles between events, so to
                #obtain elapsed time we add one:
                timestep += (ts+1)
                flags = (raw[0] & 0xf8) >> 3
                if verbose:
                   print("%8d   flags=%02x data=%02x"%(timestep, flags, data))
                # TODO: log flags
                data_commands += 1
                data_bytes.append(data)
                data_times.append(timestep)
            elif (command == self.FE_FIFO_CMD_STAT):
                ts = raw[0] & 0x7
                self.short_timestamps[ts] += 1
                timestep += (ts+1)
                flags = (raw[0] & 0xf8) >> 3
                if verbose:
                   print("%8d   flags=%02x"%(timestep, flags))
                stat_commands += 1
                stat_bytes.append(flags)
                stat_times.append(timestep)
            elif (command == self.FE_FIFO_CMD_TIME):
                ts = raw[0] + (raw[1] << 8)
                self.long_timestamps[ts] += 1
                #Unlike stat and data commands, we don't add one here; if we did
                #we'd be overcounting in the common case where a time command immediately
                #preceeds a stat or data command. Consequence is that timestep will be off
                #by one in the case of lone time commands (which is rare, and inconsequential
                #in practice).
                timestep += ts
                time_commands += 1
                if verbose:
                   print("%8d" % timestep)
            elif (command == self.FE_FIFO_CMD_STRM):
                # nothing to do or report
                pass
            else:
                print ("ERROR: unknown command (%d)" % command) 

        return (data_times, data_bytes, stat_times, stat_bytes)


    def split_packets(self, rawdata):
        """Split raw USB capture data into packets.
        
        Returns:
            list
                Each list element is one packet and is presented in a dictionary with the following keys:
                    * 'timestamp'
                    * 'size' in bytes
                    * 'contents' list of bytes
        """
        from phywhisperer.protocol import IncompletePacket
        # operates destructively so make a copy:
        rawdata_copy = rawdata[:]
        handler = PWPacketHandler()
        packets = []
        incomplete = False
        while rawdata_copy and not incomplete:
            # use ViewSB to avoid duplicating it here:
            try:
                packets.append(handler.handle_bytes_received(defines=self, data=rawdata_copy))
            except IncompletePacket:
                incomplete = True
                continue
        return packets


    def set_capture_size(self, size=8188):
        """Set how many events to capture (events include data, USB status, and timestamps).
        
        Args:
            size(int, option): number of events to capture. 0 = unlimited (until overflow). Max = 2^24-1. Since the capture FIFO can hold 8188 events, setting this to > 8188 may result in overflow.

        """
        if (size >= 2**24) or (size < 0):
            raise ValueError('Illegal size value.')
        self.capture_size = size
        size_bytes = [size & 255, (size >> 8) & 255, (size >> 16) & 255]
        self.usb.cmdWriteMem(self.REG_CAPTURE_LEN, size_bytes)


    def ns_trigger(self, delay_in_ns):
        """Convert a nS number to delay or width cycles for set_trigger()"""
        cycles = (float(delay_in_ns) * 1.0E-9) / (1.0 / float(self.usb_trigger_freq))
        return round(cycles)

    def us_trigger(self, delay_in_us):
        """Convert a uS number to delay or width cycles for set_trigger()"""
        cycles = (float(delay_in_us) * 1.0E-6) / (1.0 / float(self.usb_trigger_freq))
        return round(cycles)

    def ms_trigger(self, delay_in_ms):
        """Convert a mS number to delay or width cycles for set_trigger()"""
        cycles = (float(delay_in_ms) * 1.0E-3) / (1.0 / float(self.usb_trigger_freq))
        return round(cycles)


    def set_trigger(self, delay=0, width=1, enable=True):
        """Program the output trigger delay and width. Both are measured in clock cycles of USB-derived 240 MHz clock.
           The capture delay is automatically set to match the trigger delay; use set_capture_delay to set it to a
           different value. Use ns_trigger(), us_trigger(), and ms_trigger() to convert values as needed.
        
        Args:
            delay (int): range in [0, 2^20-1] cycles.
            width (int): range in [1, 2^17-1] cycles.
            enable (bool, optional): set to 'False' to disable trigger generation on hardware pins.
        """
        if (delay >= 2**20) or (delay < 0):
            raise ValueError('Illegal delay value.')
        if (width >= 2**17) or (width < 1):
            raise ValueError('Illegal width value.')
        delay_bytes = [delay & 255, (delay >> 8) & 255, (delay >> 16) & 255]
        width_bytes = [width & 255, (width >> 8) & 255, (width >> 16) & 255]
        self.usb.cmdWriteMem(self.REG_TRIGGER_DELAY, delay_bytes)
        self.usb.cmdWriteMem(self.REG_TRIGGER_WIDTH, width_bytes)
        self.set_capture_delay(int(delay/4))
        if enable == True:
            self.usb.cmdWriteMem(self.REG_TRIGGER_ENABLE, [1])
        else:
            self.usb.cmdWriteMem(self.REG_TRIGGER_ENABLE, [0])


    def set_capture_delay(self, delay):
        """Program the capture delay, measured in clock cycles of USB-derived 60 MHz clock.
        
        Args:
            delay (int): range in [0, 2^18-1] cycles of 60 MHz clock.
        """
        if (delay >= 2**18) or (delay < 0):
            raise ValueError('Illegal delay value.')
        delay_bytes = [delay & 255, (delay >> 8) & 255, (delay >> 16) & 255]
        self.usb.cmdWriteMem(self.REG_CAPTURE_DELAY, delay_bytes)


    def set_pattern(self, pattern, mask=None):
        """Set the pattern and its bitmask used for capture and trigger output.
        
        Args:
            pattern (list of ints): list of between 1 and 64 bytes 
            mask (list, optional): list of bytes, must have same size as 'pattern' if
                set. Defaults to [0xff]*len(pattern) if not set.
        """
        if mask is None:
            mask = [0xFF] * len(pattern)
        
        if len(pattern) != len(mask):
            raise ValueError('pattern and mask must be of same size.')
        elif len(pattern) > self.MAX_PATTERN_LENGTH:
            raise ValueError('pattern and mask cannot be more than 64 bytes.')
        # extend the mask to full width (cheaper to do here than in HW):
        mask = [0]* (self.MAX_PATTERN_LENGTH - len(mask)) + mask
        self.usb.cmdWriteMem(self.REG_PATTERN, pattern[::-1])
        self.usb.cmdWriteMem(self.REG_PATTERN_MASK, mask[::-1])
        self.usb.cmdWriteMem(self.REG_PATTERN_BYTES, [len(pattern)])
        self.pattern = pattern
        self.mask = mask


    def arm(self):
        """Arm PhyWhisperer for capture and optionally generating a trigger.
        Use set_pattern to program the pattern and bitmask which will initiate
        the capture and/or trigger operation.
        Use set_trigger to program the trigger parameters.
        Use set_capture_size and set_capture_delay to program the capture parameters.
        """
        self.usb.cmdWriteMem(self.REG_ARM, [1])


    def check_fifo_errors(self, underflow=0, overflow_blocked=0):
        """Check whether an underflow or overflow occured on the capture FIFO.
        (Overflows are blocked, underflows are not.)
        
        Args:
            underflow (int, optional): expected status, 0 or 1
            overflow_blocked (int, optional): expected status, 0 or 1
        """
        status = self.usb.cmdReadMem(self.REG_SNIFF_FIFO_STAT,1)[0]
        fifo_underflow = (status & 2) >> 1
        fifo_overflow_blocked = (status & 16) >> 4
        assert fifo_underflow == underflow
        assert fifo_overflow_blocked == overflow_blocked


    def fifo_empty(self):
        """Returns True if the capture FIFO is empty, False otherwise.
        """
        if self.usb.cmdReadMem(self.REG_SNIFF_FIFO_STAT,1)[0] & 1:
            return True
        else:
            return False


    def fifo_over_empty_threshold(self):
        """Returns True if the capture FIFO has more entries than the empty threshold (128).
        """
        fifo_stat = self.usb.cmdReadMem(self.REG_SNIFF_FIFO_STAT,1)[0]
        fifo_empty = fifo_stat & 1
        fifo_empty_threshold = fifo_stat & 4
        if fifo_empty or fifo_empty_threshold:
            return False
        else:
            return True


    def armed(self):
        """Returns True if the PhyWhisperer is armed.
        """
        if self.usb.cmdReadMem(self.REG_ARM,1)[0]:
            return True
        else:
            return False


    def wait_disarmed(self):
        """Blocks until armed() returns false.
        """
        while self.armed():
            pass


    def get_fpga_buildtime(self):
        """Returns date and time when FPGA bitfile was generated.
        """
        raw = self.usb.cmdReadMem(self.REG_BUILDTIME,4)
        # definitions: Xilinx XAPP1232
        day = raw[3] >> 3
        month = ((raw[3] & 0x7) << 1) + (raw[2] >> 7)
        year = ((raw[2] >> 1) & 0x3f) + 2000
        hour = ((raw[2] & 0x1) << 4) + (raw[1] >> 4)
        minute = ((raw[1] & 0xf) << 2) + (raw[0] >> 6)
        return "FPGA build time: {}/{}/{}, {}:{}".format(month, day, year, hour, minute)


    def trigger_clock_phase_shift(self, steps=1):
        """Shifts the trigger clock phase (and by extension the output trigger) in steps
        of 18.6ps (18.6 ps = 1/960 MHz / 56)
        
        Args:
            steps (int): Number of steps to shift the phase (positive or negative integer).
        """
        if not type(steps) == int or steps == 0:
            raise ValueError('Illegal steps value, must be non-zero integer.')
        if steps > 0:
            value = [1]
        else:
            value = [0]
        for i in range(abs(steps)):
            self.usb.cmdWriteMem(self.REG_TRIG_CLK_PHASE_SHIFT, value)
            while (self.usb.cmdReadMem(self.REG_TRIG_CLK_PHASE_SHIFT, 1)[0] == 1):
                # phase shift incomplete
                pass


    def set_stat_pattern(self, pattern, mask=0x1f):
        """ Set a 5-bit pattern and mask for the USB status lines.
        
        Args:
            pattern (int): 5-bit number
            mask (int): non-zero 5-bit number (default: 0x1f)
        """
        if pattern < 0 or pattern > 0x1f:
            raise ValueError('Illegal pattern value, must be <= 0x1f.')
        if mask < 1 or mask > 0x1f:
            raise ValueError('Illegal mask value, must be <= 0x1f and > 0.')
        self.usb.cmdWriteMem(self.REG_STAT_PATTERN, [pattern, mask])


    def stat_pattern_matched(self):
        """ Returns 1 if a stat pattern match occurred (automatically resets to 0 when armed,
        and when a new match pattern is written).
        Actual match value is stored in self.stat_pattern_match_value.
        """
        matched, value = self.usb.cmdReadMem(self.REG_STAT_MATCH, 2)
        self.stat_pattern_match_value = value
        return matched


    def register_sink(self, event_sink):
        """ ViewSB: Registers a USBEventSink to receive any USB events. 
        
        Args:
            event_sink (sniffer.USBEventSink): The sniffer.USBEventSink object to receive any USB events that occur.
        """
        self.sniffer.register_sink(event_sink)


    def _device_stop_capture(self):
        # nothing to do?
        pass


    def run_capture(self, size=8188, burst=True, pattern=[0], mask=[0], statistics_callback=None, statistics_period=0.1, halt_callback=lambda _ : False, ):
        """ Runs a capture for ViewSB, including power cycling the device to catch the descriptors.
        
        Runs following internally::
        
            self.reset_fpga()
            self.set_power_source("host")
            self.set_power_source("off")
            time.sleep(0.5)
            self.set_usb_mode("auto")
            self.set_capture_size(size)
            self.arm()
            self.set_trigger(enable=False)
            self.set_pattern(pattern=pattern, mask=mask)
            self.set_power_source("host")
            time.sleep(0.25)
        
        """


        self.reset_fpga()
        self.set_power_source("host")
        self.set_power_source("off")
        time.sleep(0.5)
        self.set_usb_mode("auto")
        self.set_capture_size(size)
        self.arm()
        self.set_trigger(enable=False)
        self.set_pattern(pattern=pattern, mask=mask)
        self.set_power_source("host")
        time.sleep(0.25)

        #self.reset_fpga()
        #self.set_usb_mode("HS")
        #self.set_capture_size(size)
        #self.set_trigger(enable=False)
        #self.set_pattern(pattern=pattern, mask=mask)
        #time.sleep(5)
        #print("GO!!!!!!!!!!!!!!!!!!!")
        #self.arm()

        self._start_comms_thread(burst)

        elapsed_time = 0.0
        try:

            # Continue until the user-supplied halt condition is met.
            while not halt_callback(elapsed_time): 

                # If we have a statistics callback, call it.
                if callable(statistics_callback):
                    statistics_callback(self, elapsed_time)

                # Wait for the next statistics-interval to occur.
                time.sleep(statistics_period)
                elapsed_time = elapsed_time + statistics_period

        finally:
            self._device_stop_capture()


    def __comms_thread_body(self, burst, burst_size=8192, timeout=10):
        """ ViewSB internal function that executes as our comms thread.
        
        Args:
            burst (bool): If True, read all FIFO at once, then pass on to decoder and frontend;
                     otherwise, read smaller chunks and process them concurrently.
            burst_size (int): Number of entries to read at a time when burst=False
        """

        if burst:
            self.wait_disarmed()
            rawdata = self.read_capture_data()
            #logging.warning("*** received %d entries!" % len(rawdata))
            self.handle_incoming_bytes(rawdata)

        else:
            notdone = True
            starttime = time.time()
            while notdone:
                raw = self.usb.cmdReadMem(self.REG_SNIFF_FIFO_RD, 4*burst_size)
                if raw[-2] & (128 + 4) == (128 + 4):
                    notdone = False
                if time.time() - starttime > timeout:
                    logging.warning("Capture timed out!")
                    notdone = False
                # filter out the empty FIFO reads:
                rawdata = []
                for i in range(int(len(raw)/4)):
                    if raw[i*4+2] & 3 != self.FE_FIFO_CMD_STRM:
                        rawdata.append(raw[i*4:i*4+3])
                #logging.warning("Handling %d entries. Notdone=%d" % (len(rawdata), notdone))
                self.handle_incoming_bytes(rawdata)
            #logging.warning("Capture done.")


    def _start_comms_thread(self, burst):
        """ ViewSB: start the background thread that handles our core communication. """

        self.commthread = threading.Thread(target=self.__comms_thread_body, args=[burst], daemon=True)
        self.__comm_term = False
        self.__comm_exc = None

        self.commthread.start()

        self.__comm_term = False


    def close(self):
        """ Terminates our connection to the PhyWhisperer device. """

        if self.viewsb:
            self.__comm_term = True
            self.commthread.join()
        self.usb.close()



class ForkedPdb(pdb.Pdb):
    """A Pdb subclass that may be used
    from a forked multiprocessing child

    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin



