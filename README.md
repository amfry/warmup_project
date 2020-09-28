# CompRobo: Warmup_project
### Abby Fry and Vienna Scheyer

## Robot Telop
For our teleop, we went with a pretty straight forward implementation with our robot able to move forwards, backwards, turn clockwise,and counter clockwise at varying speeds.  The user can also pause the robot. The key mapping for the desctibed movements are as follows.
![teleop](https://github.com/amfry/warmup_project/blob/master/images/teleop.jpeg)
We opted for the robot to continue moving in the direction of the latest push press until the pause button was pressed because it seemed prefferable to only moving the robot forwards a set amount with each button press.  We also opted to turn rather than have a move left/right command as the driver of the robot could turn the neato's heading to the desired angle rather than driving forwards and trying to turn at the same time.

## Driving in a Square
The robot moves in an approximataly 1 by 1 meter square path by driving in a straight line at a specified speed for set time, then turning counter clockwise for a set time at a set speed. The diagram shows the set time amounts the neato used to turn and drive forward while completing a square.
![Square](https://github.com/amfry/warmup_project/blob/master/images/Square.jpeg)
Using the time implemntation, we needed to spend some time tuning the speed/time paramters of our square.  The end results was still a square that was approximatley 1 by 1.  However, using a time implementation allowed us to focused more time into the other challenges.

We originally attemped to implement an odometery version of driving in a square but where having challenges turning the neato to a precise location.  We pivoted to the time implementation for the sake of moving on but after implemnting other challenges, it seems like a proportional controller could have helped our odometery implemntation move to the desired location.
## Wall Following
 
![Wall States](https://github.com/amfry/warmup_project/blob/master/images/wall_follow_states.jpg)
## Person Following
In person following, the neato pursues a "person," following a specified distance of 1 meter.  To do this, our neato moves through 3 stages.  In stage 1, the neato completes a 360 lidar 
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
