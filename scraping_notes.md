`extract_threads.py` gets all of the threads & posts from my mysql database of my xenforo forum. It grabs all relevant information and only grabs posts from the macbook board repair forum. It does some joins to get the thread titles as well and parses it nicely into a separate json file for each thread, while stripping out annoying HTML elements and blankspace.

Next up we need to get some training data on information that is unique to my industry. We'll have to teach it what a macbook board number is, what common resistor values, diodes, chips, etc are. These mysql queries grab a bunch of industry jargon and outputs it to its own file, so we have a list of common chips, resistors, capacitors, etc. This way, later on, we can teach the AI to know when someone is talking about a chip, a capacitor, a resistor, etc. 

`get_jargon_lists` will grab every different type of jargon from the forum and output it to a CSV. The CSV will have each piece of jargon along with how many times each one was mentioned. Giving descriptions for over 12k different things is untenable, so what we're doing here is we're focusing on creating explanations for the most popular terms. 

`annotation.py` goes through my jargon lists once I have edited them with definitions of jargon(this is done manually, unfortunately a real brain has to work before we can train computer brain) and annotates my threads so that the model knows what I want them to learn from the thread, and understands what some of the jargon terms from the thread mean.

We are not even close to training a model yet. This is just the groundwork before we get to that. 
