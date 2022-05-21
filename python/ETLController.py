# -*- coding: utf-8 -*-
"""
Version Number ||| Mod By  ||| Version Date
---------------------------------------------------------
1.00           |||  GM     ||| 19 May  2022

"""

from weather_mySQl_snowflake import runweatherPipe
from stravaPipeline import stravaPipe

### here want to get config from database on where to run or not
### need to add log / configuration table 


runweatherPipe()
stravaPipe()
