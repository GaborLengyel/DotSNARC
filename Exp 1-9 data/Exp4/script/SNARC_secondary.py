# -*- coding: utf-8 -*-

# 2014.05.03.   main(); exp_info['interactive_setting']; resp_code list
# 2014.04.17.   error feedback, resp_code; instruction change; exp_info[task];
#               triangle_dir > stim_dir; notation 'empty';
# 2014.03.28    new response_button-s;
# 2014.02.25.   resp_butt; range_in_instr; num stim size;
# 2013.11.27.   first version;

import time, random
from psychopy import visual, core, sound, event, gui

def main(exp_info = {'participant':'subject_name',
            'task':['line', 'triangle'],
            'notation':['arabic', 'dot', 'empty'],
            'response_buttons': ['CD', 'DC', 'te', 'et', 'QP', 'PQ'],
            'range_in_instr':True,
            'autopilot':False,
            'interactive_setting':True}):

    exp_info['dateStr']= time.strftime("%m_%d_%H%M", time.localtime())
    exp_info['exp_id']= 'SNARC'
    
    resp_butt = {'Q':'Q', 'P':'P', 't':'Tab', 'e':'Enter', 'C':'bal Ctrl', 'D':u'jobb oldalon a numerikus részen a tizedes vessző'}
    resp_code = {'Q':['q'], 'P':['p'], 't':['tab'], 'e':['return'], 'C':['lctrl'], 'D':['num_decimal', 'num_separator', 'num_delete']}
    
    if exp_info['interactive_setting']:
        dlg = gui.DlgFromDict(exp_info, title='SNARC', fixed=['dateStr', 'exp_id', 'interactive_setting'],
                              order = ['participant', 'task', 'notation', 'response_buttons', 'range_in_instr', 'autopilot', 'interactive_setting'],
                              tip = {'participant':u'Identifier of the participant.',
                                     'task':u'The primary task.',
                                     'notation':u'Notation of the background values.',
                                     'response_buttons':u'Which keys to use as response buttons.',
                                     'range_in_instr':u'Let the participant know about the number range in the instruction.',
                                     'autopilot':u'Use for testing: it will press the response buttons (works only with keyboard response_device).',
                                     'interactive_setting':u'The user can set the parameters in this window.'})
        if not dlg.OK:
            core.quit()
    
    if exp_info['autopilot']:
        import autopilot
        event.waitKeys = autopilot.waitKeys
    
    # Visual objects
    win = visual.Window([1200,600], allowGUI=True, fullscr=True, waitBlanking=True, monitor='testMonitor', units='pix') # Create window
    text_stimulus = visual.TextStim(win, pos=[0, 7], height = 150, text="dummy")
    dot_object = visual.PatchStim(win,tex="none", mask="gauss", size=(10,10),color='black')
    triangle_up = visual.Polygon(win, edges=3, radius=100, lineWidth = 3)
    triangle_down = visual.Polygon(win, edges=3, radius=100, lineWidth = 3)
    triangle_down.setOri(180)
    color = [0.5, 0.5, 0.5]
    line_vertical = visual.Rect(win, 8, 140, lineColor=color, fillColor = color)
    line_horizontal = visual.Rect(win, 140, 8, lineColor=color, fillColor = color)
    
    trial_clock = core.Clock()
    
    if exp_info['notation'] == 'arabic':
        numbers = range(1,10)
    elif exp_info['notation'] == 'dot':
        numbers = range(1*5,10*5,5)
    elif exp_info['notation'] == 'empty':
        numbers = [0] # These numbers will not be shown
    numbers = numbers * 40
    
    def draw_random_dots(dots_n = 100, shift_x=0, shift_y=0, range_x=100, range_y=100):
        #print dots_n, shift_x, shift_y, range_x, range_y
        for i in range(dots_n):
            dot_object.setColor(random.choice(['black', 'white']))
            dot_object.setPos([random.randint(-range_x, range_x)+shift_x, random.randint(-range_y, range_y)+shift_y])
            dot_object.draw()
    
    # Make a log file
    fileName = exp_info['participant']
    dataFile = open(fileName+'.csv', 'a')
    dataFile.write(str(exp_info)+'\n')
    
    
    # Instruction
    if exp_info['task']=='triangle':
        primary_task_text = u"A képernyőn egy háromszöget fogsz látni. Ha a háromszög felfelé mutat, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha a háromszög lefelé mutat, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt.\n\n"
    elif exp_info['task']=='line':
        primary_task_text = u"A képernyőn egy vonalat fogsz látni. Ha a vonal függőleges, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha a vonal vízszintes, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt.\n\n"
    if exp_info['notation'] in ['arabic', 'dot']:
        range_in_instr = u'' if not exp_info['range_in_instr'] else u' A számok %s és %s közt fognak előfordulni.\n\n'%(min(numbers), max(numbers))
        secondary_stim_text = u'A háttérben '+(u'egy arab számot' if exp_info['notation']=='arabic' else u'pontokat')+u' láthatsz, amivel semmi tennivalód nincs, azt figyelmen kívül hagyhatod.' + range_in_instr
    elif exp_info['notation'] == 'empty':
        secondary_stim_text = u''
    text_instruction = visual.TextStim(win, pos=[0,0], text=primary_task_text+secondary_stim_text+u'A feladat során próbálj meg mindig helyesen és egyben gyorsan is válaszolni.\n\nNyomj egy gombot, ha kezdhetjük.')
    text_instruction.draw()
    win.flip()
    event.waitKeys()
    
    random.shuffle(numbers)
    # Trials
    for number in numbers:
        # Draw secondary stimulus
        if exp_info['notation']=='dot':
            draw_random_dots(dots_n = number)
        elif exp_info['notation']=='arabic':
            text_stimulus.setText(str(number))
            text_stimulus.draw()
        # no action s needed for 'empty' notation
            
        # Draw primary stimulus
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
        dataFile.write('%s SNARC %s %s %s %i %s %s\n' %(exp_info['participant'], exp_info['notation'], exp_info['response_buttons'], stim_dir, number, response, RT))
        core.wait(0.7)
    
    if exp_info['autopilot']:
        autopilot.print_results()
    win.close()

# To run with interactive settings
main()

# To run with settings directed from function call
subject_name = 'subject_name'

''' # CD arabic-dot-empty
main(exp_info = {'participant':subject_name,'task':'line','notation':'arabic','response_buttons':'CD','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'dot','response_buttons':'CD','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'empty','response_buttons':'CD','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
#'''

''' # DC arabic-dot-empty
main(exp_info = {'participant':subject_name,'task':'line','notation':'arabic','response_buttons':'DC','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'dot','response_buttons':'DC','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'empty','response_buttons':'DC','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
#'''

''' # CD dot-arabic-empty
main(exp_info = {'participant':subject_name,'task':'line','notation':'dot','response_buttons':'CD','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'arabic','response_buttons':'CD','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'empty','response_buttons':'CD','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
#'''

''' # DC dot-arabic-empty
main(exp_info = {'participant':subject_name,'task':'line','notation':'dot','response_buttons':'DC','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'arabic','response_buttons':'DC','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
main(exp_info = {'participant':subject_name,'task':'line','notation':'empty','response_buttons':'DC','range_in_instr':True,'autopilot':False, 'interactive_setting':False})
#'''
