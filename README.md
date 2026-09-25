# hh71vm-nck-gen

Generates the network unlock code (NCK) for the Alcatel LINKHUB HH71VM from its
IMEI, to remove the carrier SIM lock.

Tested only on the HH71VM. Other devices that use the same algorithm may work, but
they are untested. Use at your own risk.

## Usage

Requires Python 3, with no other dependencies.

    python3 nck.py <IMEI> [<IMEI> ...]

On Windows, use `py nck.py` instead. The IMEI is the 15-digit number on the label
under the router.

Example, with a made-up IMEI:

    $ python3 nck.py 012345678901234
    012345678901234
      NCK:   6318552905 (478883)
      NSCK:  8532047882 (407823)
      SPCK:  0942002456 (328911)
      SIM:   1523150021 (542477)
      C:     0536453544 (527474)
      Other: 9308353322 (504072)
      T6:    4862357454 (041781)

To remove the carrier lock, use the **NCK** line.

## 10 or 16 digits

Some devices accept the 10-digit code. Others accept the full 16 digits: the
10-digit code followed by the six digits in parentheses, with no space. For the
example above:

- 10 digits: `6318552905`
- 16 digits: `6318552905478883`

The modem allows only a limited number of unlock attempts, and a wrong code uses
one up. Check the IMEI before entering a code.
