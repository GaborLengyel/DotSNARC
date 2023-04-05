# -*- coding: utf-8 -*-

# 2016.11.25. Automatic and parity SNARC paradigms in a single script (main_automatic and main_parity);

'''Automatic SNARC effect paradigm
'''

# 2015.11.27.   fix_area;
# 2015.11.13.   minor modifications;
# 2015.10.21.   black "shadow" for symb stims; background_stim_color; small code fixes;
# 2014.10.20.   new 'task': 'color'; 'delay' param;
#               draw_random_dots dot_poss and dot_cols params;
# 2014.09.13    small fixes;
# 2014.05.03.   main(); exp_info['interactive_setting']; resp_code list
# 2014.04.17.   error feedback, resp_code; instruction change; exp_info[task];
#               triangle_dir > stim_dir; notation 'empty';
# 2014.03.28    new response_button-s;
# 2014.02.25.   resp_butt; range_in_instr; num stim size;
# 2013.11.27.   first version;

import time, random
from psychopy import visual, core, sound, event, gui
import numpy as np

def main_automatic(exp_info = {'participant':'participant_id',
            'task':['color', 'line', 'triangle'],
            'notation':['dot', 'arabic', 'empty'],
            'background_stim_color': ['random', 'default', 'white'],
            'delay':[0, 200, 400, 600],
            'response_buttons': ['CD', 'DC', 'te', 'et', 'QP', 'PQ'],
            'range_in_instr':True,
            'autopilot':False,
            'interactive_setting':True}):

    exp_info['dateStr']= time.strftime("%m_%d_%H%M", time.localtime())
    exp_info['exp_id']= 'SNARC_automatic'
    
    resp_butt = {'Q':'Q', 'P':'P', 't':'Tab', 'e':'Enter', 'C':'bal Ctrl', 'D':u'jobb oldalon a numerikus részen a tizedes vessző'}
    resp_code = {'Q':['q'], 'P':['p'], 't':['tab'], 'e':['return'], 'C':['lctrl'], 'D':['num_decimal', 'num_separator', 'num_delete', 'delete']}
    
    if exp_info['interactive_setting']:
        dlg = gui.DlgFromDict(exp_info, title='SNARC', fixed=['dateStr', 'exp_id', 'interactive_setting'],
                              order = ['participant', 'task', 'notation', 'background_stim_color', 'delay', 'response_buttons', 'range_in_instr', 'autopilot', 'interactive_setting'],
                              tip = {'participant': u'Identifier of the participant.',
                                     'task': u'The primary task.',
                                     'notation': u'Notation of the background values. In color task it is the only stim.',
                                     'background_stim_color': u'Color of the bakcground stimuli. Ignored in color task.',
                                     'delay': u'Delay in the presentation of the relevant feature (in ms).',
                                     'response_buttons': u'Which keys to use as response buttons.',
                                     'range_in_instr': u'Let the participant know about the number range in the instruction.',
                                     'autopilot': u'Use for testing: it will press the response buttons.',
                                     'interactive_setting': u'Parameters can be set in this window.'})
        if not dlg.OK:
            core.quit()
    
    if exp_info['autopilot']:
        import autopilot
        event.waitKeys = autopilot.waitKeys
    
    # Visual objects
    win = visual.Window([1200,600], allowGUI=True, fullscr=True, waitBlanking=True, monitor='testMonitor', units='pix') # Create window
    symb_stim = visual.TextStim(win, pos=[0, 7], height = 80, text='dummy')
    symb_stim_2 = visual.TextStim(win, pos=[0+4, 7-4], height = 80, text='dummy')  # shadow stim
    symb_stim_random = visual.GratingStim(win, tex='none', mask='none', size=(100, 100))
    dot_object = visual.GratingStim(win, tex='none', mask='circle', size=(10, 10), color='black')
    triangle_up = visual.Polygon(win, edges=3, radius=100, lineWidth=3)
    triangle_down = visual.Polygon(win, edges=3, radius=100, lineWidth=3)
    triangle_down.setOri(180)
    line_color = [0.5, 0.5, 0.5]
    line_vertical = visual.Rect(win, 4, 140, lineColor=line_color, fillColor = line_color)
    line_horizontal = visual.Rect(win, 140, 4, lineColor=line_color, fillColor = line_color)
    
    trial_clock = core.Clock()
    
    if exp_info['notation'] == 'arabic':
        numbers = range(1,10)
    elif exp_info['notation'] == 'dot':
        numbers = range(1*5,10*5,5)
        mid_number = (5+50)/2  # used for changing the area
    elif exp_info['notation'] == 'empty':
        numbers = [0] # These numbers will not be shown
    numbers = numbers * 40
    
    def draw_random_dots(dots_n = 100, dot_color='default', dot_poss=None, dot_cols=None, shift_x=0, shift_y=0, range_xy=100, fix_area=True):
        """dot_cols param overwrites color param.
        """
        #print dots_n, shift_x, shift_y, range_xy
        #print color, dot_poss, dot_cols
        
        # dot_poss=[] in def line will not do, cause it stores the previous values
        if not dot_poss:
            dot_poss = []
        if not dot_cols:
            dot_cols = []
        use_given_poss = bool(dot_poss)
        use_given_cols = bool(dot_cols)
        
        if fix_area:
            new_range_xy = int(((((range_xy*2)**2) * (dots_n/float(mid_number))) ** 0.5)/2)  # square root of (original_area * percent_to_be_resized)
            #print dots_n, mid_number, range_xy, new_range_xy
        else:
            new_range_xy = range_xy

        for i in range(dots_n):
            if use_given_cols:
                dot_object.setColor(dot_cols[i])
            else:
                if dot_color in ['default', 'random']:
                    dot_cols.append(random.choice(['black', 'white']))
                elif dot_color == 'red':
                    dot_cols.append(random.choice([(0, -1, -1), (1, 0.5, 0.5)])) # dark and light red
                elif dot_color == 'green':
                    dot_cols.append(random.choice([(-1, 0, -1), (0.5, 1, 0.5)])) # dark and light green
                elif dot_color == 'blue':
                    dot_cols.append(random.choice([(-1, -1, 0), (0.5, 0.5, 1)])) # dark and light blue
                else:
                    dot_cols.append(dot_color)
                dot_object.setColor(dot_cols[-1], 'rgb')
            if use_given_poss:
                dot_object.setPos(dot_poss[i])
            else:
                dot_poss.append([random.randint(-new_range_xy, new_range_xy)+shift_x, random.randint(-new_range_xy, new_range_xy)+shift_y])
                dot_object.setPos(dot_poss[-1])
            dot_object.draw()
        return dot_poss, dot_cols
    
    # Make a log file
    fileName = exp_info['participant']
    dataFile = open(fileName+'.csv', 'a')
    dataFile.write(str(exp_info)+'\n')
    
    
    # Instruction
    if exp_info['task']=='triangle':
        primary_task_text = u"A képernyőn egy háromszöget fogsz látni. Ha a háromszög felfelé mutat, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha a háromszög lefelé mutat, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt.\n\n"
    elif exp_info['task']=='line':
        primary_task_text = u"A képernyőn egy vonalat fogsz látni. Ha a vonal függőleges, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha a vonal vízszintes, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt.\n\n"
    elif exp_info['task']=='color':
        primary_task_text = u"A képernyőn pontokat vagy arab számot fogsz látni, aminek a színéről kell dönteni. Ha az inger vörös, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha az inger kék, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt. Az ingerek mennyisége nem fontos a színdöntés szempontjából, azt figyelmen kívül hagyhatod.\n\n"
    if exp_info['notation'] in ['arabic', 'dot'] and exp_info['task']!='color':
        range_in_instr = u'' if not exp_info['range_in_instr'] else u' A %s %s és %s közt fognak előfordulni.\n\n'%(u'számok' if exp_info['notation']=='arabic' else u'számuk', min(numbers), max(numbers))
        secondary_stim_text = u'A háttérben '+(u'egy arab számot' if exp_info['notation']=='arabic' else u'pontokat')+u' láthatsz, amivel semmi tennivalód nincs, azt figyelmen kívül hagyhatod.' + range_in_instr
    elif exp_info['notation'] == 'empty':
        secondary_stim_text = u''
    else:
        secondary_stim_text = u''
    text_instruction = visual.TextStim(win, pos=[0,0], text=primary_task_text + secondary_stim_text + u'A feladat során próbálj meg mindig helyesen és egyben gyorsan is válaszolni.\n\nNyomj egy gombot, ha kezdhetjük.')
    text_instruction.draw()
    win.flip()
    event.waitKeys()
    
    random.shuffle(numbers)
    # Trials
    for number in numbers:
        
        # specify the colors if necessary
        if exp_info['task']=='color':
            if random.choice([True, False]):
                stim_color = 'red'
                stim_dir = 'up'
            else:
                stim_color = 'blue'
                stim_dir = 'down'
        else:
            stim_color = exp_info['background_stim_color']

        if stim_color == 'random':
            symb_stim_random.tex = np.random.choice([-1, 1], (50, 50))  # random pattern
            #symb_stim_random.tex = np.tile([[-1,1], [1,-1]], (10, 10))  # checker pattern

        # 1 Draw the stimuli without the relevant feature
        if int(exp_info['delay']): # if the delay is not 0
            if exp_info['task']=='color':
                if exp_info['notation']=='dot':
                    dot_poss, dot_cols = draw_random_dots(dots_n = number, dot_color='white')
                elif exp_info['notation']=='arabic':
                    symb_stim.setColor('white')
                    symb_stim.setText(str(number))
                    symb_stim.draw()
            else:
                if exp_info['notation']=='dot':
                    dot_poss, dot_cols = draw_random_dots(dots_n = number, dot_color=stim_color)
                    # color could be only 'default' or 'random' now
                elif exp_info['notation']=='arabic':
                    if stim_color == 'random':
                        symb_stim_random.mask = 'number_masks/'+str(number)+'.png'
                        symb_stim_random.draw()
                    else:
                        symb_stim.setColor('white' if stim_color=='default' else stim_color)
                        symb_stim.setText(str(number))
                        symb_stim.draw()
            win.flip()
            core.wait(int(exp_info['delay'])/1000.0)

        # Draw the stimuli with relevant features
        # 2a Draw secondary/numeric stimulus
        if exp_info['notation']=='dot':
            if stim_color in ['default', 'random']: # keeps the random color
                if int(exp_info['delay']):
                    draw_random_dots(dots_n = number, dot_poss=dot_poss, dot_cols=dot_cols)
                else:
                    draw_random_dots(dots_n = number, dot_color=stim_color)
            else: # uses new color
                if int(exp_info['delay']):
                    draw_random_dots(dots_n = number, dot_color=stim_color, dot_poss=dot_poss)
                else:
                    draw_random_dots(dots_n = number, dot_color=stim_color)
        elif exp_info['notation']=='arabic':
            if stim_color == 'random':
                symb_stim_random.mask = 'number_masks/'+str(number)+'.png'
                symb_stim_random.draw()
            else:
                symb_stim.setColor('white' if stim_color == 'default' else stim_color)
                symb_stim.setText(str(number))
                """
                if stim_color == 'default':
                    symb_stim_2.setColor('black')
                    symb_stim_2.setText(str(number))
                    symb_stim_2.draw()
                """
                symb_stim.draw()
        # no action is needed for 'empty' notation
            
        # 2b Draw primary/non-numeric stimulus
        if exp_info['task']!='color':
            if random.choice([True, False]):
                if exp_info['task']=='triangle':
                    triangle_up.draw()
                else: # line
                    line_vertical.draw()
                stim_dir = 'up'
            else:
                if exp_info['task']=='triangle':
                    triangle_down.draw()
                else: # line
                    line_horizontal.draw()            
                stim_dir = 'down'
    
        # Measure response
        win.flip()
        trial_clock.reset()
        response = event.waitKeys()[0]
        if response == 'escape':
            core.quit()
        RT = trial_clock.getTime()
        win.flip()
        
        # Feedback
        if (stim_dir == 'up' and response in resp_code[exp_info['response_buttons'][0]]) or (stim_dir == 'down' and response in resp_code[exp_info['response_buttons'][1]]):
            pass # it was correct
        else:
            feedback_sound = sound.Sound('incorrect.wav')
            feedback_sound.play()
        
        # Write log
        dataFile.write('%s SNARC %s %s %s %s %s %i %s %s\n' %(exp_info['participant'], exp_info['task'], exp_info['notation'], exp_info['response_buttons'], exp_info['delay'], stim_dir, number, response, RT))
        core.wait(0.7)
    
    if exp_info['autopilot']:
        autopilot.print_results()
    win.close()



"""Parity SNARC effect paradigm"""

# 2014.05.03.   resp_code list
# 2014.04.17.   first version;

import time, random
from psychopy import visual, core, sound, event, gui

def main_parity(exp_info = {'participant':'subject_name',
            'response_buttons': ['CD', 'DC', 'te', 'et', 'QP', 'PQ'],
            'range_in_instr':True,
            'autopilot':False,
            'interactive_setting':True}):

    exp_info['dateStr']= time.strftime("%m_%d_%H%M", time.localtime())
    exp_info['exp_id']= 'SNARC_parity'

    resp_butt = {'Q':'Q', 'P':'P', 't':'Tab', 'e':'Enter', 'C':'bal Ctrl', 'D':u'jobb oldalon a numerikus részen a tizedes vessző'}
    resp_code = {'Q':['q'], 'P':['p'], 't':['tab'], 'e':['return'], 'C':['lctrl'], 'D':['num_decimal', 'num_separator', 'num_delete', 'delete']}

    if exp_info['interactive_setting']:
        dlg = gui.DlgFromDict(exp_info, title='SNARC', fixed=['dateStr', 'exp_id', 'interactive_setting'],
                            order = ['participant', 'response_buttons', 'range_in_instr', 'autopilot', 'interactive_setting'],
                            tip = {'participant':u'Identifier of the participant.',
                                   'response_buttons':u'Which keys to use as response buttons.',
                                   'range_in_instr':u'Let the participant know about the number range in the instruction.',
                                   'autopilot':u'Use for testing: it will press the response buttons.',
                                   'interactive_setting': u'Parameters can be set in this window.'})
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
    
    

exp_info = {'participant':'participant_id',
            'condition':['1', '2', '3', '4'],
            'autopilot':False}

dlg = gui.DlgFromDict(exp_info, title='SNARC_super',
                      order = ['participant', 'condition', 'autopilot'],
                      tip = {'participant': u'Identifier of the participant.',
                             'condition': u'Number of the condition version.',
                             'autopilot': u'Use for testing: it will press the response buttons.'})
if not dlg.OK:
    core.quit()
   
if exp_info['condition'] == '1':
    # 1. arabic-DC, dot-DC, arabic-CD, dot-CD
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

elif exp_info['condition'] == '2':
    # 2. arabic-CD, dot-CD, arabic-DC, dot-DC
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

elif exp_info['condition'] == '3':
    # 3. dot-DC, arabic-DC, dot-CD, arabic-CD
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
elif exp_info['condition'] == '4':
    # 4. dot-CD, arabic-CD, dot-DC, arabic-DC
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'dot', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_automatic(exp_info = {'participant':exp_info['participant'], 'task':'color', 'notation':'arabic', 'background_stim_color': 'random', 'delay':0, 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'CD', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})
    main_parity(exp_info = {'participant':exp_info['participant'], 'response_buttons': 'DC', 'range_in_instr':True, 'autopilot':exp_info['autopilot'], 'interactive_setting':False})

