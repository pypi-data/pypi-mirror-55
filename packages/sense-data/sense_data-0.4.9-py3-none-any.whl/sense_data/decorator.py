#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                          
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved                                                      
Author: xuwei                                        
Email: weix@sensedeal.ai                                 
Description:                                    
'''


import time
import sense_core as sd

def catch_except_log(func):
    def try_catch(*args, **kwargs):
        _num = 1
        while True:
            try:
                r = func(*args, **kwargs)
                return r
            except Exception as e:
                time.sleep(1)
                _num += 1
                if _num > 4:
                    sd.log_exception("%s: %s" %(func.__name__, e))
                    return
    return try_catch