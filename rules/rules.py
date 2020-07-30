rules = [
    # expiration_days < 5 AND current_inventory > 20
    {
        "conditions": {
            "all": [
                {"name": "videos_by_user", "operator": "less_than", "value": 4,},
                {"name": "videos_by_user", "operator": "greater_than", "value": 2,},
            ]
        },
        "actions": [{"name": "set_importance", "params": {"importance": 3},},],
    },
    {
        "conditions": {
            "all": [{"name": "videos_by_user", "operator": "less_than", "value": 2,}]
        },
        "actions": [{"name": "set_importance", "params": {"importance": 1},},],
    },
    {
        "conditions": {
            "all": [
                {"name": "videos_by_user", "operator": "greater_than", "value": 4,},
            ]
        },
        "actions": [{"name": "set_importance", "params": {"importance": 6},},],
    },
]
