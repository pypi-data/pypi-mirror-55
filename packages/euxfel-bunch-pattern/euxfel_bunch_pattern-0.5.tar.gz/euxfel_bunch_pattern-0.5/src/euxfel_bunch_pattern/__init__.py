import numpy as np

from ._version import __version__

# These values are from page 10 of the XFEL timing systems specification,
# version 2.2, updated following a screenshot of the bunch pattern decoder
# device.
CHARGE_MASK = 0xf

# Charge in nC for the 16 possible 4 bit combinations
CHARGE_VALUES = np.array([
    0.0, .02, .03, .04,
    .06, .09, .13, .18,
    .25, .36, .50, .71,
    1.0, 1.42, 2.0, 4.0,
])

LASER_MASK = 0x3ff << 4

LASER_I1_LASER1 = 1 << 4
LASER_I1_LASER2 = 1 << 5
LASER_I1_LASER3 = 1 << 6
LASER_I2_LASER1 = 1 << 7
LASER_SEED1 = 1 << 8
LASER_SEED2 = 1 << 9
LASER_SEED3 = 1 << 10
LASER_SEED4 = 1 << 11
LASER_SEED5 = 1 << 12
LASER_SEED6 = 1 << 13
LASER_SEED7 = 1 << 14
LASER_SEED8 = 1 << 15
LASER_SEED9 = 1 << 16

DESTINATION_MASK = 0xf << 18

# 16 possible bit combinations for destinations, only 9 used at present
DESTINATION_NONE = 0 << 18
DESTINATION_I1LST = 1 << 18  # Laser stand-alone
DESTINATION_T5D = 2 << 18  # SASE2 dump
DESTINATION_G1D = 3 << 18   # Gun dump/valve
DESTINATION_T4D = 4 << 18   # SASE1/3 dump
DESTINATION_ILD = 5 << 18   # Injector dump
DESTINATION_B1D = 6 << 18   # B1 dump
DESTINATION_B2D = 7 << 18   # B2 dump
DESTINATION_TLD = 8 << 18
_DESTINATIONS = {DESTINATION_NONE, DESTINATION_I1LST, DESTINATION_T5D,
                 DESTINATION_G1D, DESTINATION_T4D, DESTINATION_ILD,
                 DESTINATION_B1D, DESTINATION_B2D, DESTINATION_TLD}

EVT_TRIGGER_25 = 1 << 22  # ?

TDS_INJ = 1 << 31
TDS_BC1 = 1 << 30
TDS_BC2 = 1 << 29
WIRE_SCANNER = 1 << 28
PHOTON_LINE_DEFLECTION = 1 << 27  # Soft kick (e.g. SA3)
BEAM_DISTRIBUTION_KICK = 1 << 26
# ----------------------------------------------------------------------------

def get_charge(bunchpattern):
    """Extract charge values in nC from bunch pattern data

    Parameters
    ----------
    bunchpattern : int or numpy array of integers
      The bunch pattern data
    """
    charge_bits = bunchpattern & CHARGE_MASK
    return CHARGE_VALUES[charge_bits]

def indices_at_destination(bunchpattern, destination):
    """Find which pulses are sent to a given destination

    Parameters
    ----------
    bunchpattern: numpy array
      The bunch pattern data
    destination: int
      One of the DESTINATION_* constants in this module.

    Returns
    -------
    indices: numpy array
      The 0-based indexes of the pulses for the specified destination
    """
    if destination not in _DESTINATIONS:
        raise ValueError("Unrecognised destination: {}".format(destination))

    matched = (bunchpattern & DESTINATION_MASK) == destination
    return matched.nonzero()[0]

def indices_at_sase(bunchpattern, sase):
    """Find which pulses are sent to a given SASE (1-3)

    Parameters
    ----------
    bunchpattern: numpy array
      The bunch pattern data
    sase: int
      Number 1-3.

    Returns
    -------
    indices: numpy array
      The 0-based indexes of the pulses for the specified destination
    """
    if not (1 <= sase <= 3):
        raise ValueError("Invalid SASE value {!r}, expected 1-3")
    destination = DESTINATION_T5D if (sase == 2) else DESTINATION_T4D
    matched = (bunchpattern & DESTINATION_MASK) == destination

    if sase == 1:
        # Pulses to SASE 1 when soft kick is off
        matched &= (bunchpattern & PHOTON_LINE_DEFLECTION) == 0
    elif sase == 3:
        # Pulses to SASE 3 when soft kick is on
        matched &= (bunchpattern & PHOTON_LINE_DEFLECTION) != 0

    return matched.nonzero()[0]

