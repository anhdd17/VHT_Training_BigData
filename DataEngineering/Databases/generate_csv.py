import csv

data = [
    ['id', 'cut', 'color', 'clarity', 'carat', 'price'],
    [1, 'Ideal', 'E', 'SI1', 0.71, 2159],
    [2, 'Premium', 'E', 'SI1', 0.72, 2316],
    [3, 'Good', 'E', 'SI2', 0.73, 2317],
    [4, 'Very Good', 'E', 'VS2', 0.74, 2442],
    [5, 'Ideal', 'F', 'VS1', 0.75, 2492]
]

with open('diamonds.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
