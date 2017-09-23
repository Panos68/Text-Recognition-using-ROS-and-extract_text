import os
import sys
import difflib
import time
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

number=0
dictionary=["TURN RIGHT","TURN LEFT","STOP"]

def twist_robot(angular_speed, duration,direction):
	'''
	'''
	msg = Twist()
	msg.linear.x = 0
	msg.linear.y = 0
	msg.linear.z = 0
	msg.angular.x = 0
	msg.angular.y = 0

	if direction == "TURN RIGHT":
		sense = -1.0
	elif direction == "TURN LEFT":
		sense = 1.0
	elif direction == "STOP":
		sense = 0

	msg.angular.z = sense*float(angular_speed)
	
	init_time = rospy.Time.now()
	end_time = rospy.Time.now()

	pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
	
	while (end_time - init_time).to_sec() < duration:
		pub.publish(msg)
		end_time = rospy.Time.now()
		time.sleep(0.2)

	msg.angular.z = 0
	pub.publish(msg)


def callbacktwist(direction):
	twist_robot(0.4,5,direction.data)

if __name__ == '__main__':
    try:
	while not rospy.is_shutdown():
		rospy.init_node('talker', anonymous=True)
		rospy.Subscriber("chatter", String, callbacktwist)
		rate = rospy.Rate(10) # 10hz
		pub = rospy.Publisher('chatter', String, queue_size=1)
		while True:
			os.system("rosservice call /image_saver/save")
			os.system("tesseract camperapic.jpg before_extract")
			os.system("python extract_text.py camerapic.jpg"+" extract1.png")
			os.system("tesseract "+"extract1.png"+" after_extract")

			filenames = ["before_extract.txt", "after_extract.txt"]
			with open('/home/panos/thesis/finaltext.txt', 'w') as outfile:
			    for fname in filenames:
				with open(fname) as infile:
				    outfile.write(infile.read())

			with open('finaltext.txt', 'r') as myfile:
				data=myfile.readlines()	
		
			for x in range(0, len(data)):
				for y in range(0, len(dictionary)):
					seq=difflib.SequenceMatcher(None, dictionary[y],data[x])	
					d=seq.ratio()*100
					if (d>60):
						print(dictionary[y])
						msg=String()
						msg.data=dictionary[y]
						pub.publish(msg)
    except rospy.ROSInterruptException:
        pass
