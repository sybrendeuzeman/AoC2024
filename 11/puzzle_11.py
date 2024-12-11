import pandas as pd
#input = "125 17"
input = "4610211 4 0 59 3907 201586 929 33750"

# Part 1
class Stone:
    def __init__(self, number):
        self.number = number

    def update(self):
        if self.number == 0:
            self.number = 1
        elif not len(str(self.number)) % 2:
            half_point = len(str(self.number))//2      
            
            new_stone = Stone(int(str(self.number)[half_point:len(str(self.number))]))
            self.number = int(str(self.number)[0:half_point])
            return new_stone
        else:
            self.number *= 2024
    
    def retrieve_value(self):
        self.number

list_stones = [
    Stone(int(number_stone))
    for number_stone
    in input.split(' ')
]

for i in range(25):
    list_new_stones = [
        stone
        for stone
        in [
            stone.update()
            for stone
            in list_stones
        ]
        if stone is not None
    ]

    list_stones += list_new_stones

print('The number of stones is:', len(list_stones))

# Part 2

def get_new_number(number):
    if number == 0:
        return [1]
    elif not len(str(number)) % 2:
        half_point = len(str(number))//2      
        return [
            int(str(number)[half_point:len(str(number))]),
            int(str(number)[0:half_point])
        ]
    else:
        return number * 2024


df_stones = pd.DataFrame(
    {
        'number_stone' : [int(number_stone) for number_stone in input.split(' ')],
        'amount' : [1 for number_stone in input.split(' ')]
    }
)

for i in range(75):
    df_stones['number_stone'] = df_stones['number_stone'].apply(get_new_number)    
    df_stones = df_stones.explode('number_stone')
    df_stones = df_stones.groupby('number_stone').agg("sum")
    df_stones = df_stones.reset_index()

total = df_stones.agg({'amount' : 'sum'})

print('The number of stones is:', total)