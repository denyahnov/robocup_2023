# `NOT FINISHED YET!`
# Menacing Monkeys
## Soccer Standard - *2023 RoboCup Junior Australia*

<img src="https://user-images.githubusercontent.com/60083582/227090580-5c1e3e4b-3019-415a-8782-f7282df9f62e.png" width="360" height="360" />

### **Contents:**
- [Introduction](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#introduction)
- [Strategy](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#strategy)
	- Game
	- Building
	- Robot Logic
- [Robot Design](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#robot-design)
- [Robot Code](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#robot-code)
- [Photos](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#photos)
	- Last Year's Designs
	- New Prototypes
	- Final Design

### **Introduction:**

We are Dennis, Saum and Jones, a group of year 10s from Melbourne High School. We are a small team of 3 and operate on a weekly basis. We have a variety of experience in various robotics competitions and have competed in RoboCup before.

### **Strategy:**
**Game:**
Our strategy was heavily based on adaptability to the current situation. We wanted to be able to get ball possession as quickly as possible after a ball reset as we found that getting to the ball quick enough and to push it into our opponents direction was enough to gain an advantage in matches. We chose to run 2 robots with the same design, opting out of using a designated 'goalie' design. This was partly due to the previously stated decision, but also because we chose to use inter-robot communication. The ability for the robots to relay information like ball possession would allow them to play defense/offense completely autonomously, without the need of specific roles.

![Soccer Field](https://user-images.githubusercontent.com/60083582/185514513-ba5dd76e-ddfc-4a0a-9a91-03beb1630f51.png)

**Building:**
We found that while powerful robots are good, we wanted a quick robot than could out-manuever the other team. Because of this, our Robots were designed for speed. The choice to use EV3 Medium Motors for our drivebase was a result of this consideration, as we found that the heavier and larger motors are quite bulky and hard to build a solid design with. Here are some of the [prototypes](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#photos) we designed. We learnt new things and improved the robot with every iteration of the design.

**Robot Logic:**
```mermaid
graph LR
FoundBall[Robot can see the ball?] -- No --> Return
FoundBall -- Yes --> Teammate[Teammate has ball?] -- No --> HasBall[Is the robot holding the ball?] -- Yes --> Score(Chase the ball and curve towards the opponent goal)
HasBall -- No --> Chase(Chase the ball and aim forwards)
Teammate -- Yes --> Return(Return to the goal)

IsConnected[Are the robots bluetooth connected?] -- Yes --> Send(Send robot information) --> Receive(Receive other robot information)
Receive --> Process(Process information) --> Send
```
### **Robot Design:**
Originally, our design choices for this competition were to use 2 identical robots with 4 EV3 Medium Motors, 1 BBR 360 IRSeeker, 1 I2C Compass Sensor, 1 EV3 Ultrasonic Sensor and an EV3 Touch Sensor. We decided that the identity between robots would help resolve issues and keep code as similar as possible. However after the State Competition, we decided to swap from the 360 sensor to 2 HiTechnic IrSeeker v2 Sensors because of their accuracy and reliability.

Because of the limited time working on the robot in person, we began testing out with [different robot designs](https://github.com/denyahnov/robocup_2023/blob/main/EngineeringJournal.md#photos) using parts from home or [Studio 2.0](https://www.bricklink.com/v2/build/studio.page), a virtual LEGO builder.

We use 4 motors with omniwheels positioned around the robot to form an X-drive (holonomic), which allows the robot to move in any direction rather than 2. We use omniwheels that are completely legal since they are built from LEGO pieces. Our design is quite unqiue as the motors are stacked on top of each other to reduce the space consumed by them. We then use gear trains to align the wheel shafts in a perfect X.

<img src="https://user-images.githubusercontent.com/60083582/227100512-e9f32a52-ba2e-4808-a4f3-4d94c4be7d3c.png" width="300" height="300" />

This year, we challenged ourselves by using a [BBR IRSeeker](https://irseeker.buildingblockrobotics.com/) which allowed us to have 360 degree infrared vision with just 1 EV3 port used. We had no previous experience using these sensors and through trial and error built our [own wrapper](https://github.com/denyahnov/ir-seeker) based on limited online documentation for easy use of the sensor.

We use the compass for reading our angle which is used in straightening ourselves as well as curving at the opponent goal. We use an  Ultrasonic positioned on the side of our robots to read our position on the field horizontally. This helps the robot figure out where it is on the field at all times. We also use a touch sensor to hit the crossbar of our goal for a defender robot to know it's position.

| **Motor**         |  **Pros**                     |  **Cons**                           |
|------------------ | ----------------------------- | ------------------------------------|
| EV3 Medium Motor  |  Fast, Lightweight, Small     |  Weaker, Need Geartrain for X-Drive |
| EV3 Large Motor   |  Strong, Easy to Incorporate  |  Slower, Bulkier, Heavier           |

### **Robot Code:**
Our robots are coded in [Python](https://www.python.org/) language using the [ev3dev](https://www.ev3dev.org/) library. All our code is publicly available on our [GitHub repository](https://github.com/denyahnov/robocup_2023/). 

We built our own wrappers for [ev3dev](https://github.com/denyahnov/robocup_tools) and the [infrared sensor](https://github.com/denyahnov/ir-seeker). These allowed us to have Custom Menus and ready to use Classes which sped up our coding process.

We have structured our code very methodically. Python allows us to import code from different files and compile it into one main file:
- `behaviours.py` stores all our robot behaviours such as Attack, Chase, Defend, Track, etc
- `brick.py` stores our system functions such as changing brick color and playing a sound
- `calibration.py` allows us to calibrate our sensors as well as storing the values
- `comms.py` allows us to connect the 2 robots via bluetooth and send information between them
- `custom_sensors.py` stores the classes for any custom sensors we use like the IR Seeker
- `drivebase.py` initalises our motors and stores all our movement functions
- `main.py` is the main file that we run
- `menu.py` allows us to run a Graphical User Interface within the program
- `sensors.py` initalises our sensors and stores all the sensor related functions

We started off by using [EV3Sim](https://ev3sim.mhsrobotics.club/), an application developed by the school to practice coding in a virtual environment. It helped us build the foundation of our code while working from home.

We use a holonomic drive which allows us to move in any direction. We use a simple formula to calculate each motor's speed based on a given angle from 0-360 degrees. 

![Holonomic Logic](https://user-images.githubusercontent.com/60083582/227095958-4d676bfd-1925-47ca-b222-6488c20c24c1.png)

Our code accounts for robot inconsistency and faulty sensors. The main chunk of logic stays the same but small functions like converting ball position to robot direction has configurable variables that shift between robots. We use algorithms to average our Ultrasonic sensor values remove outliers, excluding any extremely rapid increases/decreases in value as to account for objects blocking the ultrasonic.

We use bluetooth for communication between robots. We have one robot run as a server and the other connects afterwards as a client. The robots relay whatever information they recieve between themselves e.g. Ball Possession, Current Attack/Defense State, etc.

We do not use any sensors like touch or colour to detect if the robot has possession of the ball, instead we use the infrared proximity. We instead use a touch sensor to hit the crossbar of our goal for the robot to know it's position.

We even tried using odometry to locate our robot on the field without the use of sensors. By using the motor degree positions, we could estimate where we were on the field given we calibrate before the match begins. Unfortunately, we found that referees picking our robots up and robot being knocked over would ruin the data, providing an inaccurate location.

We made an easy way for us to debug code and see sensor values by visualing the robot position. We pass it the ball angle and strength, and it returns out an x,y position.

![RobotPosition](https://user-images.githubusercontent.com/60083582/230255733-2c85afd2-8f82-41af-99da-d7c4d70fbb2c.png)

We use a cubic function to correct our turning angle based on how far we are from a target angle.

![CompassFix](https://user-images.githubusercontent.com/60083582/227074173-46f1c8af-d7eb-4157-b3d9-9cbd1b7b24a6.png)

During our testing, we found it hard to see what the robot was actually thinking. This led us to developing a graphical visualiser which could replay matches based on data that the robot saved.

```mermaid
graph LR
input[Sensor Input] -- Infrared --> IrInput(Return value from 0-11)
input -- Compass --> cInput[Compass value?]
cInput -- 3-179 --> left(Curve left)
cInput -- 180-356 --> right(Curve Right)
cInput -- Else --> straight(Do nothing)
right --> formula(Curve speed = angle from '0')
left --> formula
input -- Ultrasonic --> question[Greater than 20cm change from average of previous values?]
question -- Yes --> dont(Do nothing)
question -- No --> do(Append value to previous values)
do --> remove(Remove last value in list)
dont --> returnUltrasonic(Return list)
remove--> returnUltrasonic
```

![IrSensorValues](https://user-images.githubusercontent.com/60083582/185833817-af29420e-4e08-4fae-9abd-7d05557f1ff4.png)
![CompassValue](https://user-images.githubusercontent.com/60083582/186033284-3bef35e7-2be7-4249-83a1-fac46f4491df.png)

### **Photos:**
#### **Last year's designs:**

![First Prototype](https://media.discordapp.net/attachments/496240143494021120/939835121182330930/SoccerV2.png?width=210&height=270)
![Second Prototype](https://media.discordapp.net/attachments/516360486963380226/946962209639112735/UpdatedSoccerRobotRENDER.png?width=200&height=270)

#### **New Prototypes:**

**Design 1 - Version 1**

<img src="https://user-images.githubusercontent.com/60083582/230257264-2f7419bf-bab1-4634-87e6-0409e55ef248.png" width="360" />
<img src="https://user-images.githubusercontent.com/60083582/230257456-4955fd23-e41b-432a-8cb7-a6fdf5049263.png" width="360" /> <img src="https://user-images.githubusercontent.com/60083582/230257349-0c4ab067-466c-4c03-94e7-0b5d71e42a03.png" width="360" />
<img src="https://user-images.githubusercontent.com/60083582/230256085-a9555cdb-e4b2-482b-9931-5c6ec12b5264.png" width="360" />

**Design 2 - Version 1**

![image](https://user-images.githubusercontent.com/60083582/230258032-899a1230-2334-4c0a-a047-4b62b191e06b.png)
![image](https://user-images.githubusercontent.com/60083582/230258107-171fc435-bbdb-4fb4-a04e-db65f6f90277.png)

**Design 2 - Version 2**

![image](https://user-images.githubusercontent.com/60083582/230258166-d5174a03-47a2-4ad5-a62c-9602cc66eb3c.png)
![image](https://user-images.githubusercontent.com/60083582/230258195-797eac9a-fffd-4687-8047-189e902da71b.png)

**Design 2 - Version 3**

![image](https://user-images.githubusercontent.com/60083582/230258247-6c0dbc3a-5a2c-4bb5-9fad-a14b6fcbc730.png)
![image](https://user-images.githubusercontent.com/60083582/230258271-b015fc5c-c455-4454-bb9f-b8812adeb6ee.png)
![image](https://user-images.githubusercontent.com/60083582/230258322-29c1c040-eedf-4c4e-b4cf-2da40a71147b.png)
![image](https://user-images.githubusercontent.com/60083582/230258355-c1d53f5d-f209-4015-8adc-72d1b82baa36.png)

**Design 2 - Version 4**

![image](https://user-images.githubusercontent.com/60083582/230258418-cd5758f5-e152-4b9f-9e1e-71a2a10e5a92.png)
![image](https://user-images.githubusercontent.com/60083582/230258454-ddbf192e-e1ab-43d5-89bf-22e2e8469e64.png)
![image](https://user-images.githubusercontent.com/60083582/230258480-8d4384aa-320e-462f-9de3-6b786289c59c.png)

#### **Design 2 - Version 5:**

![image](https://user-images.githubusercontent.com/60083582/230258539-e521a508-2f07-4a3d-a17a-2d58501dd646.png)
![image](https://user-images.githubusercontent.com/60083582/230258560-5d401c4e-737a-471c-8a9a-25891a8b691b.png)

#### **Victorian States Design:**

![image](https://github.com/denyahnov/robocup_2023/assets/60083582/6d5b1373-2f81-4e98-865d-0b89b5a4a8b5)
![image](https://github.com/denyahnov/robocup_2023/assets/60083582/328e3627-a649-4c43-9420-3d394e3de9db)
![image](https://github.com/denyahnov/robocup_2023/assets/60083582/2ee3b8eb-cbce-469b-8b42-47199ec4e8b7)
![image](https://github.com/denyahnov/robocup_2023/assets/60083582/587b9218-9e17-46f8-aaa7-f8989f75105e)
![image](https://github.com/denyahnov/robocup_2023/assets/60083582/5a64abe9-954e-47d5-a26f-40be6953225b)

#### **Australian Nationals Redesign**
<img src="https://user-images.githubusercontent.com/60083582/265250889-06a9cfff-e295-4625-8d7a-5240a8fb9ef3.png" width="400" />
<img src="https://user-images.githubusercontent.com/60083582/265252366-8d4aa6f5-07aa-4f8b-80b4-f4d2adc59690.png" width="400" />

