#!/bin/bash
#test CFD fraction
###################
###### Pool2 ######
###################

#SPE B4C 10nm
<<com
python3 analyze_SPErun.py -r 126 -c 2 -os 2
python3 analyze_SPErun.py -r 127 -c 2 -os 2
python3 analyze_SPErun.py -r 128 -c 2 -os 2
com

#PE B4C 10nm
<<com
python3 analyze_PErun.py -r 129 -c 2 -os 2
python3 analyze_PErun.py -r 130 -c 2 -os 2
python3 analyze_PErun.py -r 131 -c 2 -os 2
com

#SPE DLC 2.5 shitty
<<com
python3 analyze_SPErun.py -r 151 -c 2 -os 2
python3 analyze_SPErun.py -r 152 -c 2 -os 2
python3 analyze_SPErun.py -r 153 -c 2 -os 2
com

#PE DLC 2.5 shitty
<<com
python3 analyze_PErun.py -r 154 -c 2 -os 2
python3 analyze_PErun.py -r 155 -c 2 -os 2
com

#SPE DLC B4C 4nm
<<com
python3 analyze_SPErun.py -r 191 -c 2 -os 2
python3 analyze_SPErun.py -r 192 -c 2 -os 2
python3 analyze_SPErun.py -r 193 -c 2 -os 2
com

#PE B4C 4nm
<<com
python3 analyze_PErun.py -r 195 -c 2 -os 2
python3 analyze_PErun.py -r 196 -c 2 -os 2
python3 analyze_PErun.py -r 197 -c 2 -os 2
com

#SPE DLC 3nm
<<com
python3 analyze_SPErun.py -r 219 -c 2 -os 2
python3 analyze_SPErun.py -r 220 -c 2 -os 2
python3 analyze_SPErun.py -r 221 -c 2 -os 2
com

#PE DLC 3nm
<<com
python3 analyze_PErun.py -r 228 -c 2 -os 2
python3 analyze_PErun.py -r 229 -c 2 -os 2
python3 analyze_PErun.py -r 230 -c 2 -os 2
com

#Timing Pavia SC Ne/iso 90/10
#Pool2
#<<com
python3 process_TIMErun.py -r 030 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 030 -cDUT 2 -os 2
python3 process_TIMErun.py -r 036 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 036 -cDUT 2 -os 2
python3 process_TIMErun.py -r 037 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 037 -cDUT 2 -os 2
python3 process_TIMErun.py -r 046 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 046 -cDUT 2 -os 2
python3 process_TIMErun.py -r 047 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 047 -cDUT 2 -os 2
python3 process_TIMErun.py -r 048 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 048 -cDUT 2 -os 2
python3 process_TIMErun.py -r 049 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 049 -cDUT 2 -os 2
python3 process_TIMErun.py -r 050 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 050 -cDUT 2 -os 2
python3 process_TIMErun.py -r 051 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 051 -cDUT 2 -os 2
python3 process_TIMErun.py -r 055 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 055 -cDUT 2 -os 2
python3 process_TIMErun.py -r 056 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 056 -cDUT 2 -os 2
#com


#Timing Vacuum Chamebr Ne/iso 94/6
#Pool2
#<<com
python3 process_TIMErun.py -r 036 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 036 -cDUT 4 -os 2
python3 process_TIMErun.py -r 037 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 037 -cDUT 4 -os 2
python3 process_TIMErun.py -r 046 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 046 -cDUT 4 -os 2
python3 process_TIMErun.py -r 047 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 047 -cDUT 4 -os 2
python3 process_TIMErun.py -r 048 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 048 -cDUT 4 -os 2
python3 process_TIMErun.py -r 049 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 049 -cDUT 4 -os 2
python3 process_TIMErun.py -r 050 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 050 -cDUT 4 -os 2
python3 process_TIMErun.py -r 051 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 051 -cDUT 4 -os 2
python3 process_TIMErun.py -r 055 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 055 -cDUT 4 -os 2
python3 process_TIMErun.py -r 056 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 056 -cDUT 4 -os 2
#com

#Timing Pavia SC standard gas to compare with Ne/iso 90/10 
#Pool2
#<<com
python3 process_TIMErun.py -r 061 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 061 -cDUT 2 -os 2
python3 process_TIMErun.py -r 062 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 062 -cDUT 2 -os 2
python3 process_TIMErun.py -r 063 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 063 -cDUT 2 -os 2
python3 process_TIMErun.py -r 064 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 064 -cDUT 2 -os 2
python3 process_TIMErun.py -r 065 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 065 -cDUT 2 -os 2
python3 process_TIMErun.py -r 066 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 066 -cDUT 2 -os 2
#com

#Timing Vacuum standard gas to compare with Ne/iso 94/6
#Pool2
#<<com
python3 process_TIMErun.py -r 061 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 061 -cDUT 4 -os 2
python3 process_TIMErun.py -r 062 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 062 -cDUT 4 -os 2
python3 process_TIMErun.py -r 063 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 063 -cDUT 4 -os 2
python3 process_TIMErun.py -r 064 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 064 -cDUT 4 -os 2
python3 process_TIMErun.py -r 065 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 065 -cDUT 4 -os 2
python3 process_TIMErun.py -r 066 -pDUT 6 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 066 -cDUT 4 -os 2
#com

#Timing Pavia SC with CsI 
#Pool2
#<<com
python3 process_TIMErun.py -r 069 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 069 -cDUT 2 -os 2
python3 process_TIMErun.py -r 070 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 070 -cDUT 2 -os 2
python3 process_TIMErun.py -r 071 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 071 -cDUT 2 -os 2
python3 process_TIMErun.py -r 072 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 072 -cDUT 2 -os 2
python3 process_TIMErun.py -r 073 -pDUT 3 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 073 -cDUT 2 -os 2
#com

#Timing Pavia SC with B4C 10nm
#Pool2
#<<com
python3 process_TIMErun.py -r 113 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 113 -cDUT 2 -os 2
python3 process_TIMErun.py -r 114 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 114 -cDUT 2 -os 2
python3 process_TIMErun.py -r 115 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 115 -cDUT 2 -os 2
python3 process_TIMErun.py -r 116 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 116 -cDUT 2 -os 2
#com

#Timing Pavia SC with B4C 4nm
#Pool2
#<<com
python3 process_TIMErun.py -r 186 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 186 -cDUT 2 -os 2
python3 process_TIMErun.py -r 187 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 187 -cDUT 2 -os 2
python3 process_TIMErun.py -r 188 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 188 -cDUT 2 -os 2
python3 process_TIMErun.py -r 189 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 189 -cDUT 2 -os 2
python3 process_TIMErun.py -r 190 -pDUT 2 -cDUT 2 -os 2
python3 analyze_TIMErun.py -r 190 -cDUT 2 -os 2
#com

#Timing Pavia Multipad
#Pool2
#<<com
#pad77
python3 process_TIMErun.py -r 266 -pDUT 2 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 266 -cDUT 4 -os 2
python3 process_TIMErun.py -r 270 -pDUT 2 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 270 -cDUT 4 -os 2
python3 process_TIMErun.py -r 274 -pDUT 2 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 274 -cDUT 4 -os 2
#com

#Timing DLC 2.5nm
#<<com
python3 process_TIMErun.py -r 417 -pDUT 5 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 417 -cDUT 4 -os 2
python3 process_TIMErun.py -r 418 -pDUT 5 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 418 -cDUT 4 -os 2
python3 process_TIMErun.py -r 419 -pDUT 5 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 419 -cDUT 4 -os 2
python3 process_TIMErun.py -r 420 -pDUT 5 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 420 -cDUT 4 -os 2
python3 process_TIMErun.py -r 421 -pDUT 5 -cDUT 4 -os 2
python3 analyze_TIMErun.py -r 421 -cDUT 4 -os 2
#com

###################
###### Pool3 ######
###################

#Timing DLC 2.5nm
#<<com
python3 process_TIMErun.py -r 454 -pDUT 2 -cDUT 4 -os 3
python3 analyze_TIMErun.py -r 454 -cDUT 4 -os 3
python3 process_TIMErun.py -r 455 -pDUT 2 -cDUT 4 -os 3
python3 analyze_TIMErun.py -r 455 -cDUT 4 -os 3
#com

#SPE DLC 2.5nm
<<com
python3 analyze_SPErun.py -r 468 -c 4 -os 3
python3 analyze_SPErun.py -r 469 -c 4 -os 3
python3 analyze_SPErun.py -r 470 -c 4 -os 3
python3 analyze_SPErun.py -r 471 -c 4 -os 3
com

#PE DLC 2.5nm
<<com
python3 analyze_PErun.py -r 464 -c 4 -os 3
python3 analyze_PErun.py -r 465 -c 4 -os 3
python3 analyze_PErun.py -r 466 -c 4 -os 3
python3 analyze_PErun.py -r 467 -c 4 -os 3
com

###################
###### Pool4 ######
###################

#Timing Pavia Multipad
#pool4
#<<com
#pad88
python3 process_TIMErun.py -r 274 -pDUT 2 -cDUT 4 -os 4
python3 analyze_TIMErun.py -r 274 -cDUT 2 -os 4
#pad22
python3 process_TIMErun.py -r 342 -pDUT 2 -cDUT 4
python3 analyze_TIMErun.py -r 342 -cDUT 2 -os 4
python3 process_TIMErun.py -r 344 -pDUT 2 -cDUT 4
python3 analyze_TIMErun.py -r 344 -cDUT 2 -os 4
#pad28
python3 process_TIMErun.py -r 352 -pDUT 2 -cDUT 4 -os 4
python3 analyze_TIMErun.py -r 352 -cDUT 2 -os 4
#pad55
python3 process_TIMErun.py -r 355 -pDUT 2 -cDUT 2 -os 4
python3 analyze_TIMErun.py -r 355 -cDUT 2 -os 4
#com

###################
###### Pool5 ######
###################

#Timing DLC 2.5nm + 5mm MgF2
#<<com
python3 process_TIMErun.py -r 464 -pDUT 3 -cDUT 2 -os 5
python3 analyze_TIMErun.py -r 464 -cDUT 2 -os 5
python3 process_TIMErun.py -r 465 -pDUT 3 -cDUT 2 -os 5
python3 analyze_TIMErun.py -r 465 -cDUT 2 -os 5
python3 process_TIMErun.py -r 466 -pDUT 3 -cDUT 2 -os 5
python3 analyze_TIMErun.py -r 466 -cDUT 2 -os 5
python3 process_TIMErun.py -r 467 -pDUT 3 -cDUT 2 -os 5
python3 analyze_TIMErun.py -r 467 -cDUT 2 -os 5
#com

#SPE DLC 2.5nm + 5mm MgF2
<<com
python3 analyze_SPErun.py -r 456 -c 2 -os 5
python3 analyze_SPErun.py -r 457 -c 2 -os 5
python3 analyze_SPErun.py -r 458 -c 2 -os 5
python3 analyze_SPErun.py -r 459 -c 2 -os 5
com

#PE DLC 2.5nm + 5mm MgF2
<<com
python3 analyze_PErun.py -r 454 -c 2 -os 5
python3 analyze_PErun.py -r 455 -c 2 -os 5
com