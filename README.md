# PCBS_workingmemory 
## INTRODUCTION

Many studies have reported a negative correlation between aging and working memory (Klencklen, and al. 2017). The working memory, firstly introduced by Baddeley in 1974, is a cognitive process that enables to keep in memory a certain amount of information during a short period. This type of memory can be perfectly illustrated in a spatial working memory task (Song, and al., 2013). 
Therefore, this project aims to show a decline of the working memory with aging, by programming a spatial working memory task performed by individuals from two types of individuals: young adults (from 18 to 30 years) and adults (over 30 years). This aged delimitation has been done seconding the presumably apogee of the working memory at the end of the teenagehood (25-30 years), preceding the decline of this type of memory (Klingberg, 2007). 

The task will consist of 3 blocks of 4 trials. In each trial, a virgin matrix of 3x3 will be presented, and the block will begin 2 seconds after the participant pressed the space bar. Colors corresponding to a specific localisation on the matrix will successively and randomly pop up such as creating a sequence of 5, 7, and 9 colors corresponding to the 1st, 2nd and 3rd block. This way, the difficulty of the task increases. Each participant is hence, confronted to 12 trials with increasing difficulty. 
The colors appear successively at a speed 1/1 s. 
At the end of each trial, the participant will have to reproduce the sequence: either by clicking on the cell of the matrix or by assimilating the digit pad to the matric cells.

Once the participant did the 5, 7 or 9 manipulations seconding the block, the subject is not informed of the success of the task and the following trial begins after a 2 seconds black screen.
Each block is separated by a black screen, and starts when the participant press the spacebar. 
At the end of all the blocks, the participant will be informed by a plot of his/her successness by blocks. There will be an average of the trials per block for his/her participation.
 
The experiment collects the data of each participant and all the data will be little by little added to an overall plot, distinguishing the 2 categories of participants, only for the purpose of the experimenters. 
  

## CODE EXPLANATION
### main.py
#### Setting the constants of the stimuli
Constants have first been created, such as indicating the size of the stimuli trials (5, 7 and 9), the size of the blocs (3 trials per block), the size of the canvas (background matrix), the duration between the duration between the stimuli presentation (1s), the duration between each trial (1s), the coulours that'll correspond to the stimuli and the background canvas. Texts are also add and will appear right before a trial ("Get ready!") and right after the presentation of the stimuli ("Now, your turn to reproduce the sequence!")
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

Creation of the 9 stimuli corresponding to the 9 localizations that a square can have on the background. 
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



  ## REFERENCES

Klencklen, G., Lavenex, P. B., Brandner, C., & Lavenex, P. (2017). Working memory decline in normal aging: Memory load and representational demands affect performance. Learning and Motivation, 60, 10-22.

Klingberg, T. (2009). The overflowing brain: Information overload and the limits of working memory. Oxford University Press.

Song, W., Zhang, K., Sun, J., Ma, L., Jesse, F. F., Teng, X., … Li, W. (2013). A simple spatial working memory and attention test on paired symbols shows developmental deficits in schizophrenia patients. Neural plasticity, 2013, 130642. doi:10.1155/2013/130642

