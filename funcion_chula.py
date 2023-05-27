# -*- coding: utf-8 -*-
"""
Created on Fri May 26 19:55:16 2023

@author: mromg
"""
def lista_num(num):
    num_up_values = []
    num_down_values = []
    num_down = 0
    num_up = 0
    
    if str(num)[-1] == '9':
        num_down = num - 0.004
        num_up = num + 0.006
    elif str(num)[-1] == '5':
        num_down = num - 0.006
        num_up = num + 0.004  
        
    num_down_values.append(num_down)
    num_up_values.append(num_up)
        
    for i in range(5):
        if str(num_down)[-1] == '9':
            num_down = num_down - 0.004
            num_down_values.append(num_down)
        elif str(num_down)[-1] == '5':
            num_down = num_down - 0.006
            num_down_values.append(num_down)
        if str(num_up)[-1] == '9':
            num_up = num_up + 0.006
            num_up_values.append(num_up)
        elif str(num_up)[-1] == '5':
            num_up = num_up + 0.004
            num_up_values.append(num_up)
            
    return num_up_values, num_down_values

num_up_values, num_down_values = lista_num(1.545)