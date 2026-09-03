# Day 43 性能分析示例
import timeit
import cProfile
import tracemalloc

# 比较不同数据结构
def benchmark_data_structures():
    data = list(range(10000))
    data_set = set(data)
    
    t_list = timeit.timeit(lambda: 9999 in data, number=1000)
    t_set = timeit.timeit(lambda: 9999 in data_set, number=1000)
    print(f'list 查找: {t_list:.4f}s')
    print(f'set  查找: {t_set:.6f}s')
    print(f'set 快 {t_list/t_set:.0f} 倍')

# 内存分析
def memory_analysis():
    tracemalloc.start()
    data = [i ** 2 for i in range(100000)]
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics('lineno')[:3]:
        print(stat)

# 瓶颈分析
def slow_code():
    result = []
    for i in range(50000):
        result.append(i ** 2)
    return sum(result)

def fast_code():
    return sum(i ** 2 for i in range(50000))

if __name__ == '__main__':
    benchmark_data_structures()
    print()
    cProfile.run('slow_code()', sort='cumulative')
    t1 = timeit.timeit(slow_code, number=10)
    t2 = timeit.timeit(fast_code, number=10)
    print(f'slow: {t1:.4f}s, fast: {t2:.4f}s')
