# VoteForMe-Sanrio
<h2>Sanrio Voting Script</h2>

A python script powered by Selenium to vote for my favourite Sanrio characters in the 2025 Sanrio Character Ranking
Vote for your favourite characters from your terminal! You don't have to do it yourself :>

Please note the following
- This project is for fun and learning purposes only and is not to be abused. 
- You can vote for as many characters as you like per day according to the Sanrio website.
- When the voting period has ended, the script will simply end.
- Please vote according to the rules.


<h3>Set-up and Run</h3>
Install Selenium by running this line in the terminal
```
pip install selenium
```


Navigate to the folder you have cloned the repository to using the terminal, and run

```
python SanrioTestScript.py
```

<h3>How to use normally</h3>
Type 'n' or click enter when asked:

```
Do you want to use the override variables?(y/n)
```

And allow the page to load.
You will then be asked your Country and Character you want to vote for.

Dont worry if you spell anything wrong! The code is very forgiving and will ask you to confirm your choices.

example: 
```
Which Country are you from? unitedr staes
Confirm (y/n) you have chosen 'United States': y
Which Character are you voting for? usahaner
Confirm (y/n) you have chosen 'U・SA・HA・NA': y
```

Once you confirm your choices, the script will run, voting for the character you selected.
When the vote is complete you will recieve a message 

```
Voted for U・SA・HA・NA
```

You will have the option to vote for another character until you've voted for everyone you wanted to!

```
Do you want to vote for another character?(y/n) y
Which Character are you voting for? heweeo kity
Confirm (y/n) you have chosen 'Hello Kitty': y
Voted for Hello Kitty
Do you want to vote for another character?(y/n) n
Thanks for voting!
```


<h3>Override Variables</h3>
To use this it is recommended you have some knowledge of inspecting elements. 

If you want to use the override variables, go to the script at line 18 and edit the following to your preferences.
To use these you need to make sure that the string matches the exact values in the dropdowns. 

eg. ageValue = "21" would not work, but ageValue = "20-29 years old" would.

```
ageValue = "Your Age group"
sexValue = "Your Gender"
expValue = "Your experience voting in the Sanrio Ranking"
regionValue = "Your Country"

```
You can enter as many names as you want in the "characterList" variable, make sure that the name matches the exact name used on the site for the 'alt' attribute

eg. "usahana" wouldn't work, it would have to be "U・SA・HA・NA" 
```
characterList = ['Your character','Your 2nd character']
```
