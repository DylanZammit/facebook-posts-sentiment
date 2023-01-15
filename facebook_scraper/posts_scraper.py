from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent

from facebook_scraper.exceptions import TemporarilyBanned, NotFound
from traceback import format_exc
from datetime import datetime
import facebook_scraper as fs 
from entities import Post
from utils import time_it, rsleep, Sentiment
import pandas as pd



class FacebookScraper:

    def __init__(
            self, 
            cookies=None, 
            posts_per_page=50, 
        ):
        """
        Creates FB instance by logging in
        """

        if cookies: fs.set_cookies(cookies)

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, opearting_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()

        fs.set_user_agent(user_agent)

        self.posts_per_page = posts_per_page

        # Should not be hardcoded!!!
        self.translate_pages = ['newsbook.com.mt', 'TelevisionMalta', 'ONE.com.mt', 'NetNewsMalta']

    def scrape_posts(self, page_name, num_posts=None, since=None, do_sentiment=True):
        '''
        scrapes facebook posts of a particular page
        page_name - name of facebook page
        num_posts - number of posts to scrape
        since - scrape posts since since
        '''
        if do_sentiment:
            do_translate = page_name in self.translate_pages
            sent = Sentiment(do_translate)

        if since is None: since = pd.Timestamp('2000-01-01')
        if num_posts is None: num_posts = 1000000

        ppp = self.posts_per_page
        options = {
            'posts_per_page': ppp,
        }

        posts = fs.get_posts(page_name, options=options, extra_info=True, page_limit=None)

        page_posts = []
        users = []
        for i, post in enumerate(posts):

            if i > 0 and (i+1)%ppp==0: rsleep(10, 10, q=False)
            post_details = {}

            try:
                post_time = str(post['time'])
                if i >= num_posts: break
                if pd.Timestamp(post_time) < since: break

                post_id = int(post['post_id'])
                print(f'{i+1}) Post={post_id} on {post_time}')
                has_text = True if post['text'] is not None else False
                caption = post.get('text', None)
                num_comments = post['comments']
                num_shares = post['shares']
                has_image = post['image'] is not None
                has_video = post['video'] is not None
                video_watches = post['video_watches']
                was_live = post['was_live']

                if has_image:
                    post_type = 2
                elif has_video:
                    post_type = 3
                elif has_text:
                    post_type = 1
                else:
                    post_type = None

                reactions = post['reactions']
                if reactions is None: reactions = {}
                num_like = reactions.get('like', 0)
                num_love = reactions.get('love', 0)
                num_haha = reactions.get('haha', 0)
                num_wow = reactions.get('wow', 0)
                num_angry = reactions.get('angry', 0)
                num_sad = reactions.get('sad', 0)
                num_reacts = post.get('reaction_count', 0)

                if do_sentiment:
                    sent_label, sent_score = sent.get_sentiment(caption)
                else:
                    sent_label, sent_score = None, None

                page_posts.append(
                    Post(
                        page_name=page_name,
                        post_id=post_id,
                        has_text=has_text,
                        has_video=has_video,
                        has_image=has_image,
                        post_time=post_time,
                        was_live=was_live,
                        post_type=post_type,
                        num_shares=num_shares,
                        num_comments=num_comments,
                        num_reacts=num_reacts,
                        num_like=num_like,
                        num_haha=num_haha,
                        num_love=num_love,
                        num_wow=num_wow,
                        num_sad=num_sad,
                        num_angry=num_angry,
                        caption=caption,
                        sent_label=sent_label,
                        sent_score=sent_score
                    )
                )

            except TemporarilyBanned as e:
                print(f'Temporarily banned')
                break
            except Exception as e:
                print('Unhandled error. Stopping scraping')
                print(format_exc())

        self.users = users
        return page_posts

    def scrape_page(self, page_name):
        '''
        scrape page details
        page_name - name of fb page
        '''
        today = str(datetime.now())

        page_details = fs.get_page_info(page_name)
        num_likes = page_details.get('likes', None)
        num_followers = page_details.get('Follower_count', None)
        page_name = page_details.get('Name', None)
        page_id = page_details.get('id', None)
        if page_id is None: page_id = 1
        self.page_id = int(page_id)
        if num_likes is None:
            print(f'Could not get page likes for {page_name}')
        if num_followers is None:
            print(f'Could not get page followers for {page_name}')

        page = Page(
            for_date=today,
            num_likes=num_likes,
            num_followers=num_followers,
            page_name=page_name,
            name=page_name
        )

        return page


@time_it
def get_posts(page_name, num_posts=None, since=None, do_sentiment=True):

    posts = []
    if num_posts is None and since is None:
        print('Specify either number of posts or since arg')
        return

    for i in range(5):
        print(f'Attempt #{i+1}')
        extractor = FacebookScraper(cookies='cookies.txt')

        posts = extractor.scrape_posts(
            page_name=page_name,
            num_posts=num_posts,
            since=since,
            do_sentiment=do_sentiment,
        )

        if len(posts) > 0: break
        rsleep(30, q=False)

    if len(posts) > 0:
        print('Failed to read posts after 5 attempts')
    else:
        print(f'{len(posts)} posts loaded')
        
    posts = [p.__dict__ for p in posts]
    df_posts = pd.DataFrame(posts)

    return df_posts

# malta facebook news pages
# newsbook.com.mt,TelevisionMalta,ONE.com.mt,NetNewsMalta,maltatoday,timesofmalta,TheMaltaIndependent
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', help='list of comma-separated page names', type=str)
    parser.add_argument('--n_posts', help='Number of posts to read [default=inf]', type=int)
    parser.add_argument('--since', help='datetime to read posts since: "%%Y-%%m-%%d', type=str)
    parser.add_argument('--sentiment', help='perform sentiment analysis on comments and posts', action='store_true')
    parser.add_argument('--store', help='store to csv', action='store_true') 
    args = parser.parse_args()

    since = pd.Timestamp(args.since) if args.since is not None else args.since

    df = pd.DataFrame()
    for page in args.pages.split(','):
        try:
            print(f'Reading {page} posts')

            df_posts = get_posts(
                page,
                args.n_posts,
                since,
                args.sentiment,
            )

            df = pd.concat([df, df_posts])
        except Exception as e:
            print(f'Error reading {page}')
            print(format_exc())

    if args.store:
        df.to_csv(f'facebook_posts.csv')
    breakpoint()
