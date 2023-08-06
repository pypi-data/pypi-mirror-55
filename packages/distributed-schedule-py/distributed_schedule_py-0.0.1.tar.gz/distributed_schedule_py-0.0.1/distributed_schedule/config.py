import logging


def set_logging_level(loglevel):
    logging.basicConfig(
        level=loglevel,
        format='%(asctime)s - %(thread)d - %(filename)s - %(lineno)d - %(levelname)s - %(message)s'
    )


def div_shard(shard: int, length: int) -> []:
    """
    example :  shard : 7 length : 3 res => [[0, 3, 6], [1, 4], [2, 5]]
    :param shard:
    :param length:
    :return:
    """
    if length <= 0:
        return []

    if length >= shard:
        return [[i] for i in range(shard)]

    res = [[] for _ in range(length)]
    cur_v = [i for i in range(shard)]
    v = int(shard/length)
    for j in range(length):
        for i in range(v):
            res[j].append(cur_v[j+i*length])

    if v*length != shard:
        i = 0
        for j in range(v*length, shard):
            res[i].append(j)
            i += 1
    return res