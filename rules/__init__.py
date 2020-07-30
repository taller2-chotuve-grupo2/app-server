from business_rules.actions import BaseActions, rule_action, fields
from business_rules.variables import BaseVariables, numeric_rule_variable


class VideoVariables(BaseVariables):
    def __init__(self, video):
        self.video = video

    @numeric_rule_variable
    def videos_by_user(self):
        return self.video.videos_by_user

    @numeric_rule_variable
    def likes_by_video(self):
        return self.video.likes_count

    @numeric_rule_variable
    def dislikes_by_video(self):
        return self.video.dislikes_count

    @numeric_rule_variable
    def comments_by_video(self):
        return self.video.comments_count


class VideoActions(BaseActions):
    def __init__(self, video):
        self.video = video

    @rule_action(params={"importance": fields.FIELD_NUMERIC})
    def set_importance(self, importance):
        self.video.importance += importance


def make_limit(low, high):
    return {"low": low, "high": high}


def make_importance(low, medium, high):
    return {"low": low, "medium": medium, "high": high}


def make_rule(variable, limits, importance):
    return [
        {
            "conditions": {
                "all": [
                    {"name": variable, "operator": "less_than", "value": limits["low"],}
                ]
            },
            "actions": [
                {
                    "name": "set_importance",
                    "params": {"importance": importance["low"]},
                },
            ],
        },
        {
            "conditions": {
                "all": [
                    {
                        "name": variable,
                        "operator": "less_than",
                        "value": limits["high"],
                    },
                    {
                        "name": variable,
                        "operator": "greater_than_or_equal_to",
                        "value": limits["low"],
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_importance",
                    "params": {"importance": importance["medium"]},
                },
            ],
        },
        {
            "conditions": {
                "all": [
                    {
                        "name": variable,
                        "operator": "greater_than_or_equal_to",
                        "value": limits["high"],
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_importance",
                    "params": {"importance": importance["high"]},
                },
            ],
        },
    ]


rule_videos = make_rule("videos_by_user", make_limit(2, 4), make_importance(1, 3, 5))
rule_like = make_rule("likes_by_video", make_limit(2, 5), make_importance(1, 3, 5))
rule_dislike = make_rule(
    "dislikes_by_video", make_limit(3, 5), make_importance(0, -2, 4)
)


rules = rule_videos + rule_like + rule_dislike
