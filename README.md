# Subreddit Image Scraper
Scrapes the given number of posts in the *hot* category of a subreddit and downloads their images into an organized series of folders
Currently, it is focused on [/r/awwnime](https://www.reddit.com/r/awwnime) however it can handle other subreddits.

## Usage
Run with python giving command line arguments <Subreddit(string)> <post count (int)> <include GIFs (bool)>
Ex. > python awwwnimeScraper.py awwnime 100 false

## Notes
1. Folder categorization is based off of the name of the show/source in brackets (ex. [Show title]) with the folder Unknown for posts with no source/show
2. **YOU MUST CHANGE THE SOURCE FOLDER** at least until custom destination folders are supported