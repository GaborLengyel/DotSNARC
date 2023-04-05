# -*- coding: utf-8 -*-

# 2014.05.03.   resp_code list
# 2014.04.17.   first version;

import time, random
from psychopy import visual, core, sound, event, gui

exp_info = {'participant':'subject_name',
            'response_buttons': ['CD', 'DC', 'te', 'et', 'QP', 'PQ'],
            'range_in_instr':True,
            'autopilot':False}

exp_info['dateStr']= time.strftime("%m_%d_%H%M", time.localtime())
exp_info['exp_id']= 'SNARC'

resp_butt = {'Q':'Q', 'P':'P', 't':'Tab', 'e':'Enter', 'C':'bal Ctrl', 'D':u'jobb oldalon a numerikus részen a tizedes vessző'}
resp_code = {'Q':['q'], 'P':['p'], 't':['tab'], 'e':['return'], 'C':['lctrl'], 'D':['num_decimal', 'num_separator', 'num_delete', 'delete']}

dlg = gui.DlgFromDict(exp_info, title='SNARC', fixed=['dateStr', 'exp_id'],
                      order = ['participant', 'response_buttons', 'range_in_instr', 'autopilot'],
                      tip = {'participant':u'Identifier of the participant.',
                             'response_buttons':u'Which keys to use as response buttons.',
                             'range_in_instr':u'Let the participant know about the number range in the instruction.',
                             'autopilot':u'Use for testing: it will press the response buttons.'})
if not dlg.OK:
    core.quit()

if exp_info['autopilot']:
    import autopilot
    event.waitKeys = autopilot.waitKeys

# Visual objects
win = visual.Window([1200,600], allowGUI=True, fullscr=True, waitBlanking=True, monitor='testMonitor', units='pix') # Create window
text_stimulus = visual.TextStim(win, pos=[0, 7], height = 150, text="dummy")

trial_clock = core.Clock()

numbers = range(1,10)
numbers = numbers * 40

# Make a log file
fileName = exp_info['participant']
dataFile = open(fileName+'.csv', 'a')
dataFile.write(str(exp_info)+'\n')


# Instruction
primary_task_text = u"A képernyőn egy számot fogsz látni. Ha a szám páros, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha a szám páratlan, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt.\n\n"
range_in_instr = u'' if not exp_info['range_in_instr'] else u' A számok %s és %s közt fognak előfordulni.\n\n'%(min(numbers), max(numbers))
text_instruction = visual.TextStim(win, pos=[0,0], text=primary_task_text+range_in_instr+u'A feladat során próbálj meg mindig helyesen és egyben gyorsan is válaszolni.\n\nNyomj egy gombot, ha kezdhetjük.')
text_instruction.draw()
win.flip()
event.waitKeys()

random.shuffle(numbers)
# Trials
for number in numbers:
    text_stimulus.setText(str(number))
    text_stimulus.draw()

    # Measure response
    win.flip()
    trial_clock.reset()
    response = event.waitKeys()[0]
    if response == 'escape':
        core.quit()
    RT = trial_clock.getTime()
    win.flip()
    
    # Feedback
    if (number%2==0 and response in resp_code[exp_info['response_buttons'][0]]) or (number%2==1 and response in resp_code[exp_info['response_buttons'][1]]):
        pass # it was correct
    else:
        feedback_sound = sound.Sound('incorrect.wav')
        feedback_sound.play()
    
    # Write log
    dataFile.write('%s SNARC_only %s %i %s %s\n' %(exp_info['participant'],exp_info['response_buttons'], number, response, RT))
    core.wait(0.7)

if exp_info['autopilot']:
    autopilot.print_results()
