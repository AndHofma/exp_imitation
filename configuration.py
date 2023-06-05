"""
This module contains helper functions for running an auditory imitation experiment using PsychoPy.
The functions are responsible for creating the experiment window, initializing the stimuli, collecting
participant info, and managing output results. They also include utility functions for presenting messages on screen.
"""

# Import necessary libraries
from psychopy import event, monitors, visual, gui, core
import random
import os
import datetime

# Setup paths
# test stimulus directory
stim_path = 'test_stimuli/'
# practice stim directory
practice_stim_path = 'practice_stimuli/'
# output directory for experiment results
output_path = 'results/'
# directory for the pictograms used
pics_path = 'pics/'
# directory for all recordings
record_path = 'recordings/'
# directory for randomized stimuli
random_path = 'randomization/'

# to use in acoustic lab - second monitor name fixed here
def create_window():
    """
    Create and initialize the experiment window.

    Returns:
    win: A PsychoPy visual.Window object for the experiment.
    """
    # Create a monitor object for the second screen
    second_monitor = monitors.Monitor(name='EA273WMi')
    # Set the appropriate settings for the second monitor
    second_monitor.setSizePix((1920, 1080))  # Set the desired resolution of the second screen

    # Create and return a window for the experiment on the second monitor
    return visual.Window(monitor=second_monitor,  # Use the second monitor
                         size=(1920, 1080),
                         screen=1,  # Specify the index of the second screen (0 for the first screen, 1 for the second, etc.)
                         allowGUI=True,
                         fullscr=True,
                         color=(255, 255, 255)
                         )


# to use for testing on laptop
# def create_window():
#    """
#    Create and initialize the experiment window.
#
#    Returns:
#    win : A PsychoPy visual.Window object for the experiment.
#    """
#    # Create a monitor object
#    currentMonitor = monitors.Monitor(name='testMonitor')
#
#    # Create and return a window for the experiment
#    return visual.Window(monitors.Monitor.getSizePix(currentMonitor),
#                         monitor="testMonitor",
#                         allowGUI=True,
#                         fullscr=True,
#                         color=(255, 255, 255)
#                         )


def initialize_stimuli(window):
    """
    Initializes the visual and auditory stimuli for the experiment.

    Parameters:
    window (Window): A PsychoPy window object.

    Returns:
    Tuple containing various stimuli objects and parameters required for the experiment.
    """

    # set up different TextStim needed throughout experiment
    # Define the possible positions and corresponding labels for the pictograms
    positions = [(-0.5, 0), (0.5, 0)]  # left and right positions
    labels = ['left', 'right']  # corresponding labels

    # Randomize the order - this will be randomized between participants
    # Positions and labels are shuffled in the same order
    indices = list(range(len(positions)))
    random.shuffle(indices)
    positions = [positions[i] for i in indices]
    labels = [labels[i] for i in indices]

    # Pictograms order
    pictograms_order = [os.path.join(pics_path, 'no_bracket.png'), os.path.join(pics_path, 'bracket.png')]

    # fixation cross
    fixation = visual.ShapeStim(window,
                                vertices=((0, -0.13), (0, 0.13), (0, 0), (-0.09, 0), (0.09, 0)),
                                lineWidth=15,
                                closeShape=False,
                                lineColor="black",
                                name='fixation')

    # Create pictograms
    bracket_pic = visual.ImageStim(window,
                                   image=pictograms_order[1],
                                   pos=positions[1]
                                   )

    nobracket_pic = visual.ImageStim(window,
                                     image=pictograms_order[0],
                                     pos=positions[0]
                                     )

    # Labels for the positions
    bracket_pos_label = labels[1]
    nobracket_pos_label = labels[0]

    # pictograms
    audio_pic = visual.ImageStim(window,
                                 image=pics_path + 'audio.png',
                                 pos=(0, 0),
                                 name='audio_pic')

    rec_pic = visual.ImageStim(window,
                               image=pics_path + 'rec.png',
                               pos=(0, 0),
                               name='rec_pic')

    # response prompt
    prompt = visual.TextStim(window,
                             color='black',
                             pos=(0, 0.6),
                             wrapWidth=2)
    # feedback
    feedback = visual.TextStim(window,
                               pos=(0, 0),
                               wrapWidth=2,
                               height=0.2)

    # default parameters for the recordings
    fs = 44100  # Sample rate
    # Calculate the recording duration in seconds
    visual_frames = 350
    # automatically estimate monitor's refresh rate from window object
    estimated_frame_rate = window.getActualFrameRate()
    # If for some reason the function fails to get the actual frame rate, it will return None.
    # In this case, you could default to a reasonable estimate, e.g., 60 Hz.
    if estimated_frame_rate is None:
        estimated_frame_rate = 60

    rec_seconds = visual_frames / estimated_frame_rate

    return pictograms_order, fixation, bracket_pic, nobracket_pic, bracket_pos_label, nobracket_pos_label, \
        audio_pic, rec_pic, prompt, feedback, fs, rec_seconds


def get_participant_info():
    """
    Open a dialogue box to get participant information, including current date and time, subject_ID and experiment name.

    Returns:
    A dictionary containing the participant's information.
    """
    # Define experiment name and configuration
    experiment_name = "Imitation-Task"  # Production-Dual-Task
    experiment_config = {
        'experiment': 'imitation_experiment',
        'subject': 'subject_ID',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")  # Use strftime to format the date string
    }
    # Create a dialogue box for the subject to enter their information
    info_dialog = gui.DlgFromDict(experiment_config,
                                  title=f'{experiment_name} Experiment',
                                  fixed=['experiment', 'cur_date']
                                  )

    if info_dialog.OK:
        return experiment_config
    else:
        core.quit()


def append_result_to_csv(result, practice_filename, test_filename, participant_info):
    """
    Append a single trial result to the appropriate CSV file (either practice or test).

    Parameters:
    result (dict): A dictionary containing the trial result.
    practice_filename (str): Path to the practice CSV file.
    test_filename (str): Path to the test CSV file.
    participant_info (dict): A dictionary containing the participant's information.
    """
    # Determine which CSV file to append to based on the phase
    output_filename = practice_filename if result['phase'] == 'practice' else test_filename

    # Append the trial result to the CSV file
    with open(output_filename, 'a') as output_file:
        output_file.write(
            f"{participant_info['experiment']},"
            f"{participant_info['subject']},"
            f"{participant_info['cur_date']},"
            f"{result['trial']},"
            f"{result['phase']},"
            f"{result['stimulus']},"
            f"{result['recording']},"
            f"{result['response']},"
            f"{result['accuracy']},"
            f"{result['manip']},"
            f"{result['name_stim']},"
            f"{result['condition']},"
            f"{result['bracket_pic_position']},"
            f"{result['nobracket_pic_position']},"
            f"{result['start_time']},"
            f"{result['end_time']},"
            f"{result['duration']}\n"
        )


def show_message(win, message, wait_for_keypress=True, duration=1, text_height=0.1):
    """
    Show a message on the screen.

    Parameters:
    win (Window): The PsychoPy window object.
    message (str): The message to display.
    wait_for_keypress (bool, optional): Whether to wait for a keypress. Defaults to True.
    duration (float, optional): Time in seconds to wait if wait_for_keypress is False. Defaults to 1.
    text_height (float, optional): The height of the text. Defaults to 0.1.
    """
    # Create a text stimulus with the given message
    text_stim = visual.TextStim(win, text=message, wrapWidth=2, height=text_height, color="black")
    text_stim.draw()
    # Flip the window to display the message
    win.flip()
    # Wait for a keypress or for a set duration
    if wait_for_keypress:
        event.waitKeys()
    else:
        core.wait(duration)
