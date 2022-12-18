# Basic/ Beginner Python
from math import floor, ceil
import numpy as np

# Basic print code
print("Text")

# Basic variables
text = "Hello world my name is "
name = "CJ. "
text2 = "I am "
age = 17
text3 = " years old."
print(text + name + text2 + str(age) + text3)

# Math calculations with variables

secs = 86400
days = 7
print("How many seconds or in a week?")
print(secs * days)

letter = 6
possibility = 26
total = possibility ** letter
print(total)

disk_size = 16 * 1024 * 1024 * 1024
sector_size = 512
sector_amount = disk_size / sector_size
print(sector_amount)

x = input("Enter number to calculate ratio: ")
ratio = (1 + int(x) ** (1/2)) / 2
print(ratio)

bill = 100.58
tip = bill * 0.15
total = bill + tip
share = total / 2
rounded_total = np.round(total, 2)
rounded_share = np.round(share, 2)

print("A party of 5 went out to eat, the bill was $" + str(bill))
print("The total cost of the meal including a 15% tip is:" + str(rounded_total))
print("Each person needs to pay $" + str(rounded_share) + " to split the bill evenly.")

set1 = [19, 492, 29]
set2 = [4, 25, 96]
print("What is the maximum value in the given set? " + str(set1))
print(max(set1))
print("What is the maximum value in the given set? " + str(set2))
print(max(set2))

num1 = 3635.253
num2 = 29884.0493
print("What is the floor for " + str(num1))
print(floor(num1))
print("What is the ceiling for " + str(num2))
print(ceil(num2))

# Getting input from users
name = input("Enter name: ")
print("the given name is: " + str(name) + ". Hello!!")

# Uppercase, Lowercase functions
low = "Original TEXT One, "
upp = "original teXT twO"
before = str(low) + str(upp)
print("Original: \n" + str(before))
print("Is the variable 'upp' capitalized?")
text_phrase = str(upp.isupper())
print(text_phrase)

after = str(low.lower()) + str(upp.upper())
print("Revised: \n" + str(after))
print("Is the variable 'upp' capitalized now?")
text_phrase = str(upp.upper().isupper())
print(text_phrase)

# `Return Values


def print_alpha_nums(abc_list, num_list):
    for char in abc_list:
        for num in num_list:
            print(char, num)
    return


print(print_alpha_nums(['a', 'b', 'c'], [1, 2, 3]))


def lucky_number(name2):
    number = len(name2) * 3
    print("\nHello " + str(name2) + ", your lucky number is " + str(number))


lucky_number("Carlton")
lucky_number("rhino")

# Define shout with the parameter, word


def shout(word):
    """Return a string with three exclamation marks"""
    # Concatenate the strings: shout_word
    shout_word = word + '!!!'
    # Replace print with return
    return shout_word
# Pass 'congratulations' to shout: yell


yell = shout('congratulations')


# Print yell
print(yell)

# Functions


def square(value):

    new_value = value**2
    print(new_value)


square(5)


def square():
    """Return the square of a value"""
    new_value = 4**2
    print(new_value)


square()


def square(value):

    new_value = value**2
    return new_value


num = square(3)

print(num)


def raise_to_power(value1, value2):
    """Raise value1 to the power of value2"""
    new_value = value1 ** value2
    print(new_value)


raise_to_power(3, 4)
raise_to_power(3, 0)

# Tuples
tuple1 = (5, 10, 15)
a, b, c = tuple1
print("Tuples")
print(b)
print(a)
print(c)

sec_num = tuple1[1]
print(sec_num)


# Back to Functions


def raise_both(value1, value2):
    """Raise value1 to the power of value2
    and vice versa"""
    new_value1 = value1 ** value2
    new_value2 = value2 ** value1
    new_tuple = (new_value1, new_value2)
    return new_tuple


result = raise_both(3, 2)
print(result)


# Define shout with parameters word1 and word2
def shout(word1, word2):
    """Concatenate strings with three exclamation marks"""
    # Concatenate word1 with '!!!': shout1
    shout1 = word1 + "!!!"

    # Concatenate word2 with '!!!': shout2
    shout2 = word2 + "!!!"

    # Concatenate shout1 with shout2: new_shout
    new_shout = (shout1 + shout2)

    # Return new_shout
    return new_shout


# Pass 'congratulations' and 'you' to shout(): yell
yell = shout('congratulations', 'you')

# Print yell
print(yell)

# Tuples
tuple1 = (5, 10, 15)
a, b, c = tuple1
print("Tuples")
print(b)
print(a)
print(c)

sec_num = tuple1[1]
print(sec_num)

nums = [3, 4, 6]
num1, num2, num3 = nums
print(nums)
print(num1, num2, num3)

nums[0] = 2
print(nums)

nums_data = (3, 4, 6)
# Unpack nums into num1, num2, and num3
num1, num2, num3 = nums_data

# Construct even_nums
even_nums = nums_data

print(even_nums)


# Define shout_all with parameters word1 and word2
def shout_all(word1, word2):
    # Concatenate word1 with '!!!': shout1
    shout1 = word1 + '!!!'

    # Concatenate word2 with '!!!': shout2
    shout2 = word2 + '!!!'
    # Construct a tuple with shout1 and shout2: shout_words
    shout_words = (shout1, shout2)

    # Return shout_words
    return shout_words


# Pass 'congratulations' and 'you' to shout_all(): yell1, yell2
yell1 = 'congratulations!!!'
yell2 = 'you!!!'
shout_all('congratulations', 'you')

# Print yell1 and yell2
print(yell1)
print(yell2)


def raise_both(value1, value2):
    """Raise value1 to the power of value2 and vice versa."""
    new_value1 = value1 ** value2
    new_value2 = value2 ** value1

    new_tuple = (new_value1, new_value2)

    return print(new_tuple)


raise_both(3, 5)

tuple1 = (5, 10, 15)
a, b, c = tuple1
print("Tuples")
print(b)
print(a)
print(c)
sec_num = tuple1[1]
print(sec_num)
