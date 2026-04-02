from pybaseball import batting_stats
from matplotlib import pyplot as plt
import math

leading_digit_quantities = 9 * [0]

data = batting_stats(2015, 2025, ind=0)
print(max(data["HR"]))
print(min(data["HR"]))
print(len(data["HR"]))
for num in data["HR"]:
    first_digit = int(str(num)[0])
    leading_digit_quantities[first_digit - 1] += 1

print(leading_digit_quantities)

digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
benford_probs = [len(data["HR"])*math.log10(1 + 1 / digit) for digit in digits]
fig = plt.bar(digits, leading_digit_quantities,)
plt.plot(digits, benford_probs, color='red', marker='o',)
plt.xlabel("Leading digit")
plt.ylabel("Frequency")
plt.title("Leading digit of home run counts from qualified MLB hitters, 2015-2025")
plt.savefig("distribution.png")

