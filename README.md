# DrawToMars
Takes an image as input, detects triangles and circles using OpenCV, and creates a minigame based on the original image, using Pygame.
### How it works:
+ Triangles turn into asteroids and planets. The size of the shape determines the size and speed of the in-game object.
+ Circles turn into wormholes. They can randomly teleport the car to different wormholes.
+ Fuel is determined by the total number of drawn objects.
+ If the car runs out of fuel, the game waits a few seconds and resets the car.

### Controls:
+ Up = Thrust
+ Left, Right = Direction
+ Down = Slow Down

![](https://raw.githubusercontent.com/LedioTerolli/DrawToMars/master/gif_starter_1.gif)
![](https://raw.githubusercontent.com/LedioTerolli/DrawToMars/master/example.gif)

### License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
