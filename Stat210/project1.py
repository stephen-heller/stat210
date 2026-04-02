from matplotlib import pyplot as plt
import math


data_as_strs = (input("Please enter the leading digit frequencies,, separated by spaces, e.g. \n100 50 23 16 8 4 3 2 1\n").split())
data = [int(x) for x in data_as_strs]
digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
benford_probs = [sum(data)*math.log10(1 + 1 / digit) for digit in digits]
fig = plt.bar(digits, data,)
plt.plot(digits, benford_probs, color='red', marker='o',)
plt.xlabel("Leading digit")
plt.ylabel("Frequency")
plt.title("Leading digit of home run counts from qualified MLB hitters, 2015-2025")
plt.savefig("distribution.png")

