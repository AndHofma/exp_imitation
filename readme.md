# Step-by-step guide

This is a reproduction / imitation experiment where participants are supposed to imitate an auditory model stimulus as precisely as possible.
The model stimulus is a recording of three coordinates names from an experienced female speaker.
The name coordinates either include a prosodic phrase boundary after the second name or not.
The phrase boundary is acoustically marked by inserting a pause after the second name, lengthening of the last vowel 
of the second name in relation to the whole name - relative to the same segment in the no-boundary name sequence and 
by a pitch rise from the first to the second syllabe on the second name.
These combinations of prosodic cues are manipulated to be at maximum or minimum levels.

We used [PsychoPy](https://www.psychopy.org/) to set up the experiment.

Follow the steps below in the given order to ensure a successful setup and execution.

To download and use the project files from GitHub, follow (all necessary of) these steps:

## 1. GitHub
* Install Git on your computer by downloading it from the following link if you have a Windows system: https://git-scm.com/download/win
  * Choose 32 or 64-bit, whereas **64-bit** is the **most common one**

* After installing Git, open the Command Prompt (CMD) on your computer.

## 2. Opening Windows Command Prompt
The Command Prompt is a program on Windows computers used to execute commands. 
To open it, follow these steps:

* Press **Win + R** keys to open the *Run* dialog box.
* Type *cmd* and press Enter.

## 3. Downloading Project Files from GitHub
* Navigate to the folder where you want to download the project files using the *cd* command in the Windows command prompt. 
* Replace your_desired_folder with the path to the folder:
  * `cd your_desired_folder` (e.g. `cd "C:\Users\Andrea_Hofmann\OneDrive\PhD\exp_imitation"`)
* Clone the GitHub repository by running the following command:
  * `git clone https://github.com/AndHofma/exp_imitation.git`
  * The project files will be downloaded to a folder named after the repository within the specified folder.

## 4. Checking Python Installation and Version
* To check if Python is installed on your computer and determine its version, open the Windows Command Prompt (if not still open) and run the following command:
  * `python --version`
* If Python is installed, the command will display the installed version (e.g., "Python 3.8.15"). 
* If Python is not installed, the command will not be recognized.

## 5. Creating a Virtual Environment with Python 3.8
* To create a virtual environment with Python 3.8, first, make sure you have Python 3.8 installed on your computer.
* If not, download and install it for Windows (most commonly 64-bit): https://www.python.org/downloads/release/python-3810/
* Open the Windows Command Prompt.
* Navigate to the project folder using the *cd* command. 
* Replace *your_project_folder* with the path to your project folder:
  * `cd your_project_folder` (e.g. `cd "C:\Users\Andrea_Hofmann\OneDrive\PhD\exp_imitation\imitation_task"`)
* Run the following command to create the virtual environment. 
* Replace *your_env_name* with your desired name for the virtual environment (e.g. *imitation_env*):
  * `py -3.8 -m venv your_env_name` (e.g. `py -3.8 -m venv imitation_env`)
* After the virtual environment is created, activate it with the following command:
  * `your_env_name\Scripts\activate` (e.g. `imitation_env\Scripts\activate`)

## 6. Installing Python Packages from requirements.txt
* To install the required Python packages from the requirements.txt file, run the following command in the activated virtual environment:
  * `pip install -r requirements.txt`
* This command will install all the necessary packages listed in the requirements.txt file.

### 6A. Checking for Microsoft Visual C++ 14.0 or greater and installing if necessary
* Some Python packages need Microsoft Visual C++ 14.0 or a newer version to work.
* If you get an error message, e.g. "Microsoft Visual C++ 14.0 or greater is required." - you have o install the required tools and follow these steps:
  * a. Visit the following link to download the "Build Tools for Visual Studio":
    * https://visualstudio.microsoft.com/visual-cpp-build-tools/
  * b. On the webpage, click on the "Download" button under "Build Tools for Visual Studio 2022".
  * c. Run the downloaded installer. During the installation process, make sure to choose the "C++ build tools" option. Additionally, ensure that "MSVC v142 - VS 2019 C++ x64/x86 build tools" or a later version and the "Windows 10 SDK" components are selected.
  * d. Continue with the installation. After it's finished, restart your computer to make sure the new tools are set up correctly on your system.
* These instructions will guide you through the process of installing the Microsoft C++ Build Tools, which include the necessary Microsoft Visual C++ version for your Python packages.

After finishing this step go back to step 6.

## 7. Running the Experiment
To start and run the experiment, follow these steps:

* Ensure the virtual environment is activated (you should see the virtual environment name in the command prompt).
* Navigate to the folder containing the main Python script for the experiment using the *cd* command, if you're not already there.
* Run the main Python script by typing the following command:
  * `python imitation_experiment.py`

## 8. Experiment-Start
* First, a small dialogue window will appear. 
* Enter the subject id and press "OK". 
* The results will be recorded for each subject in a separate folder in the file "*phase*\_*task_name*\_*subject_ID*\_*timestamp*.csv" in the "**results**" folder.
* The audio recordings will be stored for each subject in a separate folder in the files "*task*\_*subject_ID*\_*task_name*\_*stimulus_ID*.csv" in the "**recordings**" folder.
