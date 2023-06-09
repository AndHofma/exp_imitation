"""
path_and_randomization.py
-------------------------

This module provides functionalities for verifying the existence of necessary file and directory paths, creating
participant-specific paths and results files, loading and randomizing audio stimuli, and saving randomized stimuli
as CSV files. The module helps streamline the process of preparing the experiment's setup by handling necessary
file system operations and the randomization of stimuli.

Functions:
----------
check_and_create_config_paths(stim_path, practice_stim_path, output_path, pics_path, record_path, random_path, participant_info):
    Verifies the existence of necessary directories for experiment execution, raises exceptions with appropriate
    error messages if any of the directories are not found. If certain directories don't exist, it creates them.
    It also creates participant-specific directories and results files.

load_stimuli(stim_path):
    Loads '.wav' stimuli files from the provided directory.

randomize_stimuli(stimuli_files):
    Randomizes the order of stimuli files given certain constraints.

constraint_randomization(stimuli):
    Applies constraint-based randomization to a list of stimuli data.

save_randomized_stimuli(randomized_stimuli, participant_info):
    Saves the randomized stimuli file names to a CSV file in a participant-specific directory.

load_and_randomize(stim_path, participant_info):
    Loads stimuli files from a provided directory, randomizes them, and saves the randomized stimuli.

get_manip(filename):
    Extracts the 'manip' value from a stimulus filename.

get_name_stim(filename):
    Extracts the 'name_stim' value from a stimulus filename.

get_stimulus_data(filename):
    Extracts the 'manip' and 'name_stim' values from a stimulus filename.
"""


# Import necessary libraries
import os
import random
import csv


def check_and_create_config_paths(stim_path, practice_stim_path, output_path, pics_path, record_path,
                                  random_path, participant_info):
    """
    Verifies the existence of necessary directories, raises exceptions if directories are not found,
    creates directories if they don't exist, and sets up participant-specific paths and results files.

    Parameters:
    stim_path (str): Path to the directory with test stimuli.
    practice_stim_path (str): Path to the directory with practice stimuli.
    output_path (str): Path to the output directory.
    pics_path (str): Path to the directory with pictures.
    record_path (str): Path to the directory for recorded files.
    random_path (str): Path to the directory for randomization files.
    participant_info (dict): Information about the participant, including subject identifier.

    Raises:
    Exception: If any of the necessary directories (stim_path, practice_stim_path, or pics_path) are not found.
    """
    # Check if the input directory for test stimuli exists
    if not os.path.exists(stim_path):
        # Raise exception if not
        raise Exception("No input folder detected. Please make sure that "
                        "'test_stimuli_path' is correctly set in the configurations")

    # Check if the input directory for test stimuli exists
    if not os.path.exists(practice_stim_path):
        # Raise exception if not
        raise Exception("No input folder detected. Please make sure that "
                        "'practice_stimuli_path' is correctly set in the configurations")

    # Check if the pics directory exists
    if not os.path.exists(pics_path):
        # Raise exception if not
        raise Exception("No pics folder detected. Please make sure that "
                        "'pics_path' is correctly set in the configurations")

    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # Check if the path to recorded files exists, if not, create it
    if not os.path.exists(record_path):
        os.mkdir(record_path)

    # Check if the path to randomization files exists, if not, create it
    if not os.path.exists(random_path):
        os.mkdir(random_path)

    # Path setup - results per participant
    subj_path_results = os.path.join(output_path, participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)


def load_stimuli(stim_path):
    """
    Loads stimuli files from a given directory.

    Parameters:
    stim_path (str): Path to directory containing the stimuli files.

    Returns:
    list: A list of stimuli filenames.
    """
    # Use a list comprehension to get all '.wav' files in the directory
    return [f for f in os.listdir(stim_path) if f.endswith('.wav')]


def randomize_stimuli(stimuli_files):
    """
    Randomize a list of stimuli files given certain constraints.

    Args:
    stimuli_files (list of str): List of stimuli file names.

    Returns:
    list of str: Randomized list of stimuli files.
    """
    # Extract stimulus data for each file
    stimulus_data = [get_stimulus_data(file) for file in stimuli_files]

    # Randomize order of stimuli with constraints
    randomized_stimuli_data = constraint_randomization(stimulus_data)

    # Now, extract the filenames from the data
    randomized_stimuli = [data['filename'] for data in randomized_stimuli_data]

    return randomized_stimuli


def constraint_randomization(stimuli):
    """
    Apply constraint randomization: Not more than 3 of the same name_stim,
    and not more than 2 of the same manip should be played.

    Args:
    stimuli (list of dict): List of stimuli data.

    Returns:
    list of dict: Randomized list of stimuli data.
    """
    stimuli_copy = stimuli.copy()
    random.shuffle(stimuli_copy)

    randomized_stimuli = []
    while stimuli_copy:
        valid_stimulus_found = False
        for stimulus in stimuli_copy:
            if (
                    sum(stim['name_stim'] == stimulus['name_stim'] for stim in randomized_stimuli[-3:]) < 3 and
                    sum(stim['manip'] == stimulus['manip'] for stim in randomized_stimuli[-2:]) < 2
            ):
                randomized_stimuli.append(stimulus)
                stimuli_copy.remove(stimulus)
                valid_stimulus_found = True
                break
        if not valid_stimulus_found:
            print(
                "Warning: Constraints cannot be satisfied for remaining stimuli. Adding remaining stimuli in random order.")
            randomized_stimuli.extend(stimuli_copy)
            break
    return randomized_stimuli


def save_randomized_stimuli(randomized_stimuli, participant_info):
    """
    Save randomized stimuli as a csv file.

    Args:
    randomized_stimuli (list of str): List of randomized stimuli file names.
    file_path (str): Path to save the randomized stimuli.
    """
    # Create a directory for this participant if it doesn't exist
    directory = os.path.join('randomization', participant_info['subject'])
    os.makedirs(directory, exist_ok=True)

    # Define file path
    filename = f"{participant_info['subject']}_{participant_info['cur_date'].replace(':', '-').replace(' ', '_')}_randomized_imitation_stimuli.csv"
    filepath = os.path.join(directory, filename)

    # Write csv file
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename"])  # header
        for row in randomized_stimuli:
            writer.writerow([row])
    print(f"Saved randomized stimuli to {filepath}")


def load_and_randomize(stim_path, participant_info):
    """
    Load stimuli files from a directory, randomize them,
    and save the randomized stimuli.

    Args:
    stimuli_path (str): Path to directory containing the stimuli files.
    save_path (str): Path to save the randomized stimuli.
    """
    # Load stimuli files
    stimuli_files = load_stimuli(stim_path)
    # Randomize stimuli
    randomized_stimuli = randomize_stimuli(stimuli_files)
    # Save randomized stimuli
    save_randomized_stimuli(randomized_stimuli, participant_info)

    return randomized_stimuli


def get_manip(filename):
    """
    Extracts the manip from a stimulus filename.

    The function assumes that the filename follows a specific format,
    where different parts of the name are separated by underscores ('_'),
    and the manip is the fourth part.

    Parameters:
    filename (str): The stimulus filename.

    Returns:
    str: The manip extracted from the filename.
    """
    split_name = [part for part in filename.split('_') if part]
    return split_name[3]  # Change the indexes as per the actual structure of your filenames


def get_name_stim(filename):
    """
    Extracts the name_stim from a stimulus filename.

    The function assumes that the filename follows a specific format,
    where different parts of the name are separated by underscores ('_'),
    and the name_stim is the first part.

    Parameters:
    filename (str): The stimulus filename.

    Returns:
    str: The name_stim extracted from the filename.
    """
    split_name = [part for part in filename.split('_') if part]
    return split_name[0]  # Change the indexes as per the actual structure of your filenames


def get_stimulus_data(filename):
    """
    Extracts the manip and name_stim from a stimulus filename.

    Parameters:
    filename (str): The stimulus filename.

    Returns:
    dict: A dictionary containing the manip and name_stim extracted from the filename.
    """
    return {
        'filename': filename,
        'manip': get_manip(filename),
        'name_stim': get_name_stim(filename),
    }
