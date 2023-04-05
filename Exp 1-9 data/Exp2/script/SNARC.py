# -*- coding: utf-8 -*-

# 2014.02.25.   resp_butt; range_in_instr; num stim size;
# 2013.11.27.   first version;

import time, random
from psychopy import visual, core, event, gui

exp_info = {'participant':'subject_name',
            'notation':['arabic', 'dot'],
            'response_buttons': ['te', 'et', 'QP', 'PQ'],
            'range_in_instr':True,
            'autopilot':False}

exp_info['dateStr']= time.strftime("%m_%d_%H%M", time.localtime())
exp_info['exp_id']= 'SNARC'

resp_butt = {'Q':'Q', 'P':'P', 't':'Tab', 'e':'Enter'}

dlg = gui.DlgFromDict(exp_info, title='SNARC', fixed=['dateStr', 'exp_id'],
                      order = ['participant', 'notation', 'response_buttons', 'range_in_instr', 'autopilot'],
                      tip = {'participant':u'Identifier of the participant.',
                             'notation':u'Notation of the background values.',
                             'response_buttons':u'Which keys to use as response buttons.',
                             'range_in_instr':u'Let the participant know about the number range in the instruction.',
                             'autopilot':u'Use for testing: it will press the response buttons (works only with keyboard response_device).'})
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

trial_clock = core.Clock()

if exp_info['notation'] == 'arabic':
    numbers = range(1,10)
elif exp_info['notation'] == 'dot':
    numbers = range(1*5,10*5,5)
numbers = numbers * 40

def draw_random_dots(dots_n = 100, shift_x=0, shift_y=0, range_x=100, range_y=100):
    #print dots_n, shift_x, shift_y, range_x, range_y
    # dots
    for i in range(dots_n):
        dot_object.setColor(random.choice(['black', 'white']))
        dot_object.setPos([random.randint(-range_x, range_x)+shift_x, random.randint(-range_y, range_y)+shift_y])
        dot_object.draw()

# Make a log file
fileName = exp_info['participant']
dataFile = open(fileName+'.csv', 'a')
dataFile.write(str(exp_info)+'\n')


# Instruction
range_in_instr = u'' if not exp_info['range_in_instr'] else u' A számok %s és %s közt fognak előfordulni.'%(min(numbers), max(numbers))
print range_in_instr
text_instruction = visual.TextStim(win, pos=[0,0], text=u"A képernyőn egy háromszöget fogsz látni. Ha a háromszög felfelé mutat, akkor nyomd meg a '"+resp_butt[exp_info['response_buttons'][0]]+u"' billentyűt. Ha a háromszög lefelé mutat, nyomd meg a '"+resp_butt[exp_info['response_buttons'][1]]+u"' billentyűt.\n\nA háromszög mögött "+(u'egy arab számot' if exp_info['notation']=='arabic' else u'pontokat')+u' láthatsz, amivel semmi tennivalód nincs, azt figyelmen kívül hagyhatod.'+range_in_instr+u'\n\nNyomj egy gombot, ha kezdhetjük.')
text_instruction.draw()
win.flip()
event.waitKeys()

random.shuffle(numbers)
# Trials
for number in numbers:
    if exp_info['notation']=='dot':
        draw_random_dots(dots_n = number)
    elif exp_info['notation']=='arabic':
        text_stimulus.setText(str(number))
        text_stimulus.draw()
    if random.choice([True, False]):
        triangle_up.draw()
        triangle_dir = 'up'
    else:
        triangle_down.draw()
        triangle_dir = 'down'

    win.flip()
    trial_clock.reset()
    response = event.waitKeys()[0]
    if response == 'escape':
        core.quit()
    RT = trial_clock.getTime()
    win.flip()

    dataFile.write('%s SNARC %s %s %s %i %s %s\n' %(exp_info['participant'], exp_info['notation'], exp_info['response_buttons'], triangle_dir, number, response, RT))
    core.wait(0.7)

if exp_info['autopilot']:
    autopilot.print_results()
