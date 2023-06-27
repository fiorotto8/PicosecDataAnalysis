#!/bin/bash

#For Chiara Local
#<<com
python3 analyze_SPErun.py -r C103/A275C540/noise+signal/ -c 1
python3 analyze_SPErun.py -r C103/A275C550/noise+signal/ -c 1
python3 analyze_SPErun.py -r C103/A275C560/noise+signal/ -c 1
python3 analyze_SPErun.py -r C104/A275C540/noise+signal/ -c 1
python3 analyze_SPErun.py -r C104/A275C550/noise+signal/ -c 1
python3 analyze_SPErun.py -r C104/A275C560/noise+signal/ -c 1
python3 analyze_SPErun.py -r C105/A275C540/noise+signal/ -c 1
python3 analyze_SPErun.py -r C105/A275C550/noise+signal/ -c 1
python3 analyze_SPErun.py -r C105/A275C560/noise+signal/ -c 1
#com

#For alexandra Pool2
<<com
python3 analyze_PErun.py -r 133 -c 4
python3 analyze_PErun.py -r 135 -c 4
python3 analyze_PErun.py -r 136 -c 4
python3 analyze_PErun.py -r 161 -c 4
python3 analyze_PErun.py -r 162 -c 4
python3 analyze_SPErun.py -r 163 -c 4
python3 analyze_SPErun.py -r 164 -c 4
com


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
#irst PE run B4c 7nm
<<com
python3 analyze_PErun.py -r 323 -c 4
python3 analyze_PErun.py -r 324 -c 4
python3 analyze_PErun.py -r 329 -c 4
python3 analyze_PErun.py -r 330 -c 4
com
#second PE run B4c 7nm
<<com
python3 analyze_PErun.py -r 373 -c 4
python3 analyze_PErun.py -r 374 -c 4
python3 analyze_PErun.py -r 375 -c 4
python3 analyze_PErun.py -r 376 -c 4
com

#CsI PEs
<<com
python3 analyze_PErun.py -r 389 -c 4
python3 analyze_PErun.py -r 390 -c 4
python3 analyze_PErun.py -r 391 -c 4
com

#precess timing runs
<<com
python3 process_TIMErun.py -r 182 -cDUT 2
python3 process_TIMErun.py -r 183 -cDUT 2
python3 process_TIMErun.py -r 184 -cDUT 2
python3 process_TIMErun.py -r 185 -cDUT 2
python3 process_TIMErun.py -r 186 -cDUT 2
python3 process_TIMErun.py -r 187 -cDUT 2
python3 process_TIMErun.py -r 188 -cDUT 2
python3 process_TIMErun.py -r 189 -cDUT 2
python3 process_TIMErun.py -r 190 -cDUT 2
python3 process_TIMErun.py -r 191 -cDUT 2
python3 process_TIMErun.py -r 192 -cDUT 2
python3 process_TIMErun.py -r 193 -cDUT 2
python3 process_TIMErun.py -r 194 -cDUT 2
python3 process_TIMErun.py -r 195 -cDUT 2
python3 process_TIMErun.py -r 196 -cDUT 2
python3 process_TIMErun.py -r 197 -cDUT 2
python3 process_TIMErun.py -r 198 -cDUT 2
python3 process_TIMErun.py -r 199 -cDUT 2
python3 process_TIMErun.py -r 200 -cDUT 2
python3 process_TIMErun.py -r 209 -cDUT 2
python3 process_TIMErun.py -r 211 -cDUT 2
python3 process_TIMErun.py -r 212 -cDUT 2
python3 process_TIMErun.py -r 213 -cDUT 2
python3 process_TIMErun.py -r 214 -cDUT 2
python3 process_TIMErun.py -r 215 -cDUT 2
python3 process_TIMErun.py -r 216 -cDUT 2
python3 process_TIMErun.py -r 217 -cDUT 2
python3 process_TIMErun.py -r 218 -cDUT 2
python3 process_TIMErun.py -r 219 -cDUT 2
python3 process_TIMErun.py -r 220 -cDUT 2
python3 process_TIMErun.py -r 221 -cDUT 2
python3 process_TIMErun.py -r 222 -cDUT 2
python3 process_TIMErun.py -r 223 -cDUT 2
python3 process_TIMErun.py -r 224 -cDUT 2
python3 process_TIMErun.py -r 225 -cDUT 2
python3 process_TIMErun.py -r 226 -cDUT 2
python3 process_TIMErun.py -r 227 -cDUT 2
python3 process_TIMErun.py -r 228 -cDUT 2
python3 process_TIMErun.py -r 229 -cDUT 2
python3 process_TIMErun.py -r 236 -cREF 2
python3 process_TIMErun.py -r 237 -cREF 2
python3 process_TIMErun.py -r 239
python3 process_TIMErun.py -r 240 -cREF 2
python3 process_TIMErun.py -r 243
python3 process_TIMErun.py -r 244
python3 process_TIMErun.py -r 342
python3 process_TIMErun.py -r 343
python3 process_TIMErun.py -r 344
python3 process_TIMErun.py -r 345
python3 process_TIMErun.py -r 346
python3 process_TIMErun.py -r 347
python3 process_TIMErun.py -r 348
python3 process_TIMErun.py -r 350
python3 process_TIMErun.py -r 355
python3 process_TIMErun.py -r 357
python3 process_TIMErun.py -r 359
python3 process_TIMErun.py -r 360
python3 process_TIMErun.py -r 361
python3 process_TIMErun.py -r 362
python3 process_TIMErun.py -r 380
python3 process_TIMErun.py -r 381
python3 process_TIMErun.py -r 382
python3 process_TIMErun.py -r 399
python3 process_TIMErun.py -r 400
python3 process_TIMErun.py -r 401
python3 process_TIMErun.py -r 402
python3 process_TIMErun.py -r 403
com

#analyse timing runs
<<com
python3 analyze_TIMErun.py -r 182
python3 analyze_TIMErun.py -r 183
python3 analyze_TIMErun.py -r 184
python3 analyze_TIMErun.py -r 185
python3 analyze_TIMErun.py -r 186
python3 analyze_TIMErun.py -r 187
python3 analyze_TIMErun.py -r 188
python3 analyze_TIMErun.py -r 189
python3 analyze_TIMErun.py -r 190
python3 analyze_TIMErun.py -r 191
python3 analyze_TIMErun.py -r 192
python3 analyze_TIMErun.py -r 193
python3 analyze_TIMErun.py -r 194
python3 analyze_TIMErun.py -r 195
python3 analyze_TIMErun.py -r 196
python3 analyze_TIMErun.py -r 197
python3 analyze_TIMErun.py -r 198
python3 analyze_TIMErun.py -r 199
python3 analyze_TIMErun.py -r 200
python3 analyze_TIMErun.py -r 209
python3 analyze_TIMErun.py -r 211
python3 analyze_TIMErun.py -r 212
python3 analyze_TIMErun.py -r 213
python3 analyze_TIMErun.py -r 214
python3 analyze_TIMErun.py -r 215
python3 analyze_TIMErun.py -r 216
python3 analyze_TIMErun.py -r 217
python3 analyze_TIMErun.py -r 218
python3 analyze_TIMErun.py -r 219
python3 analyze_TIMErun.py -r 220
python3 analyze_TIMErun.py -r 221
python3 analyze_TIMErun.py -r 222
python3 analyze_TIMErun.py -r 223
python3 analyze_TIMErun.py -r 224
python3 analyze_TIMErun.py -r 225
python3 analyze_TIMErun.py -r 226
python3 analyze_TIMErun.py -r 227
python3 analyze_TIMErun.py -r 228
python3 analyze_TIMErun.py -r 229
python3 analyze_TIMErun.py -r 236
python3 analyze_TIMErun.py -r 237
python3 analyze_TIMErun.py -r 239
python3 analyze_TIMErun.py -r 240
python3 analyze_TIMErun.py -r 243
python3 analyze_TIMErun.py -r 244
python3 analyze_TIMErun.py -r 342
python3 analyze_TIMErun.py -r 343
python3 analyze_TIMErun.py -r 344
python3 analyze_TIMErun.py -r 345
python3 analyze_TIMErun.py -r 346
python3 analyze_TIMErun.py -r 347
python3 analyze_TIMErun.py -r 348
python3 analyze_TIMErun.py -r 350
python3 analyze_TIMErun.py -r 355
python3 analyze_TIMErun.py -r 357
python3 analyze_TIMErun.py -r 359
python3 analyze_TIMErun.py -r 360
python3 analyze_TIMErun.py -r 361
python3 analyze_TIMErun.py -r 362
python3 analyze_TIMErun.py -r 380
python3 analyze_TIMErun.py -r 381
python3 analyze_TIMErun.py -r 382
python3 analyze_TIMErun.py -r 399
python3 analyze_TIMErun.py -r 400
python3 analyze_TIMErun.py -r 401
python3 analyze_TIMErun.py -r 402
python3 analyze_TIMErun.py -r 403
com
