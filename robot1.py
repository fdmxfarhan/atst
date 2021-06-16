from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils
from math import *

class MyRobot1(RCJSoccerRobot):
    def readAll(self):
        self.orientation = (self.data[self.name]['orientation'] * 180)/pi
        self.x_robot = self.data[self.name]['x']
        self.y_robot = self.data[self.name]['y']

        self.x_ball = self.data['ball']['x']
        self.y_ball = self.data['ball']['y']

        ####################################### Find The goal keeper robot
        x_robot_1 = self.data['Y1']['x']
        y_robot_1 = self.data['Y1']['y']
        
        x_robot_2 = self.data['Y2']['x']
        y_robot_2 = self.data['Y2']['y']
        
        x_robot_3 = self.data['Y3']['x']
        y_robot_3 = self.data['Y3']['y']
        
        distance1 = sqrt((x_robot_1 - self.x_ball)**2 + (y_robot_1 - self.y_ball)**2)
        distance2 = sqrt((x_robot_2 - self.x_ball)**2 + (y_robot_2 - self.y_ball)**2)
        distance3 = sqrt((x_robot_3 - self.x_ball)**2 + (y_robot_3 - self.y_ball)**2)

        if(self.name[1] == '1'):
            if(distance1 > distance2 and distance1 > distance3):
                self.role = 'GoalKeeper'
            else: self.role = 'Forward'
        if(self.name[1] == '2'):
            if(distance2 > distance1 and distance2 > distance3):
                self.role = 'GoalKeeper'
            else: self.role = 'Forward'
        if(self.name[1] == '3'):
            if(distance3 > distance2 and distance3 > distance1):
                self.role = 'GoalKeeper'
            else: self.role = 'Forward'
        


    def move(self, x, y):
        robot_pos = self.data[self.name]
        target_pos = {'x': x, 'y': y}
        angle, robot_angle = self.get_angles(target_pos, robot_pos)
        direction = utils.get_direction(angle)
        if direction == 0:
            left_speed = -10
            right_speed = -10
        else:
            left_speed = direction * 10 - 5
            right_speed = direction * -10 -5
        if(left_speed > 10): left_speed = 10
        if(left_speed <-10): left_speed =-10
        if(right_speed > 10): right_speed = 10
        if(right_speed <-10): right_speed =-10
        
        self.left_motor.setVelocity(left_speed)
        self.right_motor.setVelocity(right_speed)
    def motor(self, left_speed, right_speed):
        if(left_speed > 10): left_speed = 10
        if(left_speed <-10): left_speed =-10
        if(right_speed > 10): right_speed = 10
        if(right_speed <-10): right_speed =-10
        
        self.left_motor.setVelocity(left_speed)
        self.right_motor.setVelocity(right_speed)

    def run(self):
        self.role = 'Forward'
        passedGoal = False
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                self.data = self.get_new_data()
                self.readAll()
                if(self.role == 'Forward'):
                    # Robot Behind ball -> move ball to the goal
                    if(self.x_robot < self.x_ball and self.x_robot > self.x_ball-0.17 and self.y_robot > self.y_ball-0.1 and self.y_robot < self.y_ball + 0.1):
                        self.move(self.x_ball, self.y_ball)
                    # go behind the ball
                    else:
                        # When Robot is after ball (goal be khodi nazane)
                        if(self.x_robot > self.x_ball and self.y_robot > self.y_ball-0.1 and self.y_robot < self.y_ball + 0.1):
                            if(self.y_ball > self.y_robot):
                                self.move(self.x_ball - 0.1, self.y_ball - 0.2)
                            else:
                                self.move(self.x_ball - 0.1, self.y_ball + 0.2)
                        else:
                            self.move(self.x_ball - 0.1, self.y_ball)
                elif(self.role == 'GoalKeeper'):
                    if(self.x_robot > -0.6 and not passedGoal): 
                        self.move(-0.7, self.y_ball)
                    else:
                        if(self.x_robot < -0.5):    passedGoal = False
                        else:                       passedGoal = True
                        
                        if(self.y_ball > self.y_robot):
                            self.motor(-8 -(self.orientation * 20) /180, -8 + (self.orientation * 20) /180)
                        else:
                            self.motor(8 -(self.orientation * 20) /180, 8 + (self.orientation * 20) /180)
                
                
