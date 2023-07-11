"""
This module contains helper functions for running an auditory imitation experiment using PsychoPy.
The functions are responsible for creating the experiment window, initializing the stimuli, collecting
participant info, and managing output results. They also include utility functions for presenting messages on screen.
"""

# Import necessary libraries
from psychopy import event, monitors, visual, gui, core
import datetime
import os
import csv

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
# def create_window():
#    """
    #Create and initialize the experiment window.
#
#    Returns:
#    win: A PsychoPy visual.Window object for the experiment.
#    """
#    # Create a monitor object for the second screen
#    second_monitor = monitors.Monitor(name='EA273WMi')
#    # Set the appropriate settings for the second monitor
#    second_monitor.setSizePix((1920, 1080))  # Set the desired resolution of the second screen
#
#    # Create and return a window for the experiment on the second monitor
#    return visual.Window(monitor=second_monitor,  # Use the second monitor
#                         size=(1920, 1080),
#                         screen=1,  # Specify the index of the second screen (0 for the first screen, 1 for the second, etc.)
#                         allowGUI=True,
#                         fullscr=True,
#                         color=(255, 255, 255)
#                         )


# to use for testing on laptop
def create_window():
   """
   Create and initialize the experiment window.
   Returns:
   win : A PsychoPy visual.Window object for the experiment.
   """
   # Create a monitor object
   currentMonitor = monitors.Monitor(name='testMonitor')

   # Create and return a window for the experiment
   return visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                        monitor="testMonitor",
                        allowGUI=True,
                        fullscr=True,
                        color=(255, 255, 255)
                        )


def initialize_stimuli(window):
    """
    Initializes the visual and auditory stimuli for the experiment.

    Parameters:
    window (Window): A PsychoPy window object.

    Returns:
    Tuple containing various stimuli objects and parameters required for the experiment.
    """

    # fixation cross
    fixation = visual.ShapeStim(window,
                                vertices=((0, -0.13), (0, 0.13), (0, 0), (-0.09, 0), (0.09, 0)),
                                lineWidth=15,
                                closeShape=False,
                                lineColor="black",
                                name='fixation')

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

    return fixation, audio_pic, rec_pic, prompt, fs, rec_seconds


def get_participant_info():
    """
    Open a dialogue box with 3 fields: current date and time, subject_ID and experiment name.
    Returns a dictionary with the entered information.
    """
    exp_data = {
        'experiment': 'imitation_experiment',
        'subject': 'subject_ID',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")  # Use strftime to format the date string
    }
    # Dialogue box to get participant information
    info_dialog = gui.DlgFromDict(dictionary=exp_data,
                                  title='Imitation-Experiment',
                                  fixed=['experiment','cur_date']
                                  )

    if info_dialog.OK:
        return exp_data
    else:
        core.quit()


def append_result_to_csv(result, output_filename):
    """
    Appends the result of a trial to the appropriate CSV file (practice or test phase).

    Parameters:
    result (dict): A dictionary containing the data for a single trial.
    output_filename (str): The path of the CSV file for storing phase results.

    The function writes the trial data, including phase, stimulus, response, accuracy, and timing info, to the CSV file.
    """
    # Check if file exists to write headers
    file_exists = os.path.isfile(output_filename)

    with open(output_filename, 'a') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()  # File doesn't exist yet, so write a header
        writer.writerow(result)


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
