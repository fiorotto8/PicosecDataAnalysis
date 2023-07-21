#!/bin/bash
###################
###### Pool2 ######
###################

#SPE B4C 10nm
#<<com
python3 analyze_SPErun.py -r 126 -c 2
python3 analyze_SPErun.py -r 127 -c 2
python3 analyze_SPErun.py -r 128 -c 2
#com

#PE B4C 10nm
#<<com
python3 analyze_PErun.py -r 129 -c 2
python3 analyze_PErun.py -r 130 -c 2
python3 analyze_PErun.py -r 131 -c 2
#com

#SPE DLC 2.5 shitty
#<<com
python3 analyze_SPErun.py -r 151 -c 2
python3 analyze_SPErun.py -r 152 -c 2
python3 analyze_SPErun.py -r 153 -c 2
#com

#PE DLC 2.5 shitty
#<<com
python3 analyze_PErun.py -r 154 -c 2
python3 analyze_PErun.py -r 155 -c 2
#com

#SPE DLC B4C 4nm
#<<com
python3 analyze_SPErun.py -r 191 -c 2
python3 analyze_SPErun.py -r 192 -c 2
python3 analyze_SPErun.py -r 193 -c 2
#com

#PE B4C 4nm
#<<com
python3 analyze_PErun.py -r 195 -c 2
python3 analyze_PErun.py -r 196 -c 2
python3 analyze_PErun.py -r 197 -c 2
#com

#SPE DLC 3nm
#<<com
python3 analyze_SPErun.py -r 219 -c 2
python3 analyze_SPErun.py -r 220 -c 2
python3 analyze_SPErun.py -r 221 -c 2
#com

#PE DLC 3nm
#<<com
python3 analyze_PErun.py -r 228 -c 2
python3 analyze_PErun.py -r 229 -c 2
python3 analyze_PErun.py -r 230 -c 2
#com

#Timing Pavia SC Ne/iso 90/10 
#Pool2
<<com
python3 analyze_TIMErun.py -r 30 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 30 -cDUT 2
python3 analyze_TIMErun.py -r 36 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 36 -cDUT 2
python3 analyze_TIMErun.py -r 37 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 37 -cDUT 2
python3 analyze_TIMErun.py -r 46 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 46 -cDUT 2
python3 analyze_TIMErun.py -r 47 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 47 -cDUT 2
python3 analyze_TIMErun.py -r 48 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 48 -cDUT 2
python3 analyze_TIMErun.py -r 49 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 49 -cDUT 2
python3 analyze_TIMErun.py -r 50 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 50 -cDUT 2
python3 analyze_TIMErun.py -r 51 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 51 -cDUT 2
python3 analyze_TIMErun.py -r 55 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 55 -cDUT 2
python3 analyze_TIMErun.py -r 56 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 56 -cDUT 2
com


#Timing Vacuum Chamebr Ne/iso 94/6 
#Pool2
<<com
python3 analyze_TIMErun.py -r 36 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 36 -cDUT 4
python3 analyze_TIMErun.py -r 37 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 37 -cDUT 4
python3 analyze_TIMErun.py -r 46 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 46 -cDUT 4
python3 analyze_TIMErun.py -r 47 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 47 -cDUT 4
python3 analyze_TIMErun.py -r 48 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 48 -cDUT 4
python3 analyze_TIMErun.py -r 49 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 49 -cDUT 4
python3 analyze_TIMErun.py -r 50 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 50 -cDUT 4
python3 analyze_TIMErun.py -r 51 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 51 -cDUT 4
python3 analyze_TIMErun.py -r 55 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 55 -cDUT 4
python3 analyze_TIMErun.py -r 56 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 56 -cDUT 4
com

#Timing Pavia SC standard gas to compare with Ne/iso 90/10 
#Pool2
<<com
python3 analyze_TIMErun.py -r 61 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 61 -cDUT 2
python3 analyze_TIMErun.py -r 62 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 62 -cDUT 2
python3 analyze_TIMErun.py -r 63 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 63 -cDUT 2
python3 analyze_TIMErun.py -r 64 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 64 -cDUT 2
python3 analyze_TIMErun.py -r 65 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 65 -cDUT 2
python3 analyze_TIMErun.py -r 66 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 66 -cDUT 2
com

#Timing Vacuum standard gas to compare with Ne/iso 94/6 
#Pool2
<<com
python3 analyze_TIMErun.py -r 61 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 61 -cDUT 4
python3 analyze_TIMErun.py -r 62 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 62 -cDUT 4
python3 analyze_TIMErun.py -r 63 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 63 -cDUT 4
python3 analyze_TIMErun.py -r 64 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 64 -cDUT 4
python3 analyze_TIMErun.py -r 65 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 65 -cDUT 4
python3 analyze_TIMErun.py -r 66 -pDUT 6 -cDUT 4
python3 process_TIMErun.py -r 66 -cDUT 4
com

#Timing Pavia SC with CsI 
#Pool2
<<com
python3 analyze_TIMErun.py -r 69 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 69 -cDUT 2
python3 analyze_TIMErun.py -r 70 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 70 -cDUT 2
python3 analyze_TIMErun.py -r 71 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 71 -cDUT 2
python3 analyze_TIMErun.py -r 72 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 72 -cDUT 2
python3 analyze_TIMErun.py -r 73 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 73 -cDUT 2
com

#Timing Pavia SC with B4C 10nm
#Pool2
<<com
python3 analyze_TIMErun.py -r 113 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 113 -cDUT 2
python3 analyze_TIMErun.py -r 114 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 114 -cDUT 2
python3 analyze_TIMErun.py -r 115 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 115 -cDUT 2
python3 analyze_TIMErun.py -r 116 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 116 -cDUT 2
com

#Timing Pavia SC with B4C 4nm
#Pool2
<<com
python3 analyze_TIMErun.py -r 186 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 186 -cDUT 2
python3 analyze_TIMErun.py -r 187 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 187 -cDUT 2
python3 analyze_TIMErun.py -r 188 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 188 -cDUT 2
python3 analyze_TIMErun.py -r 189 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 189 -cDUT 2
python3 analyze_TIMErun.py -r 190 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 190 -cDUT 2
com

#Timing Pavia Multipad
#Pool2
<<com
#pad77
python3 analyze_TIMErun.py -r 266 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 266 -cDUT 4
python3 analyze_TIMErun.py -r 270 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 270 -cDUT 4
python3 analyze_TIMErun.py -r 274 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 274 -cDUT 4
com

#Timing DLC 2.5nm
<<com
python3 analyze_TIMErun.py -r 417 -pDUT 5 -cDUT 4
python3 process_TIMErun.py -r 417 -cDUT 4
python3 analyze_TIMErun.py -r 418 -pDUT 5 -cDUT 4
python3 process_TIMErun.py -r 418 -cDUT 4
python3 analyze_TIMErun.py -r 419 -pDUT 5 -cDUT 4
python3 process_TIMErun.py -r 419 -cDUT 4
python3 analyze_TIMErun.py -r 420 -pDUT 5 -cDUT 4
python3 process_TIMErun.py -r 420 -cDUT 4
python3 analyze_TIMErun.py -r 421 -pDUT 5 -cDUT 4
python3 process_TIMErun.py -r 421 -cDUT 4
com

###################
###### Pool3 ######
###################

#Timing DLC 2.5nm
<<com
python3 analyze_TIMErun.py -r 454 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 454 -cDUT 4
python3 analyze_TIMErun.py -r 455 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 455 -cDUT 4
com

#SPE DLC 2.5nm
<<com
python3 analyze_SPErun.py -r 468 -c 4
python3 analyze_SPErun.py -r 469 -c 4
python3 analyze_SPErun.py -r 470 -c 4
python3 analyze_SPErun.py -r 471 -c 4
com

#PE DLC 2.5nm
<<com
python3 analyze_PErun.py -r 464 -c 4
python3 analyze_PErun.py -r 465 -c 4
python3 analyze_PErun.py -r 466 -c 4
python3 analyze_PErun.py -r 467 -c 4
com

###################
###### Pool4 ######
###################

#Timing Pavia Multipad
#pool4
<<com
#pad88
python3 analyze_TIMErun.py -r 274 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 274 -cDUT 2  
#pad22
python3 analyze_TIMErun.py -r 342 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 342 -cDUT 2  
python3 analyze_TIMErun.py -r 344 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 344 -cDUT 2  
#pad28
python3 analyze_TIMErun.py -r 352 -pDUT 2 -cDUT 4
python3 process_TIMErun.py -r 352 -cDUT 2  
#pad55
python3 analyze_TIMErun.py -r 355 -pDUT 2 -cDUT 2
python3 process_TIMErun.py -r 355 -cDUT 2  
com

###################
###### Pool5 ######
###################

#Timing DLC 2.5nm + 5mm MgF2
<<com
python3 analyze_TIMErun.py -r 464 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 464 -cDUT 2
python3 analyze_TIMErun.py -r 465 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 465 -cDUT 2
python3 analyze_TIMErun.py -r 466 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 466 -cDUT 2
python3 analyze_TIMErun.py -r 467 -pDUT 3 -cDUT 2
python3 process_TIMErun.py -r 467 -cDUT 2
com

#SPE DLC 2.5nm + 5mm MgF2
<<com
python3 analyze_SPErun.py -r 456 -c 2
python3 analyze_SPErun.py -r 457 -c 2
python3 analyze_SPErun.py -r 458 -c 2
python3 analyze_SPErun.py -r 459 -c 2
com

#PE DLC 2.5nm + 5mm MgF2
<<com
python3 analyze_PErun.py -r 454 -c 2
python3 analyze_PErun.py -r 455 -c 2
com