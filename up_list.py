"""
B站UP主关注列表配置
包含需要监控的UP主的UID和名字
"""

# UP主列表：{UID: UP主名字}
UP_LIST = {
    4401694: "林亦LYi",
    130636947: "塑料叉FOKU",
}

# 特殊UP主列表（这些UP主的视频不进行关键词过滤，直接推送）
# 如果某个UP主的所有视频都值得关注，可以将其UID添加到此列表中
NO_FILTER_UIDS = [
    # 你可以在这里添加不需要关键词过滤的UP主UID
    419743655,  # BiBiPiano
    946974,  # 影视飓风
    125526,  # -LKs-
    1780480185,  # 飓多多StormCrew
    41759,  # -小拉-
    21151219,  # 我叫小马驹
]

# UP主名字映射（包含UP_LIST和NO_FILTER_UIDS中的所有UP主）
# 用于显示UP主名字，即使UP主不在UP_LIST中
UP_NAME_MAP = {
    **UP_LIST,  # 从UP_LIST中获取名字
    # NO_FILTER_UIDS中的UP主名字（从注释中提取）
    419743655: "BiBiPiano",
    946974: "影视飓风",
    125526: "-LKs-",
    1780480185: "飓多多StormCrew",
    41759: "-小拉-",
    21151219: "我叫小马驹",
}

# 提取所有UID列表（自动包含UP_LIST和NO_FILTER_UIDS中的所有UP主）
# 使用set去重，确保不重复监控
TARGET_UIDS = list(set(list(UP_LIST.keys()) + NO_FILTER_UIDS))

# 关键词过滤列表（用于视频内容过滤）
KEYWORDS = [
    "AIGC",
    "工作流",
    "模型",
]