"""
This module is part of a PsychoPy experiment, which consists of a practice phase and a main experiment phase.
In each phase, the participant listens to an auditory stimulus and responds to a prompt on screen.
The participant's response is recorded, along with other trial data, and this data is saved in a CSV file.
The stimuli for each phase are loaded from a specific directory and can be randomized.
The output paths for the CSV files are checked and created if necessary at the start of the experiment.
At the end of each phase, a message is displayed on the screen.
"""

# Import necessary PsychoPy libraries
from path_and_randomization import check_and_create_config_paths, load_stimuli, load_and_randomize
from configuration import get_participant_info, create_window, stim_full_path, output_full_path, pics_full_path, record_full_path, practice_stim_full_path, random_full_path
from imitation_functions import show_message, conduct_experiment_phase
from psychopy import core
from instructions import instructImitationTask, instructPracticeImitationEnd, imitationEnd

# Get participant information from a GUI prompt
participant_info = get_participant_info()

# Check and create necessary paths for stimuli and output, returning filenames for output CSVs
check_and_create_config_paths(stim_full_path, practice_stim_full_path, pics_full_path, output_full_path, record_full_path, random_full_path, participant_info)

# Create a window for displaying stimuli
window = create_window()

# Load stimuli from the specified path for the practice phase
practice_files = load_stimuli(practice_stim_full_path)

# Load and/or randomize stimuli from the specified path for the test phase
randomized_test_stimuli = load_and_randomize(stim_full_path, participant_info)

# Display instructions for the imitation task
show_message(window, instructImitationTask)

# Conduct the practice phase of the experiment, recording participant's responses and other trial data
conduct_experiment_phase(window, practice_files, 'practice', practice_stim_full_path, participant_info)

# Clear the screen
window.flip()

# Display instructions for the end of the practice phase
show_message(window, instructPracticeImitationEnd)

# Conduct the main test phase of the experiment, recording participant's responses and other trial data
conduct_experiment_phase(window, randomized_test_stimuli, 'test', stim_full_path, participant_info)

# Clear the screen
window.flip()

# Display the final message to end the experiment, waiting for a keypress from the participant
show_message(window, imitationEnd)

# Close the window and quit the core PsychoPy routines
window.close()
core.quit()
