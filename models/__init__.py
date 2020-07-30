from services import video_service
from flask import current_app
import pandas as pd
from business_rules import run_all
from rules import VideoActions, VideoVariables, rules


class Video:
    def __init__(self, args):
        print(args)
        self.id = args["id"]
        # self.title = args["title"]
        self.videos_by_user = args["videosByUser"]
        self.likes_count = args["likesCount"]
        self.dislikes_count = args["dislikesCount"]
        self.comments_count = args["commentsCount"]
        self.importance = 0

    def __str__(self):
        return self.importance


class Feed(object):
    def __init__(self):
        self.videos_importance = []

    def expired(self):
        return True

    def regenerate(self, query_params):
        current_app.logger.info("GET FEED")
        response = video_service.make_feed_request(query_params)
        if response.status_code == 200:
            videos_feed = response.json()
            # res = json.loads(videos)
            df = pd.DataFrame(videos_feed)
            df["videosByUser"] = df["owner"].groupby(df["owner"]).transform("count")
            videos = [Video(kwargs) for kwargs in df.to_dict(orient="records")]
            for video in videos:
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
        current_app.logger.info(self.videos_importance)
        return self.videos_importance
        # return self.videos_importance.sort(key=lambda video: video["importance"])
