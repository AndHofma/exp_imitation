"""
This module assists with stimulus handling for experimental purposes. It includes functions for:

- Checking and creating necessary directories and files.
- Loading, generating, shuffling, grouping, and rearranging stimuli.
- Extracting specific attributes from stimulus filenames.

"""

# Import necessary libraries
import os
import random
from collections import defaultdict
import datetime
import pickle
import csv


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


def load_or_generate_stimuli(stimuli_path, random_path):
    """
    Loads or generates randomized stimuli.

    This function loads the stimuli from the provided stimuli_path. It then checks if a file containing randomized
    stimuli already exists at the specified random_path. If it does, it loads the randomized stimuli from the file.
    If it doesn't, it generates randomized stimuli from the loaded stimuli, saves them to a file at the random_path,
    and writes them to a CSV file at the same location.

    At the end, the function verifies that the original and randomized stimuli contain the same elements,
    and returns the randomized stimuli.

    Parameters:
    stimuli_path (str): Path to directory containing the stimuli files.
    random_path (str): Path to directory where the randomized stimuli file and CSV file will be stored.

    Returns:
    list: List of randomized stimuli filenames.
    """
    # Load the stimuli
    stimuli = load_stimuli(stimuli_path)

    # Append filename to the random_path
    random_file_path = os.path.join(random_path, 'randomized_stimuli.pkl')
    random_csv_file_path = os.path.join(random_path, 'randomized_stimuli.csv')

    # Check if randomized stimuli file already exists
    if os.path.isfile(random_file_path):
        # Load the randomized stimuli from the file
        with open(random_file_path, 'rb') as randomized_file:
            randomized_stimuli = pickle.load(randomized_file)
    else:
        # Generate randomized stimuli
        randomized_stimuli = create_randomized_stimuli(stimuli_path)

        # Save the randomized stimuli to a file
        with open(random_file_path, 'wb') as randomized_file:
            pickle.dump(randomized_stimuli, randomized_file)

        # Write the randomized stimuli to a CSV file
        with open(random_csv_file_path, 'w', newline='') as randomized_csv_file:
            writer = csv.writer(randomized_csv_file)
            for row in randomized_stimuli:
                writer.writerow([row])  # write each item in a new row

    # Verify that the original stimuli and randomized stimuli contain the same elements
    original_stimuli_set = set(stimuli)
    randomized_stimuli_set = set(randomized_stimuli)
    assert original_stimuli_set == randomized_stimuli_set, "The original and randomized stimuli are not the same"

    return randomized_stimuli


def shuffle_stimuli(stimuli):
    """
    Shuffles stimuli in-place.

    Parameters:
    stimuli (list): List of stimuli filenames.

    Returns:
    list: List of shuffled stimuli filenames.
    """
    # Use random.shuffle for in-place shuffling
    random.shuffle(stimuli)
    return stimuli


def group_stimuli(stimuli):
    """
    Groups stimuli by speaker.

    Parameters:
    stimuli (list): List of stimuli filenames.

    Returns:
    dict: A dictionary with speaker names as keys and lists of their stimuli as values.
    """
    groups = defaultdict(list)  # Use defaultdict to automatically create new keys as needed
    for stimulus in stimuli:
        name_stim = stimulus[:5]
        groups[name_stim].append(stimulus)  # Add stimulus to the speaker's list

    return groups


def rearrange(stimuli, condition_limit=3, name_stim_limit=3, manip_limit=3):
    """
    Rearranges stimuli to avoid exceeding the condition, name_stim, or manip limit for consecutive stimuli.

    Parameters:
    stimuli (list): List of stimuli filenames.
    condition_limit (int): Maximum number of consecutive stimuli with the same condition.
    name_stim_limit (int): Maximum number of consecutive stimuli with the same name_stim.
    manip_limit (int): Maximum number of consecutive stimuli with the same manip.

    Returns:
    list: List of rearranged stimuli filenames.
    """
    rearranged = stimuli.copy()  # Create a copy of the stimuli list to rearrange

    # These are the attributes we are interested in
    attributes = {'condition': get_condition, 'name_stim': get_name_stim, 'manip': get_manip}

    for attribute, get_attribute in attributes.items():
        for i in range(len(rearranged)):
            attribute_count = 1  # Initialize attribute count

            # Check subsequent stimuli for the same attribute
            for j in range(i + 1, len(rearranged)):
                # If the current stimulus has the same attribute as the previous, increment attribute count
                if get_attribute(rearranged[j]) == get_attribute(rearranged[i]):
                    attribute_count += 1

                else:
                    # Reset attribute count if the attribute changes
                    attribute_count = 1

                # If the attribute limit is reached, find a stimulus with a different attribute to swap
                if attribute_count > eval(f'{attribute}_limit'):
                    swapped = False  # Flag to track whether a suitable swap candidate was found
                    for k in range(j + 1, len(rearranged)):
                        # If a stimulus with a different attribute is found, swap it with the current stimulus
                        if get_attribute(rearranged[k]) != get_attribute(rearranged[j]):
                            rearranged[j], rearranged[k] = rearranged[k], rearranged[j]
                            swapped = True
                            break  # Break out of the loop once a swap is made

                    # If no suitable swap candidate is found, break out of the loop
                    if not swapped:
                        break

    return rearranged


def create_randomized_stimuli(stim_path):
    """
    Creates a randomized list of stimuli while maintaining certain constraints.

    Parameters:
    path (str): Path to directory containing the stimuli files.

    Returns:
    list: List of randomized stimuli filenames.
    """
    # Load and group stimuli by name_stim
    stimuli = load_stimuli(stim_path)
    random.seed(666)
    groups = group_stimuli(stimuli)

    randomized_stimuli = []
    # Shuffle and rearrange each name_stim's stimuli
    for name_stim, stimuli in groups.items():
        shuffled = shuffle_stimuli(stimuli)
        rearranged = rearrange(shuffled)
        randomized_stimuli.extend(rearranged)  # Add the rearranged stimuli to the final list

    return randomized_stimuli


def get_condition(filename):
    """
    Extracts the condition from a stimulus filename.

    The function assumes that the filename follows a specific format,
    where different parts of the name are separated by underscores ('_'),
    and the condition is the second part.

    Parameters:
    filename (str): The stimulus filename.

    Returns:
    str: The condition extracted from the filename.
    """
    split_name = [part for part in filename.split('_') if part]
    return split_name[1]  # Change the index as per the actual structure of your filenames


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
