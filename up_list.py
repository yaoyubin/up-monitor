"""
B站UP主和YouTube频道关注列表配置
包含需要监控的UP主/频道的ID和名字
"""

# UP主列表：{UID: UP主名字}
UP_LIST = {
    41759: "-小拉-",
    125526: "-LKs-",
    946974: "影视飓风",
    4401694: "林亦LYi",
    21151219: "8KRAW",
    130636947: "塑料叉FOKU",
    419743655: "BiBiPiano",
    1780480185: "飓多多StormCrew",
}

# 特殊UP主列表（这些UP主的视频不进行关键词过滤，直接推送）
# 如果某个UP主的所有视频都值得关注，可以将其UID添加到此列表中
NO_FILTER_UIDS = [
    # 示例：17280004,  # 蓝波球的球
    # 你可以在这里添加不需要关键词过滤的UP主UID
    419743655,  # BiBiPiano
    946974,  # 影视飓风
    125526,  # -LKs-
    1780480185,  # 飓多多StormCrew
    41759,  # -小拉-
    21151219,  # 8KRAW
] 

# YouTube频道列表：{Channel ID: 频道名字}
# Channel ID 格式：UCxxxxx（24个字符）
YOUTUBE_CHANNELS = {
    "UCVomjkM_t0EcctTWSE1Jvxg": "贝拉聊财金",
}

# YouTube特殊频道列表（这些频道的视频不进行关键词过滤，直接推送）
# 如果某个频道的所有视频都值得关注，可以将其Channel ID添加到此列表中
YOUTUBE_NO_FILTER_CHANNELS = [
    # 示例：'UCxxxxx',  # 频道名字
    # 你可以在这里添加不需要关键词过滤的YouTube频道ID
    "UCVomjkM_t0EcctTWSE1Jvxg",  # 贝拉聊财金
]

# UP主名字映射（自动包含UP_LIST和NO_FILTER_UIDS中的所有UP主）
# 用于显示UP主名字，即使UP主不在UP_LIST中
# 此映射会自动从UP_LIST和查询结果中生成
# 现在也包含YouTube频道名字
UP_NAME_MAP = {
    **UP_LIST,  # 从UP_LIST中获取名字
    **YOUTUBE_CHANNELS,  # 从YOUTUBE_CHANNELS中获取名字
}

# 关键词过滤列表（用于视频内容过滤）
KEYWORDS = [
    "AIGC",
    "工作流",
    "模型",
]