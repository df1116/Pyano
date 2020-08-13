
-- PYANO --

Pyano is an application that wable to is do a variety of piano related commands (and other instruments given time). Primarily the application will record piano pieces and print out sheet music for the music. The application will then allow the user to edit the sheet music by either clicking and moving notes or by using commands. The application will also allow for the playback and saving of sheet music.

The user should run the Pyano.py file to run the TP. Make sure to run the file as a script (Ctrl+Shift+E).

The following libraries need to be installed (python -m pip install X):
 	- aubio
	- pyaudio
	- numpy
	- scipy

In application commands can be seen on the helper screen and are:
	- On the home screen:
		- Click on one of the piano keys to play the piano

	- On the record screen:
		- Click on a key to edit it
		- "Up" and "Down" keys to change the pitch of the note
		- "Left" and "Right" keys to change the duration of the note
		- 'c' key: inputs a note next to the one selected
		- 'v' key: inputs a note above the one selected