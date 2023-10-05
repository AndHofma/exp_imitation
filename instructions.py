"""
instructions.py
---------------

This module contains strings of instructions for the experiment, provided in German. These instructions guide
the participant through the imitation task and provide information about the experiment's progression and tasks
to be performed.

Variables:
----------
instructImitationTask : str
    The welcome message and instructions for the imitation task. It guides the participant about the listening
    and repeating task with the help of visual cues (headphone and microphone symbols).

instructPracticeImitationEnd : str
    Instructions provided at the end of the practice phase. It informs the participant about the total number
    of recordings they will hear during the experiment, the estimated duration of the experiment, and the option
    for a break after the first half of the experiment.

imitationEnd : str
    The final message displayed to the participant at the end of the experiment. It acknowledges the participant's
    effort and guides them to end the experiment by pressing the Enter key.
"""


instructImitationTask = """
Willkommen zum Immitationsexperiment! \n
Sie hören zweimal hintereinander eine Aufnahme der Ihnen bekannten Namenssequenzen.
Bitte hören Sie genau hin, denn Sie sollen das Gehörte so exakt wie möglich nachsprechen.
Sie sehen ein Kopfhörer-Symbol, wenn die Aufnahmen abgespielt werden.
Sobald ein Mikrofon-Symbol erscheint, beginnt die Aufnahme.
Dann sprechen Sie das Gehörte so genau wie möglich nach.  \n 
Drücken Sie die Eingabetaste (Enter), um mit zwei Übungsbeispielen zu beginnen.
"""

instructPracticeImitationEnd = """
Das waren die Übungsbeispiele. \n
Falls Sie noch Fragen haben, geben Sie bitte der Versuchsleiterin Bescheid.
Sie hören 80 verschiedene Aufnahmen, jeweils zweimal, in fünf Blöcken.
Das Experiment dauert insgesamt ca. 15 Minuten.
Nach jedem Block können Sie eine Pause machen, wenn Sie dies wünschen. \n
Drücken Sie die Eingabetaste (Enter), um mit dem Experiment zu starten.
"""

imitationEnd = """
Geschafft!
Vielen Dank!
Drücken Sie die Eingabetaste (Enter), um das Experiment zu beenden.
"""
