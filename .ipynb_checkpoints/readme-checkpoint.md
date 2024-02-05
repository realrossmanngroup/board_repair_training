I want to be able to feed some AI the following, and have it learn how to solve board repair problems. At the very least, be able to answer entry level questions.

1) Data from my web forum at https://boards.rossmanngroup.com/forums/macbook-logic-board-repair-questions.15/

2) Articles from my wiki at https://repair.wiki

On the forum, I want to give weight to answers by *larossmann*, *dukefawks*, and *2informaticos*

Once I have figured out how to do that, some sort of continuous system that keeps injesting data from the forum & wiki & sending it to some AI to be learned from would be amazing, but first let's get it to work at all.

Here are the steps I need to follow:

1. Get threads from forum, get rid of crap, and turn it into JSON files.
*DONE!* `extract_threads.py` grabs each post and turns it into a JSON file without the bold/italics tags & HTML junk

2. Get jargon from forum so I can teach the model industry jargon(chips, resistors, caps, board model numbers, etc)

`get_jargon_list_multithreaded.py` does this and outputs csv files to `jargon_lists` with jargon, along with a count of how often it was mentioned. Signal names/chips that are mentioned are high up on the priority list for definitions. 

3. Annotate the forum thread JSON files with a prompt to the model to learn board repair from the thread as well as with jargon terms & definitions that are specific to that thread.

*DONE* `annotation.py` goes through my jargon lists once I have edited them with definitions of jargon(this is done manually, unfortunately a real brain has to work before we can train computer brain) and annotates my threads so that the model knows what I want them to learn from the thread, and understands what some of the jargon terms from the thread mean.

We are not even close to training a model yet. This is just the groundwork before we get to that.

5. Tokenize data

6. Find a worthwhile model to train

7. Train it

8. If it wasn't a complete fail, grab articles from repair.wiki in a manner that the AI likes to train it

9. If it was a complete fail... try & try again.

10. Retire, once computer fixes boards better than me. 
