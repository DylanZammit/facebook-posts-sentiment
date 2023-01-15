# Facebook Post Scraper
This repo uses [this facebook scraper](https://github.com/kevinzg/facebook-scraper) to neatly extract post information and format them. You can specify the pages, the number of posts, posts since a particular date and whether you want to get sentiment of the caption of a post.
## How to use

The main python script is `posts_scraper.py`, which accepts the following arguments.
- **pages**: A list of comma-separated  facebook pages
- **n_posts**: The number of posts to scrape
- **since**: Scrape posts from this date till now
- **sentiment**: Whether to extract sentiment of the post caption
- **store**: Whether to store the result to a csv

An example run would be as follows

    python posts_scraper.py 
	    --pages page1,anotherpage2 
	    --n_posts 10 
		--since 2023-01-01 
		--sentiment 
		--store

