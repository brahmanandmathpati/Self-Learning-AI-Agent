"""Plain-language "What am I looking at?" text for every page (pure data, no Streamlit).

Each entry: (what it is, what to look for, Roman-Marathi helper line). Keys are the hero titles of the pages.
"""

from __future__ import annotations

GUIDE: dict[str, tuple[str, str, str]] = {
    "Overview": (
        "This is the home page of a program that teaches itself to play games and then proves it learned.",
        "Follow the three steps below: watch it learn, see the proof, then compare the agents.",
        "He home page aahe; tin steps follow kara: learning paha, proof paha, mag agents compare kara.",
    ),
    "Training": (
        "This page trains an agent on a game. The agent plays again and again and slowly gets better.",
        "Look at the status strip: the score line should go up and the random-move share should go down.",
        "Agent game khelto ani hallu hallu shikto; score vadhla ani random moves kami zale mhanje learning chalu aahe.",
    ),
    "Agent comparison": (
        "This page puts the agents side by side on the same game, using test games they never trained on.",
        "Look at the winner sentence first, then check that the bars are higher than the Random bar.",
        "Same game var sagle agents cha score pahun konta jast changla te kalte; Random peksha uncha bar changla.",
    ),
    "Evaluation": (
        "This page checks if the agent really learned, or if the good score was just luck.",
        "Look for the verdict badge. Press 'Why?' to see the two numbers behind it.",
        "Score luck ne ala ki kharech shikla te ithe tapasle jate; verdict badge ani 'Why?' bagha.",
    ),
    "Ablation study": (
        "This page removes one trick at a time and shows how much the score drops without it.",
        "Look for the biggest drop. That trick matters the most.",
        "Ek ek trick kadhun pahila; jyachya shivay score jast padto toch sarvat mahatvacha.",
    ),
    "Environments": (
        "This page shows the games the agent plays and what it sees in each one.",
        "Look at the goal, the actions and the reward of each game.",
        "Agent kon kon te games khelto, tyanche goal ani reward kay aahe te ithe aahe.",
    ),
    "Run explorer": (
        "This page lists every saved training run so any result can be checked again.",
        "Open a run and look at its seed, settings and learning curve.",
        "Pratyek training run save aahe; seed ani settings pahun result parat tapasta yeto.",
    ),
    "Reflection": (
        "This page explains a run in plain words. Every sentence is built from numbers in the database.",
        "Look at the numbers quoted in each sentence; they come from the saved results.",
        "Run cha sope bhashet explanation; pratyek vakyatil number database madhun yete.",
    ),
    "Vision Lab": (
        "This page lets the agent learn hand gestures from a camera, photos or videos.",
        "Look at how the accuracy changes as you add more examples.",
        "Camera, photos kiva videos pasun agent hat che gestures shikto; examples vadhle ki accuracy badalte.",
    ),
    "About the project": (
        "This page says who built the project and which version you are using.",
        "Look at the team and the version number.",
        "Project kon banavla ani konta version aahe te ithe aahe.",
    ),
}

FALLBACK = ("This page is part of the Self-Learning AI Agent project.",
            "Use the Help button for the meaning of any word.",
            "Konta pan shabd samajla nahi tar Help button dabva.")

HELP_TITLE = "Help & glossary"
