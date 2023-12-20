`extract_threads.py` gets all of the threads & posts from my mysql database of my xenforo forum. It grabs all relevant information and only grabs posts from the macbook board repair forum. It does some joins to get the thread titles as well and parses it nicely into a separate json file for each thread, while stripping out annoying HTML elements and blankspace.

Next up we need to get some training data on information that is unique to my industry. We'll have to teach it what a macbook board number is, what common resistor values, diodes, chips, etc are. These mysql queries grab a bunch of industry jargon and outputs it to its own file, so we have a list of common chips, resistors, capacitors, etc. This way, later on, we can teach the AI to know when someone is talking about a chip, a capacitor, a resistor, etc. 

`get_capacitors.sql`
`get_chips.sql`
`get_diodes.sql`
`get_macbook_board_models.sql`
`get_resistors.sql`
`get_transistors.sql`

The mysql query in `get_macbook_board_models.sql` grabs a copy of every macbook board model numbers and puts it into a csv. `get_resistors.sql` does the same for resistor numbers, etc. 

