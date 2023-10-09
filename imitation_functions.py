"""
imitation_functions.py
----------------------

This module contains functions to conduct and manage a PsychoPy-based audio experiment.
The functions handle stimuli presentation, participant responses recording, results saving,
and display management.

Dependencies:
    - PsychoPy: For stimuli presentation and timing.
    - sounddevice: For recording audio responses from participants.
    - scipy.io.wavfile: To save audio responses in .wav format.
    - csv: To save trial results in a CSV format.

Modules:
    - configuration: For appending results to a CSV and initializing stimuli.
    - path_and_randomization: To get manipulations and stimulus names.
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
from imitation_configuration import append_result_to_csv, initialize_stimuli
import os
from imitation_path_and_randomization import get_manip, get_name_stim
import csv


# Results list
results = []


def present_trial(fixation, window, audio_pic, rec_seconds, fs, rec_pic, stimuli_full_path,
                  participant_info, stimulus_file, phase_name, trial_counter):
    """
    Present a trial to the participant.

    Parameters:
        fixation (object): Visual fixation point.
        window (object): PsychoPy visual window.
        audio_pic (object): Visual indicator that audio is playing.
        rec_seconds (float): Duration for recording in seconds.
        fs (int): Sampling rate for recording.
        rec_pic (object): Visual indicator that recording is taking place.
        stimuli_full_path (str): Path to the directory containing stimuli files.
        participant_info (dict): Information about the participant.
        stimulus_file (str): Name of the stimulus file to present.
        phase_name (str): Name of the experiment phase ('practice' or other).
        trial_counter (int): Counter indicating the current trial number.

    Returns:
        str: Name of the recorded response file.
    """
    # Display fixation point for 1 second
    fixation.name = 'fixation'
    fixation.draw()
    window.flip()
    core.wait(1.0)
    window.flip()

    # Check if stimulus_file is a string (path) or a Sound object
    if isinstance(stimulus_file, str):
        imitation_stimulus1 = sound.Sound(os.path.join(stimuli_full_path, stimulus_file), sampleRate=48000)
        imitation_stimulus2 = sound.Sound(os.path.join(stimuli_full_path, stimulus_file), sampleRate=48000)
    else:
        imitation_stimulus1 = stimulus_file
        imitation_stimulus2 = stimulus_file

    # Loop twice to play stimulus and show audio_pic
    for stimulus in [imitation_stimulus1, imitation_stimulus2]:
        audio_pic.draw()
        window.flip()
        stimulus.play()

        core.wait(stimulus.getDuration()+0.3)  # wait for the duration of the sound + 0.7 seconds
        window.flip()  # clear the screen

    # Start recording the participant's verbal response
    response_record = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

    # Present rec_pic for 350 frames
    for frame in range(300):
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
    write(os.path.join(subj_path_rec, 'imitation' + '_' + participant_info['subject'] + '_' + phase_name + '_' +
                       "{:02d}".format(trial_counter) + '_' + filename + '.wav'), fs, response_record)
    response_record_name = 'imitation' + '_' + participant_info['subject'] + '_' + phase_name + '_' + \
                           "{:02d}".format(trial_counter) + '_' + filename + '.wav'

    return response_record_name


def display_pause_screen(window, block_number, total_blocks):
    """
    Display a pause screen in between blocks.

    Parameters:
        window (object): PsychoPy visual window.
        block_number (int): Current block number.
        total_blocks (int): Total number of blocks.
    """
    message = f"Block {block_number + 1} von {total_blocks} geschafft. Drücken Sie Enter, wenn Sie weitermachen möchten."
    show_message(window, message)


def conduct_experiment_phase(window, phase_stimuli, phase_name, stimuli_full_path, participant_info):
    """
    Conduct a phase of the experiment.

    Parameters:
        window (object): PsychoPy visual window.
        phase_stimuli (list): List of stimuli for the current phase.
        phase_name (str): Name of the experiment phase.
        stimuli_full_path (str): Path to the directory containing stimuli files.
        participant_info (dict): Information about the participant.

    Returns:
        list: List of dictionaries containing trial data.
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

    # Get the total number of blocks
    total_blocks = len(phase_stimuli)

    # Open file once, before the loop
    with open(output_filename, 'a', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=['experiment',
                                                         'subjectID',
                                                         'date',
                                                         'trial',
                                                         'phase',
                                                         'stimulus',
                                                         'recording',
                                                         'manip',
                                                         'name_stim',
                                                         'start_time',
                                                         'end_time',
                                                         'duration',
                                                         ])

        if phase_name == 'practice':
            for stimulus_file in phase_stimuli:
                response_record_name = present_trial(
                    fixation, window, audio_pic, rec_seconds, fs, rec_pic, stimuli_full_path,
                    participant_info, stimulus_file, phase_name, trial_counter)

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
                    'subjectID': participant_info['subject'],
                    'date': participant_info['cur_date'],
                    'trial': "{:02d}".format(trial_counter),
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
        else:
            # Present each set of stimuli as one block
            # Enumerate provides the block number (starting from 0, so we add 1)
            for block_number, (name_coord, stimuli_block) in enumerate(phase_stimuli.items()):
                for stimulus_file in stimuli_block:
                    response_record_name = present_trial(
                        fixation, window, audio_pic, rec_seconds, fs, rec_pic, stimuli_full_path,
                        participant_info, stimulus_file, phase_name, trial_counter)

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
                        'subjectID': participant_info['subject'],
                        'date': participant_info['cur_date'],
                        'trial': "{:02d}".format(trial_counter),
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

                # After each block, show the prompt unless it's the last block or the phase is 'practice'
                if block_number + 1 != total_blocks:
                    display_pause_screen(window, block_number, total_blocks)

    return results


def show_message(window, message, wait_for_keypress=True, duration=1, text_height=0.1):
    """
    Display a text message on the screen.

    Parameters:
        window (object): PsychoPy visual window.
        message (str): Message to be displayed.
        wait_for_keypress (bool): If True, waits for key press; otherwise waits for a duration.
        duration (float): Time in seconds to wait if not waiting for a keypress.
        text_height (float): Height of the text (default is 0.1).
    """
    text_stim = visual.TextStim(window, text=message, wrapWidth=2, height=text_height, color="black")
    text_stim.draw()
    window.flip()
    if wait_for_keypress:
        event.waitKeys(keyList=['return'])
    else:
        core.wait(duration)
