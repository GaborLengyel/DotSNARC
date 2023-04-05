# -*- coding: utf-8 -*-
# 2012.12.07.   First version

"""
Autopilot for PsychoPy experiments.

What does it do?
================
- Autopilot responds instead of the participants.
- It can return a list which lines called it and how many times.
- Works only with waitKeys() at the moment.
-- It returns 'autopilot' response.

Similar OpenSesame feature: enable auto-response (in Run menu or in Preferences)
Similar Presentation feature (maybe): http://www.neurobs.com/menu_presentation/menu_features/features_list#Programmability

What is it good for?
====================
It is useful to
- specify the number of keypresses from different places
- test the conditions and stimuli
- test the logfile
- test any error within the script that is only detectable while running

How to use it?
==============

# At the beggining of the script:
autopilot_on=True
if autopilot_on: # exp_info['autopilot']
    import autopilot
    event.waitKeys = autopilot.waitKeys

# At the end of the script:
if autopilot_on: # exp_info['autopilot']
    autopilot.print_results()

"""

import inspect

call_lines = []

def waitKeys(maxWait=0, keyList=None, timeStamped=False): # http://www.psychopy.org/api/event.html
    global call_lines
    call_lines.append(inspect.stack()[1][2]) # http://benno.id.au/blog/2011/01/06/python-get-caller
    return ['autopilot'] # it was None formerly

def print_results():
    print 'Autopilot calling lines and number of calls:'
    for line in sorted(set(call_lines)):
        print 'Line', line, ':', call_lines.count(line)

"""
def test_calling_line():
    print inspect.stack()[1][2] # http://benno.id.au/blog/2011/01/06/python-get-caller
test_calling_line()
#"""