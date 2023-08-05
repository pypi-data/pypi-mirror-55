#!/usr/bin/env python
# coding: utf-8

# # Technique Fields
# Field types for each technique.

# In[1]:


from enum import Enum


# In[2]:


class OCV( Enum ):
    Rest_time_T     = float
    Record_every_dE = float
    Record_every_dT = float


# In[3]:


class CV( Enum ):
    vs_initial       = bool
    Voltage_step     = float
    Scan_Rate        = float
    Scan_number      = int
    Record_every_dE  = float
    Average_over_dE  = bool
    N_Cycles         = int
    Begin_measuring_I = float
    End_measuring_I   = float


# In[ ]:


class CA( Enum ):
    Voltage_step      = float
    vs_initial        = bool
    Duration_step     = float
    Step_number       = int
    Record_every_dT   = float
    Record_every_dI   = float
    N_Cycles          = int


# In[ ]:


class CALIMIT( Enum ):
    Voltage_step      = float
    vs_initial        = bool
    Duration_step     = float
    Step_nuber        = int
    Record_every_dT   = float
    Record_every_dI   = float
    Test1_Config      = int
    Test1_Value       = float
    Test2_Config      = int
    Test2_Value       = float
    Test3_Config      = int
    Test3_Value       = float
    Exit_Cond         = int
    N_Cycles          = int

