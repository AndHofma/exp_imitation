"""
path_and_randomization.py
-------------------------

This module provides utilities for handling, randomizing, and processing auditory stimuli.

The primary components of the module focus on:

1. **Randomization**:
    - The `randomize_stimuli_based_on_name_coordination` function provides a systematic way to segregate
      stimuli based on predefined coordination groups and then randomize their order.

    - The `randomize_stimuli` function extracts relevant data from each stimulus filename and randomizes the stimuli.

2. **File and Directory Handling**:
    - `check_and_create_config_paths` ensures the necessary directories exist for stimuli, practice stimuli,
      output results, pictures, recordings, and randomized stimuli. If they don't, directories are created as needed.

    - The `load_stimuli` function fetches all '.wav' stimuli files from a specified directory.

    - The `save_randomized_stimuli` function saves randomized stimuli data for each participant in a structured CSV format.

3. **Data Extraction**:
    - The `get_manip` function extracts manipulation types from filenames.

    - The `get_name_stim` function retrieves the unique identifier (names) from the stimulus filename.

    - The `get_stimulus_data` function offers a standardized method for extracting relevant details from stimulus filenames.

4. **Utilities**:
    - The `load_and_randomize` function is a comprehensive utility that wraps the process of loading, randomizing,
      and saving stimuli.

Module-wide, the `name_coordinations` list defines the name coordination groups used for stimuli randomization.

The module aims to provide a robust set of tools to manage auditory stimuli, especially for experimental settings where
the order and categorization of stimuli can influence results. By following the predefined patterns and using the
utilities in this module, researchers can ensure systematic, reproducible randomization and handling of stimuli.

"""


# Import necessary libraries
import os
import random
import csv


# Define name coordination groups for stimuli randomization
name_coordinations = [
    'gabi__leni__',
    'leni__mimmi_',
    'lilli_gabi__',
    'moni__lilli_',
    'nelli_moni__'
]

def randomize_stimuli_based_on_name_coordination(stimuli_data_list):
    """
    Randomize the given stimuli data based on predefined name coordinations.

    Parameters:
    - stimuli_data_list (list): List of dictionaries containing stimulus data.

    Returns:
    - list: List of randomized stimulus data dictionaries.

    The function segregates stimuli data into predefined coordination groups,
    randomizes the order of these groups, and further randomizes stimuli within each group.
    """
    # Split stimuli into groups based on name coordination
    coordination_groups = {coordination: [] for coordination in name_coordinations}
    for stimulus_data in stimuli_data_list:
        stimulus = stimulus_data['filename']
        for coordination in name_coordinations:
            if stimulus.startswith(coordination):
                coordination_groups[coordination].append(stimulus_data)
                break
    # Randomize the order of name coordinations
    random.shuffle(name_coordinations)
    # Randomize stimuli within each coordination group
    for coordination in name_coordinations:
        random.shuffle(coordination_groups[coordination])
    # Combine the stimuli data back into a single list
    randomized_stimuli_data = []
    for coordination in name_coordinations:
        randomized_stimuli_data.extend(coordination_groups[coordination])
    return randomized_stimuli_data


def check_and_create_config_paths(stim_full_path, practice_stim_full_path, pics_full_path,
                                  output_full_path, record_full_path, random_full_path,
                                  participant_info):
    """
    Check the existence of provided paths and create directories if they don't exist.

    Parameters:
    - stim_full_path (str): Path to the directory containing test stimuli.
    - practice_stim_full_path (str): Path to the directory containing practice stimuli.
    - output_full_path (str): Directory where output results will be stored.
    - pics_full_path (str): Directory containing picture stimuli.
    - record_full_path (str): Directory where recordings will be saved.
    - random_full_path (str): Directory where randomized stimuli will be stored.
    - participant_info (dict): Dictionary containing participant's details.

    Raises:
    - Exception: If any of the input directories (stimuli, practice stimuli, or pics) does not exist.

    The function ensures all required directories exist before the experiment starts.
    """
    # Check if the input directory for test stimuli exists
    if not os.path.exists(stim_full_path):
        # Raise exception if not
        raise Exception("No input folder detected. Please make sure that "
                        "'test_stimuli_path' is correctly set in the configurations")

    # Check if the input directory for test stimuli exists
    if not os.path.exists(practice_stim_full_path):
        # Raise exception if not
        raise Exception("No input folder detected. Please make sure that "
                        "'practice_stimuli_path' is correctly set in the configurations")

    # Check if the pics directory exists
    if not os.path.exists(pics_full_path):
        # Raise exception if not
        raise Exception("No pics folder detected. Please make sure that "
                        "'pics_path' is correctly set in the configurations")

    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_full_path):
        os.mkdir(output_full_path)

    # Check if the path to recorded files exists, if not, create it
    if not os.path.exists(record_full_path):
        os.mkdir(record_full_path)

    # Check if the path to randomization files exists, if not, create it
    if not os.path.exists(random_full_path):
        os.mkdir(random_full_path)

    # Path setup - results per participant
    subj_path_results = os.path.join(output_full_path, participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)


def load_stimuli(stim_full_path):
    """
    Load the list of '.wav' stimuli files from a given directory.

    Parameters:
    - stim_full_path (str): Directory path where stimuli files are located.

    Returns:
    - list: List of filenames of stimuli.

    """
    # Use a list comprehension to get all '.wav' files in the directory
    return [f for f in os.listdir(stim_full_path) if f.endswith('.wav')]


def randomize_stimuli(stimuli_files):
    """
    Extract stimulus data from provided files and randomize them.

    Parameters:
    - stimuli_files (list): List of stimuli filenames.

    Returns:
    - dict: Dictionary where keys are name coordinations and values are lists of randomized filenames.

    This function first extracts relevant data from each filename, then randomizes stimuli
    based on name coordinations and segregates them for further use.
    """
    # Extract stimulus data for each file
    stimulus_data = [get_stimulus_data(file) for file in stimuli_files]

    # Randomize order of stimuli with constraints
    randomized_stimuli_data = randomize_stimuli_based_on_name_coordination(stimulus_data)

    # Now, extract the filenames from the data
    randomized_stimuli = [data['filename'] for data in randomized_stimuli_data]

    # Segregate stimuli based on their name_coord prefix and save as separate lists
    segregated_stimuli = {}
    for name_coord in name_coordinations:
        segregated_stimuli[name_coord] = [stim for stim in randomized_stimuli if stim.startswith(name_coord)]

    return segregated_stimuli


def save_randomized_stimuli(randomized_stimuli, participant_info):
    """
    Save the randomized stimuli to a CSV file.

    Parameters:
    - randomized_stimuli (dict): Dictionary containing randomized stimuli filenames.
    - participant_info (dict): Dictionary containing participant's details.

    This function writes the randomized stimuli to a CSV file in a directory named
    after the participant's subject code. The filename contains the subject code and current date.
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


def load_and_randomize(stim_full_path, participant_info):
    """
    Load, randomize, and save stimuli.

    Parameters:
    - stim_full_path (str): Directory path where stimuli files are located.
    - participant_info (dict): Dictionary containing participant's details.

    Returns:
    - dict: Dictionary containing randomized stimuli filenames.

    This function wraps the process of loading stimuli, randomizing them, and then saving them to a CSV.
    """
    # Load stimuli files
    stimuli_files = load_stimuli(stim_full_path)
    # Randomize stimuli
    randomized_stimuli = randomize_stimuli(stimuli_files)
    # Save randomized stimuli
    save_randomized_stimuli(randomized_stimuli, participant_info)

    return randomized_stimuli


def get_manip(filename):
    """
    Extract manipulation type from the stimulus filename.

    Parameters:
    - filename (str): Stimulus filename.

    Returns:
    - str: Manipulation type extracted from the filename.

    The manipulation type is determined from the last segment of the filename before the ".wav" extension.
    """
    split_name = [part for part in filename.split('_') if part]
    return split_name[-1].replace('.wav', '')  # Last segment without the .wav extension


def get_name_stim(filename):
    """
    Extract the names of the stimulus from the filename.

    Parameters:
    - filename (str): Stimulus filename.

    Returns:
    - str: Extracted names from the filename.

    This function is used to retrieve the unique identifier of the stimulus from the filename.
    """
    extracted_names = filename.split('_bra_')[0] + '_'
    return extracted_names


def get_stimulus_data(filename):
    """
    Extract relevant stimulus data from a given filename.

    Parameters:
    - filename (str): Stimulus filename.

    Returns:
    - dict: Dictionary containing 'filename', 'manip', and 'name_stim' extracted from the filename.

    This function provides a standardized way to extract relevant details from stimulus filenames.
    """
    return {
        'filename': filename,
        'manip': get_manip(filename),
        'name_stim': get_name_stim(filename),
    }

