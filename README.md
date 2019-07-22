# PythonFlashCards
Building a flashcard game in python in different configurations
An exploration in python development by Jacob Cohen-Rosenthal

My goal is to eventually develop useful educational technology software.
I'm starting with a simple flashcard game and my goal is to incrementally add layers of complexity to it.
I realize that others have done much of this before, including may python hobbyists, and of course anki, and outside of python, quizlet and chegg etc.
For the purpose of learning, and perhaps accidental discovery, I'm trying to think of all the implementations on my own instead of using
or even reading code that others have already built. After I've built a working model I will then examine other people’s solutions and see what I can learn from them.
I hope to take the idea from a simple text based version, to a UI version (learning pyqt along the way, maybe also trying pygame) to a webapp version(learning flask, html, and perhaps some javascript along the way), then perhaps also taking it to iOS (with pythonista?) and to Android (kivy?)

Desired functionality (in rough chronological order):
Display card deck
Add and delete items
Quizzes
Enter answer
Multiple choice
Self report
Matching
true/false
Multitype combined quizzes
Cusotomizable quizzes - can replace unwanted questions without having to regenerate whole quiz. -can add in fill in the blank questions on the fly, or custom choose/write multiple choice.
Importing quizlet, anki, chegg etc. decks. Exporting to those as well
Notes on card backs, web links
Pictures 
Combining decks
Sharing decks
Live updating of deck contents across platforms
Live accessibility of decks through an API
When creating cards auto suggest based on other users cards
Record session results
Spaced repetition (SRS)
Audio output
Collaborative deck creation with personalized notes
Etymology features
Speech recognition
Handwriting recognition for cards written on an touchscreen/ipad
Doodle notes
Handwriting recognition to convert hand written notes into e-cards
SRS forgetting curves generated based on peer data (age peer, experience peer).
Scan a book and make appropriate cards from the likely important or new words (or concepts-much more difficult)
Computer/phone plugin to easily add items encountered in daily life into a deck. Right click on any word in your computer in various programs, and like the current ‘define’ option, create an option to ‘create card’. 



After using flashcard apps in my classroom as a teacher, and after reading reviews, I’ve come up with some improvements and ideas to existing popular flashcard/quiz apps that I’d like to try out. If you have any suggestions, please help me add to this list:
Better integration/ interoperability between flashcards and learning games. If you play a flashcard game, your results and score should be added into your performance history, updating your SRS data.
More convenient and user friendly onboarding (Anki’s problem) while still allowing for more features and customization (Quizlet’s problem) 
Easier way to have a group collaborate to quickly flashcard-erize / knowledgepoint-erize a large textbook or set of information.
Way to combine the cognitive reinforcement of handwriting cards with the power of SRS and other digital flashcard functionality





First, in version 0.1, I've made a simple text based game within python that uses a dictionary built in-program. 





