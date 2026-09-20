#!/usr/bin/env python3
import json
import os
import random

# Game config
SVG_WIDTH = 860
SVG_HEIGHT = 280
CELL_SIZE = 12
CELL_SPACING = 3
GRID_X = 40
GRID_Y = 50
COLS = 52
ROWS = 7

# Color palette
BG_COLOR = "#0d1117"
EMPTY_CELL = "#161b22"
LEVEL_1 = "#064e3b"
LEVEL_2 = "#047857"
LEVEL_3 = "#10b981"
LEVEL_4 = "#22c55e"

TARGET_COLORS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4]

def get_grid():
    # Randomly generate grid
    grid = []
    for c in range(COLS):
        col = []
        for r in range(ROWS):
            val = random.choices([0, 1, 2, 3, 4], weights=[0.6, 0.2, 0.1, 0.05, 0.05])[0]
            col.append(val)
        grid.append(col)
    return grid

def generate_svg():
    grid = get_grid()
    
    # We will pick 5 targets for the game loop
    targets = [
        {"c": 8, "r": 5, "t_start": 0},
        {"c": 22, "r": 2, "t_start": 4},
        {"c": 35, "r": 4, "t_start": 8},
        {"c": 15, "r": 1, "t_start": 12},
        {"c": 45, "r": 6, "t_start": 16},
    ]
    
    # Force targets to be active in the grid
    for t in targets:
        grid[t["c"]][t["r"]] = 4
        
    CYCLE_DUR = 20
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" width="{SVG_WIDTH}" height="{SVG_HEIGHT}">
    <defs>
        <!-- Gradients and Filters -->
        <linearGradient id="rocketBody" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#48CAE4" />
            <stop offset="100%" stop-color="#0077B6" />
        </linearGradient>
        <linearGradient id="rocketWindow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#CAF0F8" />
            <stop offset="100%" stop-color="#90E0EF" />
        </linearGradient>
        <linearGradient id="laserGrad" x1="0%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stop-color="#00f2fe" stop-opacity="0" />
            <stop offset="50%" stop-color="#4facfe" stop-opacity="1" />
            <stop offset="100%" stop-color="#ffffff" stop-opacity="1" />
        </linearGradient>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feComponentTransfer in="blur" result="enhancedGlow">
                <feFuncA type="linear" slope="1.5" />
            </feComponentTransfer>
            <feMerge>
                <feMergeNode in="enhancedGlow" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        <filter id="superGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="8" result="blur1" />
            <feGaussianBlur stdDeviation="3" result="blur2" />
            <feMerge>
                <feMergeNode in="blur1" />
                <feMergeNode in="blur2" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        <filter id="engineGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
    </defs>

    <!-- Background -->
    <rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="{BG_COLOR}" rx="10" />
    
    <!-- Cinematic Stars Background -->
    <g fill="#ffffff" filter="url(#glow)">
        <circle cx="120" cy="40" r="1.5"><animate attributeName="opacity" values="0.2; 1; 0.2" dur="3s" repeatCount="indefinite"/></circle>
        <circle cx="280" cy="180" r="1"><animate attributeName="opacity" values="0.1; 0.8; 0.1" dur="4s" repeatCount="indefinite" begin="1s"/></circle>
        <circle cx="450" cy="30" r="2"><animate attributeName="opacity" values="0.3; 1; 0.3" dur="2.5s" repeatCount="indefinite" begin="0.5s"/></circle>
        <circle cx="680" cy="220" r="1.5"><animate attributeName="opacity" values="0.2; 0.9; 0.2" dur="3.5s" repeatCount="indefinite" begin="2s"/></circle>
        <circle cx="790" cy="90" r="2"><animate attributeName="opacity" values="0.1; 1; 0.1" dur="5s" repeatCount="indefinite" begin="1.5s"/></circle>
        <circle cx="180" cy="240" r="1"><animate attributeName="opacity" values="0.4; 1; 0.4" dur="2s" repeatCount="indefinite"/></circle>
        <circle cx="550" cy="160" r="1.5"><animate attributeName="opacity" values="0.2; 0.7; 0.2" dur="4s" repeatCount="indefinite" begin="0.8s"/></circle>
    </g>

    <!-- HUD -->
    <g font-family="Consolas, monospace" font-size="12" fill="#8b949e">
        <text x="25" y="30" font-weight="bold" fill="#00f2fe" filter="url(#glow)">MISSION: ACTIVE</text>
        <text x="200" y="30" fill="#ffffff">DAVID SANCHEZ</text>
        <text x="350" y="30">BUILD • LEARN • INNOVATE</text>
        <text x="560" y="30">CLOUD • DATA ENGINEERING • ML &amp; GEN-AI</text>
        
        <text x="25" y="{SVG_HEIGHT - 20}" font-size="11" fill="#4facfe">&lt;/&gt; TURNING IDEAS INTO INTELLIGENT SOFTWARE &lt;/&gt;</text>
        <text x="{SVG_WIDTH - 200}" y="{SVG_HEIGHT - 20}" font-size="11">TARGETS ELIMINATED: 5</text>
    </g>

    <!-- Contribution Grid -->
    <g transform="translate({GRID_X}, {GRID_Y})">
'''
    # Render grid cells
    for c in range(COLS):
        for r in range(ROWS):
            val = grid[c][r]
            color = EMPTY_CELL
            if val == 1: color = LEVEL_1
            elif val == 2: color = LEVEL_2
            elif val == 3: color = LEVEL_3
            elif val == 4: color = LEVEL_4
            
            x = c * (CELL_SIZE + CELL_SPACING)
            y = r * (CELL_SIZE + CELL_SPACING)
            
            is_target = False
            for i, t in enumerate(targets):
                if t["c"] == c and t["r"] == r:
                    is_target = True
                    target_idx = i
                    break
            
            if is_target:
                t_start = targets[target_idx]["t_start"]
                # Pacing: 
                # Move: 0 to 1.0s
                # Aim: 1.0s to 1.5s
                # Fire & Travel: 1.5s to 1.7s
                # Impact: 1.7s
                t_hit = t_start + 1.7
                
                svg += f'''
                <!-- Target Cell Glow -->
                <rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{color}">
                    <animate attributeName="fill" values="{color}; #ffffff; {LEVEL_4}; {color}" begin="{t_start + 1.0}s" dur="0.7s" />
                    <animate attributeName="fill" values="{color}; {EMPTY_CELL}" begin="{t_hit}s" dur="0.1s" fill="freeze" />
                </rect>
                
                <!-- Explosion Particles -->
                <g transform="translate({x + CELL_SIZE/2}, {y + CELL_SIZE/2})">
                    <!-- Core Flash -->
                    <circle cx="0" cy="0" r="0" fill="#ffffff" filter="url(#superGlow)">
                        <animate attributeName="r" values="0; 10; 25; 30" keyTimes="0; 0.1; 0.7; 1" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                        <animate attributeName="opacity" values="1; 1; 0; 0" keyTimes="0; 0.1; 0.8; 1" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                    </circle>
                    <!-- Energy Wave -->
                    <circle cx="0" cy="0" r="0" fill="none" stroke="#00f2fe" stroke-width="2" filter="url(#glow)">
                        <animate attributeName="r" values="5; 30; 40" keyTimes="0; 0.5; 1" begin="{t_hit}s" dur="0.5s" repeatCount="indefinite" />
                        <animate attributeName="opacity" values="1; 0; 0" keyTimes="0; 0.6; 1" begin="{t_hit}s" dur="0.5s" repeatCount="indefinite" />
                    </circle>
                    <!-- Debris -->
                    <circle cx="0" cy="0" r="1.5" fill="#22c55e" filter="url(#glow)">
                        <animateTransform attributeName="transform" type="translate" values="0,0; -15,-15" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                        <animate attributeName="opacity" values="1; 0" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="0" cy="0" r="1.5" fill="#4facfe" filter="url(#glow)">
                        <animateTransform attributeName="transform" type="translate" values="0,0; 15,-10" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                        <animate attributeName="opacity" values="1; 0" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="0" cy="0" r="2" fill="#10b981" filter="url(#glow)">
                        <animateTransform attributeName="transform" type="translate" values="0,0; -5,20" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                        <animate attributeName="opacity" values="1; 0" begin="{t_hit}s" dur="0.4s" repeatCount="indefinite" />
                    </circle>
                </g>
                '''
            else:
                svg += f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{color}" />\n'
                
    svg += '</g>\n'
    
    # ------------------
    # ROCKET MOVEMENT
    # ------------------
    rocket_y = GRID_Y + ROWS * (CELL_SIZE + CELL_SPACING) + 40 # Cinematic spacing
    
    svg += f'''
    <!-- Rocket Group -->
    <g transform="translate(0, {rocket_y})">
        <!-- X Movement -->
        <g>
    '''
    
    for i in range(len(targets)):
        t_curr = targets[i]
        t_next = targets[(i+1)%len(targets)]
        
        x_curr = GRID_X + t_curr["c"] * (CELL_SIZE + CELL_SPACING) + CELL_SIZE/2
        x_next = GRID_X + t_next["c"] * (CELL_SIZE + CELL_SPACING) + CELL_SIZE/2
        
        t_start_move = t_curr["t_start"] + 2.5 # Wait after explosion
        dur_move = 1.0 # Smooth rapid move
        
        # Pacing constraint check
        actual_dur = dur_move
        if i == len(targets) - 1:
            t_start_move = t_curr["t_start"] + 2.5
            actual_dur = CYCLE_DUR - t_start_move + 1.0
        
        # Rocket translate
        svg += f'''
            <animateTransform attributeName="transform" type="translate" 
                values="{x_curr},0; {x_next},0" 
                begin="{t_start_move}s" dur="{dur_move}s" 
                repeatCount="indefinite" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1" />
        '''
        
    x_first = GRID_X + targets[0]["c"] * (CELL_SIZE + CELL_SPACING) + CELL_SIZE/2
    svg += f'''
            <animateTransform attributeName="transform" type="translate"
                values="{x_first},0; {x_first},0"
                begin="0s" dur="1.0s"
                repeatCount="indefinite" fill="freeze" />
    '''

    svg += '''
            <!-- The Rocket Shape & Banking -->
            <g transform="translate(-12, -18)">
                
                <!-- Engine Exhaust -->
                <path d="M7,28 L17,28 L12,42 Z" fill="#00f2fe" filter="url(#engineGlow)">
                    <animate attributeName="d" values="M7,28 L17,28 L12,42 Z; M8,28 L16,28 L12,38 Z; M7,28 L17,28 L12,45 Z; M7,28 L17,28 L12,42 Z" dur="0.15s" repeatCount="indefinite" />
                    <animate attributeName="fill" values="#00f2fe; #ffffff; #00f2fe" dur="0.3s" repeatCount="indefinite" />
                </path>
                
                <!-- Rocket Chassis -->
                <path d="M12,0 L20,12 L18,28 L6,28 L4,12 Z" fill="url(#rocketBody)" filter="url(#engineGlow)" />
                <!-- Cockpit -->
                <ellipse cx="12" cy="14" rx="4" ry="6" fill="url(#rocketWindow)" />
                <!-- Wings -->
                <path d="M6,16 L-2,30 L6,26 Z" fill="#0077B6" />
                <path d="M18,16 L26,30 L18,26 Z" fill="#0077B6" />
                
                <!-- Subtle Bobbing -->
                <animateTransform attributeName="transform" type="translate" values="-12,-18; -12,-22; -12,-18" dur="3s" repeatCount="indefinite" />
            </g>
        </g>
    </g>
    '''
    
    # ------------------
    # PROJECTILES
    # ------------------
    for i, t in enumerate(targets):
        c_x = GRID_X + t["c"] * (CELL_SIZE + CELL_SPACING) + CELL_SIZE/2
        c_y = GRID_Y + t["r"] * (CELL_SIZE + CELL_SPACING) + CELL_SIZE/2
        
        t_fire = t["t_start"] + 1.5
        dur_fly = 0.2
        
        p_start_y = rocket_y - 20
        p_end_y = c_y
        
        svg += f'''
        <!-- Laser Projectile {i} -->
        <rect x="{c_x - 1.5}" y="{p_start_y}" width="3" height="15" rx="1.5" fill="url(#laserGrad)" filter="url(#superGlow)" opacity="0">
            <animate attributeName="opacity" values="0; 1; 1; 0" keyTimes="0; 0.1; 0.9; 1" begin="{t_fire}s" dur="{dur_fly}s" repeatCount="indefinite" />
            <animate attributeName="y" values="{p_start_y}; {p_end_y}" begin="{t_fire}s" dur="{dur_fly}s" repeatCount="indefinite" calcMode="linear" />
        </rect>
        '''
        
    svg += '</svg>'
    
    # Write to file
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svgs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "rocket-shooting-game.svg")
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_svg()
