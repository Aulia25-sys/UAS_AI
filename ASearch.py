import heapq
import tkinter as tk
from tkinter import messagebox
import random

# Fungsi heuristik: Manhattan Distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementasi A* Search
def a_star_with_steps(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited = set()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        visited.add(current)
        
        if current == goal:
            # Rekonstruksi jalur
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], visited
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if maze[neighbor[0]][neighbor[1]] == 1 or maze[neighbor[0]][neighbor[1]] == 2:
                    continue  # Tembok atau benteng
                
                tentative_g = g_score[current] + 1
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None, visited

class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Search Maze Solver")
        
        self.rows = 10
        self.cols = 10
        self.cell_size = 40
        self.maze = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)
        
        # Variabel untuk animasi
        self.current_visited = []
        self.current_path = []
        self.animation_running = False
        
        self.create_widgets()
        self.draw_maze()

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        tk.Button(control_frame, text="Start", command=self.run_a_star).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset_maze).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Generate Maze", command=self.generate_random_maze).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Add Tower", command=self.add_tower_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Clear Path", command=self.clear_path).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root,
                               width=self.cols * self.cell_size,
                               height=self.rows * self.cell_size,
                               borderwidth=0,
                               highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.status_label = tk.Label(self.root, text="Click Start to solve maze", bd=1, relief=tk.SUNKEN)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.tower_mode = False

    def handle_click(self, event):
        if self.animation_running:
            return
            
        j = event.x // self.cell_size
        i = event.y // self.cell_size
        if 0 <= i < self.rows and 0 <= j < self.cols:
            if (i, j) == self.start or (i, j) == self.goal:
                return
            if self.tower_mode:
                self.maze[i][j] = 2  # Benteng (tembok permanen)
                self.tower_mode = False
                self.status_label.config(text="Tower placed. Click Start to solve maze.")
            else:
                self.maze[i][j] = 1 - self.maze[i][j]  # Toggle wall
            self.draw_maze()

    def add_tower_mode(self):
        if self.animation_running:
            return
        self.tower_mode = True
        self.status_label.config(text="Click on the grid to place a tower (red wall).")

    def generate_random_maze(self):
        if self.animation_running:
            return
        self.maze = [[1 if random.random() < 0.3 else 0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.goal[0]][self.goal[1]] = 0
        self.clear_path()
        self.draw_maze()

    def reset_maze(self):
        if self.animation_running:
            return
        self.maze = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.clear_path()
        self.draw_maze()

    def clear_path(self):
        self.current_visited = []
        self.current_path = []
        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        
        # Gambar grid
        for i in range(self.rows + 1):
            self.canvas.create_line(0, i * self.cell_size, self.cols * self.cell_size, i * self.cell_size, fill="gray")
        for j in range(self.cols + 1):
            self.canvas.create_line(j * self.cell_size, 0, j * self.cell_size, self.rows * self.cell_size, fill="gray")
        
        # Gambar sel maze
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                if self.maze[i][j] == 1:
                    color = 'black'  # Tembok biasa
                elif self.maze[i][j] == 2:
                    color = 'red'    # Benteng (tembok permanen)
                else:
                    color = 'white'  # Ruang kosong
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        
        # Gambar sel yang dikunjungi (explored nodes)
        for (x, y) in self.current_visited:
            if (x, y) not in self.current_path:  # Jangan timpa jalur solusi
                self.canvas.create_rectangle(y*self.cell_size+2, x*self.cell_size+2,
                                           y*self.cell_size+self.cell_size-2,
                                           x*self.cell_size+self.cell_size-2,
                                           fill='lightblue', outline='blue')
        
        # Gambar jalur solusi (lebih menonjol)
        for (x, y) in self.current_path:
            self.canvas.create_rectangle(y*self.cell_size+2, x*self.cell_size+2,
                                       y*self.cell_size+self.cell_size-2,
                                       x*self.cell_size+self.cell_size-2,
                                       fill='lightgreen', outline='green', width=2)

        # Gambar titik awal dan tujuan
        sx, sy = self.start
        gx, gy = self.goal
        self.canvas.create_oval(sy*self.cell_size+5, sx*self.cell_size+5, 
                               sy*self.cell_size+35, sx*self.cell_size+35, 
                               fill='blue', outline='darkblue', width=2)
        self.canvas.create_oval(gy*self.cell_size+5, gx*self.cell_size+5, 
                               gy*self.cell_size+35, gx*self.cell_size+35, 
                               fill='orange', outline='darkorange', width=2)

    def run_a_star(self):
        if self.animation_running:
            return
            
        self.clear_path()
        path, visited = a_star_with_steps(self.maze, self.start, self.goal)
        
        if path:
            self.status_label.config(text=f"Solving... Found path with {len(path)} steps, explored {len(visited)} nodes.")
            self.animate_search(path, visited)
        else:
            self.status_label.config(text="No path found.")
            messagebox.showinfo("Result", "No path found from start to goal.")

    def animate_search(self, final_path, visited_nodes):
        self.animation_running = True
        visited_list = list(visited_nodes)
        
        def animate_visited(index=0):
            if index < len(visited_list):
                self.current_visited.append(visited_list[index])
                self.draw_maze()
                self.root.after(50, lambda: animate_visited(index + 1))  # 50ms delay
            else:
                # Setelah selesai menampilkan visited nodes, tampilkan jalur solusi
                self.root.after(500, lambda: animate_path(0))  # Pause 500ms sebelum menampilkan jalur
        
        def animate_path(index=0):
            if index < len(final_path):
                self.current_path.append(final_path[index])
                self.draw_maze()
                self.root.after(100, lambda: animate_path(index + 1))  # 100ms delay untuk path
            else:
                # Animasi selesai
                self.animation_running = False
                self.status_label.config(text=f"Path found! {len(final_path)} steps, {len(visited_nodes)} nodes explored. Click Clear Path to reset.")
        
        # Mulai animasi
        animate_visited()

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGUI(root)
    root.mainloop()