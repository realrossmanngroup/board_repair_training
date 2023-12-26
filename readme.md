I want to be able to feed some AI the following, and have it learn how to solve board repair problems. At the very least, be able to answer entry level questions.

1) Data from my web forum at https://boards.rossmanngroup.com/forums/macbook-logic-board-repair-questions.15/

2) Articles from my wiki at https://repair.wiki

On the forum, I want to give weight to answers by *larossmann*, *dukefawks*, and *2informaticos*

Once I have figured out how to do that, some sort of continuous system that keeps injesting data from the forum & wiki & sending it to some AI to be learned from would be amazing, but first let's get it to work at all.

So we have several steps here.

1. Get threads from forum, get rid of crap, and turn it into JSON files.
DONE! `/threads/extract_threads.py` grabs each post and turns it into a JSON file without the bold/italics tags & HTML junk

2. Get jargon from forum so I can teach the model industry jargon(chips, resistors, caps, board model numbers, etc)

a) resistors - DONE `get_resistors.sql` & `resistors.csv`
b) capacitors - DONE `get_capacitors.sql` & `capacitors.csv`
c) diodes - DONE `get_diodes.sql` & `diodes.csv`
d) chips - HALF DONE `get_chips.sql` & `chips.csv` - still need to add context(what chips are for what, etc)
e) signal names - WORKING ON IT `get_signal_names.sql` This has to grab stuff like `PM_SLP_S4_L` & `PPBUS_G3H` from threads and list them all.
f) board model numbers - HALF DONE `get_macbook_board_models.sql` gets board models mentioned on the forum, `get_board_list.py` gets a list of boards from a table that is maintained by the community of boards. `macbook_board_models.ods` is my attempt at manually resolving board names as well as teaching the model what typos are, `macbook_board_models.csv` is the flattened version of this.

3. Tokenize data

4. Find a worthwhile model to train

5. Train it

6. If it wasn't a complete fail, grab articles from repair.wiki in a manner that the AI likes to train it
