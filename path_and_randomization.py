"""
This module assists with stimulus handling for experimental purposes. It includes functions for:

- Checking and creating necessary directories and files.
- Loading, generating, shuffling, grouping, and rearranging stimuli.
- Extracting specific attributes from stimulus filenames.

"""

# Import necessary libraries
import os
import random
import csv
from collections import defaultdict
import datetime


def check_and_create_config_paths(stim_path, practice_stim_path, output_path, pics_path, record_path, random_path, participant_info):
    """
    Function checks the existence of specific directories and raises
    exceptions with appropriate error messages if any of the directories are not found.
    Also, creates necessary participant directories and result files.
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

    # Create the output files with headers and save them in results/
    practice_output_filename = os.path.join(subj_path_results,
                                            f"imitation_practice_results_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    test_output_filename = os.path.join(subj_path_results,
                                        f"imitation_test_results_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    for output_file in [practice_output_filename, test_output_filename]:
        with open(output_file, 'w') as file:
            file.write(
                'experiment,subject_ID,date,trial,phase,stimulus,recording,response,response_accuracy,manipulation,second_name,condition,bracket_pic_position,nobracket_pic_position,start_time,end_time,duration \n'
            )
    return practice_output_filename, test_output_filename


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

    # Group by name_stim
    names = defaultdict(list)
    for data in stimulus_data:
        names[data['name_stim']].append(data)

    # Randomize order of names
    name_order = list(names.keys())
    random.shuffle(name_order)

    # Initialize list to store the final order of stimuli
    randomized_stimuli_data = []

    # Iterate over manips in randomized order
    for name in name_order:
        # Randomly order stimuli with constraints
        name_stimuli_ordered = constraint_randomization(names[name])

        # Append stimuli to final list
        randomized_stimuli_data.extend(name_stimuli_ordered)

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
