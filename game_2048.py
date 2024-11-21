import tkinter as tk
import random
import colors

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('2048游戏')
        self.grid_cells = []
        self.matrix = [[0] * 4 for _ in range(4)]
        self.score = 0
        
        # 添加重新开始按钮
        self.restart_button = tk.Button(
            self.window,
            text='重新开始',
            command=self.restart_game,
            font=('Arial', 12, 'bold')
        )
        self.restart_button.grid(row=0, column=0, pady=10)
        
        # 添加分数显示
        self.score_label = tk.Label(
            self.window,
            text=f'分数: {self.score}',
            font=('Arial', 12, 'bold')
        )
        self.score_label.grid(row=0, column=1, pady=10)
        
        self.init_grid()
        self.init_matrix()
        
        # 绑定按键事件
        self.window.bind('<Left>', self.left)
        self.window.bind('<Right>', self.right)
        self.window.bind('<Up>', self.up)
        self.window.bind('<Down>', self.down)
        
    def init_grid(self):
        background = tk.Frame(self.window, bg=colors.GRID_COLOR)
        background.grid()
        
        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(
                    background,
                    bg=colors.EMPTY_CELL_COLOR,
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(
                    cell,
                    bg=colors.EMPTY_CELL_COLOR,
                    font=('Arial', 30, 'bold')
                )
                cell_number.place(relx=0.5, rely=0.5, anchor='center')
                grid_row.append(cell_number)
            self.grid_cells.append(grid_row)
            
    def init_matrix(self):
        # 初始时随机放置两个数字
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()
        
    def add_new_tile(self):
        # 在空位置随机添加一个新数字(2或4)
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = random.choice([2, 4])
            
    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.matrix[i][j]
                if value == 0:
                    self.grid_cells[i][j].configure(
                        text='',
                        bg=colors.EMPTY_CELL_COLOR
                    )
                else:
                    self.grid_cells[i][j].configure(
                        text=str(value),
                        bg=colors.CELL_COLORS.get(value),
                        fg=colors.CELL_NUMBER_COLORS.get(value)
                    )
        # 更新分数显示
        self.score_label.config(text=f'分数: {self.score}')
        self.window.update_idletasks()
        
    def compress(self, matrix):
        # 压缩非零数字
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if matrix[i][j] != 0:
                    new_matrix[i][pos] = matrix[i][j]
                    pos += 1
        return new_matrix
    
    def merge(self, matrix):
        # 合并相同的数字
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                    matrix[i][j] *= 2
                    matrix[i][j + 1] = 0
                    self.score += matrix[i][j]
        return matrix
    
    def reverse(self, matrix):
        # 矩阵反转
        return [row[::-1] for row in matrix]
    
    def transpose(self, matrix):
        # 矩阵转置
        return [[matrix[j][i] for j in range(4)] for i in range(4)]
    
    def left(self, event):
        # 向左移动
        self.matrix = self.compress(self.matrix)
        self.matrix = self.merge(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.add_new_tile()
        self.update_grid()
        self.game_over()
        
    def right(self, event):
        # 向右移动
        self.matrix = self.reverse(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.matrix = self.merge(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.matrix = self.reverse(self.matrix)
        self.add_new_tile()
        self.update_grid()
        self.game_over()
        
    def up(self, event):
        # 向上移动
        self.matrix = self.transpose(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.matrix = self.merge(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.matrix = self.transpose(self.matrix)
        self.add_new_tile()
        self.update_grid()
        self.game_over()
        
    def down(self, event):
        # 向下移动
        self.matrix = self.transpose(self.matrix)
        self.matrix = self.reverse(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.matrix = self.merge(self.matrix)
        self.matrix = self.compress(self.matrix)
        self.matrix = self.reverse(self.matrix)
        self.matrix = self.transpose(self.matrix)
        self.add_new_tile()
        self.update_grid()
        self.game_over()
        
    def game_over(self):
        # 检查游戏是否结束
        if any(0 in row for row in self.matrix):
            return

        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return
                
        for j in range(4):
            for i in range(3):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return
                
        # 如果没有可移动的方向，游戏结束
        game_over = tk.Toplevel()
        game_over.title('游戏结束')
        tk.Label(
            game_over,
            text=f'游戏结束!\n您的得分是: {self.score}',
            font=('Arial', 20)
        ).pack()
        
    def start(self):
        self.window.mainloop()

    # 添加重新开始游戏的方法
    def restart_game(self):
        # 重置分数
        self.score = 0
        self.score_label.config(text=f'分数: {self.score}')
        
        # 重置矩阵
        self.matrix = [[0] * 4 for _ in range(4)]
        
        # 重新初始化游戏
        self.init_matrix()
        self.update_grid()

if __name__ == '__main__':
    game = Game2048()
    game.start() 
