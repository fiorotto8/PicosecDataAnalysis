#!/bin/bash

#single photoelectron no tracking
#firsts SPEs B4C 7nm
<<com
python3 analyze_SPErun.py -r 313 -c 4
python3 analyze_SPErun.py -r 315 -c 4
python3 analyze_SPErun.py -r 317 -c 4
python3 analyze_SPErun.py -r 318 -c 4
python3 analyze_SPErun.py -r 319 -c 4
python3 analyze_SPErun.py -r 320 -c 4
python3 analyze_SPErun.py -r 321 -c 4
python3 analyze_SPErun.py -r 322 -c 4
com

#second SPEs B4C 7nm
<<com
python3 analyze_SPErun.py -r 363 -c 4
python3 analyze_SPErun.py -r 364 -c 4
python3 analyze_SPErun.py -r 365 -c 4
python3 analyze_SPErun.py -r 366 -c 4
python3 analyze_SPErun.py -r 367 -c 4
python3 analyze_SPErun.py -r 368 -c 4
python3 analyze_SPErun.py -r 369 -c 4
python3 analyze_SPErun.py -r 370 -c 4
com

#CsI photoelctrons
<<com
python3 analyze_SPErun.py -r 383 -c 4
python3 analyze_SPErun.py -r 384 -c 4
python3 analyze_SPErun.py -r 385 -c 4
python3 analyze_SPErun.py -r 386 -c 4
python3 analyze_SPErun.py -r 387 -c 4
python3 analyze_SPErun.py -r 388 -c 4
com

#photoelectrons from beam
#first PE run B4c 7nm
#<<com
python3 analyze_PErun.py -r 323 -c 4
python3 analyze_PErun.py -r 324 -c 4
python3 analyze_PErun.py -r 329 -c 4
python3 analyze_PErun.py -r 330 -c 4
#com
#second PE run B4c 7nm
#<<com
python3 analyze_PErun.py -r 373 -c 4
python3 analyze_PErun.py -r 374 -c 4
python3 analyze_PErun.py -r 375 -c 4
python3 analyze_PErun.py -r 376 -c 4
#com

#CsI PEs
#<<com
python3 analyze_PErun.py -r 389 -c 4
python3 analyze_PErun.py -r 390 -c 4
python3 analyze_PErun.py -r 391 -c 4
#com

#timing runs
<<com
python3 analyze_TIMErun.py -r 013
python3 analyze_TIMErun.py -r 014
python3 analyze_TIMErun.py -r 015
python3 analyze_TIMErun.py -r 017
python3 analyze_TIMErun.py -r 073
python3 analyze_TIMErun.py -r 074
python3 analyze_TIMErun.py -r 075
python3 analyze_TIMErun.py -r 076
python3 analyze_TIMErun.py -r 077
python3 analyze_TIMErun.py -r 078
python3 analyze_TIMErun.py -r 098
python3 analyze_TIMErun.py -r 099
python3 analyze_TIMErun.py -r 100
python3 analyze_TIMErun.py -r 101
python3 analyze_TIMErun.py -r 102
python3 analyze_TIMErun.py -r 112
python3 analyze_TIMErun.py -r 113
python3 analyze_TIMErun.py -r 114
python3 analyze_TIMErun.py -r 115
python3 analyze_TIMErun.py -r 116
python3 analyze_TIMErun.py -r 117
python3 analyze_TIMErun.py -r 118
python3 analyze_TIMErun.py -r 119
python3 analyze_TIMErun.py -r 120
python3 analyze_TIMErun.py -r 138
python3 analyze_TIMErun.py -r 139
python3 analyze_TIMErun.py -r 140
python3 analyze_TIMErun.py -r 163
python3 analyze_TIMErun.py -r 164
python3 analyze_TIMErun.py -r 165
python3 analyze_TIMErun.py -r 191
python3 analyze_TIMErun.py -r 192
python3 analyze_TIMErun.py -r 193
python3 analyze_TIMErun.py -r 194
python3 analyze_TIMErun.py -r 195
python3 analyze_TIMErun.py -r 212
python3 analyze_TIMErun.py -r 213
python3 analyze_TIMErun.py -r 214
python3 analyze_TIMErun.py -r 224
python3 analyze_TIMErun.py -r 225
python3 analyze_TIMErun.py -r 226
python3 analyze_TIMErun.py -r 278
python3 analyze_TIMErun.py -r 279
python3 analyze_TIMErun.py -r 280
python3 analyze_TIMErun.py -r 281
python3 analyze_TIMErun.py -r 282
com