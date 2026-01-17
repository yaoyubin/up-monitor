"""
B站UP主关注列表配置
包含需要监控的UP主的UID和名字
"""

# UP主列表：{UID: UP主名字}
UP_LIST = {
    4401694: "林亦LYi",
    130636947: "塑料叉FOKU",
}

# 提取所有UID列表（用于main.py）
TARGET_UIDS = list(UP_LIST.keys())

# 关键词过滤列表（用于视频内容过滤）
KEYWORDS = [
    "AIGC",
    "工作流",
    "模型",
]

# 特殊UP主列表（这些UP主的视频不进行关键词过滤，直接推送）
# 如果某个UP主的所有视频都值得关注，可以将其UID添加到此列表中
NO_FILTER_UIDS = [
    # 你可以在这里添加不需要关键词过滤的UP主UID
    419743655,  # BiBiPiano
    946974,  # 影视飓风
    125526,  # -LKs-
    1780480185,  # 飓多多StormCrew
    41759,  # -小拉-
]