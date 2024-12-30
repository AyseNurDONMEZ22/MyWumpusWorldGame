import tkinter as tk
import random

class WumpusGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wumpus Dünyası")

        # Ayarlar
        self.grid_size = 4
        self.cell_size = 100
        self.world = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player_position = (3, 0)
        self.performance = 0
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed[3][0] = True

        # Bileşenler
        self.wumpus_position = self.place_randomly()
        self.pits = [self.place_randomly() for _ in range(3)]
        self.gold_position = self.place_randomly(exclude=[self.wumpus_position] + self.pits)

        # İşaretler
        self.signs = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generate_signs()

        # Canvas oluştur
        self.canvas = tk.Canvas(master, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
        self.canvas.pack()

        # Kontroller
        self.create_controls()

        # İlk çizim
        self.draw_world()

    def place_randomly(self, exclude=[]):
        while True:
            position = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if position not in exclude and position != self.player_position:
                return position

    def generate_signs(self):
        for pit in self.pits:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x, y = pit[0] + dx, pit[1] + dy
                if 0 <= x < self.grid_size and 0 <= y < self.grid_size and (x, y) != self.gold_position:
                    self.signs[x][y] += "R"  # Rüzgar

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = self.wumpus_position[0] + dx, self.wumpus_position[1] + dy
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size and (x, y) != self.gold_position:
                self.signs[x][y] += "K"  # Koku

    def create_controls(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack()

        tk.Button(control_frame, text="Yukarı", command=lambda: self.move_player("UP")).grid(row=0, column=1)
        tk.Button(control_frame, text="Sol", command=lambda: self.move_player("LEFT")).grid(row=1, column=0)
        tk.Button(control_frame, text="Sağ", command=lambda: self.move_player("RIGHT")).grid(row=1, column=2)
        tk.Button(control_frame, text="Aşağı", command=lambda: self.move_player("DOWN")).grid(row=2, column=1)

    def draw_world(self):
        self.canvas.delete("all")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if self.revealed[i][j]:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

                    # İşaretler
                    if "R" in self.signs[i][j]:
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 10, text="~", fill="blue")
                    if "K" in self.signs[i][j]:
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 10, text="*", fill="green")

                    # Wumpus, çukur veya altın
                    if (i, j) == self.wumpus_position:
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="W", fill="red", font=("Helvetica", 16))
                    elif (i, j) in self.pits:
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="O", fill="black", font=("Helvetica", 16))
                    elif (i, j) == self.gold_position:
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="$", fill="gold", font=("Helvetica", 16))
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="gray")

        # Oyuncu çizimi
        px, py = self.player_position
        x1, y1 = py * self.cell_size, px * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        self.canvas.create_rectangle(x1 + 30, y1 + 30, x2 - 30, y2 - 30, outline="blue", width=3)

        # Performans gösterimi
        self.canvas.create_text(self.grid_size * self.cell_size / 2, 20, text=f"Puan: {self.performance}", fill="black", font=("Helvetica", 16))

    def move_player(self, direction):
        print(f"Hamle: {direction}")
        print(f"Mevcut Pozisyon: {self.player_position}")
        x, y = self.player_position

        if direction == "UP" and x > 0:
            self.player_position = (x - 1, y)
        elif direction == "DOWN" and x < self.grid_size - 1:
            self.player_position = (x + 1, y)
        elif direction == "LEFT" and y > 0:
            self.player_position = (x, y - 1)
        elif direction == "RIGHT" and y < self.grid_size - 1:
            self.player_position = (x, y + 1)

        print(f"Yeni Pozisyon: {self.player_position}")
        self.performance -= 1
        self.revealed[self.player_position[0]][self.player_position[1]] = True
        self.check_position()
        self.draw_world()

    def check_position(self):
        x, y = self.player_position

        if (x, y) in self.pits:
            self.performance -= 100
            self.display_message("Çukura düştünüz. Kaybettiniz!")
        elif (x, y) == self.wumpus_position:
            self.performance -= 100
            self.display_message("Wumpus tarafından yakalandınız. Kaybettiniz!")
        elif (x, y) == self.gold_position:
            self.performance += 100
            self.display_message("Altını buldunuz. Kazandınız!")

    def display_message(self, message):
        self.canvas.create_text(self.grid_size * self.cell_size / 2, self.grid_size * self.cell_size / 2, text=message, fill="red", font=("Helvetica", 16))
        self.master.after(3000, self.reset_game)

    def reset_game(self):
        self.player_position = (3, 0)
        self.performance = 0
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed[3][0] = True
        self.wumpus_position = self.place_randomly()
        self.pits = [self.place_randomly() for _ in range(3)]
        self.gold_position = self.place_randomly(exclude=[self.wumpus_position] + self.pits)
        self.signs = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generate_signs()
        self.draw_world()

# Oyun başlat
root = tk.Tk()
game = WumpusGame(root)
root.mainloop()
