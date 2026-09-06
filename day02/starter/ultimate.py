# Day 2 终极挑战：战斗记录分析器
# 难度：★★★★★
#
# 目标：分析一组游戏战斗记录，输出统计报告。
#
# 这不是背包管理器的重复版：
# - 挑战 5 练“修改列表中的数据”；
# - 本题练“读取列表中的字典，筛选和统计数据”。
#
# 只使用 Day 1–2 已学内容：函数、字典、列表、for、if、append、return、sum、len。


def get_player_records(records, player_name):
    """返回某个玩家参与的所有记录。

    每条记录示例：
        {
            "player": "小戡",
            "enemy": "史莱姆",
            "damage": 20,
            "win": True
        }

    参数：
        records: 战斗记录列表
        player_name: 要查找的玩家名

    返回：
        只包含该玩家记录的新列表
    """
    result = []

    # TODO：遍历 records
    # TODO：如果 record["player"] 等于 player_name，就加入 result
    # TODO：return result
    for record in records:
        if record['player'] == player_name:
            result.append(record)
    return result


def calculate_total_damage(records):
    """计算记录列表中的总伤害。"""
    total = 0

    # TODO：遍历 records
    # TODO：把 record["damage"] 加到 total
    # TODO：return total
    for record in records:
        total += record['damage']
    return total

def count_wins(records):
    """统计获胜场数。"""
    wins = 0

    # TODO：遍历 records
    # TODO：如果 record["win"] 是 True，wins 加 1
    # TODO：return wins
    for record in records:
        if record['win']:
            wins += 1
    return wins


def build_battle_report(records, player_name):
    """为一个玩家生成战斗统计字典。

    返回格式：
        {
            "玩家": "小戡",
            "战斗场数": 2,
            "胜利场数": 1,
            "总伤害": 55
        }

    提示：本函数不要重新遍历和统计所有东西，
    要调用上面已经写好的 3 个函数。
    """
    # TODO：先用 get_player_records 得到该玩家记录
    # TODO：调用 calculate_total_damage 和 count_wins
    # TODO：创建并 return 报告字典
    player_records=get_player_records(records, player_name)
    total_damage = calculate_total_damage(player_records)
    wins = count_wins(player_records)
    player_total={}
    player_total["玩家"]=player_name
    player_total["战斗场数"]=len(player_records)
    player_total['总伤害']=total_damage
    player_total['胜利场数']=wins
    return player_total


if __name__ == "__main__":
    battle_records = [
        {"player": "小戡", "enemy": "史莱姆", "damage": 20, "win": True},
        {"player": "小戡", "enemy": "哥布林", "damage": 35, "win": False},
        {"player": "小红", "enemy": "史莱姆", "damage": 18, "win": True},
    ]

    print(build_battle_report(battle_records, "小戡"))
    # 期望：
    # {'玩家': '小戡', '战斗场数': 2, '胜利场数': 1, '总伤害': 55}

