# anki-uworld-to-filtered-deck
An anki addon that takes in a list of UWorld question IDs, and creates filtered decks from those questions by searing the AnKing deck for notes tagged with those UWorld question IDs. 
<b>Meant to be used with the AnKing anki deck.</b> If you do not have the AnKing deck, this addon will not work. Best results on AnKing v10 or higher. 

<b>This is not my idea. There are existing addons that perform similar functionality - this addon is my implementation of that idea.</b>


# Usage
1. Tools → UWorld Filtered Decks → Enter a comma-separated list of question IDs and hit enter
2. Filtered decks will be created under a new UWorld deck for each question. Questions with no corresponding 

# Configuration
Configuration options can be found in the add-on config, accessible from Tools → Add-ons → Select the add-on → Config.

<ul>
  <li>By default, there is no search text that is added to the end of the filtered deck search. I personally use (is:due OR is:new) so that studying the tag pulls all new or due cards - this replicates studying by deck most closely. To modify this search text that's added, change the value of the supplementalSearchText variable in the config.</li>
  <li>By default, there is a limit of 300 cards that are added to the deck. I chose this because it's sufficiently high that I'd never personally want to study a deck that large without breaking it up. If you'd like to change the limit of the number of cards pulled into the filtered deck, modify the numCards in the config.</li>
</ul>

 # Notes
This add-on creates the filtered deck. It does not regularly rebuild that filtered deck. For that, I recommend one of the rebuild all add-ons.
Bug reports should be added to the [issues page]([url](https://github.com/sachingooo/anki-uworld-to-filtered-deck/issues)).
