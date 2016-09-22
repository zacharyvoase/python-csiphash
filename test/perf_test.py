"""A naive benchmark script."""

import textwrap
import timeit


def time_hashing(message_size):
    setup = textwrap.dedent('''
    import random
    import csiphash
    key = ''.join(chr(random.randint(0, 255)) for _ in xrange(16))
    message = ''.join(chr(random.randint(0, 255)) for _ in xrange({message_size}))
    ''').format(message_size=message_size)
    statement = 'csiphash.siphash24(key, message)'

    results = []
    for _ in xrange(3):
        results.append(timeit.timeit(setup=setup, stmt=statement, number=1000000))
    return sum(results) / 3.0


# From the SipHash paper (http://cr.yp.to/siphash/siphash-20120620.pdf):
# > A fair rule-of-thumb for the distribution on message-sizes on an Internet
# > backbone is that roughly one-third of messages are 43 bytes (TCP ACKs),
# > one-third are about 256 bytes (common PPP dialup MTU), and one-third are 1500
# > bytes (common Ethernet MTU).
MESSAGE_SIZES = [43, 256, 1500]


if __name__ == '__main__':
    for message_size in MESSAGE_SIZES:
        average_time = time_hashing(message_size)
        print 'siphash24(char[{message_size}]) = {average_time:0.2f} microseconds'.format(message_size=message_size, average_time=average_time)
