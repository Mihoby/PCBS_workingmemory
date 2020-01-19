import expyriment
import numpy as np

# Constants

TRIAL_SIZE = [1, 1, 1]
BLOCK_SIZE = [1, 1, 1]

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


def main():
    # configuration
    exp = expyriment.design.Experiment(name="Text Experiment")
    #expyriment.control.set_develop_mode(True)
    expyriment.control.initialize(exp)

    # Reused stimulus
    virgin_canvas = expyriment.stimuli.Canvas(size=(CANVAS_SIZE, CANVAS_SIZE), colour=CANVAS_COLOR)
    virgin_canvas.preload()
    stim_prepare = expyriment.stimuli.TextLine(text=TEXT_BTW_STIM)
    stim_prepare.preload()
    your_turn_stim = expyriment.stimuli.TextLine(TEXT_BTW_TRANSITION)
    your_turn_stim.preload()

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

    # Constructing and preloading stimuli corresponding to a square on a grey canvas
    square_on_canvas = []

    for which_block in range(len(RECT_RELATIVE_POSITIONS)):
        canvas = expyriment.stimuli.Canvas(size=(SIZE_SQUARE * 3 + 10, SIZE_SQUARE * 3 + 10), colour=CANVAS_COLOR)
        square = expyriment.stimuli.Canvas(size=(SIZE_SQUARE, SIZE_SQUARE), colour=COLOURS[which_block],
                                              position=RECT_RELATIVE_POSITIONS[which_block])
        square.plot(canvas)
        canvas.preload()
        square_on_canvas.append(canvas)

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

    # Beginning of the experiment

    expyriment.control.start()
    exp.mouse.show_cursor()
    score_player = 0

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


if __name__ == '__main__':
    main()
