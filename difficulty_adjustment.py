
def DA(blocks, rolling=False, n_back=10, target=15):
    def f(x):
        total_time = x[-1] - x[0]
        avg_time = total_time / (n_back - 1)
        print("total_time =", total_time, ". target =", target, ". n_back = ", n_back)
        return target / avg_time 

    if len(blocks) < n_back:
        return 1
    largest_block = max(blocks.keys())
    if largest_block < n_back:
        return 1
    if not rolling:
        if largest_block % n_back == 0:
            return f([blocks[largest_block - n_back + i]['header']['timestamp'] for i in range(n_back)]) 
        else:
            return 1 # not rolling so no update
            # num = len(blocks) // n_back * n_back # take off extras
            # return f([blocks[num - n_back + i]['header']['timestamp'] for i in range(n_back)]) 
    else:
        return f([blocks[largest_block - n_back + i + 1]['header']['timestamp'] for i in range(n_back)])  

def create_test_blocks(n, additive=1, multiplier=1):
    return { i: {'timestamp':i * multiplier + additive} for i in range(n) }

def run_test(n, expected, n_back=10, target=15, rolling=False, additive=1, multiplier=1):
    blocks = create_test_blocks(n, additive=additive, multiplier=multiplier)
    da = DA(blocks, rolling=rolling, n_back=n_back, target=target)
    print(da)
    assert da == expected, "{} should equal {}".format(da, expected)

def test1():
    run_test(20, 15, n_back=10, target=15, rolling=False, additive=1, multiplier=1)

def test2():
    run_test(20, 15, n_back=10, target=15, rolling=False, additive=2, multiplier=1)

def test3():
    run_test(20, 7.5, n_back=10, target=15, rolling=False, additive=1, multiplier=2)

def test4():
    run_test(20, 5, n_back=10, target=15, rolling=False, additive=2, multiplier=3)

def run_tests():
    for i in range(1,4+1):
        eval('test{}()'.format(i))

if __name__ == '__main__':
    run_tests()
