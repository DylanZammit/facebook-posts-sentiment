from random import randint
import regex as re
import time
import functools
from traceback import format_exc
from transformers import pipeline                  
from googletrans import Translator


class Sentiment:

    def __init__(self, do_translate=True):
        self.do_translate = do_translate

        self.sent_pl = pipeline(
                model='cardiffnlp/twitter-roberta-base-sentiment-latest',
                max_length=512,
                truncation=True
            )
        if do_translate:
            self.translate = Translator().translate
            #self.translate = pipeline(model='Helsinki-NLP/opus-mt-mt-en')

    def get_sentiment(self, msg):
        if msg == '': return None, None

        msg = self.translate(msg).text if self.do_translate else msg
        sentiment = self.sent_pl(msg)[0]
        sent_label = sentiment['label']
        sent_score = sentiment['score']
        return sent_label, sent_score

def rsleep(t, cap=10, q=True):
    '''
    random sleep
    t - minimum number of seconds to sleep
    cap - sleeps up to 10 extra seconds randomly
    q - quiet
    '''
    sleep = t+randint(0, cap)
    if not q: print(f'Sleep for {sleep} seconds...', end='', flush=True)
    time.sleep(sleep)
    if not q: print('done', flush=True, end='\r')

def time_it(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        logger = kwargs.get('logger', None)
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()
        disp = f"Function {f.__name__} ran in {end - start:0.2f} seconds"
        if logger is not None:
            logger.info(disp)
        else:
            print(disp)

        return result
    return wrapper

