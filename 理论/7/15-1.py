def sort_merge_algorithm(data, memory_blocks):
    # 分割数据，模拟内存块限制
    runs = [data[i:i+memory_blocks] for i in range(0, len(data), memory_blocks)]

    print("初始分块:")
    for idx, run in enumerate(runs):
        runs[idx] = sorted(run, key=lambda x: x[0])  # 按第一个属性排序
        print(f"运行 {idx + 1}: {runs[idx]}")

    # 合并过程
    pass_num = 1
    while len(runs) > 1:
        print(f"\n第 {pass_num} 轮合并:")
        new_runs = []
        for i in range(0, len(runs), memory_blocks - 1):
            # 从当前轮次中选取可合并的块
            to_merge = runs[i:i + (memory_blocks - 1)]
            if len(to_merge) > 1:  # 只有超过一个块时才进行合并
                merged_run = merge_runs(to_merge)
                new_runs.append(merged_run)
                print(f"合并: {to_merge} -> {merged_run}")
            else:
                new_runs.extend(to_merge)  # 单块无需合并，直接加入
        runs = new_runs
        pass_num += 1

    print("\n最终排序结果:")
    print(runs[0])


def merge_runs(runs):
    # 使用多路归并合并多个块
    import heapq
    merged = list(heapq.merge(*runs, key=lambda x: x[0]))
    return merged


# 输入数据
input_data = [
    ("kangaroo", 17), ("wallaby", 21), ("emu", 1), ("wombat", 13),
    ("platypus", 3), ("lion", 8), ("warthog", 4), ("zebra", 11),
    ("meerkat", 6), ("hyena", 9), ("hornbill", 2), ("baboon", 12)
]

# 每个块只能容纳一个元组，内存最多容纳三个块
memory_blocks = 3

# 执行排序合并算法
sort_merge_algorithm(input_data, memory_blocks)