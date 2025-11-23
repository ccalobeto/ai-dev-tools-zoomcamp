# Snake Game

A classic Snake game built with Svelte 5 and Tailwind CSS.

## Features

- **Two Game Modes:**
  - **Walls Mode**: Hit walls = Game Over
  - **Pass-Through Mode**: Snake wraps around to the opposite side

- **WASD + Arrow Keys**: Control the snake with either keyboard layout
- **Grid-based gameplay**: Clean 20x20 grid with visual borders
- **Score tracking**: See how long you can survive!

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

This project is configured to deploy to GitHub Pages. The deployment workflow is located at `../../.github/workflows/deploy-snake.yml` and triggers automatically when changes are pushed to this directory.

**Live Demo:** https://ccalobeto.github.io/ai-dev-tools-zoomcamp/

## Controls

- **W / ↑** - Move Up
- **S / ↓** - Move Down
- **A / ←** - Move Left
- **D / →** - Move Right

## Tech Stack

- Svelte 5 (with runes)
- Vite
- Tailwind CSS
