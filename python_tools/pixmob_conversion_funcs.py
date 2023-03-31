import itertools
import python_tools.config as cfg


# This file contains functions used for converting between different representations of the PixMob data
# packets, including:
#
# - "run length" (time between IR light high/low switches), measured in microseconds, and also in pulses(could be called
#       bit widths or chunks)
# - "bits" (high/low IR light value at each unit of 694.44 microseconds)
# - hexadecimal
# - string representations parsed by the Arduino to send the IR signals.

def bits_to_hex(bit_list):
    # Example: [1, 1, 1, 1, 0, 0, 0, 0] -> 0xf0
    return hex(int(("".join([str(i) for i in bit_list])), 2))


def bits_to_run_length_microseconds(bit_list):
    # Convert bit list to run length in number of pulses/chunks, then multiply each of those lengths by the pulse/chunk
    # length in microseconds
    # Example: [1, 4, 2] -> [700, 2800, 1400]
    # Note that in this example, cfg.PULSE_LENGTH is 700
    return [pulses * cfg.PULSE_LENGTH for pulses in bits_to_run_lengths_pulses(bit_list)]


def bits_to_run_lengths_pulses(bit_list):
    # convert from a list of 1s and 0s to run length by number of pulses
    # Example: [1, 1, 1, 0, 0, 0, 0, 1] -> [3, 4, 1]
    # TODO for compatibility this is going to need to max out at 9 for now
    #   Throw an exception if the bit list isn't just ones and zeroes?
    run_lengths = []
    # groupby returns groups of adjacent matching things
    for _, group in itertools.groupby(bit_list):
        run_lengths.append(sum(1 for _ in group))
    return run_lengths


def bits_to_arduino_string(bit_list):
    # String to send to the arduino in the format "[<length>]NumberNumberNumber,"
    # Numbers are the run length in pulses.
    # Numbers have to be one digit, so I might make a v2 without that limitation?
    run_lengths = bits_to_run_lengths_pulses(bit_list)
    out = "[" + str(len(run_lengths)) + "]"
    out += "".join([str(int(i)) for i in run_lengths])
    return out + ","
