def str2int(args):
    from diskhash import Str2int
    import argparse
    parser = argparse.ArgumentParser(description='String to index')
    parser.add_argument('ifile', metavar='FILE', nargs=1, type=str,
                            help='Input file')
    parser.add_argument(
                    '--output', default=None, type=str,
                            help='Output file for index')
    args = parser.parse_args(args)

    s = Str2int(args.index, 'w')
    for i,line in enumerate(open(args.ifile, 'rt')):
        s.insert(line, i)

if __name__ == '__main__':
    from sys import argv
    str2int(argv)
