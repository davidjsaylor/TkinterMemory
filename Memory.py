import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Memory Game')
        
        # Canvas setup
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.grid(row=1, column=1)
        
        # Initial screen with title and logo
        self.title_text = self.canvas.create_text(400, 350, text='Memory', fill='red', font=('Arial', 44, 'bold'))
        self.logo_text = self.canvas.create_text(400, 400, text='How quick are you?', fill='black', font=('Arial', 24))

        # Toolbar with game control buttons
        toolbar = tk.Frame(root)
        toolbar.grid(row=2, column=1, sticky='WE')
        toolbar.rowconfigure(1, weight=1)
        toolbar.columnconfigure(2, weight=1)
        tk.Button(toolbar, text='Start New Game', command=self.start_game, width=15).grid(row=1, column=1)
        self.timer_label = tk.Label(toolbar, text='00:00')
        self.timer_label.grid(row=1, column=2)
        tk.Button(toolbar, text='Exit', command=root.quit, width=15).grid(row=1, column=3)
        
        # Game state initialization
        self.tiles = {}
        self.selected = []
        self.game_active = False
        self.completed_text = None

    def start_game(self):
        if self.game_active and self.completed_text:
            self.canvas.delete(self.completed_text)
        self.game_active = True
        self.canvas.delete(self.title_text)
        self.canvas.delete(self.logo_text)
        self.setup_game()
        self.start_timer()

    def setup_game(self):
        self.colors = ['red', 'red', 'blue', 'blue', 'green', 'green', 'yellow', 'yellow',
                       'purple', 'purple', 'orange', 'orange', 'gray', 'gray', 'cyan', 'cyan']
        random.shuffle(self.colors)
        self.draw_tiles()

    def draw_tiles(self):
        for i in range(16):
            row = i // 4
            col = i % 4
            x1 = col * 200
            y1 = row * 200
            x2 = x1 + 200
            y2 = y1 + 200
            tile = self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightgrey', tags='rect')
            self.tiles[tile] = (self.colors[i], False)  # Color, matched state
            self.canvas.tag_bind(tile, '<Button-1>', lambda event, t=tile: self.on_tile_click(t))

    def on_tile_click(self, tile):
        if not self.game_active:
            return
        if self.tiles[tile][1]:  # If already matched, ignore
            return
        if tile in self.selected:
            return  # Already selected
        color = self.tiles[tile][0]
        self.canvas.itemconfig(tile, fill=color)
        self.selected.append(tile)

        if len(self.selected) == 2:
            if self.tiles[self.selected[0]][0] == self.tiles[self.selected[1]][0]:
                self.tiles[self.selected[0]] = (self.tiles[self.selected[0]][0], True)
                self.tiles[self.selected[1]] = (self.tiles[self.selected[1]][0], True)
                self.selected.clear()
                if all(matched for color, matched in self.tiles.values()):
                    self.game_active = False
                    self.show_completed_message()
            else:
                self.root.after(500, self.hide_tiles)

    def hide_tiles(self):
        for tile in self.selected:
            self.canvas.itemconfig(tile, fill='lightgrey')
        self.selected.clear()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        self.timer_label.config(text=f'{minutes:02}:{seconds:02}')
        self.root.after(1000, self.update_timer)

    def show_completed_message(self):
        self.timer_running = False
        self.completed_text = self.canvas.create_text(400, 400, text='Completed!', fill='black', font=('Arial', 44, 'bold'))

def main():
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
