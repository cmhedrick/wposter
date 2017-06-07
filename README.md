# WPoster
*Currently Supports WordPress 4.7.5*
### What Is It & What Can It Do?
The name comes from WordPress (popular CMS) and Poster (as in a Wall Poster), because it takes information from WordPress instance and displays it. 

WPoster takes advantage of a WordPress's insecure `wp-json`. Which is a part of the default install. It's a fun thing to play around with and is a source of lots of information. 

So far the tool can do the following recon functions:
1. Enumerate Users (ID & Name)
2. Retrive Post Information (Post ID & Title)
3. ~~Create HTML copy of page, to read in browser locally~~ Almost done...

### Why?
This project was inspired by a bunch of CTF's that use WordPress (usually out of date versions) as a CMS. This project also falls somewhere in the OSINT spectrum too. The motivation is for it is because of the #100DaysOfCode

### Install and Config (Will change in future):
The project currently is written in python3 because Guido said so ;)
This install is just going to cover how to install it in a virtual environment. But if you want to install it without, then you can always just run the pip commands as root.

1. First Clone the Repo
`git clone https://github.com/cmhedrick/wposter.git`

2. Change into the wposter directory
`cd wposter/`
3. Set up a python3 virtual envrionment
`virtualenv -p python3 env`
4. Activate your environment
`source env/bin/activate`
5. Install the dependencies
`pip install -r requirements.txt`
6. Set up your config file. This can be done by opening up `config.py.copy` in any text editor and copy and pasting a url between the single quotes.  
e.g `URL = 'targetSite.com'` then doing save as `config.py`
*Alternatively you can leave it blank*
7. Run the program
`python wposter.py`

### Using The Program
The interface should be straight forward. The only part no so straight forward yet is the beginning of it. Remember to call `set` each time you start a new session!

1. `set`
`set` is the absolute first command you must run! If you have already put an actual URL into the `URL` var in `config.py` than you just need to use `set`. Otherwise when you call `set` you will be prompted to enter a URL.
2. `users`
This command will scrape then enumerate the users of the site. It provdes you with the UserID and the Username.
3. `posts`
Will enumerate all the posts on the site. Providing you with PostID and Title.
4. `read`
**Not fully implemented yet!** But this will eventually allow a user to call the function to get another prompt. Which then will scrape a copy of the WordPress post with that given ID. This way the copy can be open locally in your browser!
5. `q`
Kills the session. Provides a cute message on exit.
