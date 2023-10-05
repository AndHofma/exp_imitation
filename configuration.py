"""
configuration.py
----------------
This module contains utilities and functions for initializing, configuring, and running an auditory imitation experiment
using the PsychoPy library. The main components can be broadly categorized into:

1. **Initialization & Configuration**:
    - Setting up paths for stimuli, recordings, results, pictograms, and randomization.
    - Functionality to initialize the experiment window (`create_window`) suitable for laboratory and personal environments.
    - Initialization of visual stimuli like pictograms, prompts, and fixation crosses (`initialize_stimuli`).
    - Participant information retrieval with a date-time stamped unique identifier (`get_participant_info`).

2. **Experiment Execution**:
    - Function to append experimental results to a CSV file in a consistent manner (`append_result_to_csv`).
    - A utility to display messages on the experiment window, with options for a timed display or waiting for a user response (`show_message`).

The module is designed to be versatile, allowing for easy setup on different machines (like laboratory setups or personal laptops)
and ensuring consistent data capture across different sessions and participants.
"""


# Import necessary libraries
from psychopy import event, monitors, visual, gui, core
import datetime
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Setup paths
# test stimulus directory
stim_path = 'stimuli/test_stimuli/'
stim_full_path = resource_path(stim_path)
# practice stim directory
practice_stim_path = 'stimuli/practice_stimuli/'
practice_stim_full_path = resource_path(practice_stim_path)
# output directory for experiment results
output_path = 'results/'
output_full_path = resource_path(output_path)
# directory for the pictograms used
pics_path = 'pics/'
pics_full_path = resource_path(pics_path)
# directory for all recordings
record_path = 'recordings/'
record_full_path = resource_path(record_path)
# directory for randomized stimuli
random_path = 'randomization/'
random_full_path = resource_path(random_path)

# to use in acoustic lab - second monitor name fixed here
# def create_window():
#    """
#    Create and initialize the experiment window.
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
    Create and initialize the experiment window suitable for testing on a laptop.

    Returns:
    win: A PsychoPy visual.Window object for the experiment tailored for standard laptop displays.
    """
    # Create a monitor object
    current_monitor = monitors.Monitor(name='testMonitor')

    # Create and return a window for the experiment
    return visual.Window(monitors.Monitor.getSizePix(current_monitor),
                         monitor="testMonitor",
                         allowGUI=True,
                         fullscr=True,
                         color=(255, 255, 255)
                         )


def initialize_stimuli(window):
    """
    Initialize and configure visual stimuli elements used in the experiment.

    Parameters:
    window: A PsychoPy visual.Window object where stimuli will be displayed.

    Returns:
    Tuple containing:
        fixation: Visual element representing the fixation cross.
        audio_pic: Pictogram representing audio.
        rec_pic: Pictogram representing recording.
        prompt: Text element for prompts.
        fs: Sample rate for recordings.
        rec_seconds: Duration in seconds for each recording.
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
                                 image=pics_full_path + 'audio.png',
                                 pos=(0, 0),
                                 name='audio_pic')

    rec_pic = visual.ImageStim(window,
                               image=pics_full_path + 'rec.png',
                               pos=(0, 0),
                               name='rec_pic')

    # response prompt
    prompt = visual.TextStim(window,
                             color='black',
                             pos=(0, 0.6),
                             wrapWidth=2)

    # default parameters for the recordings
    fs = 48000  # Sample rate
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
    Capture participant information before starting the experiment. Uses a GUI dialog.

    Returns:
    exp_data: A dictionary containing the experiment details and participant information. Returns None if the dialog is canceled.
    """
    exp_data = {
        'experiment': 'imitation_experiment',
        'subject': 'subjectID',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")  # Use strftime to format the date string
    }
    # Dialogue box to get participant information
    info_dialog = gui.DlgFromDict(dictionary=exp_data,
                                  title='Imitation-Experiment',
                                  fixed=['experiment', 'cur_date']
                                  )

    if info_dialog.OK:
        return exp_data
    else:
        core.quit()


def append_result_to_csv(writer, result, file_exists, output_file):
    """
    Append the result data of an experiment iteration to a CSV file.

    Parameters:
    writer: A csv.DictWriter object to write the data.
    result: A dictionary containing the result data.
    file_exists: Boolean indicating if the file already exists.
    output_file: File object where the result should be written.
    """
    if not file_exists:
        writer.writeheader()  # File doesn't exist yet, so write a header
    writer.writerow(result)
    output_file.flush()  # Flush Python's write buffer
    os.fsync(output_file.fileno())  # Tell the OS to flush its buffers to disk


def show_message(win, message, wait_for_keypress=True, duration=1, text_height=0.1):
    """
    Display a message on the experiment window. Optionally, wait for a keypress or show the message for a specified duration.

    Parameters:
    win: A PsychoPy visual.Window object where the message will be displayed.
    message: The message text to be displayed.
    wait_for_keypress: If True, waits for a keypress before proceeding. If False, waits for the specified duration.
    duration: Duration (in seconds) for which the message should be displayed. Only used if `wait_for_keypress` is False.
    text_height: Height of the text (default is 0.1).
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
