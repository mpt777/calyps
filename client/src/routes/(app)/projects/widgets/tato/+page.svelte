<script>
import { onMount } from 'svelte';

onMount(() => {
    const perfectFrameTime = 1000 / 60;
    let deltaTime = 0;
    let lastTimestamp = 0;

  let context, controller, rectangle, loop, wall, movingWall, teleportWall, badDude, pewpew, canWin;
  context = document.getElementById("gameCanvas").getContext("2d");

  let gridNum = 16;

  let walls = [];
  let movingWalls = [];
  let deathWalls = [];
  let endGoals = [];
  let badDudes = [];
  let badDudesPewPew = [];
  let shootyThings = [];
  let movingPlatforms = [];
  let pewpewCornerIcon = [];
  let playerLives = [];
  let healthPickUps = [];
  let teleportWalls = [];
  let scoreCounter = [];

  let spawnBlock;

  let gravity = 1;
  let speed = 4;
  let jumpHeight = 9;
  let maxGravity = 25;

  //This counts out score, and it is used to place the squares in the top right corner
  let pewCount = 0;
  let pewCountBadDudes = 0;

  let levelPusher = false;
  let downTimer = 0;

  let coolDownCounter = 0;
  let coolDownTime = 50;

  let jumpCoolDownCounter = 0;
  let jumpCoolDownTime = 1;

  let playerTeleportBlockCounter = 0; // this tests to see if the player is colliding with any of the teleport blocks. If it is not, then it stays zero, and the player can teleport again
  let playerMovingPlatformTimer = 0;
  let playerMovingPlatformCounter = 0;

  let textBoxCounter = 0;


  let gamePause = false;
  //COLOR
  let spawnColor = "rgba(230, 0, 155, 0)"; //pink

  //images
  let HEART_IMAGE = "/widgets/tato/heart.png";
  let GOAL_IMAGE = "/widgets/tato/plates.png";
  let GRASS_IMAGE = "/widgets/tato/grass.png";
  let STONE_IMAGE = "/widgets/tato/stone.png";
  let ARROW_PEW = "/widgets/tato/arrow_pew.png";
  let WOOD_IMAGE = "/widgets/tato/wood.png";
  let WATER_IMAGE = "/widgets/tato/water.png";
  let SMOOTH_STONE = "/widgets/tato/smooth_stone.png";
  let LAVA_IMAGE = "/widgets/tato/lava.png";
  let WOOD_PLATFORM = "/widgets/tato/wood_platform.png";
  let STONE_MAP = "/widgets/tato/stone_map.png";
  let SMOOTH_STONE_MAP = "/widgets/tato/smooth_stone_map.png";
  let SAND_IMAGE = "/widgets/tato/sand.png";
  let CLOUD_IMAGE = "/widgets/tato/cloud.png";
  let DOOR_IMAGE = "/widgets/tato/door.png";
  let LEAVES_IMAGE = "/widgets/tato/leaves.png";
  let DIRT_IMAGE = "/widgets/tato/dirt.png";
  let CYAN_IMAGE = "/widgets/tato/cyan.png";

  let TURRET_RIGHT = "/widgets/tato/turret.png";

  let SMOOTH_GRASS = "/widgets/tato/smooth_grass.png";
  let SMOOTH_DARK_GRASS = "/widgets/tato/smooth_dark_grass.png";
  let CLOUD_MAP = "/widgets/tato/cloud_map.png";

  context.canvas.height = 624;
  context.canvas.width = 960;

  let gameH = context.canvas.height;
  let gameW = context.canvas.width;


  //This is a text-box stuff 

  wall = function (x, y, width, height, color) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.color = color;
  };

  //#############################################################################################################

  /* Each sprite sheet tile is 16x16 pixels in dimension. */
  let SPRITE_SIZE = 32;

  /* The Animation class manages frames within an animation frame set. The frame
  set is an array of values that correspond to the location of sprite images in
  the sprite sheet. For example, a frame value of 0 would correspond to the first
  sprite image / tile in the sprite sheet. By arranging these values in a frame set
  array, you can create a sequence of frames that make an animation when played in
  quick succession. */
  let Animation = function (frame_set, delay = 15) {

      this.count = 0; // Counts the number of game cycles since the last frame change.
      this.delay = delay; // The number of game cycles to wait until the next frame change.
      this.frame = 0; // The value in the sprite sheet of the sprite image / tile to display.
      this.frame_index = 0; // The frame's index in the current animation frame set.
      this.frame_set = frame_set; // The current animation frame set that holds sprite tile values.

  };

  Animation.prototype = {

      /* This changes the current animation frame set. For example, if the current
      set is [0, 1], and the new set is [2, 3], it changes the set to [2, 3]. It also
      sets the delay. */
      change: function (frame_set, delay = 15) {

          if (this.frame_set != frame_set) { // If the frame set is different:

              this.count = 0; // Reset the count.
              this.delay = delay; // Set the delay.
              this.frame_index = 0; // Start at the first frame in the new frame set.
              this.frame_set = frame_set; // Set the new frame set.
              this.frame = this.frame_set[this.frame_index]; // Set the new frame value.

          }

      },

      /* Call this on each game cycle. */
      update: function (deltaTime) {

          this.count += 1 * deltaTime; // Keep track of how many cycles have passed since the last frame change.

          if (this.count >= this.delay) { // If enough cycles have passed, we change the frame.

              this.count = 0; // Reset the count.
              /* If the frame index is on the last value in the frame set, reset to 0.
              If the frame index is not on the last value, just add 1 to it. */
              this.frame_index = (this.frame_index == this.frame_set.length - 1) ? 0 : this.frame_index + 1;
              this.frame = this.frame_set[this.frame_index]; // Change the current frame value.

          }

      }

  };
  /*       
      player = {

      animation:new Animation(),// You don't need to setup Animation right away.
      jumping:true,
      height:16,    width:16,
      x:0,          y:40 - 18,
      x_velocity:0, y_velocity:0

    };
  */
  /* The sprite sheet object holds the sprite sheet graphic and some animation frame
  sets. An animation frame set is just an array of frame values that correspond to
  each sprite image in the sprite sheet, just like a tile sheet and a tile map. */
  let sprite_sheet = {
      frame_sets: [[0, 1], [2, 3, 4, 5], [7, 8, 9, 10], [6], [11]], // standing still, walk right, walk left
      image: new Image()
  };


  //############################################################################

  rectangle = {
      animation: new Animation(),
      //color: "red",
      height: (gridNum * 2) - 2,
      jumping: true,
      width: gridNum,
      x: gridNum * 2,
      y: gridNum * 2,
      shoot: false,
      dirFacing: 0,
      level: 0,
      jumpSpeed: 0,
      storyMode: false,
      down: false,
      powerUp: false,
      enemyJump: false,
      lifeCount: 3,
      canTeleport: true
  };

  movingWall = function (x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, delayTimeX, delayTimeY, centeredMoveAni = 0, startDelayX = 0, startDelayY = 0) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.color = color;
      this.xMove = xMove;
      this.yMove = yMove;
      this.moveSpeedX = moveSpeedX;
      this.moveSpeedY = moveSpeedY;
      this.xOriginal = x;
      this.yOriginal = y;
      this.moveSwitchX = Math.sign(xMove);
      this.moveSwitchY = Math.sign(yMove);
      this.delayTimeX = delayTimeX;
      this.delayCounterX = 0;
      this.delayTimeY = delayTimeY;
      this.delayCounterY = 0;
      this.moveSwitchXTF = false;
      this.moveSwitchYTF = false;
      this.centeredMoveAni = centeredMoveAni;
      this.startDelayX = startDelayX;
      this.startDelayY = startDelayY;
  };

  teleportWall = function (x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, delayTimeX, delayTimeY, centeredMoveAni = 0, startDelayX = 0, startDelayY = 0, sendIndex = 0) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.color = color;
      this.xMove = xMove;
      this.yMove = yMove;
      this.moveSpeedX = moveSpeedX;
      this.moveSpeedY = moveSpeedY;
      this.xOriginal = x;
      this.yOriginal = y;
      this.moveSwitchX = Math.sign(xMove);
      this.moveSwitchY = Math.sign(yMove);
      this.delayTimeX = delayTimeX;
      this.delayCounterX = 0;
      this.delayTimeY = delayTimeY;
      this.delayCounterY = 0;
      this.moveSwitchXTF = false;
      this.moveSwitchYTF = false;
      this.centeredMoveAni = centeredMoveAni;
      this.startDelayX = startDelayX;
      this.startDelayY = startDelayY;
      this.sendIndex = sendIndex;
  };

  badDude = function (x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, delayTimeX, delayTimeY, badDudeCoolDown, direction, centeredMoveAni = 0, startDelayX = 0, startDelayY = 0) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.color = color;
      this.xMove = xMove;
      this.yMove = yMove;
      this.moveSpeedX = moveSpeedX;
      this.moveSpeedY = moveSpeedY;
      this.xOriginal = x;
      this.yOriginal = y;
      this.moveSwitchX = Math.sign(xMove);
      this.moveSwitchY = Math.sign(yMove);
      this.badDudeCoolDown = badDudeCoolDown;
      this.badDudeCoolDownOG = badDudeCoolDown;
      this.delayTimeX = delayTimeX;
      this.delayCounterX = 0;
      this.delayTimeY = delayTimeY;
      this.delayCounterY = 0;
      this.direction = direction;
      this.moveSwitchXTF = false;
      this.moveSwitchYTF = false;
      this.centeredMoveAni = centeredMoveAni;
      this.startDelayX = startDelayX;
      this.startDelayY = startDelayY;
  };

  pewpew = function (x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, direction) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.color = color;
      this.xMove = xMove;
      this.yMove = yMove;
      this.moveSpeedX = moveSpeedX;
      this.moveSpeedY = moveSpeedY;
      this.xOriginal = x;
      this.yOriginal = y;
      this.direction = direction;
      this.isColliding = false;
      this.shotFromEnemy = false;
  };

  controller = {

      left: 0,
      right: 0,
      up: 0,
      down: 0,
      keyListener: function (event) {

          let key_state = (event.type == "keydown") ? 1 : 0;

          switch (event.keyCode) {
              case 37: //left
                  controller.left = key_state;
                  break;
              case 38: //up
                  controller.up = key_state;
                  break;
              case 39: //right
                  controller.right = key_state;
                  break;
              case 32: //space
                  controller.shoot = key_state;
                  controller.up = key_state;
                  break;
              case 40: //
                  controller.down = 1;
                  controller.downActive = key_state;
                  break;
          }

      }
  };


  function playerFall() {

      if (!(placeFree(rectangle.x, rectangle.y + 1))) {
          gravity = 0;
          jumpCoolDownCounter += 1 * deltaTime;
      } else if (gravity <= maxGravity) {
          gravity += 1;
      } else {
          gravity = maxGravity;
      }

      if (jumpCoolDownCounter >= jumpCoolDownTime) { //change what jump timer needs to equal to change the jumping cooldown
          jumpCoolDownCounter -= jumpCoolDownTime;
          rectangle.jumping = true;
      }

      for (let i = gravity; i > 0; i--) {
          if (placeFree(rectangle.x, rectangle.y + (i * deltaTime))) {
              rectangle.y += i * deltaTime;
              break;
          }
      }

  }

  function playerJump() {

      if (!controller.up && !rectangle.enemyJump) {
          rectangle.jumpSpeed = 0;
      }

      if (!(placeFree(rectangle.x, rectangle.y - 1))) {
          rectangle.jumpSpeed = 0;
      } else {
          rectangle.jumpSpeed -= 0.5;
      }

      for (let j = rectangle.jumpSpeed; j > 0; j--) {
          if (placeFree(rectangle.x, rectangle.y - j)) {
              rectangle.y -= j * deltaTime;
          }
      }
  }

  function drawRectangle() {
      drawArray(pewpewCornerIcon);
      //draw(rectangle);
  }

  function drawCornerIcon() {
      for (let i = 0; i < rectangle.lifeCount; i++) {
          playerLives[i] = new wall(gameW - gridNum - 10 - (20 * (i)), gridNum, 10, 10, HEART_IMAGE);
      }
      
      //drawArray(playerLives);
      drawArrayOfImages(playerLives);
      drawArrayOfImages(scoreCounter);
  }

  function drawHealthPickups() {
      movingAnimation(healthPickUps);
      //drawArray(healthPickUps);
      drawArrayOfImages(healthPickUps);
  }

  function drawTeleportWalls() {
      movingAnimation(teleportWalls);
      //drawArray(teleportWalls);
      drawArrayOfImages(teleportWalls);
  }

  function playerSpawnMovementReset() {
      rectangle.x = spawnBlock.x;
      rectangle.y = spawnBlock.y;
      rectangle.jumpSpeed = 0;
      controller.right = 0;
      controller.left = 0;
      controller.up = 0;
      controller.down = 0;
      gravity = 0;
  }

  function loadLevel() {

      clearArrays();

      if (rectangle.level == 0) {

          spawnBlock = new wall(gridNum * 2, gridNum * 36, gridNum, gridNum, spawnColor);

          walls[0] = new wall(0, gameH - gridNum, gameW, gridNum, GRASS_IMAGE);

          //movingWalls[0] = 0;

          //movingPlatforms[0] = 0;

          endGoals[0] = new movingWall(gridNum * 9, gridNum * 33, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[1] = new movingWall(gridNum * 19, gridNum * 33, gridNum, gridNum, GRASS_IMAGE, 0, gridNum, 0, .3, 0, 0);
          endGoals[2] = new movingWall(gridNum * 24, gridNum * 33, gridNum, gridNum, SMOOTH_STONE, 0, gridNum, 0, .1, 0, 0);
          endGoals[3] = new movingWall(gridNum * 29, gridNum * 33, gridNum, gridNum, WATER_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[4] = new movingWall(gridNum * 34, gridNum * 33, gridNum, gridNum, STONE_IMAGE, 0, gridNum, 0, .11, 0, 0);
          endGoals[5] = new movingWall(gridNum * 39, gridNum * 33, gridNum, gridNum, LAVA_IMAGE, 0, gridNum, 0, .11, 0, 0);
          endGoals[6] = new movingWall(gridNum * 44, gridNum * 33, gridNum, gridNum, WOOD_IMAGE, 0, gridNum, 0, .11, 0, 0);
          //deathWalls[0] = 0;

          //badDudes[0] = 0;
          //healthPickUps[0] = 0;
      }

      if (rectangle.level == 1) { // new start

          spawnBlock = new wall(gridNum * 2, gridNum * 36, gridNum, gridNum, spawnColor);

          walls[0] = new wall(0, gridNum * 38, gameW, gridNum, GRASS_IMAGE);
          walls[1] = new wall(gridNum * 8, gameH - 5 * gridNum, gridNum * 5, gridNum, GRASS_IMAGE);
          walls[2] = new wall(gridNum * 40, gameH - 5 * gridNum, gridNum * 10, gridNum, GRASS_IMAGE);
          walls[3] = new wall(gridNum * 43, gameH - 10 * gridNum, gridNum * 4, gridNum, GRASS_IMAGE);


          //movingWalls[0] = 0 //new movingWall(gridNum * 31, gridNum * 29, gridNum * 5, gridNum, "pink", gridNum * 17, 0, 1, 0, 0, 0);

          movingPlatforms[0] = new movingWall(gridNum * 18, gridNum * 36, gridNum * 17, gridNum * 3, SMOOTH_STONE, 0, 0, 0, 0, 0, 0);
          movingPlatforms[1] = new movingWall(gridNum * 27, gridNum * 35, gridNum * 5, gridNum * 1, SMOOTH_STONE, 0, 0, 0, 0, 0, 0);

          endGoals[0] = new movingWall(gridNum * 29, gridNum * 30, gridNum, gridNum, GOAL_IMAGE, 0, -gridNum, 0, .1, 0, 0);
          endGoals[1] = new movingWall(gridNum * 44.5, gridNum * 25, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[2] = new movingWall(gridNum * 57, gridNum * 35, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);

          //deathWalls[0] = 0; //new wall(gridNum * 30, gameH - gridNum, gridNum * 24, gridNum, "orange");

          healthPickUps[0] = new movingWall(gridNum * 10, gridNum * 30, gridNum * 1, gridNum * 1, HEART_IMAGE, 0, gridNum * 1, 0, .15, 0, 0);

          badDudes[0] = new badDude(gridNum * 18, gridNum * 35, gridNum, gridNum, CYAN_IMAGE, gridNum * 8, 0, .5, 0, 0, 0, 0);
      }

      if (rectangle.level == 2) { // old start

          spawnBlock = new wall(gridNum * 2, gridNum * 36, gridNum, gridNum, spawnColor);

          walls[0] = new wall(0, gameH - gridNum, gameW, gridNum, GRASS_IMAGE);
          walls[1] = new wall(gridNum * 8, gameH - 4 * gridNum, gridNum * 5, gridNum, GRASS_IMAGE);
          walls[2] = new wall(gridNum * 16, gameH - 7 * gridNum, gridNum * 5, gridNum, GRASS_IMAGE);
          
          walls[3] = new wall(gridNum * 24, gameH - 10 * gridNum, gridNum * 6, gridNum * 9, STONE_MAP);
          walls[4] = new wall(gameW - gridNum * 6, gameH - 12 * gridNum, gridNum * 6, gridNum * 11, STONE_IMAGE);

          movingWalls[0] = new movingWall(gridNum * 31, gridNum * 29, gridNum * 5, gridNum, WOOD_IMAGE, gridNum * 17, 0, 1, 0, 0, 0);

          //movingPlatforms[0] = 0;

          endGoals[0] = new movingWall(gameW - 3 * gridNum, gameH - 15 - gridNum * 14, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[1] = new movingWall(gridNum * 13, gridNum * 26, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[2] = new movingWall(gridNum * 42, gridNum * 26, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);

          deathWalls[0] = new wall(gridNum * 30, gameH - gridNum, gridNum * 24, gridNum, WATER_IMAGE);

          badDudes[0] = new badDude(gridNum * 16, gridNum * 37, gridNum, gridNum, CYAN_IMAGE, gridNum * 7, 0, .7, 0, 0, 0, 0);
      }

      if (rectangle.level == 3) {
          let GREEN = "green";
          let DARKGREEN = "darkgreen";

          spawnBlock = new wall(gridNum * 2, gridNum * 18, gridNum, gridNum, spawnColor); //good level

          walls[0] = new wall(0, gridNum * 20, gridNum * 5, gridNum * 3, STONE_MAP);
          
          walls[1] = new wall(0, gridNum * 30, gridNum * 14, gridNum * 9, SMOOTH_GRASS);
          walls[2] = new wall(0, gridNum * 34, gridNum * 22, gridNum * 5, SMOOTH_DARK_GRASS);
          walls[3] = new wall(0, gridNum * 38, gameW, gridNum, SMOOTH_GRASS);
          walls[4] = new wall(gridNum * 12, gridNum * 19, gridNum * 24, gridNum * 3, SMOOTH_GRASS);
          walls[5] = new wall(gridNum * 25, gridNum * 17, gridNum * 5, gridNum * 6, SMOOTH_DARK_GRASS);
          
          walls[6] = new wall(gridNum * 55, gridNum * 23, gridNum * 5, gridNum * 3, STONE_MAP);
          
          walls[7] = new wall(gridNum * 38, gridNum * 7, gridNum * 6, gridNum, WOOD_IMAGE);
          walls[8] = new wall(gridNum * 46, gridNum * 13, gridNum * 6, gridNum, WOOD_IMAGE);

          movingPlatforms[0] = new movingWall(gridNum * 6, gridNum * 28, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, gridNum * 9, 0, .5, 0, 0);
          movingPlatforms[1] = new movingWall(gridNum * 31, gridNum * 19, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, gridNum * 14, 0, .5, 0, 0);
          movingPlatforms[2] = new movingWall(gridNum * 31, gridNum * 25, gridNum * 5, gridNum * .5, WOOD_PLATFORM, gridNum * 18, 0, 1, 0, 0, 0);


          //movingWalls[0] = 0;

          endGoals[0] = new movingWall(gameW - 3 * gridNum, gridNum * 20, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[1] = new movingWall(gridNum * 26, gridNum * 33, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .3, 0, 0);
          endGoals[2] = new movingWall(gridNum * 27, gridNum * 10, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);

          deathWalls[0] = new wall(gridNum * 30, gameH - gridNum, gridNum * 30, gridNum, WATER_IMAGE);

          badDudes[0] = new badDude(gridNum, gridNum * 29, gridNum, gridNum, CYAN_IMAGE, gridNum * 11, 0, .7, 0, 0, 0, 150, 0);
          badDudes[1] = new badDude(gridNum * 13, gridNum * 18, gridNum, gridNum, CYAN_IMAGE, gridNum * 11, 0, 1, 0, 0, 0, 0);

          //healthPickUps[0] = 0;
      }
      if (rectangle.level == 4) { //castle

          spawnBlock = new wall(gridNum * 2, gridNum * 35, gridNum, gridNum, spawnColor); // castle

          walls[0] = new wall(0, gridNum * 37, gridNum * 22, gridNum * 2, GRASS_IMAGE);
          //walls[0] = new wall(0, gridNum * 38, gameW, gridNum, GRASS_IMAGE);
          walls[1] = new wall(gridNum* 27, gridNum * 38, gameW, gridNum, STONE_IMAGE);
          
          walls[2] = new wall(gridNum * 35, gridNum * 13, gridNum * 10, gridNum * 21, STONE_MAP);
          walls[3] = new wall(gridNum * 59, gridNum * 13, gridNum * 5, gridNum * 25, STONE_MAP);
          walls[4] = new wall(gridNum * 22, gridNum * 30, gridNum * 5, gridNum * 24, STONE_MAP);

          movingPlatforms[0] = new movingWall(gridNum * 6, gridNum * 33, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[1] = new movingWall(gridNum * 50, gridNum * 33, gridNum * 3, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[2] = new movingWall(gridNum * 44, gridNum * 17, gridNum * 15, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[3] = new movingWall(gridNum * 26, gridNum * 34, gridNum * 3, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[4] = new movingWall(gridNum * 14, gridNum * 29, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);


          movingWalls[0] = new movingWall(gridNum * 35, gridNum * 31, gridNum * 11, gridNum * 3, SMOOTH_STONE, gridNum * 10, 0, .4, 0, 0, 0);
          movingWalls[1] = new movingWall(gridNum * 50, gridNum * 31, gridNum * 11, gridNum * 3, SMOOTH_STONE, gridNum * 10, 0, .4, 0, 0, 0);

          movingWalls[2] = new movingWall(gridNum * 35, gridNum * 26, gridNum * 10, gridNum * 2, SMOOTH_STONE, gridNum * 6, 0, .4, 0, 0, 0);
          movingWalls[3] = new movingWall(gridNum * 50, gridNum * 26, gridNum * 10, gridNum * 3, SMOOTH_STONE, gridNum * 5, 0, .4, 0, 0, 0);

          movingWalls[4] = new movingWall(gridNum * 47, gridNum * 21, gridNum * 4, gridNum * 1, SMOOTH_STONE, gridNum * 5, 0, .4, 0, 0, 0);

          movingWalls[5] = new movingWall(gridNum * 36, gridNum * 15, gridNum * 10, gridNum * 3, SMOOTH_STONE, gridNum * 9, 0, .4, 0, 0, 0);
          movingWalls[6] = new movingWall(gridNum * 50, gridNum * 15, gridNum * 10, gridNum * 3, SMOOTH_STONE, gridNum * 6, 0, .4, 0, 0, 0);

          movingWalls[7] = new movingWall(gridNum * 55, gridNum * 24, gridNum * 10, gridNum * 2, SMOOTH_STONE, gridNum * 3, 0, .2, 0, 0, 0);

          endGoals[0] = new movingWall(gameW - 21 * gridNum, gridNum * 10, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .15, 0, 0);
          endGoals[1] = new movingWall(gridNum * 18, gridNum * 33, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .3, 0, 0);
          endGoals[2] = new movingWall(gridNum * 57, gridNum * 35, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .3, 0, 0);

          //deathWalls[0] = 0 //new wall(gridNum * 30, gameH - gridNum, gridNum * 30, gridNum, "orange");

          badDudes[0] = new badDude(gridNum * 29, gridNum * 37, gridNum, gridNum, CYAN_IMAGE, gridNum * 27, 0, .5, 0, 0, 0, 150,0 );
          badDudes[1] = new badDude(gridNum * 13, gridNum * 36, gridNum, gridNum, CYAN_IMAGE, gridNum * 8, 0, .5, 0, 0, 0, 0);

          healthPickUps[0] = new movingWall(gridNum * 57, gridNum * 20, gridNum * 1, gridNum * 1, HEART_IMAGE, 0, gridNum * 1, 0, .15, 0, 0);
      }
      if (rectangle.level == 5) {

          spawnBlock = new wall(gridNum * 2, gridNum * 3, gridNum, gridNum, spawnColor);

          walls[0] = new wall(0, gridNum * 5, gridNum * 6, gridNum * 4, SMOOTH_STONE_MAP);
          walls[1] = new wall(0, 0, gridNum * 60, gridNum * 2, SMOOTH_STONE_MAP);
          walls[2] = new wall(0, 0, gridNum, gridNum * 45, SMOOTH_STONE_MAP);
          walls[3] = new wall(0, gridNum * 9, gridNum * 18, gridNum * 3, SMOOTH_STONE_MAP);
          walls[4] = new wall(gridNum * 10, gridNum * 18, gridNum * 15, gridNum * 3, SMOOTH_STONE_MAP);
          walls[5] = new wall(gridNum * 24, gridNum * 11, gridNum * 6, gridNum * 11, STONE_MAP); //middle boi
          walls[6] = new wall(gridNum * 20, gridNum * 0, gridNum * 8, gridNum * 4, STONE_MAP); //ceilling staligtite
          walls[7] = new wall(gridNum * 59, gridNum * 0, gridNum * 3, gridNum * 40, SMOOTH_STONE_MAP);
          walls[8] = new wall(gridNum * 50, gridNum * 0, gridNum * 9, gridNum * 5, SMOOTH_STONE_MAP);
          walls[9] = new wall(gridNum * 38, gridNum * 9, gridNum * 18, gridNum * 3, SMOOTH_STONE_MAP);
          walls[10] = new wall(gridNum * 42, gridNum * 10, gridNum * 8, gridNum * 3, SMOOTH_STONE_MAP);
          walls[11] = new wall(gridNum * 32, gridNum * 18, gridNum * 8, gridNum * 2, SMOOTH_STONE_MAP);
          walls[12] = new wall(gridNum * 34, gridNum * 13, gridNum * 3, gridNum * 1, SMOOTH_STONE_MAP);
          walls[13] = new wall(gridNum * 0, gridNum * 16, gridNum * 6, gridNum * 8, SMOOTH_STONE_MAP);
          walls[14] = new wall(gridNum * 0, gridNum * 36, gridNum * 11, gridNum * 9, SMOOTH_STONE_MAP);
          walls[16] = new wall(gridNum * 11, gridNum * 21, gridNum * 3, gridNum * 7, SMOOTH_STONE_MAP);
          walls[15] = new wall(gridNum * 10, gridNum * 21, gridNum * 4, gridNum * 4, SMOOTH_STONE_MAP); //fixes the small dude on the left down part
          walls[17] = new wall(gridNum * 5, gridNum * 27, gridNum * 7, gridNum * 1, SMOOTH_STONE_MAP); //wall under the turret
          walls[18] = new wall(gridNum * 1, gridNum * 33, gridNum * 5, gridNum * 3, SMOOTH_STONE_MAP); //bottom left under turret bump
          walls[19] = new wall(gridNum * 14, gridNum * 24, gridNum * 4, gridNum * 1, SMOOTH_STONE_MAP); //jutty bit above lava
          walls[23] = new wall(gridNum * 25, gridNum * 25, gridNum * 11, gridNum * 1, SMOOTH_STONE_MAP);
          walls[21] = new wall(gridNum * 51, gridNum * 29, gridNum * 8, gridNum * 2, SMOOTH_STONE_MAP); // bottom right platform goal
          walls[22] = new wall(gridNum * 44, gridNum * 32, gridNum * 4, gridNum * 1, SMOOTH_STONE_MAP);
          walls[20] = new wall(gridNum * 34, gridNum * 20, gridNum * 3, gridNum * 7, STONE_MAP); //midde sect=ret tunel down
          walls[24] = new wall(gridNum * 39, gridNum * 17, gridNum * 8, gridNum * 2, SMOOTH_STONE_MAP);
          walls[25] = new wall(gridNum * 49, gridNum * 17, gridNum * 10, gridNum * 2, SMOOTH_STONE_MAP); //right top of passage far
          walls[26] = new wall(gridNum * 57, gridNum * 16, gridNum * 10, gridNum * 2, SMOOTH_STONE_MAP);
          walls[27] = new wall(gridNum * 39, gridNum * 23, gridNum * 5, gridNum * 3, SMOOTH_STONE_MAP); //slope up 1 in secret passage
          walls[28] = new wall(gridNum * 42, gridNum * 21, gridNum * 9, gridNum * 3, SMOOTH_STONE_MAP);
          walls[29] = new wall(gridNum * 49, gridNum * 19, gridNum * 7, gridNum * 3, SMOOTH_STONE_MAP);

          //(x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, delayTimeX, delayTimeY, moveSwitchX, moveSwitchY)
          movingPlatforms[0] = new movingWall(gridNum * 21, gridNum * 14, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[1] = new movingWall(gridNum * 18, gridNum * 11, gridNum * 2, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[2] = new movingWall(gridNum * 30, gridNum * 18, gridNum * 2, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);
          movingPlatforms[3] = new movingWall(gridNum * 6, gridNum * 22, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);

          movingPlatforms[4] = new movingWall(gridNum * 12, gridNum * 32, gridNum * 4, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0); // first lava

          movingPlatforms[5] = new movingWall(gridNum * 1, gridNum * 30, gridNum * 4, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);

          movingPlatforms[6] = new movingWall(gridNum * 19, gridNum * 35, gridNum * 4, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0); // second lava down
          movingPlatforms[7] = new movingWall(gridNum * 18, gridNum * 29, gridNum * 6, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0); // " " up
          movingPlatforms[8] = new movingWall(gridNum * 30, gridNum * 21, gridNum * 7, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0); // secret tunnel bottom
          movingPlatforms[9] = new movingWall(gridNum * 26, gridNum * 32, gridNum * 4, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0); // secret tunnel bottom
          movingPlatforms[10] = new movingWall(gridNum * 34, gridNum * 23, gridNum * 5, gridNum * .5, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0);

          movingWalls[0] = new movingWall(gridNum * 30, gridNum * 35, gridNum * 11, gridNum * 3, STONE_MAP, gridNum * 1, 0, .1, 0, 0, 0, 0, 0);

          endGoals[0] = new movingWall(gridNum * 47, gridNum * 5, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .15, 0, 0);
          endGoals[1] = new movingWall(gridNum * 2, gridNum * 14, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);
          endGoals[2] = new movingWall(gridNum * 20 + (1 / 2 * gridNum), gridNum * 25, gridNum, gridNum, GOAL_IMAGE, 0, -gridNum, 0, .1, 0, 0);
          endGoals[3] = new movingWall(gridNum * 55, gridNum * 25, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .2, 0, 0);

          deathWalls[3] = new wall(0, gameH - gridNum, gridNum * 60, gridNum, LAVA_IMAGE); //ground
          deathWalls[1] = new movingWall(gridNum * 13, gridNum * 40, gridNum * 2, gridNum * 10, LAVA_IMAGE, 0, gridNum * 10, 0, 2, 0, 75); //first lava spike
          deathWalls[2] = new movingWall(gridNum * 20, gridNum * 40, gridNum * 2, gridNum * 15, LAVA_IMAGE, 0, gridNum * 15, 0, 2, 0, 100);
          deathWalls[0] = new movingWall(gridNum * 27, gridNum * 40, gridNum * 2, gridNum * 10, LAVA_IMAGE, 0, gridNum * 10, 0, 2, 0, 75);

          badDudes[0] = new badDude(gridNum * 0, gridNum * 26, gridNum, gridNum, TURRET_RIGHT, gridNum * 0, 0, 0, 0, 0, 0, 180, 1); //turret
          badDudes[1] = new badDude(gridNum * 54, gridNum * 8, gridNum, gridNum, CYAN_IMAGE, -gridNum * 15, 0, .7, 0, 0, 0, 200, 0);
          badDudes[2] = new badDude(gridNum * 10, gridNum * 17, gridNum, gridNum, CYAN_IMAGE, gridNum * 13, 0, .4, 0, 0, 0, 0, 0);
          badDudes[3] = new badDude(gridNum * 49, gridNum * 16, gridNum, gridNum, CYAN_IMAGE, gridNum * 7, 0, .4, 0, 0, 0, 0, 0);
          badDudes[4] = new badDude(gridNum * 46, gridNum * 16, gridNum, gridNum, CYAN_IMAGE, -gridNum * 7, 0, .6, 0, 0, 0, 0, 0);

          healthPickUps[0] = new movingWall(gridNum * 15, gridNum * 22, gridNum * 1, gridNum * 1, HEART_IMAGE, 0, gridNum * .5, 0, .15, 0, 0);
      }
      if (rectangle.level == 6) {
          spawnBlock = new wall(gridNum * 2, gridNum * 35, gridNum, gridNum, spawnColor); //ship Level

          walls[0] = new wall(0, gridNum * 37, gridNum * 5, gridNum * 3, GRASS_IMAGE);

          walls[1] = new wall(gridNum * 35, gridNum * 35, gridNum * 20, gridNum * 3, WOOD_IMAGE);
          walls[2] = new wall(gridNum * 31, gridNum * 34, gridNum * 6, gridNum * 3, WOOD_IMAGE);
          walls[3] = new wall(gridNum * 48, gridNum * 34, gridNum * 10, gridNum * 3, WOOD_IMAGE);
          walls[4] = new wall(gridNum * 26, gridNum * 33, gridNum * 8, gridNum * 1, WOOD_IMAGE);
          walls[5] = new wall(gridNum * 28, gridNum * 34, gridNum * 8, gridNum * 1, WOOD_IMAGE);
          walls[6] = new wall(gridNum * 50, gridNum * 31, gridNum * 6, gridNum * 5, WOOD_IMAGE);
          walls[7] = new wall(gridNum * 49, gridNum * 31, gridNum * 10, gridNum * 1, WOOD_IMAGE);

          //(x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, delayTimeX, delayTimeY, centeredMoveAni, startDelayX, startDelayY)
          //movingPlatforms[0] = new movingWall(gridNum * 12, gridNum * 13, gridNum * 5, gridNum * .5, "tan", gridNum * 2, gridNum * -2, 0.3, 0.3,0,0, 0);
          //movingPlatforms[1] = new movingWall(gridNum * 31, gridNum * 19, gridNum * 5, gridNum * .5, "tan", 0, gridNum * 14, 0, .5, 0, 0);
          //movingPlatforms[2] = new movingWall(gridNum * 31, gridNum * 25, gridNum * 5, gridNum * .5, "tan", gridNum * 18, 0, 1, 0, 0, 0);
          //movingPlatforms[3] = new movingWall(gridNum * 43, gridNum * 25, gridNum * 1, gridNum * 50, "pink", gridNum * 0, 0, 0, 0, 0, 0);
          //(x, y, width, height, color, xMove, yMove, moveSpeedX, moveSpeedY, delayTimeX, delayTimeY, centeredMoveAni, startDelayX, startDelayY)
          movingWalls[0] = new movingWall(gridNum * 8, gridNum * 37, gridNum * 4, gridNum * 1, GRASS_IMAGE, 0, gridNum * 1, 0, 0, 0, 0, 0, 0, 0); // lilly pads
          movingWalls[1] = new movingWall(gridNum * 15, gridNum * 37, gridNum * 4, gridNum * 1, GRASS_IMAGE, 0, gridNum * 1, 0, 0, 0, 0, 0, 0, 0);
          movingWalls[2] = new movingWall(gridNum * 22, gridNum * 37, gridNum * 4, gridNum * 1, GRASS_IMAGE, 0, gridNum * 1, 0, 0, 0, 0, 0, 0, 0);

          movingWalls[3] = new movingWall(gridNum * -1, gridNum * 12, gridNum * 10, gridNum * 2, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100); // cloud 1
          movingWalls[4] = new movingWall(gridNum * -1, gridNum * 10, gridNum * 6, gridNum * 3, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100);
          movingWalls[5] = new movingWall(gridNum * -1, gridNum * 7, gridNum * 3, gridNum * 3, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100);
          movingWalls[6] = new movingWall(gridNum * -1, gridNum * 14, gridNum * 3, gridNum * 1, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100);

          movingWalls[7] = new movingWall(gridNum * 22, gridNum * 14, gridNum * 10, gridNum * 2, CLOUD_MAP, gridNum * -1, 0, .04, 0, 0, 0, 1, 0, 0); //cloud 2
          movingWalls[8] = new movingWall(gridNum * 23, gridNum * 16, gridNum * 7, gridNum * 1, CLOUD_MAP, gridNum * -1, 0, .04, 0, 0, 0, 1, 0, 0);
          movingWalls[9] = new movingWall(gridNum * 30, gridNum * 11, gridNum * 9, gridNum * 7, CLOUD_MAP, gridNum * -1, 0, .04, 0, 0, 0, 1, 0, 0);
          movingWalls[10] = new movingWall(gridNum * 27, gridNum * 12, gridNum * 14, gridNum * 5, CLOUD_MAP, gridNum * -1, 0, .04, 0, 0, 0, 1, 0, 0);
          movingWalls[11] = new movingWall(gridNum * 40, gridNum * 13, gridNum * 5, gridNum * 3, CLOUD_MAP, gridNum * -1, 0, .04, 0, 0, 0, 1, 0, 0);
          movingWalls[12] = new movingWall(gridNum * 31, gridNum * 10, gridNum * 5, gridNum * 1, CLOUD_MAP, gridNum * -1, 0, .04, 0, 0, 0, 1, 0, 0); // top of cloud 2

          movingWalls[13] = new movingWall(gridNum * 51, gridNum * 7, gridNum * 11, gridNum * 2, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 0); //cloud 3
          movingWalls[14] = new movingWall(gridNum * 52, gridNum * 9, gridNum * 9, gridNum * 2, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 0);
          movingWalls[15] = new movingWall(gridNum * 53, gridNum * 5, gridNum * 6, gridNum * 4, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 0);
          movingWalls[16] = new movingWall(gridNum * 56, gridNum * 3, gridNum * 6, gridNum * 5, CLOUD_MAP, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 0);

          movingWalls[17] = new movingWall(gridNum * 13, gridNum * 13, gridNum * 5, gridNum * 1, CLOUD_MAP, gridNum * -1, 0, .05, 0, 0, 0, 0, 0, 0);
          movingWalls[18] = new movingWall(gridNum * 14, gridNum * 14, gridNum * 3, gridNum * 1, CLOUD_MAP, gridNum * -1, 0, .05, 0, 0, 0, 0, 0, 0);
          //movingWalls[18] = new movingWall(gridNum * 14, gridNum * 12, gridNum * 3, gridNum * 1, GRASS_IMAGE, gridNum * -1, 0, .05, 0, 0, 0, 0, 0, 0);

          teleportWalls[0] = new teleportWall(gridNum * 57, gridNum * 29, gridNum * 1, gridNum * 2, DOOR_IMAGE, gridNum * 0, 0, 0, 0, 0, 0, 0, 0, 0, 1); //boat telepprter
          teleportWalls[1] = new teleportWall(gridNum * 52, gridNum * 5, gridNum * 1, gridNum * 2, DOOR_IMAGE, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 0, -1);


          endGoals[0] = new movingWall(gridNum * 1, gridNum * 3, gridNum, gridNum, GOAL_IMAGE, gridNum * 1, gridNum, 0.05, .2, 0, 0); //cloud1boi
          endGoals[1] = new movingWall(gridNum * 29.5, gridNum * 30, gridNum, gridNum, GOAL_IMAGE, 0, gridNum, 0, .3, 0, 0); //boatboi
          endGoals[2] = new movingWall(gridNum * 24, gridNum * 10, gridNum, gridNum, GOAL_IMAGE, gridNum * -1, gridNum, 0.04, .2, 0, 0); //cloud2boi

          deathWalls[0] = new wall(gridNum * 0, gameH - gridNum, gameW, gridNum, WATER_IMAGE);

          badDudes[0] = new badDude(gridNum * 49, gridNum * 30, gridNum, gridNum, CYAN_IMAGE, gridNum * 9, 0, .7, 0, 0, 0, 200, 0);
          badDudes[1] = new badDude(gridNum * 47, gridNum * 34, gridNum, gridNum, CYAN_IMAGE, gridNum * -10, 0, 1, 0, 0, 0, 0);

          healthPickUps[0] = new movingWall(gridNum * 16.5, gridNum * 33, gridNum, gridNum, HEART_IMAGE, 0, gridNum, 0, .2, 0, 0);
          healthPickUps[1] = new movingWall(gridNum * 42.5, gridNum * 9, gridNum, gridNum, HEART_IMAGE, gridNum * -1, gridNum, 0.05, .2, 1, 0);
          
      }
      if (rectangle.level == 7) {
          spawnBlock = new wall(gridNum * 13, gridNum * 35, gridNum, gridNum, spawnColor); //home

          walls[0] = new wall(gridNum*10, gridNum * 37, gridNum * 40, gridNum * 3, GRASS_IMAGE);
          
          
          movingPlatforms[0] = new movingWall(gridNum * 24, gridNum * 33, gridNum * 9, gridNum * 8, WOOD_IMAGE, 0, 0, 0, 0, 0, 0, 0, 0, 0); 
          movingPlatforms[1] = new movingWall(gridNum * 24, gridNum * 33, gridNum * 1, gridNum * 8, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0, 0, 0, 0);
          movingPlatforms[2] = new movingWall(gridNum * 32, gridNum * 33, gridNum * 1, gridNum * 8, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0, 0, 0, 0); 
          movingPlatforms[3] = new movingWall(gridNum * 24, gridNum * 33, gridNum *9, gridNum * 1, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0, 0, 0, 0); 
          movingPlatforms[4] = new movingWall(gridNum * 23, gridNum * 33.5, gridNum *11, gridNum * 1, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0, 0, 0, 0); 
          movingPlatforms[5] = new movingWall(gridNum * 25, gridNum * 32.5, gridNum *7, gridNum * 1, WOOD_PLATFORM, 0, 0, 0, 0, 0, 0, 0, 0, 0); 
          
          movingPlatforms[6] = new movingWall(gridNum * 38, gridNum * 35, gridNum *11, gridNum * 2, GRASS_IMAGE, 0, 0, 0, 0, 0, 0, 0, 0, 0); 
          
          movingWalls[0] = new movingWall(gridNum * 7, gridNum * 17, gridNum * 10, gridNum * 1, CLOUD_IMAGE, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100); // cloud 1
          movingWalls[1] = new movingWall(gridNum * 8, gridNum * 15, gridNum * 8, gridNum * 3, CLOUD_IMAGE, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100);
          movingWalls[2] = new movingWall(gridNum * 9, gridNum * 14, gridNum * 4, gridNum * 3, CLOUD_IMAGE, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 100);
          
          movingWalls[3] = new movingWall(gridNum * 35, gridNum * 13, gridNum * 13, gridNum * 2, CLOUD_IMAGE, gridNum * -1, 0, .05, 0, 0, 0, 1, 0, 100);
          movingWalls[4] = new movingWall(gridNum * 37, gridNum * 15, gridNum * 9, gridNum * 1, CLOUD_IMAGE, gridNum * -1, 0, .05, 0, 0, 0, 1, 0, 100);
          movingWalls[5] = new movingWall(gridNum * 36, gridNum * 11, gridNum * 9, gridNum * 2, CLOUD_IMAGE, gridNum * -1, 0, .05, 0, 0, 0, 1, 0, 100);
          movingWalls[6] = new movingWall(gridNum * 42, gridNum * 10, gridNum * 4, gridNum * 3, CLOUD_IMAGE, gridNum * -1, 0, .05, 0, 0, 0, 1, 0, 100);
          
          teleportWalls[0] = new teleportWall(gridNum * 27, gridNum * 35, gridNum * 1, gridNum * 2, DOOR_IMAGE, gridNum * 0, 0, 0, 0, 0, 0, 0, 0, 0, 1); //boat telepprter
          
          teleportWalls[1] = new teleportWall(gridNum * 100, gridNum * 100, gridNum * 1, gridNum * 2, DOOR_IMAGE, gridNum * 1, 0, .05, 0, 0, 0, 1, 0, 0, -1);


          endGoals[0] = new movingWall(gridNum * 100, gridNum * 100, gridNum, gridNum, GOAL_IMAGE, gridNum * 1, gridNum, 0.05, .2, 0, 0); //cloud1boi

          
          deathWalls[0] = new wall(gridNum * 0, gameH - gridNum, gameW, gridNum, WATER_IMAGE);
          
          healthPickUps[0] = new movingWall(gridNum * 16.5, gridNum * 33, gridNum, gridNum, HEART_IMAGE, 0, gridNum, 0, .2, 0, 0);
          healthPickUps[1] = new movingWall(gridNum * 42.5, gridNum * 31, gridNum, gridNum, HEART_IMAGE, gridNum * -1, gridNum, 0.05, .2, 1, 0);
      }

      playerSpawnMovementReset();
  }


  function playerMovement() {

      let dir = controller.right - controller.left;

      let movingWallsTemp = {
          x: rectangle.x,
          y: rectangle.y + 6,
          width: rectangle.width,
          height: rectangle.height,
      }

      for (let s = speed; s > 0; s--) {
          if (placeFree(rectangle.x + s * dir, rectangle.y)) {
              rectangle.x += s * dir * deltaTime;
              break;
          }
      }
      //Game Bounds (Left and right)
      if (rectangle.x < 0) {
          rectangle.x = 0;
      }

      if (rectangle.x + rectangle.width > gameW) {
          rectangle.x = gameW - rectangle.width;
      }
      // end of bounds


      // Jump

      if (controller.up && !(placeFree(rectangle.x + rectangle.width * dir * -1, rectangle.y + 6)) && rectangle.jumping == true) {
          rectangle.jumping = false;
          rectangle.jumpSpeed = jumpHeight;
      }

      if (rectangle.jumpSpeed > 0) {
          playerJump();
          gravity = 0;
      } else {
          playerFall();
      }
      // end jump



      for (let i = 0; i < movingWalls.length; i++) {

          // Moving walls
          if (collisionDetect(movingWallsTemp, movingWalls[i])) {


              if (placeFree(rectangle.x + movingWalls[i].moveSpeedX * movingWalls[i].moveSwitchX, rectangle.y)) { //the place to the left or right free
                  rectangle.x += movingWalls[i].moveSpeedX * movingWalls[i].moveSwitchX * deltaTime;
              }
              if (placeFree(rectangle.x, rectangle.y + movingWalls[i].moveSpeedY * (movingWalls[i].moveSwitchY))) {
                  rectangle.y += movingWalls[i].moveSpeedY * (movingWalls[i].moveSwitchY) * deltaTime;
              }

              //might delete this line
              if (movingWalls[i].moveSwitchY == 1) {
                  rectangle.y += -0.5 * deltaTime;
              }
              gravity = 0;
          }

          let movingWallsTempWALL = {
              x: movingWalls[i].x + (movingWalls[i].moveSwitchX * 1.1),
              y: movingWalls[i].y,
              width: movingWalls[i].width,
              height: movingWalls[i].height,
          }

          if (collisionDetect(movingWallsTemp, movingWallsTempWALL)) { //makes the rectangle not stick when it jumps into the side of a moving wall
              if (rectangle.y < movingWalls[i].y + movingWalls[i].height && rectangle.y + rectangle.height > movingWalls[i].y) {
                  rectangle.x += movingWalls[i].moveSpeedX * movingWalls[i].moveSwitchX * deltaTime;
              }

          }

      }
      // Death Walls

      for (let dw = 0; dw < deathWalls.length; dw++) {
          if (collisionDetect(movingWallsTemp, deathWalls[dw])) {
              playerLossOfLife();
          }
      }
      //bad dudes
      for (let k = 0; k < badDudes.length; k++) {
          if (collisionDetect(movingWallsTemp, badDudes[k])) {
              if (rectangle.y < badDudes[k].y + badDudes[k].height && gravity != 0) {
                  
                  badDudes.splice(k, 1);

                  rectangle.enemyJump = true

                  rectangle.jumpSpeed = 6;

                  if (controller.up) {
                      rectangle.enemyJump = false;
                      rectangle.jumpSpeed = 9;
                  }

              } else {
                  playerLossOfLife();
              }
          }
      }

      //Moving Platforms

      playerMovingPlatformTimer = 0;

      for (let p = 0; p < movingPlatforms.length; p++) {
          if (movingPlatforms[p].y >= rectangle.y + (rectangle.height - 1) /*(placeFree(rectangle.x, rectangle.y + rectangle.height + gridNum   || movingPlatforms[p].moveSwitchY == -1) */ ) {

              if (controller.down == 0 && collisionDetect(movingWallsTemp, movingPlatforms[p])) {

                  if (placeFree(rectangle.x + (movingPlatforms[p].moveSpeedX * movingPlatforms[p].moveSwitchX), rectangle.y)) {
                      rectangle.x += movingPlatforms[p].moveSpeedX * movingPlatforms[p].moveSwitchX * deltaTime;
                  }

                  if (placeFree(rectangle.x, rectangle.y + ((movingPlatforms[p].moveSpeedY * movingPlatforms[p].moveSwitchY)))) {
                      rectangle.y += (movingPlatforms[p].moveSpeedY) * movingPlatforms[p].moveSwitchY * deltaTime;

                  }

                  if (movingPlatforms[p].moveSwitchY == -1) {
                      rectangle.y -= .5 * deltaTime;
                      gravity = 0;
                  }
                  playerMovingPlatformTimer += 1;
              }

          }
      }

      if (playerMovingPlatformTimer == 0) {
          playerMovingPlatformCounter += 1;
          //controller.down = 0;
      }
      if(playerMovingPlatformCounter > 2) {
          controller.down = 0;
          playerMovingPlatformCounter= 0;
      }

      //squish function
      if (placeFree(rectangle.x + 1, rectangle.y) == false && placeFree(rectangle.x - 1, rectangle.y) == false && placeFree(rectangle.x, rectangle.y + 1) == false && placeFree(rectangle.x, rectangle.y - 1)) {
          if (placeFree(rectangle.x, rectangle.y - (.5 * rectangle.height)) == false) {
              playerLossOfLife();
          }
      }


      //BadDudes pew pew
      /*
      for (let pp = 0; pp < badDudesPewPew.length; pp++) {
          if (collisionDetect(rectangle, badDudesPewPew[pp])) {
              playerLossOfLife();
          }
      }
  */

      playerTeleportBlockCounter = 0;

      if (controller.downActive == 1) {

          for (let tp = 0; tp < teleportWalls.length; tp++) { //teleportBlocks

              if (collisionDetect(rectangle, teleportWalls[tp])) {

                  if (rectangle.canTeleport) {
                      rectangle.x = teleportWalls[tp + teleportWalls[tp].sendIndex].x;
                      rectangle.y = teleportWalls[tp + teleportWalls[tp].sendIndex].y;
                      gravity = 3;
                      rectangle.jumpSpeed = 0;
                      rectangle.canTeleport = false;

                  }
                  playerTeleportBlockCounter += 1;
              }

          }
      }

      if (playerTeleportBlockCounter == 0) {
          rectangle.canTeleport = true;
      }




      for (let hp = 0; hp < healthPickUps.length; hp++) {
          if (collisionDetect(rectangle, healthPickUps[hp])) {
              playerGainLife();
              healthPickUps.splice(hp,1);
          }
      }

      if (controller.right) {
          rectangle.dirFacing = 1;
      }

      if (controller.left) {
          rectangle.dirFacing = -1;
      }

      //playerDown();
  }

  function playerAnimation() {

      if (controller.left && rectangle.jumpSpeed <= 0) { //left
          rectangle.animation.change(sprite_sheet.frame_sets[2], 10);
      }

      if (controller.right && rectangle.jumpSpeed <= 0) { //right
          rectangle.animation.change(sprite_sheet.frame_sets[1], 10);
      }

      /* If you're just standing still, change the animation to standing still. */
      if (!controller.left && !controller.right) { //standing still
          rectangle.animation.change(sprite_sheet.frame_sets[0], 15);
      }

      if ((placeFree(rectangle.x, rectangle.y + 3) || controller.up) && rectangle.dirFacing == 1) { // jump right
          rectangle.animation.change(sprite_sheet.frame_sets[3], 15)
      }

      if ((placeFree(rectangle.x, rectangle.y + 3) || controller.up) && rectangle.dirFacing == -1) { // jump left
          rectangle.animation.change(sprite_sheet.frame_sets[4], 15)
      }


      rectangle.animation.update(deltaTime);
  }

  function drawPewpew() {
      if (controller.shoot == 1 && rectangle.shoot && rectangle.dirFacing != 0) {
          shootyThings[pewCount] = new pewpew(rectangle.x, rectangle.y + (.25 * gridNum), gridNum, .5 * gridNum, "lime", gameW, 0, 5, 0, rectangle.dirFacing)
          rectangle.shoot = false;
          pewCount += 1;
      }
      if (shootyThings.length > 0) {
          shootingAnimation(shootyThings);
          drawArray(shootyThings);
      }
  }

  function drawBadDudesPewPew() {

      for (let i = 0; i < badDudes.length; i++) {
        if (badDudes[i].badDudeCoolDownOG == 0) {
            continue
        }
        if (badDudes[i].badDudeCoolDown >= 0)  {
            badDudes[i].badDudeCoolDown -= 1 * deltaTime;
        } else {
            if (badDudes[i].moveSpeedX - badDudes[i].moveSpeedY == 0) {
                badDudesPewPew[pewCountBadDudes] = new pewpew(badDudes[i].x + (gridNum * (badDudes[i].direction)), badDudes[i].y + (.25 * gridNum), gridNum, .5 * gridNum, ARROW_PEW, gameW, 0, 5, 0, badDudes[i].direction)
            } else {
                badDudesPewPew[pewCountBadDudes] = new pewpew(badDudes[i].x, badDudes[i].y + (.25 * gridNum), gridNum, .5 * gridNum, ARROW_PEW, gameW, 0, 5, 0, badDudes[i].moveSwitchX);
            }
            badDudesPewPew[pewCountBadDudes].shotFromEnemy = true;
            badDudes[i].badDudeCoolDown = badDudes[i].badDudeCoolDownOG;
            pewCountBadDudes += 1;
        }
      }


      if (badDudesPewPew.length > 0) {
          shootingAnimation(badDudesPewPew);
          //drawArray(badDudesPewPew);
          drawArrayOfImages(badDudesPewPew);
      }
  }

  function drawWalls() {
      drawArray(walls);
      drawArrayOfImages(walls);

  }

  function drawBackground() {
      let img = new Image();
      img.src = "/widgets/tato/night.png";
      context.drawImage(img, 0, 0);

  }

  function drawNephi() {
      context.drawImage(sprite_sheet.image, rectangle.animation.frame * SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE, Math.floor(rectangle.x - 0.5 * rectangle.width), Math.floor(rectangle.y - 2), SPRITE_SIZE, SPRITE_SIZE);
  }

  function collisionDetect(r1, r2) {
      if (r1.x < r2.x + r2.width &&
          r1.x + r1.width > r2.x &&
          r1.y < r2.y + r2.height &&
          r1.y + r1.height > r2.y) {
          return true;
      } else {
          return false;
      }
  }

  function placeFree(xNew, yNew) {
      let temp = {
          x: xNew,
          y: yNew,
          width: rectangle.width,
          height: rectangle.height
      };

      let allWallsTest = 0;


      for (let i = 0; i < walls.length; i++) {
          if (collisionDetect(temp, walls[i])) {
              allWallsTest += 1;
          } else {
              allWallsTest += 0;
          }
      }

      for (let mw = 0; mw < movingWalls.length; mw++) {
          if (collisionDetect(temp, movingWalls[mw])) {
              allWallsTest += 1;
          } else {
              allWallsTest += 0;
          }
      }
      if (rectangle.jumpSpeed <= 1 && controller.down == 0) {
          for (let p = 0; p < movingPlatforms.length; p++) {
              if (collisionDetect(temp, movingPlatforms[p]) && movingPlatforms[p].y >= rectangle.y + (rectangle.height - 1)) {
                  allWallsTest += 1;
              } else {
                  allWallsTest += 0;
              }
          }
      }


      if (rectangle.level == 0) {
          mainMenu(temp);
      }

      scoreKeeper(temp);
      //SQUISH FUNCTION
      if (allWallsTest > 5) {
          playerLossOfLife();
      }

      if (allWallsTest == 0) {
          return true;
      } else {
          return false;
      }

  }

  function draw(objectToDraw) {
      context.beginPath();
      context.fillStyle = objectToDraw.color;
      context.rect(objectToDraw.x, objectToDraw.y, objectToDraw.width, objectToDraw.height);
      context.fill();
  }

  function drawSpawnBlock() {
      draw(spawnBlock);
  }

  function drawMovingWalls() {
      movingAnimation(movingWalls);
      drawArray(movingWalls);
      drawArrayOfImages(movingWalls);
  }

  function drawMovingPlatforms() {
      movingAnimation(movingPlatforms);
      drawArray(movingPlatforms);
      drawArrayOfImages(movingPlatforms);
  }

  function drawBadDudes() {
      movingAnimation(badDudes);
      drawArray(badDudes);
      drawArrayOfImages(badDudes);
  }

  function drawDeathWalls() {
      movingAnimation(deathWalls);
      //drawArray(deathWalls);
      drawArrayOfImages(deathWalls);
  }

  function drawArray(arrayToDraw) {
      for (let i = 0; i < arrayToDraw.length; i++) {
          context.beginPath();
          context.fillStyle = arrayToDraw[i].color;
          context.rect(arrayToDraw[i].x, arrayToDraw[i].y, arrayToDraw[i].width, arrayToDraw[i].height);
          context.fill();
      }
  }

  function drawArrayOfImages(arrayToDraw) {
      for (let i = 0; i < arrayToDraw.length; i++) {
          let img = new Image();
          let img2 = new Image();
          img.src = arrayToDraw[i].color;
          //context.drawImage(img, arrayToDraw[i].x, arrayToDraw[i].y);


          if (arrayToDraw[i].color.includes("_map")) {
              context.drawImage(img, 0, 0, arrayToDraw[i].width, arrayToDraw[i].height, arrayToDraw[i].x, arrayToDraw[i].y, arrayToDraw[i].width, arrayToDraw[i].height);
          } else
          
          if (arrayToDraw[i].color.includes("_pew")) {
              if(arrayToDraw[i].direction == -1){
              context.drawImage(img, (SPRITE_SIZE/2), 0,16,16, arrayToDraw[i].x, arrayToDraw[i].y,16,16);
              } else {
                context.drawImage(img, 0, 0,16,16, arrayToDraw[i].x, arrayToDraw[i].y,16,16);   
              }
          } else
          
          if (arrayToDraw[i].color != WATER_IMAGE && arrayToDraw[i].color != DOOR_IMAGE && arrayToDraw[i].color != GRASS_IMAGE) { //repeats the image if the object is longer than 1 gridnum
              
              for (let k = 0; k < arrayToDraw[i].width / gridNum; k++) { // for loop increments by one in width, draws it, and then goes down the height
                  context.drawImage(img, arrayToDraw[i].x + (gridNum * k), arrayToDraw[i].y);
                  
                  for (let q = 0; q < arrayToDraw[i].height / gridNum; q++) { //
                      context.drawImage(img, arrayToDraw[i].x + (gridNum * k), arrayToDraw[i].y + (gridNum * q)); //repeats the image over the height os my object
                  }
              }
          }
          
          if (arrayToDraw[i].color == GRASS_IMAGE) {
              for (let k = 0; k < arrayToDraw[i].width / gridNum; k++) { // for loop increments by one in width, draws it, and then goes down the height
                  img2.src = DIRT_IMAGE;
                  for (let q = 0; q < arrayToDraw[i].height / gridNum; q++) { //
                      if(q != 0){
                          context.drawImage(img2, arrayToDraw[i].x + (gridNum * k), arrayToDraw[i].y + (gridNum * q));
                      } else {
                      context.drawImage(img, arrayToDraw[i].x + (gridNum * k), arrayToDraw[i].y + (gridNum * q)); //repeats the image over the height os my object
                      }
                  }
              }
          }

          if (arrayToDraw[i].color == WATER_IMAGE) {
              for (let k = 0; k < arrayToDraw[i].width / gridNum; k++) { // for loop increments by one in width, draws it, and then goes down the height
                  context.drawImage(img, arrayToDraw[i].x + (gridNum * k), arrayToDraw[i].y - 4);
              }
          }
          if (arrayToDraw[i].color == DOOR_IMAGE) {
                  context.drawImage(img, arrayToDraw[i].x, arrayToDraw[i].y);
              
          }


          //context.drawImage(sprite_sheet.image, rectangle.animation.frame * SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE, Math.floor(rectangle.x - 0.5*rectangle.width), Math.floor(rectangle.y-2), SPRITE_SIZE, SPRITE_SIZE); 
      }
  }

  function drawEndGoal() {
      movingAnimation(endGoals);
      //drawArray(endGoals);
      drawArrayOfImages(endGoals)
      
      if (endGoals.length == 0 && rectangle.jumping == true) {
          playerWin();
      }
  }

  function scoreKeeper(temp) {
      for (let i = 0; i < endGoals.length; i++) {
          if (collisionDetect(temp, endGoals[i])) {
              endGoals.splice(i,1);
              scoreCounter.push(new wall(gameW - gridNum - 10 - (20 * (scoreCounter.length)), gridNum * 2 + 5, 10, 10, GOAL_IMAGE));
          }
      }
  }

  function playerWin() {

      scoreCounter = 1;
      
      if (rectangle.storyMode == false) {
          
        let level_end = document.getElementsByClassName("level-end");
          level_end[0].classList.add("open");
          
          rectangle.lifeCount = 3;
          
              playerLives.splice(1,playerLives.length - rectangle.lifeCount);
          
      } else if (rectangle.level == 7) {
          
          let game_end = document.getElementsByClassName("story-end");
          game_end[0].classList.add("open");
          game_end[1].classList.add("open");
          
          rectangle.storyMode = false;
          canWin = true;
          
          rectangle.lifeCount = 3;
          
          playerLives.splice(1,playerLives.length - rectangle.lifeCount);
          
      } else {
          levelPusher = true;
      }
  }

  function playerLossOfLife() {
      
      rectangle.lifeCount -= 1;
      playerLives.pop();

      
      if (playerLives.length == 0) {
          
          let del = document.getElementsByClassName("death-box");
          del[0].classList.add("open");
          rectangle.storyMode = false;
          gamePause = true;
          
          rectangle.x = -100; //hides the player until the game "unpauses"
          rectangle.y = 1000;
          
      } else {
          
          playerSpawnMovementReset();
      }
      
  }


  function playerRespawn() {
          rectangle.level = 0;
          rectangle.lifeCount = 3;
          loadLevel();
  }

  function playerGainLife() {
      rectangle.lifeCount += 1;
  }


  function movingAnimation(objectToAnimate) {
      for (let ani = 0; ani < objectToAnimate.length; ani++) {

          if (objectToAnimate[ani].moveSwitchX != 0) {

              if (!objectToAnimate[ani].centeredMoveAni) {
                  if (Math.sign(objectToAnimate[ani].xMove) == 1 && objectToAnimate[ani].x <= objectToAnimate[ani].xOriginal) { //these two function make the animated bounce from start to one side
                      objectToAnimate[ani].moveSwitchXTF = true;
                  }
                  if (Math.sign(objectToAnimate[ani].xMove) == -1 && objectToAnimate[ani].x >= objectToAnimate[ani].xOriginal) { //this is teh second funtion
                      objectToAnimate[ani].moveSwitchXTF = true;
                  }
              }

              if (Math.abs(objectToAnimate[ani].x - objectToAnimate[ani].xOriginal) >= Math.abs(objectToAnimate[ani].xMove)) { //this function builds an interval with the starting position in the middle for the animated obedject to bounce between
                  objectToAnimate[ani].moveSwitchXTF = true;
              }

              if (objectToAnimate[ani].startDelayX <= 0) { // the start delay. If it is zero, start moving it, if not, subtract 1 from the start delay and try again

                  if (objectToAnimate[ani].moveSwitchXTF == true) {
                      if (objectToAnimate[ani].delayCounterX >= objectToAnimate[ani].delayTimeX) {
                          objectToAnimate[ani].moveSwitchX *= -1;
                          objectToAnimate[ani].delayCounterX = 0;
                          objectToAnimate[ani].moveSwitchXTF = false;
                      } else {
                          objectToAnimate[ani].delayCounterX += 1 * deltaTime;
                      }
                  }

                  if (objectToAnimate[ani].moveSwitchX == 1 && objectToAnimate[ani].moveSwitchXTF == false) {
                      objectToAnimate[ani].x += objectToAnimate[ani].moveSpeedX * objectToAnimate[ani].moveSwitchX * deltaTime;
                      objectToAnimate[ani].delayCounterX = 0;
                  }

                  if (objectToAnimate[ani].moveSwitchX == -1 && objectToAnimate[ani].moveSwitchXTF == false) {
                      objectToAnimate[ani].x += objectToAnimate[ani].moveSpeedX * objectToAnimate[ani].moveSwitchX * deltaTime;
                      objectToAnimate[ani].delayCounterX = 0;
                  }
              } else {
                  objectToAnimate[ani].startDelayX -= 1;
              }

          }


          if (objectToAnimate[ani].moveSwitchY != 0) {

              if (!objectToAnimate[ani].centeredMoveAni) {
                  if (Math.sign(objectToAnimate[ani].yMove) == -1 && objectToAnimate[ani].y <= objectToAnimate[ani].yOriginal) { //these two function make the animated bounce from start to one side
                      objectToAnimate[ani].moveSwitchYTF = true;
                  }
                  if (Math.sign(objectToAnimate[ani].yMove) == 1 && objectToAnimate[ani].y >= objectToAnimate[ani].yOriginal) { //this is teh second funtion
                      objectToAnimate[ani].moveSwitchYTF = true;
                  }
              }
              if (Math.abs(objectToAnimate[ani].y - objectToAnimate[ani].yOriginal) >= Math.abs(objectToAnimate[ani].yMove)) {
                  objectToAnimate[ani].moveSwitchYTF = true;
              }

              if (objectToAnimate[ani].startDelayY <= 0) {

                  if (objectToAnimate[ani].moveSwitchYTF == true) {
                      if (objectToAnimate[ani].delayCounterY >= (objectToAnimate[ani].delayTimeY || 0)) {
                          objectToAnimate[ani].moveSwitchY *= -1;
                          objectToAnimate[ani].delayCounterY -=objectToAnimate[ani].delayTimeY;
                          objectToAnimate[ani].moveSwitchYTF = false;
                      } else {
                          objectToAnimate[ani].delayCounterY += 1 * deltaTime;
                      }
                  }

                  if (objectToAnimate[ani].moveSwitchY == 1 && objectToAnimate[ani].moveSwitchYTF == false) {
                      objectToAnimate[ani].y += objectToAnimate[ani].moveSpeedY * objectToAnimate[ani].moveSwitchY * deltaTime;
                      objectToAnimate[ani].delayCounterY = 0;
                  }

                  if (objectToAnimate[ani].moveSwitchY == -1 && objectToAnimate[ani].moveSwitchYTF == false) {
                      objectToAnimate[ani].y += objectToAnimate[ani].moveSpeedY * objectToAnimate[ani].moveSwitchY * deltaTime;
                      objectToAnimate[ani].delayCounterY = 0;
                  }
              } else {
                  objectToAnimate[ani].startDelayY -= 1 * deltaTime;
              }
          }


      }
  }


  function shootingAnimation(objectToShoot) {
      for (let i = 0; i < objectToShoot.length; i++) {
          for (let w = 0; w < walls.length; w++) {
              if (collisionDetect(objectToShoot[i], walls[w])) {
                  objectToShoot[i].isColliding = true;
                  break;
              }
          }
          if (objectToShoot[i].shotFromEnemy == false) {
              for (let b = 0; b < badDudes.length; b++) {
                  if (collisionDetect(objectToShoot[i], badDudes[b])) {
                      objectToShoot[i].isColliding = true;
                      badDudes.splice(i,1);
                      break;
                  }
              }
          }

          if (objectToShoot[i].shotFromEnemy == true) {
              if (collisionDetect(objectToShoot[i], rectangle)) {
                  objectToShoot[i].isColliding = true;
                  playerLossOfLife();
              }
          }

          if (objectToShoot[i].x < 0 || objectToShoot[i].x > gameW) {
              objectToShoot[i].isColliding = true;
          }

          if (objectToShoot[i].isColliding == false) {
              objectToShoot[i].x += objectToShoot[i].moveSpeedX * objectToShoot[i].direction * deltaTime;
          }
          if (objectToShoot[i].isColliding == true) {
              if (objectToShoot[i].shotFromEnemy) {
                  pewCountBadDudes -= 1;
              } else {
                  pewCount -= 1;
              }
              objectToShoot.splice(i, 1);
          }

      }

  }

  let lastLoop = new Date();

  function gameLoop() {
      let thisLoop = new Date();
      let fps = 1000 / (thisLoop - lastLoop);
      //console.log(fps);
      lastLoop = thisLoop;
  }

  loadLevel(); //loads the level once, creating the level select screen
  sprite_sheet.image.src = "/widgets/tato/NephiSprite.png"; // Start loading the image.

  function shootingCooldown() {
      if (rectangle.powerUp == true) {
          if (rectangle.shoot) {
              pewpewCornerIcon[0] = new wall(gameW - gridNum - 10 - (20 * (0)), gridNum * 3 + 4, 10, 10, "lime");
              // rectangle.color =  "lime";
          } else {
              pewpewCornerIcon[0] = 0;
              // rectangle.color =  "red";
          }

          if (rectangle.shoot == false && coolDownCounter == coolDownTime) {
              coolDownCounter = 0;
          }
          if (coolDownCounter < coolDownTime) {
              coolDownCounter += 1
          }
          if (coolDownCounter == coolDownTime) {
              rectangle.shoot = true;
          }
      }
  }

  function mainMenu(temp) {
      if (rectangle.level == 0) {
          for (let i = 0; i < endGoals.length; i++) {
              if (collisionDetect(temp, endGoals[i])) {
                  rectangle.level = i;
                  if (rectangle.level == 0) {
                      rectangle.level = 1;
                      rectangle.storyMode = true;
                  }
                  loadLevel();
              }
          }
      }

  }

  function levelSwitcher() {
      if (levelPusher == true) {
          rectangle.level += 1;
          loadLevel();
          levelPusher = false;
          canWin = true;
      }
  }

  function clearArrays() {
      walls = [];
      movingWalls = [];
      deathWalls = [];
      endGoals = [];
      badDudes = [];
      movingPlatforms = [];
      shootyThings = [];
      badDudesPewPew = [];
      healthPickUps = [];
      teleportWalls = [];
      scoreCounter = [];
      pewCount = 0;
      pewCountBadDudes = 0;
      spawnBlock = 0;
  }



  function clearTextBox() { //clears all textboxes on screen
      let open_text_boxes = document.getElementsByClassName("open");
      
      if(open_text_boxes.length > 0) {
          open_text_boxes[0].classList.add("on");  
          
          
      
          if (controller.shoot) {
              open_text_boxes[0].classList.remove("on"); 
        open_text_boxes[0].classList.remove("open");
        
        
        controller.shoot = 0;
        }
          gamePause = true;
    }
  }


  function gameUnpause() {
      if(gamePause == true) {
          gamePause = false;
      }
  }

  function loadIntroTextBoxes() {
    let intro_text_boxes = document.getElementsByClassName("intro");
    intro_text_boxes[0].classList.add("open");
    intro_text_boxes[1].classList.add("open");
  }

  let initialLoad = 0;

  loop = function (timestamp ) {

    deltaTime = (timestamp - lastTimestamp) / perfectFrameTime;
    lastTimestamp = timestamp;
      
      
      if(gamePause == false) {
          
      gameLoop();

      drawBackground();

      drawSpawnBlock();

      drawMovingPlatforms();
      drawPewpew();

      playerMovement();
      drawBadDudesPewPew();
      
      drawEndGoal();
      
      drawMovingWalls();
      drawTeleportWalls();
      drawRectangle();
      playerAnimation();

      drawWalls();
      drawBadDudes();
      drawDeathWalls();

      
      drawHealthPickups();
      drawCornerIcon();

      shootingCooldown();
      levelSwitcher();
      drawNephi();
          
      if(initialLoad >= 0) {
          initialLoad += 1;
      }
          
          
      if(initialLoad >= 10) {
          loadIntroTextBoxes();
          initialLoad = -100;
      }
          

      } else {
          playerRespawn();
      }
  
      
      gameUnpause();
      clearTextBox();

      window.requestAnimationFrame(loop);
  };


  window.addEventListener("keydown", controller.keyListener)
  window.addEventListener("keyup", controller.keyListener);
  window.requestAnimationFrame(loop);
})
</script>


<div class="flex justify-center relative">
  <div class="game-wrapper">

    <canvas id="gameCanvas" class="on" width="800" height="600"></canvas>


    <div class="text-box intro  order1">
        <p> Welcome to Tato's Grand Adventure!</p>
        <p> By Some magical power, you have been teleported far from home. You need to collect each of the spell plates to recite the incantation to send you home.</p>
        <p> You, as Tato must run (left, right), jump (up/space), and fall through platforms (down) to collect the plates, and make it safely back home.</p>
        <p> The forces of nature are conspiring against you. They have summoned your worst nightmare, little blue boxes to stop your path! Thankfully, you can smash their little heads with a swift stomp.</p>
        <br>
        <p> Press Space to Continue </p>

    </div>

    <div class="text-box intro">
        <p> This is the level select screen! Jump into the spell plates to start Tato's Grand Adventure!</p>
        <br>
        <p> Press Space to Continue </p>
    </div>



    <div class="text-box death-box">
        <p> You Died!</p>
        <p> The forces of nature enjoy your adventure. They have granted you another life.</p>
        <br>
        <p> Press Space to Start your Adventure Again! </p>
    </div>

    <div class="text-box level-end">
        <p> Thank you for playing this level!</p>
        <p> If you want to collect all of the spell plates and make it back home, please go back to the main menu and play Story Mode!</p>
        <br>
        <p> Press Space to Start your Adventure Again! </p>
    </div>

    <div class="text-box story-end order1">
        <p> After a long and treacherous journey, you are finally home. You managed to collect all of the spell plates and foil natures' plans. You safely navigated the woods, caves, and oceans that nature has put in your path to stop your progress. </p>
        <p>You walk into your room, and lay your head on your pillow. You're tired! After all, being as awesome as Tato is pretty exhausting! You close your eyes, and you slowly begin to sleep.</p>
        <p> The End </p>
        <br>
        <p> Space </p>
    </div>


    <div class="text-box story-end credits">

        <p class="end-title"> Credits </p>

        <div class="inner-text-box">
            <p class="end-header"> <u> Guy Who Did Everything </u> </p>
            <p> <i>Marshal Taylor </i> </p>
        </div>
        
            <div class="inner-text-box">
                <p class="end-header"> <u> With a Special Thanks To </u></p>
                <p> <i>My Parents: For raising me and loving me like no one else</i> </p>
                <p> <i>Rachel: For always supporting me and loving me</i> </p>
                <p> <i>Levi: For fan-girling over my code</i></p>
                <p> <i>Aubrey: For play testing, making me laugh so hard</i> </p>

                <p class = "space"> <i>And You: Thank you for playing Tato's Grand Adventure</i> </p>
            </div>
            
            <p class="press_space"> Press Space to Start Your New Adventure </p>
        </div>
    </div>
  </div>
<style>

.game-wrapper {
    text-align: center;
    margin: 1em;
}

.text-box {
    background-color: rgba(210, 180, 140, 1); /*d2b48c dark */ /*light dbb583 */
    border-color: #a1773f;
    border-style: solid;
    border-width: 10px;
    width: 600px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-left: -310px;
    margin-top: -200px;
    text-align: left;
    padding: 10px;  
    opacity: 0;
}

.on {
    opacity: 1;
}

.order1 {
    z-index: 1;
}

.inner-text-box {
    padding-bottom: .4rem;
}
.credits {
    text-align: center;
}

.credits > p {
        margin: 0;
    padding-bottom: 1rem;
}

.end-title {
    font-size: 1.5rem;

}

.press_space {
    padding-top: 2rem;
}

.end-header {
    font-size: 1.1rem;
}

.story-end {
        margin-top: -250px;
}
.space {
    padding-top: 1.2rem;
}

</style>