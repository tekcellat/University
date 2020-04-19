from itertools import starmap
from operator import mul
from random import randint
import time
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
#from memory_profiler import profile
#liliya@bmstu.ru


start_time = time.time()

logging.basicConfig(format="[%(thread)-5d]%(asctime)s: %(message)s")
logger = logging.getLogger('async')
logger.setLevel(logging.INFO)
loop = asyncio.get_event_loop()  # event loop
executor = ThreadPoolExecutor(max_workers=3)  # thread pool

#@profile
def multi(A, B):
    if len(B) != len(A[0]):
        print("Different dimension of the matrics")
        return

    n = len(A)
    m = len(A[0])
    t = len(B[0])

    answer = [[0 for i in range(t)] for j in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(t):
                answer[i][k] += A[i][j] * B[j][k]
    return answer

#@profile
async def get_new_elem(row, tmp):
    return [sum(starmap(mul, zip(row, column))) for column in tmp]

#@profile
async def multi_async(A, B):
    tmp = tuple(zip(*B))

    results = await asyncio.gather(*[get_new_elem(row, tmp) for row in A])
    return results

#@profile
def random_matrix(n, m):
    return [[randint(0, 100) for i in range(m)] for j in range(n)]

#@profile
def main(A, B):
    if len(B) != len(A[0]):
        print("Different dimension of the matrics")
        return

    
    result = loop.run_until_complete(multi_async(A, B))
    return result

#realise with grenn potoki umnoj i analitika
if __name__ == '__main__':
    start = int(round(time.time() * 1000))
    A = random_matrix(3, 3)
    B = random_matrix(3, 3)
    
    C1 = main(A, B)
    st = time.time()
    C2 = multi(A, B)
    logger.info("Completed in {} seconds".format(time.time() - start_time))

    print("Execution Time --->", (int(round(time.time() * 1000)) - start))
    #print(time.time() - st)
    print(C2)

#umumi yaddas 129.6 10-100
#umumi yaddas 129.6 0-100
