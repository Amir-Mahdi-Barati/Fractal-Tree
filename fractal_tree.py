import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import random
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import json


class FractalTree:
    def __init__(self, **kwargs):
        """
        Professional Fractal Tree Generator
        """

        # Default parameters
        self.params = {
            'canvas_width': kwargs.get('canvas_width', 1200),
            'canvas_height': kwargs.get('canvas_height', 800),
            'trunk_color': kwargs.get('trunk_color', '#7c2d12'),
            'leaf_colors': kwargs.get('leaf_colors', ['#166534', '#22c55e', '#f59e0b']),
            'bg_color': kwargs.get('bg_color', '#0f172a'),
            'base_length': kwargs.get('base_length', 180),
            'angle_variation': kwargs.get('angle_variation', 35),
            'length_factor': kwargs.get('length_factor', 0.65),
            'max_depth': kwargs.get('max_depth', 8),
            'trunk_thickness': kwargs.get('trunk_thickness', 20),
            'thickness_factor': kwargs.get('thickness_factor', 0.75),
            'randomness': kwargs.get('randomness', 0.1),
            'upward_angle': kwargs.get('upward_angle', True),
            'smooth_lines': kwargs.get('smooth_lines', True),
            'auto_grow': kwargs.get('auto_grow', False),
            'show_grid': kwargs.get('show_grid', False)
        }

        # State variables
        self.click_count = 0
        self.current_depth = 0
        self.branches: List[Dict] = []
        self.next_id = 0
        self.tree_center = (0, 0)

        # Initialize Tkinter
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):

        self.root.title("Fractal Tree Generator - Professional")
        self.root.geometry(f"{self.params['canvas_width']}x{self.params['canvas_height'] + 100}")

        # Main container
        main_container = tk.Frame(self.root, bg='#1e293b')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Control panel
        self.create_control_panel(main_container)

        # Canvas
        self.canvas = tk.Canvas(
            main_container,
            width=self.params['canvas_width'],
            height=self.params['canvas_height'],
            bg=self.params['bg_color'],
            highlightthickness=2,
            highlightbackground='#475569'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Bind events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind('<s>', lambda e: self.save_tree())
        self.root.bind('<S>', lambda e: self.save_tree())
        self.root.bind('<r>', lambda e: self.reset_tree())
        self.root.bind('<R>', lambda e: self.reset_tree())
        self.root.bind('<space>', lambda e: self.grow_one_level())
        self.root.bind('<g>', lambda e: self.toggle_grid())
        self.root.bind('<G>', lambda e: self.toggle_grid())

        # Draw initial guide
        self.draw_guide()

    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = tk.Frame(parent, bg='#1e293b', width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)

        # Title
        title = tk.Label(
            control_frame,
            text="🌳 TREE CONTROLS",
            font=('Segoe UI', 16, 'bold'),
            fg='#22c55e',
            bg='#1e293b'
        )
        title.pack(pady=15)

        # Status display
        self.status_var = tk.StringVar(value="Ready to plant trunk")
        status_label = tk.Label(
            control_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 11),
            fg='#cbd5e1',
            bg='#1e293b'
        )
        status_label.pack(pady=10)

        # Information display
        info_frame = tk.Frame(control_frame, bg='#0f172a', relief=tk.FLAT)
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.info_text = tk.Text(
            info_frame,
            height=10,
            bg='#0f172a',
            fg='#cbd5e1',
            font=('Consolas', 9),
            relief=tk.FLAT,
            borderwidth=0
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.info_text.insert(tk.END, "Tree information will appear here...")
        self.info_text.config(state=tk.DISABLED)

        # Control buttons
        btn_frame = tk.Frame(control_frame, bg='#1e293b')
        btn_frame.pack(fill=tk.X, padx=10, pady=15)

        buttons = [
            ("🌱 Plant Trunk", self.plant_trunk_dialog),
            ("🌿 Grow One Level", self.grow_one_level),
            ("🌳 Grow Full Tree", self.grow_full_tree),
            ("💾 Save Tree", self.save_tree),
            ("🔄 Reset", self.reset_tree),
            ("🎨 Randomize Colors", self.randomize_colors),
            ("⚙️ Settings", self.open_settings)
        ]

        for text, command in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg='#3b82f6',
                fg='white',
                font=('Segoe UI', 10),
                relief=tk.RAISED,
                cursor='hand2',
                padx=10,
                pady=8
            )
            btn.pack(fill=tk.X, pady=3)

    def draw_guide(self):
        """Draw the initial guide on canvas"""
        self.canvas.delete("all")

        guide_text = [
            "FRACTAL TREE GENERATOR",
            "Click on canvas to plant trunk",
            "Continue clicking to grow branches",
            "Each branch splits into two",
            "Press SPACE to grow one level",
            "Press 'G' to toggle grid",
            "Press 'S' to save tree",
            "Press 'R' to reset"
        ]

        y_pos = 100
        for i, line in enumerate(guide_text):
            color = '#22c55e' if i == 0 else '#94a3b8'
            size = 18 if i == 0 else 12

            self.canvas.create_text(
                self.params['canvas_width'] // 2,
                y_pos,
                text=line,
                fill=color,
                font=('Segoe UI', size, 'bold' if i == 0 else 'normal'),
                tags="guide"
            )
            y_pos += 40 if i == 0 else 30

        # Draw coordinate system if grid is enabled
        if self.params['show_grid']:
            self.draw_grid()

    def draw_grid(self):
        """Draw grid lines for reference"""
        width = self.params['canvas_width']
        height = self.params['canvas_height']

        # Vertical lines
        for x in range(0, width, 50):
            self.canvas.create_line(
                x, 0, x, height,
                fill='#334155',
                width=1,
                tags="grid"
            )

        # Horizontal lines
        for y in range(0, height, 50):
            self.canvas.create_line(
                0, y, width, y,
                fill='#334155',
                width=1,
                tags="grid"
            )

        # Center lines
        self.canvas.create_line(
            width // 2, 0, width // 2, height,
            fill='#475569',
            width=2,
            tags="grid"
        )
        self.canvas.create_line(
            0, height // 2, width, height // 2,
            fill='#475569',
            width=2,
            tags="grid"
        )

    def toggle_grid(self):
        """Toggle grid visibility"""
        self.params['show_grid'] = not self.params['show_grid']
        self.canvas.delete("grid")
        if self.params['show_grid']:
            self.draw_grid()

    def on_canvas_click(self, event):
        """Handle canvas click events"""
        if self.click_count == 0:
            self.plant_trunk(event.x, event.y)
        else:
            self.grow_one_level()

        self.click_count += 1
        self.update_display()

    def plant_trunk_dialog(self):
        """Open dialog to plant trunk at specific location"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Plant Trunk")
        dialog.geometry("300x200")
        dialog.configure(bg='#1e293b')

        tk.Label(
            dialog,
            text="Enter coordinates:",
            font=('Segoe UI', 12),
            fg='#cbd5e1',
            bg='#1e293b'
        ).pack(pady=10)

        # X coordinate
        x_frame = tk.Frame(dialog, bg='#1e293b')
        x_frame.pack(pady=5)
        tk.Label(x_frame, text="X:", fg='#cbd5e1', bg='#1e293b').pack(side=tk.LEFT, padx=5)
        x_entry = tk.Entry(x_frame, width=10)
        x_entry.pack(side=tk.LEFT)
        x_entry.insert(0, str(self.params['canvas_width'] // 2))

        # Y coordinate
        y_frame = tk.Frame(dialog, bg='#1e293b')
        y_frame.pack(pady=5)
        tk.Label(y_frame, text="Y:", fg='#cbd5e1', bg='#1e293b').pack(side=tk.LEFT, padx=5)
        y_entry = tk.Entry(y_frame, width=10)
        y_entry.pack(side=tk.LEFT)
        y_entry.insert(0, str(self.params['canvas_height'] - 100))

        def plant():
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                self.plant_trunk(x, y)
                self.click_count = 1
                self.update_display()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")

        tk.Button(
            dialog,
            text="Plant Trunk",
            command=plant,
            bg='#22c55e',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=20)

    def plant_trunk(self, x, y):
        """Plant the trunk at specified coordinates"""
        self.canvas.delete("all")
        self.branches = []
        self.next_id = 0
        self.current_depth = 0
        self.tree_center = (x, y)

        # Calculate trunk direction (upward or downward)
        start_y = y
        if self.params['upward_angle']:
            end_y = y - self.params['base_length']
            base_angle = 270  # Upward
        else:
            end_y = y + self.params['base_length']
            base_angle = 90  # Downward

        # Create trunk
        trunk = {
            'id': self.next_id,
            'parent_id': None,
            'start': (x, start_y),
            'end': (x, end_y),
            'depth': 0,
            'length': self.params['base_length'],
            'angle': base_angle,
            'thickness': self.params['trunk_thickness'],
            'color': self.params['trunk_color']
        }

        self.branches.append(trunk)
        self.next_id += 1

        # Draw trunk
        self.draw_branch(trunk)

        # Draw grid if enabled
        if self.params['show_grid']:
            self.draw_grid()

    def draw_branch(self, branch):
        """Draw a single branch"""
        x1, y1 = branch['start']
        x2, y2 = branch['end']

        line_options = {
            'width': max(1, branch['thickness']),
            'fill': branch['color'],
            'capstyle': tk.ROUND,
            'joinstyle': tk.ROUND
        }

        if self.params['smooth_lines']:
            line_options['smooth'] = True

        self.canvas.create_line(x1, y1, x2, y2, **line_options)

    def get_branch_color(self, depth):
        """Get color for branch based on depth"""
        if depth == 0:
            return self.params['trunk_color']

        # Calculate color gradient
        if depth >= self.params['max_depth']:
            return self.params['leaf_colors'][-1]

        progress = depth / self.params['max_depth']
        color_index = progress * (len(self.params['leaf_colors']) - 1)

        idx1 = int(color_index)
        idx2 = min(idx1 + 1, len(self.params['leaf_colors']) - 1)
        factor = color_index - idx1

        # Interpolate between colors
        color1 = self.params['leaf_colors'][idx1]
        color2 = self.params['leaf_colors'][idx2]

        return self.interpolate_color(color1, color2, factor)

    def interpolate_color(self, color1, color2, factor):
        """Interpolate between two hex colors"""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)

        return f'#{r:02x}{g:02x}{b:02x}'

    def calculate_thickness(self, depth):
        """Calculate branch thickness based on depth"""
        base = self.params['trunk_thickness']
        factor = self.params['thickness_factor']
        return max(1, base * (factor ** depth))

    def grow_one_level(self):
        """Grow one level of branches"""
        if len(self.branches) == 0:
            messagebox.showinfo("Info", "Please plant trunk first!")
            return

        if self.current_depth >= self.params['max_depth']:
            messagebox.showinfo("Info", "Maximum depth reached!")
            return

        new_branches = []
        terminal_branches = [b for b in self.branches if b['depth'] == self.current_depth]

        for parent in terminal_branches:
            px, py = parent['end']

            # Create two child branches
            for angle_offset in [-self.params['angle_variation'], self.params['angle_variation']]:
                # Add randomness
                angle_variation = angle_offset * (1 + (random.random() - 0.5) * self.params['randomness'] * 2)

                new_angle = parent['angle'] + angle_variation
                new_length = parent['length'] * self.params['length_factor']
                new_length *= (1 + (random.random() - 0.5) * self.params['randomness'])

                # Calculate end point
                rad_angle = math.radians(new_angle)
                end_x = px + math.cos(rad_angle) * new_length
                end_y = py + math.sin(rad_angle) * new_length

                # Create new branch
                new_branch = {
                    'id': self.next_id,
                    'parent_id': parent['id'],
                    'start': (px, py),
                    'end': (end_x, end_y),
                    'depth': self.current_depth + 1,
                    'length': new_length,
                    'angle': new_angle,
                    'thickness': self.calculate_thickness(self.current_depth + 1),
                    'color': self.get_branch_color(self.current_depth + 1)
                }

                new_branches.append(new_branch)
                self.next_id += 1

        # Add and draw new branches
        for branch in new_branches:
            self.branches.append(branch)
            self.draw_branch(branch)

        self.current_depth += 1

    def grow_full_tree(self):
        """Grow tree to maximum depth"""
        if len(self.branches) == 0:
            messagebox.showinfo("Info", "Please plant trunk first!")
            return

        while self.current_depth < self.params['max_depth']:
            self.grow_one_level()

    def update_display(self):
        """Update the display with current tree information"""
        # Update status
        if len(self.branches) == 0:
            status = "Ready to plant trunk"
        elif self.current_depth == 0:
            status = "Trunk planted - Click to add branches"
        else:
            status = f"Depth: {self.current_depth} | Branches: {len(self.branches)}"

        self.status_var.set(status)

        # Update info text
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        info = f"""=== TREE INFORMATION ===
Planting Clicks: {self.click_count}
Current Depth: {self.current_depth}/{self.params['max_depth']}
Total Branches: {len(self.branches)}
Tree Center: {self.tree_center}

=== BRANCH DISTRIBUTION ===
"""

        # Branch distribution
        for depth in range(self.current_depth + 1):
            count = len([b for b in self.branches if b['depth'] == depth])
            info += f"Depth {depth}: {count} branches\n"

        info += f"""
=== CURRENT SETTINGS ===
Angle Variation: {self.params['angle_variation']}°
Base Length: {self.params['base_length']}
Length Factor: {self.params['length_factor']}
Max Depth: {self.params['max_depth']}
Randomness: {self.params['randomness']}
Growth Direction: {'Upward' if self.params['upward_angle'] else 'Downward'}
"""

        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)

    def randomize_colors(self):
        """Randomize the color scheme"""
        import colorsys

        # Generate random but harmonious colors
        base_hue = random.random()

        self.params['trunk_color'] = '#8B4513'  # Keep trunk brown

        # Generate leaf colors
        leaf_colors = []
        for i in range(3):
            hue = (base_hue + i * 0.1) % 1.0
            saturation = 0.6 + random.random() * 0.3
            value = 0.5 + random.random() * 0.3

            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'
            leaf_colors.append(hex_color)

        self.params['leaf_colors'] = leaf_colors

        # Redraw tree
        self.redraw_tree()

    def redraw_tree(self):
        """Redraw the entire tree"""
        self.canvas.delete("all")

        for branch in self.branches:
            self.draw_branch(branch)

        if self.params['show_grid']:
            self.draw_grid()

    def reset_tree(self):
        """Reset the tree to initial state"""
        self.click_count = 0
        self.current_depth = 0
        self.branches = []
        self.next_id = 0

        self.draw_guide()
        self.update_display()

    def open_settings(self):
        """Open settings dialog"""
        SettingsDialog(self.root, self.params, self.redraw_tree)

    def save_tree(self):
        """Save the tree image"""
        if len(self.branches) == 0:
            messagebox.showwarning("Warning", "No tree to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ],
            initialfile=f"fractal_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )

        if file_path:
            try:
                from PIL import Image, ImageDraw

                # Create image
                img = Image.new('RGB',
                                (self.params['canvas_width'],
                                 self.params['canvas_height']),
                                self.params['bg_color'])
                draw = ImageDraw.Draw(img)

                # Draw all branches
                for branch in self.branches:
                    x1, y1 = branch['start']
                    x2, y2 = branch['end']

                    color = branch['color'].lstrip('#')
                    rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

                    thickness = max(1, int(branch['thickness']))

                    # Draw line with thickness
                    for i in range(thickness):
                        offset = i - thickness // 2
                        draw.line([(x1 + offset, y1), (x2 + offset, y2)],
                                  fill=rgb, width=1)

                # Save image
                img.save(file_path, quality=95)
                messagebox.showinfo("Success", f"Tree saved to:\n{file_path}")

            except ImportError:
                # Fallback method
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()

                from PIL import ImageGrab
                ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
                messagebox.showinfo("Success", f"Tree saved to:\n{file_path}")

    def run(self):
        """Run the application"""
        self.root.mainloop()


class SettingsDialog:
    """Settings dialog for tree parameters"""

    def __init__(self, parent, params, callback):
        self.params = params
        self.callback = callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Tree Settings")
        self.dialog.geometry("400x600")
        self.dialog.configure(bg='#1e293b')

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.dialog,
            text="Tree Settings",
            font=('Segoe UI', 16, 'bold'),
            fg='#22c55e',
            bg='#1e293b'
        )
        title.pack(pady=15)

        # Create scrollable frame
        canvas = tk.Canvas(self.dialog, bg='#1e293b', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e293b')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Settings widgets
        self.create_setting_widgets(scrollable_frame)

        # Buttons
        button_frame = tk.Frame(self.dialog, bg='#1e293b')
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            button_frame,
            text="Apply",
            command=self.apply_settings,
            bg='#22c55e',
            fg='white',
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg='#ef4444',
            fg='white',
            padx=20,
            pady=10
        ).pack(side=tk.RIGHT, padx=5)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def create_setting_widgets(self, parent):
        settings = [
            ("Base Length", 'base_length', 50, 300, 10),
            ("Angle Variation", 'angle_variation', 15, 60, 5),
            ("Length Factor", 'length_factor', 0.5, 0.9, 0.01),
            ("Max Depth", 'max_depth', 3, 15, 1),
            ("Trunk Thickness", 'trunk_thickness', 5, 40, 1),
            ("Thickness Factor", 'thickness_factor', 0.5, 0.9, 0.01),
            ("Randomness", 'randomness', 0, 0.3, 0.01),
        ]

        self.vars = {}

        for label, key, min_val, max_val, step in settings:
            frame = tk.Frame(parent, bg='#1e293b')
            frame.pack(fill=tk.X, padx=10, pady=8)

            # Label
            tk.Label(
                frame,
                text=label + ":",
                font=('Segoe UI', 10),
                fg='#cbd5e1',
                bg='#1e293b',
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)

            # Value display
            value_label = tk.Label(
                frame,
                text=str(self.params[key]),
                font=('Consolas', 10),
                fg='#22c55e',
                bg='#1e293b',
                width=10
            )
            value_label.pack(side=tk.RIGHT, padx=(10, 0))

            # Scale
            var = tk.DoubleVar(value=self.params[key])
            scale = tk.Scale(
                frame,
                from_=min_val,
                to=max_val,
                variable=var,
                orient=tk.HORIZONTAL,
                length=180,
                bg='#1e293b',
                fg='white',
                highlightthickness=0,
                resolution=step,
                command=lambda v, k=key, l=value_label: self.update_label(l, k, float(v))
            )
            scale.pack(side=tk.RIGHT)

            self.vars[key] = var

        # Checkboxes
        check_frame = tk.Frame(parent, bg='#1e293b')
        check_frame.pack(fill=tk.X, padx=10, pady=20)

        self.upward_var = tk.BooleanVar(value=self.params['upward_angle'])
        upward_check = tk.Checkbutton(
            check_frame,
            text="Upward Growth",
            variable=self.upward_var,
            bg='#1e293b',
            fg='#cbd5e1',
            selectcolor='#1e293b',
            activebackground='#1e293b',
            activeforeground='#cbd5e1'
        )
        upward_check.pack(anchor='w', pady=5)

        self.smooth_var = tk.BooleanVar(value=self.params['smooth_lines'])
        smooth_check = tk.Checkbutton(
            check_frame,
            text="Smooth Lines",
            variable=self.smooth_var,
            bg='#1e293b',
            fg='#cbd5e1',
            selectcolor='#1e293b',
            activebackground='#1e293b',
            activeforeground='#cbd5e1'
        )
        smooth_check.pack(anchor='w', pady=5)

    def update_label(self, label, key, value):
        label.config(text=f"{value:.2f}")

    def apply_settings(self):
        # Update numerical parameters
        for key, var in self.vars.items():
            self.params[key] = var.get()

        # Update boolean parameters
        self.params['upward_angle'] = self.upward_var.get()
        self.params['smooth_lines'] = self.smooth_var.get()

        # Call callback to redraw tree
        self.callback()
        self.dialog.destroy()


# Usage Examples:
def example_1():
    """Basic tree with default parameters"""
    tree = FractalTree()
    tree.run()


def example_2():
    """Custom tree with specific parameters"""
    tree = FractalTree(
        canvas_width=1400,
        canvas_height=900,
        trunk_color='#5C4033',  # Dark brown
        leaf_colors=['#2E8B57', '#3CB371', '#FFA500'],  # Sea green to orange
        bg_color='#1a1a2e',
        base_length=200,
        angle_variation=40,
        length_factor=0.7,
        max_depth=10,
        trunk_thickness=25,
        thickness_factor=0.8,
        randomness=0.15,
        upward_angle=True,
        smooth_lines=True
    )
    tree.run()


def example_3():
    """Winter tree with blue tones"""
    tree = FractalTree(
        trunk_color='#4A3520',
        leaf_colors=['#4682B4', '#87CEEB', '#B0E0E6'],  # Steel blue to powder blue
        bg_color='#2C3E50',
        upward_angle=True
    )
    tree.run()


def example_4():
    """Autumn tree"""
    tree = FractalTree(
        trunk_color='#8B4513',
        leaf_colors=['#FFD700', '#FF8C00', '#FF4500'],  # Gold to orange red
        bg_color='#F5F5DC',  # Beige background
        base_length=220,
        angle_variation=30,
        upward_angle=True
    )
    tree.run()


if __name__ == "__main__":
    # Run with different examples
    print("Fractal Tree Generator - Professional Edition")
    print("=" * 50)
    print("Available examples:")
    print("1. example_1() - Default tree")
    print("2. example_2() - Custom large tree")
    print("3. example_3() - Winter blue tree")
    print("4. example_4() - Autumn tree")
    print()

    # Run default example
    example_1()
