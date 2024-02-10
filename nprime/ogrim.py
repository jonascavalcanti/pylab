
import sys


def main():
    number = 144
    if is_prime(number):
        print(number, "is a Prime Number")
    else:
        print(number, "is Not a Prime Number")


def is_prime(number):
    countPrime = 2

    print("Check prime number for:", number)

    for i in range(2, number):
        if number % i == 0:
           print("Number Divisible",i)
           countPrime=countPrime + 1
    
    if countPrime > 2:
        return False
    else:
        return True

if __name__ == '__main__':
    sys.exit(main())