# PCBS_workingmemory 
## INTRODUCTION

Many studies have reported a negative correlation between aging and working memory (Klencklen, and al. 2017). The working memory, firstly introduced by Baddeley in 1974, is a cognitive process that enables to keep in memory a certain amount of information during a short period. This type of memory can be perfectly illustrated in a spatial working memory task (Song, and al., 2013). 
Therefore, this project aims to show a decline of the working memory with aging, by programming a spatial working memory task performed by participants from all ages (but ideally from 18 to more). It is however supposed that the apogee of the working memory is reached at the end of teenagehood, and then follows the decline of this type of memory (Klingberg, 2007). 

The task described will consist of 3 blocks of 3 trials. In each trial, a virgin canvas (or matrix) of 3x3 will be presented, and the block will begin after the participant pressed the space bar. Colours corresponding to a specific localisation on the canvas will successively and randomly pop up such as creating a sequence of 5, 7, and 9 colours corresponding to the 1st, 2nd and 3rd block. This way, the difficulty of the task increases. Each participant is hence, confronted to 9 trials with increasing difficulty. 
The colours appear successively at a speed 1/1 s. 
At the end of each trial, the participant will have to reproduce the sequence: either by clicking on the cell of the canvas or by assimilating the digit pad to the matrix cells.
The participant won't be informed of his/her successness. 
The experiment collects the data of each participant and all the data will be little by little added to an overall plot, only for the purpose of the experimenters. 
  

## CODE EXPLANATION
### main.py
#### Setting the constants of the stimuli
Constants have first been created, such as indicating the size of the stimuli trials (5, 7 and 9), the size of the blocks (3 trials per block), the size of the canvas (background matrix), the duration between the stimuli presentation (1s), the duration between each trial (1s), the coulours that'll correspond to the stimuli and the background canvas. Texts are also add. 
<pre><code>
# Constants
TRIAL_SIZE = [5, 7, 9]
BLOCK_SIZE = [3, 3, 3]

SIZE_SQUARE = 100
TIME_BTW_STIM = 1000
TIME_BTW_TRIAL = 1000
COLOURS = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (255, 128, 0),
           (255, 0, 127), (0, 128, 255)]
CANVAS_COLOR = (100,100,100)
TEXT_BTW_STIM = "Get ready!"
TEXT_BTW_TRANSITION = "Now, your turn to reproduce the sequence!"
CANVAS_SIZE = SIZE_SQUARE * 3 + 10
RECT_RELATIVE_POSITIONS = [(-SIZE_SQUARE - 5, -SIZE_SQUARE - 5), (0, -SIZE_SQUARE - 5),
                           (SIZE_SQUARE + 5, -SIZE_SQUARE - 5),
                           (-SIZE_SQUARE - 5, 0), (0, 0), (SIZE_SQUARE + 5, 0),
                           (-SIZE_SQUARE - 5, SIZE_SQUARE + 5), (0, +SIZE_SQUARE + 5),
                           (SIZE_SQUARE + 5, +SIZE_SQUARE + 5)]
</pre></code>

#### Configuration of the stimuli
Preloading of the stimuli that'll be reused during the experiment, such as the texts. 
<pre><code>
# Reused stimulus
    virgin_canvas = expyriment.stimuli.Canvas(size=(CANVAS_SIZE, CANVAS_SIZE), colour=CANVAS_COLOR)
    virgin_canvas.preload()
    stim_prepare = expyriment.stimuli.TextLine(text=TEXT_BTW_STIM)
    stim_prepare.preload()
    your_turn_stim = expyriment.stimuli.TextLine(TEXT_BTW_TRANSITION)
    your_turn_stim.preload()
</pre></code>

For each trial within each block, random localization of the squares on the canvas will pop up successively, in sort of canceling the possibility of having more than 1 time in a row the same square localization. 
<pre><code>
# Generation of the random positions of the squares during the trials
    square_rand_pos = []  # Will contain a random number corresponding to the random position of a square on the canvas
    # for each trial for each block
    for which_block in range(len(BLOCK_SIZE)):
        block = []

        for _ in range(BLOCK_SIZE[which_block]):

            rand_trial = []

            for j in range(TRIAL_SIZE[which_block]):

                if j > 0:

                    if rand_trial[j - 1] == 0:
                        rand_trial.append(np.random.randint(1, 9))
                    elif rand_trial[j - 1] == 8:
                        rand_trial.append(np.random.randint(1, 8))
                    else:
                        choice = np.random.randint(8)
                        lower = np.random.randint(0, rand_trial[j - 1])
                        upper = np.random.randint(rand_trial[j - 1] + 1, 9)
                        if choice <= rand_trial[j - 1] :
                            rand_trial.append(lower)
                        else:
                            rand_trial.append(upper)
                else:

                    rand_trial.append(np.random.randint(9))

            block.append(rand_trial)

        square_rand_pos.append(block)
</pre></code>

Creation of the 9 stimuli corresponding to the 9 localizations that a square can have on the background canvas. 
<pre><code>
 # Constructing and preloading stimuli corresponding to a square on a grey canvas
    square_on_canvas = []

    for which_block in range(len(RECT_RELATIVE_POSITIONS)):
        canvas = expyriment.stimuli.Canvas(size=(SIZE_SQUARE * 3 + 10, SIZE_SQUARE * 3 + 10), colour=CANVAS_COLOR)
        square = expyriment.stimuli.Canvas(size=(SIZE_SQUARE, SIZE_SQUARE), colour=COLOURS[which_block],
                                              position=RECT_RELATIVE_POSITIONS[which_block])
        square.plot(canvas)
        canvas.preload()
        square_on_canvas.append(canvas)
</pre></code>

Adequation of the stimuli within the trials, within each block in a random way. 
<pre><code>
  # Creating and filling all blocks with trials and all trials with stimuli according
    # to their precalculated random order
    for block in range(len(square_rand_pos)):
        new_block = expyriment.design.Block(name="memorize " + str(len(square_rand_pos[block])) + " positions")

        for trial in range(len(square_rand_pos[block])):
            new_trial = expyriment.design.Trial()

            for sti in range(len(square_rand_pos[block][trial])):
                new_trial.add_stimulus(square_on_canvas[square_rand_pos[block][trial][sti]])

            new_block.add_trial(new_trial)

        exp.add_block(new_block)
</pre></code>

#### Formalities of the experiment, data collection 
Constraints on the experiment are added. The age of the participants will be collected into a "data" file handled by expyriment. Time durations will be insert in trials and blocks, The texts are added and will appear right before a trial ("Get ready!") and right after the presentation of the stimuli ("Now, your turn to reproduce the sequence!"), and at the end of each trial, the participant will interact with the programm. 
All data will be collected such as creating a plot that I'll talk about later. 
<pre><code>
 # Get the age of the user from the formular 
    age = present_form(exp)
    exp.data.add("AGE_PLAYER :" + age)

    # Looping on all blocks and all trials
    for block in range(len(exp.blocks)):
        stim_prepare.present()
        exp.clock.wait(TIME_BTW_TRIAL*2)
        for trial in range(len(exp.blocks[block].trials)):
            for stimuli in range(len(exp.blocks[block].trials[trial].stimuli)):
                exp.blocks[block].trials[trial].stimuli[stimuli].present()
                exp.clock.wait(TIME_BTW_STIM)

            # At the end of a trial the interaction sequence takes place 
            your_turn_stim.present()
            exp.clock.wait(TIME_BTW_TRIAL)
            virgin_canvas.present()
            score_player += sequence_interaction((block, trial), square_rand_pos, exp, square_on_canvas,
                                                 CANVAS_SIZE)
            stim_prepare.present()
            exp.clock.wait(TIME_BTW_TRIAL)

            # Adding the data to the expyriment main file
            exp.data.add([exp.blocks[block].name, "trial n°" + str(exp.blocks[block].trials[trial].id)])

    # Adding the score of the player to the expyriment main file
    exp.data.add("SCORE_PLAYER :" + str(score_player)+"\\"+str(sum(BLOCK_SIZE)))
    expyriment.control.end() 
</pre></code>

#### Ongoing Experiment 
The age of the participant will be asked. During the participant-programm interaction, either the mouse or the keypad can be used to perform the task.
If a trial is entirely successful, the participant gets one point, if no, it gets none. Data will be plot, using the curve_generator.py file.
<pre><code>
def present_form(exp):
    """ Present a formular asking the age of the user """
    while True:
        from expyriment.io import TextInput
        ti = TextInput("How old are you ?")
        response = ti.get()
        try:
            int(response)
        except ValueError:
            continue
        return response




def sequence_interaction(wich_stimulus, block_rand_pos, exp, square_on_canvas, CANVAS_SIZE):
    """ Deal with the interaction sequence by checking the inputs from the mouse and the keypad """
    liste_touches = [expyriment.misc.constants.K_KP1, expyriment.misc.constants.K_KP2, expyriment.misc.constants.K_KP3,
                     expyriment.misc.constants.K_KP4, expyriment.misc.constants.K_KP5, expyriment.misc.constants.K_KP6,
                     expyriment.misc.constants.K_KP7, expyriment.misc.constants.K_KP8, expyriment.misc.constants.K_KP9]
    win = True

    for h in range(len(block_rand_pos[wich_stimulus[0]][wich_stimulus[1]])):
        exp.keyboard.clear()
        while True:

            reference = block_rand_pos[wich_stimulus[0]][wich_stimulus[1]][h]

            key = exp.keyboard.check(liste_touches)

            if key is not None:
                square_on_canvas[key - 257].present()

                if key - 257 != reference:
                    print("Error")
                    win = False
                break

            if exp.mouse.check_button_pressed(0):
                pos = exp.mouse.position
                canvas_pos = None

                if (-CANVAS_SIZE / 2) < pos[0] < (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3 and (-CANVAS_SIZE / 2) < pos[
                    1] < (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3:
                    canvas_pos = 0
                    square_on_canvas[0].present()
                elif (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 > pos[0] > (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3 > \
                        pos[1] > (
                        -CANVAS_SIZE / 2):
                    canvas_pos = 1
                    square_on_canvas[1].present()
                elif (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 < pos[0] < (-CANVAS_SIZE / 2) + 3 * CANVAS_SIZE / 3 and (
                        -CANVAS_SIZE / 2) < pos[1] < (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3:
                    canvas_pos = 2
                    square_on_canvas[2].present()
                elif (-CANVAS_SIZE / 2) < pos[0] < (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3 and (
                        -CANVAS_SIZE / 2) + CANVAS_SIZE / 3 < pos[1] < (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3:
                    canvas_pos = 3
                    square_on_canvas[3].present()
                elif (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3 < pos[0] < (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 and (
                        -CANVAS_SIZE / 2) + CANVAS_SIZE / 3 < pos[1] < (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3:
                    canvas_pos = 4
                    square_on_canvas[4].present()
                elif (-CANVAS_SIZE / 2) + 3 * CANVAS_SIZE / 3 > pos[0] > (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 > pos[
                    1] > (
                        -CANVAS_SIZE / 2) + CANVAS_SIZE / 3:
                    canvas_pos = 5
                    square_on_canvas[5].present()
                elif (-CANVAS_SIZE / 2) < pos[0] < (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3 and (
                        -CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 < pos[1] < (-CANVAS_SIZE / 2) + 3 * CANVAS_SIZE / 3:
                    canvas_pos = 6
                    square_on_canvas[6].present()
                elif (-CANVAS_SIZE / 2) + CANVAS_SIZE / 3 < pos[0] < (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 and (
                        -CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 < pos[1] < (-CANVAS_SIZE / 2) + 3 * CANVAS_SIZE / 3:
                    canvas_pos = 7
                    square_on_canvas[7].present()
                elif (-CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 < pos[0] < (-CANVAS_SIZE / 2) + 3 * CANVAS_SIZE / 3 and (
                        -CANVAS_SIZE / 2) + 2 * CANVAS_SIZE / 3 < pos[1] < (-CANVAS_SIZE / 2) + 3 * CANVAS_SIZE / 3:
                    canvas_pos = 8
                    square_on_canvas[8].present()

                exp.mouse.wait_press(0, wait_for_buttonup=True)

                if canvas_pos is not None and canvas_pos != reference:
                    print("Error")
                    win = False
                break

    if win:
        exp.data.add("Successful trial")
        return 1

    else:
        exp.data.add("Failed trial")
        return 0
</pre></code>

### curve_generator.py
This file will read the data collected, and plot them into a graph, with the age in years on the x-axis and the score in percentage on the y-axis.
<pre><code>
# Read each data file
for i in range(number_of_files):	
    path = os.path.join(DIR, name_of_files[i])
    f = open(path,"r")
    line = f.readline()
    find_age = False
    find_score = False
    # Read each line of a data file and search for the age of the player and his score
    while line :
        if re.match(r"(.)*AGE_PLAYER(.)*", line):
            age=int(re.findall("([0-9]+)", line)[1])
            find_age = True
        if re.match(r"(.)*SCORE_PLAYER(.)*", line):
            numbers=re.findall("([0-9]+)", line)
            # Score in percentage
            score=int(numbers[1])/int(numbers[2])*100
            find_score =True
        line = f.readline() 

    if find_age and find_score:
    	ages_and_score[age]=score

lists = sorted(ages_and_score.items()) # sorted by key, return a list of tuples

ages,scores = zip(*lists)

# Display the curve
plt.xlabel('age (in years)')
plt.ylabel('score (in percentage)')
plt.plot(ages, scores)
plt.show()
</pre></code>

## PURPOSE OF THIS EXPERIMENT
This programm has been designed to assess a type of working memory, which is the spatial working memory task. 
Such a task is useful to show different capabilities of memory within the ages, but also seconding clinical status for example.

## REFERENCES

Klencklen, G., Lavenex, P. B., Brandner, C., & Lavenex, P. (2017). Working memory decline in normal aging: Memory load and representational demands affect performance. Learning and Motivation, 60, 10-22.

Klingberg, T. (2009). The overflowing brain: Information overload and the limits of working memory. Oxford University Press.

Song, W., Zhang, K., Sun, J., Ma, L., Jesse, F. F., Teng, X., … Li, W. (2013). A simple spatial working memory and attention test on paired symbols shows developmental deficits in schizophrenia patients. Neural plasticity, 2013, 130642. doi:10.1155/2013/130642

