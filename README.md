A fork of rafbradeys miscrits auto farm bot for python. I suck at scripting. Use theirs.

Changes I have tried implementing.

*Added a run mode - This will check which miscrit is encountered, and if it is not the specified "rare" miscrit, it will simply run away, and wait for the cooldown before searching again.

*Added a 2 minute and 50 second cooldown between using the "rare move" when it encounters the specified "rare" miscrit. This waits almost the entire allowed time to use the move again, before automatically losing the battle. This can provide much more time for the user to intervene before the miscrits potentially die. -I saw this in the "issues" on the original script and gave it a shot-

*Has some code for TRYING to identify when items or gold drop from the searchable object and collecting it/waiting the proper amount of time for the object to be searchable again. I have not succeeded lol.
