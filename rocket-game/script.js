// script.js – Playable Rocket Shooting Game
// Visual style matches the animated SVG: dark space background, neon green grid, cyan/blue rocket.

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas to fill the viewport while keeping a 16:9 ratio
function resizeCanvas() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const ratio = 16 / 9;
  if (w / h > ratio) {
    canvas.height = h;
    canvas.width = h * ratio;
  } else {
    canvas.width = w;
    canvas.height = w / ratio;
  }
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Game constants
const GRID_ROWS = 7;
const GRID_COLS = 20; // reasonable width for the canvas
const CELL_SIZE = 20;
const CELL_GAP = 4;
const GRID_X = (canvas.width - (GRID_COLS * (CELL_SIZE + CELL_GAP) - CELL_GAP)) / 2;
const GRID_Y = 50;

const PLAYER_WIDTH = 30;
const PLAYER_HEIGHT = 50;
const PLAYER_SPEED = 6;
const BULLET_SPEED = 8;
const BULLET_WIDTH = 3;
const BULLET_HEIGHT = 15;

// Colors
const BG_COLOR = '#0d1117';
const GRID_EMPTY = '#161b22';
const GRID_LEVELS = ['#064e3b', '#047857', '#10b981', '#22c55e'];
const ROCKET_BODY = 'url(#rocketBody)'; // will use gradient via CSS
const ROCKET_COLOR = '#48CAE4';
const BULLET_GRAD = 'linear-gradient(to top, #00f2fe 0%, #4facfe 50%, #ffffff 100%)';

// Game state
let player = { x: canvas.width / 2, y: canvas.height - 80, width: PLAYER_WIDTH, height: PLAYER_HEIGHT };
let bullets = [];
let enemies = [];
let particles = [];
let score = 0;
let lives = 3;
let gameRunning = false;
let keys = {};
let overlay = document.getElementById('overlay');
let startBtn = document.getElementById('startBtn');

// Utility functions
function rectCollision(a, b) {
  return a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
}

function createEnemies() {
  enemies = [];
  for (let c = 0; c < GRID_COLS; c++) {
    for (let r = 0; r < GRID_ROWS; r++) {
      // Randomly assign a contribution level (0‑4)
      const level = Math.floor(Math.random() * 5); // 0 empty, 1‑4 shades of green
      enemies.push({
        col: c,
        row: r,
        x: GRID_X + c * (CELL_SIZE + CELL_GAP),
        y: GRID_Y + r * (CELL_SIZE + CELL_GAP),
        width: CELL_SIZE,
        height: CELL_SIZE,
        level,
        hp: level, // hp equals level for simplicity
        alive: level > 0
      });
    }
  }
}

function resetGame() {
  player.x = canvas.width / 2;
  bullets = [];
  particles = [];
  score = 0;
  lives = 3;
  createEnemies();
  overlay.style.display = 'flex';
  overlay.innerHTML = `<h1>🚀 DAVID SANCHEZ</h1><p>BUILD • LEARN • INNOVATE</p><p>CLOUD • DATA ENGINEERING • ML &amp; GEN-AI</p><button id="startBtn">START MISSION</button>`;
  document.getElementById('startBtn').addEventListener('click', startGame);
  gameRunning = false;
}

function startGame() {
  overlay.style.display = 'none';
  gameRunning = true;
  requestAnimationFrame(gameLoop);
}

// Input handling
window.addEventListener('keydown', e => {
  keys[e.key] = true;
  // Prevent scrolling with arrow keys
  if (['ArrowLeft', 'ArrowRight', ' '].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e => { keys[e.key] = false; });

function fireBullet() {
  bullets.push({
    x: player.x + player.width / 2 - BULLET_WIDTH / 2,
    y: player.y,
    width: BULLET_WIDTH,
    height: BULLET_HEIGHT
  });
}

function updatePlayer() {
  if (keys['ArrowLeft']) player.x -= PLAYER_SPEED;
  if (keys['ArrowRight']) player.x += PLAYER_SPEED;
  // Keep inside canvas
  if (player.x < 0) player.x = 0;
  if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
  // Shooting
  if (keys[' '] && gameRunning) {
    // simple rate limit using timestamp
    const now = Date.now();
    if (!player.lastShot || now - player.lastShot > 250) {
      fireBullet();
      player.lastShot = now;
    }
  }
}

function updateBullets() {
  for (let i = bullets.length - 1; i >= 0; i--) {
    const b = bullets[i];
    b.y -= BULLET_SPEED;
    if (b.y + b.height < 0) bullets.splice(i, 1);
  }
}

function spawnExplosion(x, y) {
  const count = 12 + Math.random() * 8;
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 1 + Math.random() * 2;
    particles.push({
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 30 + Math.random() * 10,
      size: 2 + Math.random() * 2,
      color: ['#22c55e', '#4facfe', '#00f2fe'][Math.floor(Math.random() * 3)]
    });
  }
}

function updateEnemies() {
  for (let i = enemies.length - 1; i >= 0; i--) {
    const e = enemies[i];
    if (!e.alive) continue;
    // Simple down‑ward drift to increase difficulty over time
    e.y += 0.02; // slow drift
    // Collision with player (game over)
    if (rectCollision(e, player)) {
      lives = 0;
    }
  }
}

function updateParticles() {
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.vx;
    p.y += p.vy;
    p.life--;
    if (p.life <= 0) particles.splice(i, 1);
  }
}

function handleCollisions() {
  for (let i = bullets.length - 1; i >= 0; i--) {
    const b = bullets[i];
    for (let j = enemies.length - 1; j >= 0; j--) {
      const e = enemies[j];
      if (!e.alive) continue;
      if (rectCollision(b, e)) {
        // hit
        e.hp--;
        if (e.hp <= 0) {
          e.alive = false;
          spawnExplosion(e.x + e.width / 2, e.y + e.height / 2);
          score += 10;
        } else {
          // downgrade visual level
          e.level--;
        }
        bullets.splice(i, 1);
        break;
      }
    }
  }
}

function drawBackground() {
  ctx.fillStyle = BG_COLOR;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawGrid() {
  for (const e of enemies) {
    if (!e.alive) continue;
    const color = e.level === 0 ? GRID_EMPTY : GRID_LEVELS[e.level - 1];
    ctx.fillStyle = color;
    ctx.fillRect(e.x, e.y, e.width, e.height);
    // optional rounded corners for aesthetic
    ctx.strokeStyle = '#0d1117';
    ctx.strokeRect(e.x, e.y, e.width, e.height);
  }
}

function drawPlayer() {
  // Rocket body (simple triangle + rectangle)
  ctx.save();
  ctx.translate(player.x + player.width / 2, player.y + player.height);
  // Exhaust glow
  const exhaustGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, 30);
  exhaustGrad.addColorStop(0, '#00f2fe');
  exhaustGrad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = exhaustGrad;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-12, 30);
  ctx.lineTo(12, 30);
  ctx.closePath();
  ctx.fill();

  // Rocket body
  ctx.fillStyle = ROCKET_COLOR;
  ctx.beginPath();
  ctx.moveTo(0, -player.height);
  ctx.lineTo(-15, 0);
  ctx.lineTo(15, 0);
  ctx.closePath();
  ctx.fill();

  // Cockpit (ellipse)
  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.ellipse(0, -player.height + 10, 6, 8, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

function drawBullets() {
  ctx.fillStyle = '#00f2fe';
  for (const b of bullets) {
    ctx.fillRect(b.x, b.y, b.width, b.height);
  }
}

function drawParticles() {
  for (const p of particles) {
    ctx.fillStyle = p.color;
    ctx.globalAlpha = Math.max(p.life / 40, 0);
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1.0;
}

function drawHUD() {
  ctx.fillStyle = '#c9d1d9';
  ctx.font = '16px Consolas, monospace';
  ctx.textAlign = 'left';
  ctx.fillText(`Score: ${score}`, 20, 30);
  ctx.fillText(`Lives: ${lives}`, canvas.width - 100, 30);
}

function gameOver() {
  gameRunning = false;
  overlay.style.display = 'flex';
  overlay.innerHTML = `<h1>MISSION FAILED</h1><p>Score: ${score}</p><button id="restartBtn">RESTART</button>`;
  document.getElementById('restartBtn').addEventListener('click', resetGame);
}

function gameLoop() {
  if (!gameRunning) return;

  drawBackground();
  drawGrid();
  updatePlayer();
  drawPlayer();
  updateBullets();
  drawBullets();
  updateEnemies();
  handleCollisions();
  updateParticles();
  drawParticles();
  drawHUD();

  if (lives <= 0) {
    gameOver();
    return;
  }

  requestAnimationFrame(gameLoop);
}

// Initialize
resetGame();
