<script>
  import { onMount } from "svelte";

  // Game constants
  const GRID_SIZE = 20;
  const CELL_SIZE = 20;
  const INITIAL_SNAKE = [{ x: 10, y: 10 }];
  const INITIAL_DIRECTION = { x: 1, y: 0 };
  const GAME_SPEED = 150;

  // Game state using Svelte 5 runes
  let snake = $state(INITIAL_SNAKE);
  let direction = $state(INITIAL_DIRECTION);
  let food = $state({ x: 15, y: 15 });
  let gameOver = $state(false);
  let score = $state(0);
  let gameMode = $state("walls"); // 'walls' or 'pass-through'
  let gameInterval = null;

  // Generate random food position
  function generateFood() {
    let newFood;
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE),
      };
    } while (
      snake.some(
        (segment) => segment.x === newFood.x && segment.y === newFood.y,
      )
    );
    return newFood;
  }

  // Check if position is part of snake
  function isSnake(x, y) {
    return snake.some((segment) => segment.x === x && segment.y === y);
  }

  // Check if position is food
  function isFood(x, y) {
    return food.x === x && food.y === y;
  }

  // Game loop
  function gameLoop() {
    if (gameOver) return;

    const head = snake[0];
    let newHead = {
      x: head.x + direction.x,
      y: head.y + direction.y,
    };

    // Handle wall collision based on game mode
    if (gameMode === "walls") {
      // Walls mode: game over on collision
      if (
        newHead.x < 0 ||
        newHead.x >= GRID_SIZE ||
        newHead.y < 0 ||
        newHead.y >= GRID_SIZE
      ) {
        gameOver = true;
        clearInterval(gameInterval);
        return;
      }
    } else {
      // Pass-through mode: wrap around
      if (newHead.x < 0) newHead.x = GRID_SIZE - 1;
      if (newHead.x >= GRID_SIZE) newHead.x = 0;
      if (newHead.y < 0) newHead.y = GRID_SIZE - 1;
      if (newHead.y >= GRID_SIZE) newHead.y = 0;
    }

    // Check self collision
    if (
      snake.some(
        (segment) => segment.x === newHead.x && segment.y === newHead.y,
      )
    ) {
      gameOver = true;
      clearInterval(gameInterval);
      return;
    }

    // Move snake
    snake = [newHead, ...snake];

    // Check food collision
    if (newHead.x === food.x && newHead.y === food.y) {
      score++;
      food = generateFood();
    } else {
      snake.pop();
    }
  }

  // Handle keyboard input
  function handleKeyDown(event) {
    if (gameOver) return;

    switch (event.key) {
      case "ArrowUp":
      case "w":
      case "W":
        if (direction.y === 0) direction = { x: 0, y: -1 };
        break;
      case "ArrowDown":
      case "s":
      case "S":
        if (direction.y === 0) direction = { x: 0, y: 1 };
        break;
      case "ArrowLeft":
      case "a":
      case "A":
        if (direction.x === 0) direction = { x: -1, y: 0 };
        break;
      case "ArrowRight":
      case "d":
      case "D":
        if (direction.x === 0) direction = { x: 1, y: 0 };
        break;
    }
  }

  // Reset game
  function resetGame() {
    snake = [...INITIAL_SNAKE];
    direction = { ...INITIAL_DIRECTION };
    food = generateFood();
    gameOver = false;
    score = 0;
    if (gameInterval) clearInterval(gameInterval);
    gameInterval = setInterval(gameLoop, GAME_SPEED);
  }

  // Initialize game on mount
  onMount(() => {
    gameInterval = setInterval(gameLoop, GAME_SPEED);
    return () => {
      if (gameInterval) clearInterval(gameInterval);
    };
  });
</script>

<svelte:window on:keydown={handleKeyDown} />

<div class="bg-white rounded-lg shadow-2xl p-8">
  <h1 class="text-4xl font-bold text-center mb-4 text-gray-800">Snake Game</h1>

  <div class="mb-4 text-center">
    <p class="text-2xl font-semibold text-gray-700">
      Score: <span class="text-blue-600">{score}</span>
    </p>
  </div>

  <div class="mb-4 flex justify-center gap-4">
    <button
      onclick={() => {
        gameMode = "walls";
        resetGame();
      }}
      class="px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
      class:bg-blue-600={gameMode === "walls"}
      class:text-white={gameMode === "walls"}
      class:bg-gray-200={gameMode !== "walls"}
      class:text-gray-700={gameMode !== "walls"}
    >
      Walls Mode
    </button>
    <button
      onclick={() => {
        gameMode = "pass-through";
        resetGame();
      }}
      class="px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
      class:bg-blue-600={gameMode === "pass-through"}
      class:text-white={gameMode === "pass-through"}
      class:bg-gray-200={gameMode !== "pass-through"}
      class:text-gray-700={gameMode !== "pass-through"}
    >
      Pass-Through Mode
    </button>
  </div>

  <div
    class="border-2 border-gray-800 bg-gray-100 relative overflow-hidden"
    style="width: {GRID_SIZE * CELL_SIZE}px; height: {GRID_SIZE * CELL_SIZE}px;"
  >
    {#each Array(GRID_SIZE) as _, y}
      {#each Array(GRID_SIZE) as _, x}
        <div
          class="absolute transition-colors duration-100"
          style="
              left: {x * CELL_SIZE}px;
              top: {y * CELL_SIZE}px;
              width: {CELL_SIZE}px;
              height: {CELL_SIZE}px;
              {x > 0 ? 'border-left: 1px solid #d1d5db;' : ''}
              {y > 0 ? 'border-top: 1px solid #d1d5db;' : ''}
            "
          class:bg-green-500={isSnake(x, y)}
          class:bg-red-500={isFood(x, y)}
          class:rounded-full={isFood(x, y)}
        ></div>
      {/each}
    {/each}
  </div>

  {#if gameOver}
    <div class="mt-6 text-center">
      <p class="text-3xl font-bold text-red-600 mb-4">Game Over!</p>
      <button
        onclick={resetGame}
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200"
      >
        Play Again
      </button>
    </div>
  {/if}

  <div class="mt-6 text-center text-gray-600">
    <p class="text-sm">Use arrow keys or WASD to control the snake</p>
    <p class="text-xs mt-2">Eat the red food to grow and score points!</p>
    <p class="text-xs mt-1">
      <span class="font-semibold">Walls Mode:</span> Hit walls = Game Over |
      <span class="font-semibold">Pass-Through:</span> Walls wrap around
    </p>
  </div>
</div>
