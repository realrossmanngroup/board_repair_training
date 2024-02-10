I want to be able to feed an LLM the following information, and have it learn how to solve board repair problems or answer entry level questions.

1) Data from my web forum at https://boards.rossmanngroup.com/forums/macbook-logic-board-repair-questions.15/

2) Articles from my wiki at https://repair.wiki

On the forum, I want to give weight to answers by *larossmann*, *dukefawks*, and *2informaticos*

Once I have figured out how to do that, I'd like to create a continuous system for injesting data from the forum & wiki & sending it to the LLM to be learned from. First, we have to get it to work at all!

Here are the steps I need to follow:

1. Get threads from forum, get rid of crap, and turn it into JSON files. *DONE!* `01_extract_threads.py` grabs each post and turns it into a JSON file without the bold/italics tags & HTML junk. the `threads` directory contains threads that have been annotated, the ogthreads directory contains threads that have not been annotated. 

2. Get jargon from forum so I can teach the model industry jargon(chips, resistors, caps, board model numbers, etc)

`02_extract_jargon.py` extracts jargon to csv files in the `jargon_lists` directory. It includes a column that counts how often that piece of jargon was mentioned. Defining 18000+ terms is not realistic in the beginning, so I want to define the ones that are most important. *COLUMN THAT COUNTS HOW OFTEN TERM WAS MENTIONED MUST BE DELETED BEFORE NEXT STEP!

3. Annotate the forum thread JSON files with a prompt to the model to learn board repair from the thread, and annotate/define the jargon that is mentioned in that specific thread. `03_annotate_threads.py` does this. `03_annotate_threads.py` goes through my jargon lists, once I have edited them with definitions of jargon(this is done manually, unfortunately a real brain has to work before we can train computer brain) and annotates my threads so that the model knows what I want them to learn from the thread, and understands what some of the jargon terms from the thread mean.

We are not even close to training a model yet. This is just the groundwork before we get to that. I have 1000+ terms to define before I get close to that. 

*WHAT IS NOT DONE/WHAT NEEDS TO BE LEARNED/WHAT I NEED TO DO NEXT:*

What comes up next: 

5. Tokenize data

6. Find a worthwhile model to train

7. Train it

8. If it wasn't a complete fail:

a) grab articles from repair.wiki in a manner that the AI likes to train it

b) Create a data pipeline that continuously
	***grabs new threads
	***annotates them
	***feeds them to the model

c) Retire. Computer fixes boards better than me, I'm done!

9. If it was a complete fail... try & try again.