from business_rules.actions import BaseActions, rule_action, fields
from business_rules.variables import BaseVariables, numeric_rule_variable
import datetime as dt


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

    @numeric_rule_variable
    def contacts_by_user(self):
        return self.video.contacts_count

    @numeric_rule_variable
    def days_difference(self):
        return (dt.datetime.now() - self.video.createdAt).days


class VideoActions(BaseActions):
    def __init__(self, video):
        self.video = video

    @rule_action(params={"importance": fields.FIELD_NUMERIC})
    def set_importance(self, importance):
        self.video.importance += importance

    @rule_action(params={"percent": fields.FIELD_NUMERIC})
    def set_importance_likes_percent(self, percent):
        self.video.importance += percent * self.video.likes_count

    @rule_action(params={"percent": fields.FIELD_NUMERIC})
    def set_importance_degrade_percent(self, percent):
        self.video.importance += percent * self.video.days_difference


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


def make_rule_likes_percent(limits, importance):
    return [
        {
            "conditions": {
                "all": [
                    {
                        "name": "likes_by_video",
                        "operator": "less_than",
                        "value": limits["low"],
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_importance_likes_percent",
                    "params": {"percent": importance["low"]},
                },
            ],
        },
        {
            "conditions": {
                "all": [
                    {
                        "name": "likes_by_video",
                        "operator": "less_than",
                        "value": limits["high"],
                    },
                    {
                        "name": "likes_by_video",
                        "operator": "greater_than_or_equal_to",
                        "value": limits["low"],
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_importance_likes_percent",
                    "params": {"percent": importance["medium"]},
                },
            ],
        },
        {
            "conditions": {
                "all": [
                    {
                        "name": "likes_by_video",
                        "operator": "greater_than_or_equal_to",
                        "value": limits["high"],
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_importance_likes_percent",
                    "params": {"percent": importance["high"]},
                },
            ],
        },
    ]


def make_rule_degrade_date(limits, importance):
    return [
        {
            "conditions": {
                "all": [
                    {
                        "name": "days_difference",
                        "operator": "less_than",
                        "value": limits["low"],
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_importance_degrade_percent",
                    "params": {"percent": importance["low"]},
                },
            ],
        },
        {
            "conditions": {
                "all": [
                    {
                        "name": "days_difference",
                        "operator": "less_than",
                        "value": limits["high"],
                    },
                    {
                        "name": "days_difference",
                        "operator": "greater_than_or_equal_to",
                        "value": limits["low"],
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_importance_degrade_percent",
                    "params": {"percent": importance["medium"]},
                },
            ],
        },
        {
            "conditions": {
                "all": [
                    {
                        "name": "days_difference",
                        "operator": "greater_than_or_equal_to",
                        "value": limits["high"],
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_importance_degrade_percent",
                    "params": {"percent": importance["high"]},
                },
            ],
        },
    ]


rule_contacts = make_rule(
    "contacts_by_user", make_limit(2, 4), make_importance(1, 3, 6)
)
rule_videos = make_rule("videos_by_user", make_limit(2, 4), make_importance(1, 3, 5))
rule_comment = make_rule(
    "comments_by_video", make_limit(2, 5), make_importance(1, 3, 5)
)
# rule_like = make_rule("likes_by_video", make_limit(2, 5), make_importance(1, 3, 5))
rule_dislike = make_rule(
    "dislikes_by_video", make_limit(3, 5), make_importance(0, -2, -4)
)
rule_like_importance = make_rule_likes_percent(
    make_limit(5, 10), make_importance(1, 0.9, 0.7)
)

rule_date_degrade = make_rule_degrade_date(
    make_limit(10, 30), make_importance(-0.1, -0.2, -0.4),
)

rules = (
    rule_videos
    + rule_like_importance
    + rule_dislike
    + rule_contacts
    + rule_comment
    + rule_date_degrade
)
