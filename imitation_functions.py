"""
This module contains functions for running an auditory imitation experiment using PsychoPy.
The experiment has two phases, a practice phase and a test phase. In each trial, the participant listens to an
auditory stimulus and imitates it verbally, the response is recorded. Then they choose a matching pictogram.
The participant's response, choice, and other trial information are saved in a CSV file.
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


# Results list
results = []


def present_trial(fixation, window, imitation_stimulus, stimulus_file, audio_pic, rec_seconds, fs, rec_pic, participant_info):
    """
    Presents one trial to the participant and records their responses.

    Parameters:
    fixation (VisualStim): A fixation stimulus.
    window (Window): A PsychoPy window object.
    imitation_stimulus (Sound): The sound stimulus to be imitated.
    stimulus_file (str): The filename of the sound stimulus.
    audio_pic (ImageStim): The image stimulus shown when the sound is played.
    rec_seconds (int): The duration of the recording.
    fs (int): The sampling rate of the recording.
    rec_pic (ImageStim): The image stimulus shown when the participant is recording.
    participant_info (dict): Dictionary containing participant information.

    Returns:
    responseRecordName (str): The name of the recording file.
    """
    # Display fixation point for 1 second
    fixation.name = 'fixation'
    fixation.draw()
    window.flip()
    core.wait(1.0)
    window.flip()

    # Loop twice to play stimulus and show audio_pic
    for _ in range(2):
        audio_pic.draw()
        window.flip()
        imitation_stimulus.seek(0)  # reset the sound object to the beginning
        imitation_stimulus.play()
        core.wait(imitation_stimulus.getDuration() + 1.0)  # wait for the duration of the sound + 1 second
        window.flip()  # clear the screen

        # Brief pause between the two playbacks
        core.wait(0.5)  # wait for 500ms

    # Start recording the participant's verbal response
    responseRecord = sd.rec(int(rec_seconds * fs), samplerate=fs, channels=1)

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
    write(os.path.join(subj_path_rec, participant_info['subject'] + '_' + filename + '.wav'), fs, responseRecord)
    responseRecordName = participant_info['subject'] + '_' + filename + '.wav'

    return responseRecordName


def conduct_experiment_phase(window, phase_stimuli, phase_name, stimuli_path, practice_filename, test_filename, participant_info):
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
    fixation, audio_pic, rec_pic, prompt, fs, rec_seconds = initialize_stimuli(window)
    # Initialize start time and format it into string
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    trial_counter = 1

    for stimulus_file in phase_stimuli:
        # Check if stimulus_file is a string (path) or a Sound object
        if isinstance(stimulus_file, str):
            imitation_stimulus = sound.Sound(os.path.join(stimuli_path, stimulus_file))
        else:
            imitation_stimulus = stimulus_file

        responseRecordName = present_trial(fixation, window, imitation_stimulus, stimulus_file, audio_pic, rec_seconds,
                                           fs, rec_pic, participant_info)

        # Record end time and duration
        end_time = time.time()
        end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        duration = end_time - start_time
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

        # Store trial data
        results.append({
            'experiment': participant_info['experiment'],
            'subject_ID': participant_info['subject'],
            'date': participant_info['cur_date'],
            'trial': trial_counter,
            'phase': phase_name,
            'stimulus': stimulus_file,
            'recording': responseRecordName,
            'manip': get_manip(stimulus_file),
            'name_stim': get_name_stim(stimulus_file),
            'start_time': start_time_str,
            'end_time': end_time_str,
            'duration': duration_str
        })
        append_result_to_csv(results[-1], practice_filename, test_filename, participant_info)

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
