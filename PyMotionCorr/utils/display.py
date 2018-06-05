from time import gmtime, strftime


def print_time(*args):
    print('[', strftime("%Y-%m-%d %H:%M:%S", gmtime()), ']\n', *args)
