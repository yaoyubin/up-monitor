import asyncio
from bilibili_api import user
from up_list import TARGET_UIDS, NO_FILTER_UIDS

async def get_user_info(uid, semaphore):
    """获取用户信息"""
    async with semaphore:
        try:
            import sys
            print(f"正在查询 UID {uid}...", flush=True)
            sys.stdout.flush()
            u = user.User(uid=uid)
            info = await u.get_user_info()
            name = info.get('name', '未知')
            print(f"✓ UID {uid} -> {name}", flush=True)
            return {
                'uid': uid,
                'name': name,
                'success': True
            }
        except Exception as e:
            return {
                'uid': uid,
                'name': f'查询失败: {str(e)}',
                'success': False
            }

async def main():
    import sys
    sys.stdout.flush()
    
    # 合并 TARGET_UIDS 和 NO_FILTER_UIDS，去重
    all_uids = list(set(TARGET_UIDS + NO_FILTER_UIDS))
    print(f"开始查询 {len(all_uids)} 个UP主的信息（包含 {len(TARGET_UIDS)} 个监控UP主和 {len(NO_FILTER_UIDS)} 个特殊UP主）...\n", flush=True)
    
    # 使用信号量控制并发，避免触发风控
    semaphore = asyncio.Semaphore(2)
    tasks = [get_user_info(uid, semaphore) for uid in all_uids]
    results = await asyncio.gather(*tasks)
    
    print("=" * 60, flush=True)
    print(f"{'UID':<20} {'UP主名字':<30}", flush=True)
    print("=" * 60, flush=True)
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{result['uid']:<20} {result['name']:<30} {status}", flush=True)
    
    print("=" * 60, flush=True)
    success_count = sum(1 for r in results if r['success'])
    fail_count = sum(1 for r in results if not r['success'])
    print(f"\n查询完成！成功: {success_count}, 失败: {fail_count}", flush=True)
    
    # 自动更新 up_list.py
    update_up_list_file(results, success_count)
    
    # 输出格式化的列表（可用于更新代码）
    print("\n" + "=" * 60, flush=True)
    print("格式化输出（可用于代码注释）：", flush=True)
    print("=" * 60, flush=True)
    for result in results:
        if result['success']:
            print(f"    {result['uid']},  # {result['name']}", flush=True)
        else:
            print(f"    {result['uid']},  # 查询失败", flush=True)

def update_up_list_file(results, success_count):
    """更新 up_list.py 文件"""
    try:
        # 构建新的 UP_LIST 字典（按 UID 排序）
        up_list_dict = {}
        for result in sorted(results, key=lambda x: x['uid']):
            uid = result['uid']
            if result['success']:
                # 成功查询的，使用新获取的名字
                up_list_dict[uid] = result['name']
            else:
                # 查询失败的，尝试从现有的 up_list.py 中读取，如果没有则标记为"查询失败"
                try:
                    from up_list import UP_LIST
                    if uid in UP_LIST:
                        up_list_dict[uid] = UP_LIST[uid]
                    else:
                        up_list_dict[uid] = "查询失败"
                except:
                    up_list_dict[uid] = "查询失败"
        
        # 尝试从现有文件中读取 KEYWORDS 和 NO_FILTER_UIDS，保留用户的配置
        try:
            from up_list import KEYWORDS, NO_FILTER_UIDS
            keywords_list = KEYWORDS
            no_filter_list = NO_FILTER_UIDS
        except:
            # 如果读取失败，使用默认值
            keywords_list = ["AIGC", "LoRA", "工作流", "模型"]
            no_filter_list = []
        
        # 使用当前 TARGET_UIDS（已在文件顶部导入）来确定哪些UID应该写入UP_LIST
        target_uids_set = set(TARGET_UIDS)
        
        # 生成新的文件内容
        file_content = '''"""
B站UP主关注列表配置
包含需要监控的UP主的UID和名字
"""

# UP主列表：{UID: UP主名字}
UP_LIST = {
'''
        # 只写入 TARGET_UIDS 中的 UID（按 UID 排序）
        target_uids_to_write = [uid for uid in sorted(up_list_dict.keys()) if uid in target_uids_set]
        for uid in target_uids_to_write:
            name = up_list_dict[uid]
            # 转义引号，防止名字中包含引号
            name_escaped = name.replace('"', '\\"').replace("'", "\\'")
            file_content += f'    {uid}: "{name_escaped}",\n'
        
        file_content += '''}

# 提取所有UID列表（用于main.py）
TARGET_UIDS = list(UP_LIST.keys())

# 关键词过滤列表（用于视频内容过滤）
KEYWORDS = [
'''
        # 写入 KEYWORDS
        for kw in keywords_list:
            kw_escaped = kw.replace('"', '\\"').replace("'", "\\'")
            file_content += f'    "{kw_escaped}",\n'
        
        file_content += ''']

# 特殊UP主列表（这些UP主的视频不进行关键词过滤，直接推送）
# 如果某个UP主的所有视频都值得关注，可以将其UID添加到此列表中
NO_FILTER_UIDS = [
    # 示例：17280004,  # 蓝波球的球
    # 你可以在这里添加不需要关键词过滤的UP主UID
'''
        # 写入 NO_FILTER_UIDS（添加UP主名字注释）
        if no_filter_list:
            for uid in no_filter_list:
                # 优先从 up_list_dict 中查找对应的名字（最新查询结果）
                name = None
                if uid in up_list_dict:
                    name = up_list_dict[uid]
                else:
                    # 如果不在查询结果中，尝试从现有 UP_LIST 读取（可能不在 TARGET_UIDS 中）
                    try:
                        from up_list import UP_LIST as existing_up_list
                        if uid in existing_up_list:
                            name = existing_up_list[uid]
                    except:
                        pass
                
                # 如果有名字，添加注释；否则只写 UID
                if name and name != "查询失败":
                    # 转义引号，防止名字中包含引号
                    name_escaped = name.replace('"', '\\"').replace("'", "\\'")
                    file_content += f'    {uid},  # {name_escaped}\n'
                else:
                    # 如果没有找到名字，只写 UID（可能不在监控列表中或查询失败）
                    file_content += f'    {uid},\n'
        
        file_content += ']'
        
        # 写入文件
        with open('up_list.py', 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        print(f"\n✅ 已自动更新 up_list.py 文件", flush=True)
        print(f"   共更新 {success_count} 个UP主名字", flush=True)
        print(f"   已保留 KEYWORDS ({len(keywords_list)} 个) 和 NO_FILTER_UIDS ({len(no_filter_list)} 个) 配置", flush=True)
        
    except Exception as e:
        print(f"\n❌ 更新 up_list.py 失败: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())