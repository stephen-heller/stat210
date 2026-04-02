from pybaseball import batting_stats
from matplotlib import pyplot as plt

leading_digits = 9 * [0]

data = batting_stats(2015, 2025, ind=0)
print(max(data["HR"]))
for num in data["HR"]:
    first_digit = int(str(num)[0])
    leading_digits[first_digit - 1] += 1

print(leading_digits)


fig = plt.bar([1, 2, 3, 4, 5, 6, 7, 8, 9], leading_digits,)
plt.xlabel("Leading digit of home run count from 2015-2025")
plt.ylabel("Frequency")
plt.savefig("test2.png")