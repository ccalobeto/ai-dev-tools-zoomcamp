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
    const newHead = {
      x: head.x + direction.x,
      y: head.y + direction.y,
    };

    // Check wall collision
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
        if (direction.y === 0) direction = { x: 0, y: -1 };
        break;
      case "ArrowDown":
        if (direction.y === 0) direction = { x: 0, y: 1 };
        break;
      case "ArrowLeft":
        if (direction.x === 0) direction = { x: -1, y: 0 };
        break;
      case "ArrowRight":
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

<div
  class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-purple-500 to-blue-600 p-8"
>
  <div class="bg-white rounded-lg shadow-2xl p-8">
    <h1 class="text-4xl font-bold text-center mb-4 text-gray-800">
      Snake Game
    </h1>

    <div class="mb-4 text-center">
      <p class="text-2xl font-semibold text-gray-700">
        Score: <span class="text-blue-600">{score}</span>
      </p>
    </div>

    <div
      class="border-4 border-gray-800 bg-gray-100 relative"
      style="width: {GRID_SIZE * CELL_SIZE}px; height: {GRID_SIZE *
        CELL_SIZE}px;"
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
      <p class="text-sm">Use arrow keys to control the snake</p>
      <p class="text-xs mt-2">Eat the red food to grow and score points!</p>
    </div>
  </div>
</div>
