"""
imitation_functions.py
----------------------

This module contains functions for running an auditory imitation experiment. The experiment is intended for use with
the PsychoPy library and consists of two phases: a practice phase and a test phase. Each trial in the experiment involves
the participant listening to an auditory stimulus and imitating it verbally. The participant's verbal response is recorded
and they are then asked to choose a pictogram that matches the auditory stimulus.

Functions in this module can present a trial to a participant, conduct an experiment phase (either the practice phase or
the test phase), and display messages to the participant during the experiment. This module also includes functions for
recording the participant's responses and writing the results of the experiment to a CSV file.

Typical usage example:

    from imitation_functions import present_trial, conduct_experiment_phase

    present_trial(fixation, window, imitation_stimulus1, imitation_stimulus2, audio_pic, rec_seconds, fs, rec_pic,
                  participant_info, stimulus_file)

    conduct_experiment_phase(window, phase_stimuli, phase_name, stimuli_path, participant_info)

This module requires that `psychopy`, `sounddevice`, and `scipy` are installed within the Python environment you are
running this module in.
"""


# Import necessary libraries
from psychopy import core, event, visual, prefs  # import some libraries from PsychoPy
# Set the audio library preference
prefs.hardware['audioLib'] = ['ptb', 'sounddevice', 'pygame', 'pyo']
# Now, import sound
from psychopy import sound
import time
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
from configuration import append_result_to_csv, initialize_stimuli
import os
from path_and_randomization import get_manip, get_name_stim
import csv


# Results list
results = []


def present_trial(fixation, window, imitation_stimulus1, imitation_stimulus2, audio_pic, rec_seconds, fs, rec_pic, participant_info, stimulus_file):
    """
    Presents a trial in the auditory imitation experiment to the participant.

    During the trial, a fixation stimulus is presented, followed by an auditory stimulus. The auditory stimulus is
    played twice, with a short pause in between. After the auditory stimulus is played, a recording begins and the
    participant is prompted to verbally imitate the auditory stimulus. The participant's response is recorded and saved
    as a .wav file in a participant-specific directory under 'recordings'.

    Parameters:
    fixation (VisualStim): A PsychoPy visual stimulus object used as a fixation point.
    window (Window): A PsychoPy window object in which the stimuli are presented.
    imitation_stimulus1 (Sound), imitation_stimulus2 (Sound): Two instances of the same sound stimulus to be imitated.
    audio_pic (ImageStim): A PsychoPy visual stimulus object used as a pictogram shown when the auditory stimulus is played.
    rec_seconds (int): The duration of the recording in seconds.
    fs (int): The sampling rate of the recording.
    rec_pic (ImageStim): A PsychoPy visual stimulus object shown when the participant is recording their response.
    participant_info (dict): A dictionary containing participant information, including 'subject' which represents the participant ID.
    stimulus_file (str): The filename of the auditory stimulus.

    Returns:
    response_record_name (str): The name of the .wav file containing the participant's response.
    """
    # Display fixation point for 1 second
    fixation.name = 'fixation'
    fixation.draw()
    window.flip()
    core.wait(1.0)
    window.flip()

    # Loop twice to play stimulus and show audio_pic
    for stimulus in [imitation_stimulus1, imitation_stimulus2]:
        audio_pic.draw()
        window.flip()
        stimulus.play()
        core.wait(stimulus.getDuration() + 1.0)  # wait for the duration of the sound + 1 second
        window.flip()  # clear the screen

        # Brief pause between the two playbacks
        core.wait(0.5)  # wait for 500ms

    # Start recording the participant's verbal response
    response_record = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

    # Present rec_pic for 350 frames
    for frame in range(350):
        rec_pic.draw()  # Draw pic
        window.flip()  # Flip window to make rec_pic visible
    # Stop the recording after the presentation is over
    sd.stop()

    # Path setup - results per participant
    subj_path_rec = os.path.join('recordings', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_rec):
        os.makedirs(subj_path_rec)

    # Save the participant's verbal response as a .wav file
    filename = os.path.splitext(os.path.basename(stimulus_file))[0]
    write(os.path.join(subj_path_rec, participant_info['subject'] + '_' + filename + '.wav'), fs, response_record)
    response_record_name = participant_info['subject'] + '_' + filename + '.wav'

    return response_record_name


def conduct_experiment_phase(window, phase_stimuli, phase_name, stimuli_path, participant_info):
    """
    Conduct an experiment phase (practice or test).

    Parameters:
    phase_stimuli (list): List of stimuli for the current phase.
    phase_name (str): Name of the current phase ('practice' or 'test').
    stimuli_path (str): Path to the stimuli directory.
    output_filename (str): Path to the output CSV file for the current phase.
    participant_info (dict): Dictionary containing participant information.
    results (list): List to store result dictionaries.
    """

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join('results', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)

    fixation, audio_pic, rec_pic, prompt, fs, rec_seconds = initialize_stimuli(window)
    # Initialize start time and format it into string
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    trial_counter = 1

    # generate the base_filename based on task_name and phase
    output_filename = f"{subj_path_results}/{phase_name}_{participant_info['experiment']}_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    file_exists = os.path.isfile(output_filename)

    # Open file once, before the loop
    with open(output_filename, 'a') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=['experiment',
                                                         'subject_ID',
                                                         'date',
                                                         'trial',
                                                         'phase',
                                                         'stimulus',
                                                         'recording',
                                                         'manip',
                                                         'name_stim',
                                                         'start_time',
                                                         'end_time',
                                                         'duration'])

        for stimulus_file in phase_stimuli:
            # Check if stimulus_file is a string (path) or a Sound object
            if isinstance(stimulus_file, str):
                imitation_stimulus1 = sound.Sound(os.path.join(stimuli_path, stimulus_file))
                imitation_stimulus2 = sound.Sound(os.path.join(stimuli_path, stimulus_file))
            else:
                imitation_stimulus1 = stimulus_file
                imitation_stimulus2 = stimulus_file

            response_record_name = present_trial(fixation, window, imitation_stimulus1, imitation_stimulus2,
                                                 audio_pic, rec_seconds, fs, rec_pic, participant_info, stimulus_file)

            # Record end time and duration
            end_time = time.time()
            end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
            duration = end_time - start_time
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

            # Store trial data
            trial_data = {
                'experiment': participant_info['experiment'],
                'subject_ID': participant_info['subject'],
                'date': participant_info['cur_date'],
                'trial': trial_counter,
                'phase': phase_name,
                'stimulus': stimulus_file,
                'recording': response_record_name,
                'manip': get_manip(stimulus_file),
                'name_stim': get_name_stim(stimulus_file),
                'start_time': start_time_str,
                'end_time': end_time_str,
                'duration': duration_str
            }
            results.append(trial_data)

            # Write data to csv file
            append_result_to_csv(writer, trial_data, file_exists, output_file)

            if not file_exists:
                file_exists = True  # After first write, file definitely exists

            # Increment trial counter
            trial_counter += 1

    return results


def show_message(window, message, wait_for_keypress=True, duration=1, text_height=0.1):
    """
    Show a message on the screen.

    Parameters:
    message (str): The message to display.
    wait_for_keypress (bool, optional): Whether to wait for a keypress. Defaults to True.
    duration (float, optional): Time in seconds to wait if wait_for_keypress is False. Defaults to 1.
    text_height (float, optional): The height of the text. Defaults to 0.1.
    """
    text_stim = visual.TextStim(window, text=message, wrapWidth=2, height=text_height, color="black")
    text_stim.draw()
    window.flip()
    if wait_for_keypress:
        event.waitKeys(keyList=['return'])
    else:
        core.wait(duration)
