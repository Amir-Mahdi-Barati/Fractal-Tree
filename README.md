# 🌳 Fractal Tree Generator 
<img src="https://github.com/Amir-Mahdi-Barati/Fractal-Tree/blob/main/fractal_tree_img.png" 
     alt="Fractal Tree Generator" 
     width="400" 
     height="400" />
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Status](https://img.shields.io/badge/Status-Active-success)


## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Amir-Mahdi-Barati/Fractal-Tree.git
cd Fractal-Tree
```
```bash
python fractal_tree.py
```
    

**⚙️ Parameters**
Tree Structure Parameters
Parameter	Description	Default	Range
Base Length	Initial trunk length	180	50-300
Angle Variation	Branch splitting angle	35°	15-60°
Length Factor	Length reduction per level	0.65	0.5-0.9
Max Depth	Maximum recursion depth	8	3-15
Trunk Thickness	Starting branch thickness	20	5-40
Visual Parameters
Parameter	Description	Default	Range
Thickness Factor	Thickness reduction per level	0.75	0.5-0.9
Randomness	Natural variation in branches	0.1	0-0.3
Upward Growth	Tree direction	True	True/False
Smooth Lines	Anti-aliased drawing	True	True/False
**🎨 Examples**
Winter Theme
```python
tree = FractalTree(
    trunk_color='#4A3520',
    leaf_colors=['#4682B4', '#87CEEB', '#B0E0E6'],
    bg_color='#2C3E50'
)
Autumn Theme

tree = FractalTree(
    trunk_color='#8B4513',
    leaf_colors=['#FFD700', '#FF8C00', '#FF4500'],
    bg_color='#F5F5DC'
)
Custom Large Tree

tree = FractalTree(
    canvas_width=1400,
    canvas_height=900,
    base_length=200,
    max_depth=10,
    trunk_thickness=25
)
```
**🏗️ Project Structure**
```
fractal_tree.py
├── FractalTree Class
│   ├── UI Setup (setup_ui, create_control_panel)
│   ├── Drawing Functions (draw_branch, draw_grid)
│   ├── Tree Logic (plant_trunk, grow_one_level)
│   ├── Color System (get_branch_color, interpolate_color)
│   └── Utilities (save_tree, redraw_tree)
├── SettingsDialog Class
│   ├── Parameter controls
│   └── Live preview updates
└── Example Functions
    ├── example_1() - Default tree
    ├── example_2() - Custom large tree
    ├── example_3() - Winter tree
    └── example_4() - Autumn tree
```
**Algorithm**
The tree generation uses a recursive fractal algorithm:

Start with a trunk (depth 0)

For each branch at current depth:

Create two child branches

Calculate new angles: parent_angle ± angle_variation

Reduce length: new_length = parent_length × length_factor

Reduce thickness: new_thickness = parent_thickness × thickness_factor

Apply randomness for natural variation

Repeat until max_depth reached



**🤝 Contributing**
Contributions are welcome! Here's how to contribute:

Fork the repository

Create a feature branch ```(git checkout -b feature/AmazingFeature)```

Commit your changes ```(git commit -m 'Add some AmazingFeature')```

Push to the branch ```(git push origin feature/AmazingFeature)```

Open a Pull Request

Future Improvements
Continuous growth animation

Different branching patterns (binary, ternary, etc.)

Multiple trees in one canvas

Seasonal effects (leaves, flowers, snow)

SVG export support

Day/Night mode toggle

Wind animation effect

3D visualization mode
