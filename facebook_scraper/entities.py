import gender_guesser.detector as getgender
from pydantic import validate_arguments
from dataclasses import dataclass, field
#from typing import List


@validate_arguments
@dataclass(frozen=True, order=False)
class Post:
    page_name: str
    post_id: int
    post_time: str
    has_text: int = None
    has_image: int = None
    has_video: int = None
    post_type: int = None
    num_shares: int = None
    num_comments: int = None
    num_reacts: int = None
    num_like: int = None
    num_haha: int = None
    num_love: int = None
    num_wow: int = None
    num_sad: int = None
    num_angry: int = None
    was_live: int = None
    caption: str = ''
    sent_label: str = None
    sent_score: float = None


@validate_arguments
@dataclass(frozen=True, order=False)
class Page:
    for_date: str
    username: str
    name: str = None
    num_followers: int = None
    num_likes: int = None
    #posts: list[Post] = field(default_factory=list)
    posts: list = field(default_factory=list)

