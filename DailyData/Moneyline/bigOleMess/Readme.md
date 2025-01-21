## Instructions for future parsing ##

1. Pull odds. (americanConversion.py, then accumulate.py)
2. Move the returned file to the bigOleMess subfolder
3. Attach the full names by running fixAutoOdds.py. 
4. Make sure you have a csv file with the game data from basketball reference that has matching games.
5. Pass both files to doubleMergeNew.py
**Note: PTS mighted be swapped. If so, run swapPtsIssue.py on resulting data.**

There is a lot of extra mess in here, because I was generating a big data set (cleaned_data.csv) with all
game results and odds, but I did not have entire data of odds. This lead to me dealing with a bunch of data
in different formats, and trying to stich them all together. I am leaving them in here, in case of an emergency,
but they should not be needed for future use.