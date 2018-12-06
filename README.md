# ribbonline
Measuring the online ribbon wars


## Setup
Clone the repository
```
$ git clone https://github.com/danielbalcells/ribbonline.git
```
Install the Python3 requirements (virtualenv highly recommended)
```
$ cd ribbonline
$ pip install -r requirements.txt
```

## Exploring the code
Launch the Jupyter Notebook server
```
$ jupyter-notebook
```
Open `Ribbonline.ipynb` in your browser and start messing around!

## Crawling data from Twitter
Use the script in `scripts/twint_crawl.py`. Its syntax is the following:
```
Usage: python scripts/twint_crawl.py [options]

Options:
  -h, --help            show this help message and exit
  -q QUERY, --query=QUERY
                        Query string
  -s START_DATE, --since=START_DATE
                        Period start date
  -u END_DATE, --until=END_DATE
                        Period end date
  -l LIMIT, --limit=LIMIT
                        Limit number of tweets
  -L LANGUAGE, --language=LANGUAGE
                        Language of the tweet
```

If you get a `ModuleNotFoundError: No module named 'ribbonline'` error, add the `ribbonline` root directory to your `PYTHONPATH`:
```
$ cd [ribbonline_root]
$ export PYTHONPATH=$(PWD):$PYTHONPATH
```
