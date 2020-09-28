# CompRobo: Warmup_project
### Abby Fry and Vienna Scheyer

## Robot Telop
For our teleop, we went with a pretty straight forward implementation using keyboard input. The key mapping is as follows:
![teleop](https://github.com/amfry/warmup_project/blob/master/images/teleop.jpeg)

## Driving in a Square
![Square](https://github.com/amfry/warmup_project/blob/master/images/Square.jpeg)
## Wall Following
![Wall States](https://github.com/amfry/warmup_project/blob/master/images/wall_follow_states.jpg)
## Person Following
## Object Avoidance
![avoid](https://github.com/amfry/warmup_project/blob/master/images/avoidance.jpeg)
## FS Control
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
