line_number = 1
rows = 0
cols = 0
grid = None
with open('map.txt', 'r') as file:
    for line in file:
        if line_number == 1:
            rows = int(line.split(':')[1])
        elif line_number == 2:
            cols = int(line.split(':')[1])
            grid = [' '] * rows
            for i in range(0, rows):
                grid[i] = [' '] * cols
        elif line_number == 3:
            grid_size = int(line.split(':')[1])
        else:
            coords = line.strip().split(',')
            print(coords)
            grid[int(coords[0])][int(coords[1])] = 'P'
        line_number = line_number + 1
    file.close()
print(grid)


            
