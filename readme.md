# Blog Updater

Currently for [updates.snyk.io](updates.snyk.io), running `main.py` pulls blog posts from this site and is stores in the `snyk_updates` directory. Running `python main.py` takes the posts on the forepage of the website, but running `python main.py dynamic` uses `selenium` and Google Chrome to open the website and gather all of the posts that can only be viewed dynamically.