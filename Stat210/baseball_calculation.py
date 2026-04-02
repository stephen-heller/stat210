from pybaseball import batting_stats
leading_digit_quantities = 9 * [0]

data = batting_stats(2015, 2025, ind=0)
print("Max HR's hit by one player from 2015-2025:", max(data["HR"]))
print("Min HR's hit by one player from 2015-2025:", min(data["HR"]))
print("Number of qualified hitters in the data set:", len(data["HR"]))
for num in data["HR"]:
    first_digit = int(str(num)[0])
    leading_digit_quantities[first_digit - 1] += 1

print("Leading digit frequencies: ", end="")
for num in leading_digit_quantities:
    print(num, end=" ")