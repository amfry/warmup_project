# CompRobo: Warmup_project
### Abby Fry and Vienna Scheyer

## Robot Telop
For our teleop, we went with a pretty straight forward implementation where our robot can move forwards and backwards and turn clockwise and counter clockwise at varying speeds.  The user can also pause the robot. The key mapping for the described movements are as follows.
![teleop](https://github.com/amfry/warmup_project/blob/master/images/teleop.jpeg)
We opted for the robot to continue moving in the direction of the most recent key press until the pause key was pressed because it seemed preferable to only moving the robot forwards a set amount with each key press.  We also opted to turn rather than have a move left/right command so that the driver of the robot could turn the neato's heading to the desired angle rather than driving forwards and trying to turn at the same time.

## Driving in a Square
The robot moves in an approximately 1 by 1 meter square path by first driving in a straight line at a specified speed for set time and then turning counter clockwise for a set time at a set speed. The diagram shows the timing increments the neato used to turn and drive forward while completing a square.
![Square](https://github.com/amfry/warmup_project/blob/master/images/Square.jpeg)
Using the time implementation, we had to tune the speed/time paramters of our square. Despite this additional tuning step, the time implementation was overall a quick process and it allowed us to focused more on other challenges.

We originally attemped to implement an odometery version of driving in a square but we where having challenges turning the neato to a precise location.  We pivoted to the time implementation for the sake of moving on. After gaining experience from the other challenges, we see that perhaps a proportional controller could have helped our odometery implementation be more successful.

## Wall Following
In the wall following behavior, the neato aims to position itself parallel to the wall. Using lidar sensors at 
 
![Wall States](https://github.com/amfry/warmup_project/blob/master/images/wall_follow_states.jpg)
## Person Following
In person following, the neato pursues a "person" by following at a specified distance of 1 meter.  To do this, our neato begins by performing a 360 lidar scan to check for a person. If all lidar values are infinity that means no person is present, but if any lidar values are non-infinite we add those values to a lidar_range_list. We use the minimum value in the lidar_range_list to determine the desired heading because theoretically the center of a round object will be the closest point. If this desired heading is within +/- 3 degrees of the neato's current heading, the neato drives forward until it is within range of the person. Otherwise, the neato rotates until it is facing the person. For the rotation we use proportional control so that the neato comes to a smooth stop at the desired heading. The following diagram shows the neato registering the presence of a person, turning towards the person, and then moving towards the person.
![follow](https://github.com/amfry/warmup_project/blob/master/images/follow.jpeg)
## Object Avoidance
case 1: neato can't go
case 2 and 3: neato can go
neato operates by turning and driving til a case 2 or 3 can be achieved
![avoid](https://github.com/amfry/warmup_project/blob/master/images/avoidance.jpeg)
## Finite State Control
![Finite State Machine](https://github.com/amfry/warmup_project/blob/master/images/CompRobo_FSM.jpeg)
Our implementation of an FSM controller moves between the neato moving in a square and following a person depending on wether or not a person is picked up on the neato's lidar scan.
## Overal Project

### Code Structure
Each behavior implemented is it's own class.  Each class has a run method that is called in the main function. The run method calls various helper function, such as monitoring if the desired position of the robot has been achieved.  In each class we also defined many attributes in the init method, some of which were updated to new values while the program was running.
### Challenges/Areas for Improvment
### Key takeways
* Incremental development:
* Drawing as a planning tool:
* Realistic goals: When starting to project we had hopes of not doing the simplest implpmentation of every challenge.  However, we are both new to ROS and found the learning curve at the beginning quite steep. This led to us spending a lot of time on some of the early challenges with limited successs and then ended up still needing to pivot to simpler implementations.  It probably would have been better for us to do the simple strategy first and then go back and try more the more difficult strategies if there was still time left.
