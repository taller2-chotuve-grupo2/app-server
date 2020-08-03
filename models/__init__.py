from services import video_service, user_service
from flask import current_app
import pandas as pd
import datetime as dt
from business_rules import run_all
from rules import VideoActions, VideoVariables, rules


class Video:
    def __init__(self, args):
        self.id = args["id"]
        self.title = args["title"]
        self.owner = args["owner"]
        self.videos_by_user = args["videosByUser"]
        self.likes_count = args["likesCount"]
        self.dislikes_count = args["dislikesCount"]
        self.comments_count = args["commentsCount"]
        self.importance = 0
        self.createdAt = dt.datetime.strptime(
            args["createdAt"].split("T")[0], "%Y-%m-%d"
        )
        self.days_difference = (dt.datetime.now() - self.createdAt).days
        self.thumbnail = args["thumbnail"]

    def __str__(self):
        return self.importance


def updateVideosWithCount(videos):
    df = pd.DataFrame(videos)
    df["videosByUser"] = df["owner"].groupby(df["owner"]).transform("count")
    return [Video(kwargs) for kwargs in df.to_dict(orient="records")]


class Feed(object):
    def __init__(self):
        self.videos_importance = []
        self.cache_time = dt.datetime(2019, 1, 1)
        self.cache_ttl = 4 * 60

    def expired(self):
        difference = dt.datetime.now() - self.cache_time
        if difference.seconds > self.cache_ttl:
            return True
        else:
            return False

    def regenerate(self, query_params={}):
        current_app.logger.info("GET FEED")
        response = video_service.make_feed_request(query_params)
        if response.status_code == 200:
            videos_feed = response.json()
            videos = updateVideosWithCount(videos_feed)
            for video in videos:
                contacts_count = 0
                try:
                    owner = user_service.find_by_username(video.owner)
                    contacts_count = len(user_service.get_friends(owner))
                except Exception as e:
                    print("NO OWNER REGISTERED")
                finally:
                    video.contacts_count = contacts_count
                    self.cache_time = dt.datetime.now()
                run_all(
                    rule_list=rules,
                    defined_variables=VideoVariables(video),
                    defined_actions=VideoActions(video),
                )
            videos_importance = [video.__dict__ for video in videos]
            videos_importance_sorted = sorted(
                videos_importance, key=lambda video: video["importance"], reverse=True
            )
            self.videos_importance = videos_importance_sorted
        else:
            raise BaseException

    def videosSortedImportance(self):
        return self.videos_importance
