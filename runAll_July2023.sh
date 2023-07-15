#!/bin/bash


#SPE B4C 10nm
<<com
python3 analyze_SPErun.py -r 126 -c 2
python3 analyze_SPErun.py -r 127 -c 2
python3 analyze_SPErun.py -r 128 -c 2
com

#PE B4C 10nm
<<com
python3 analyze_PErun.py -r 129 -c 2
python3 analyze_PErun.py -r 130 -c 2
python3 analyze_PErun.py -r 131 -c 2
com

#SPE DLC 2.5 shitty
<<com
python3 analyze_SPErun.py -r 151 -c 2
python3 analyze_SPErun.py -r 152 -c 2
python3 analyze_SPErun.py -r 153 -c 2
com

#PE DLC 2.5 shitty
<<com
python3 analyze_PErun.py -r 154 -c 2
python3 analyze_PErun.py -r 155 -c 2
com

#SPE DLC B4C 4nm
<<com
python3 analyze_SPErun.py -r 191 -c 2
python3 analyze_SPErun.py -r 192 -c 2
python3 analyze_SPErun.py -r 193 -c 2
com

#PE B4C 4nm
<<com
python3 analyze_PErun.py -r 195 -c 2
python3 analyze_PErun.py -r 196 -c 2
python3 analyze_PErun.py -r 197 -c 2
com

#SPE DLC 3nm
<<com
python3 analyze_SPErun.py -r 219 -c 2
python3 analyze_SPErun.py -r 220 -c 2
python3 analyze_SPErun.py -r 221 -c 2
com

#PE DLC 3nm
<<com
python3 analyze_PErun.py -r  -c 2
python3 analyze_PErun.py -r  -c 2
python3 analyze_PErun.py -r  -c 2
com
