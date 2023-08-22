import sys


def fatorial(n):
    if n == 0:
        return 1
    return n * fatorial(n-1)


def main():
    n = 5
    print(fatorial(n))


if __name__ == '__main__':
    sys.exit(main())
