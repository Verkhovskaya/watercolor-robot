import serial
import time
import math

# Height
paper_height = 100;
sponge_height = 100;
brush_lengths = {
	1: 300,
	2: 300,
	3: 300,
	4: 300,
	5: 300
}
brush_height = brush_lengths[1]

# Swing
carry_position = "s050"
color_load_start = "s070"
color_load_end = "s095"

# X/Y location
color_locations = {
	'light-purple': 'x080 z560', # correct
	'dark-purple': 'x220 z700', # correct
	'light-green': 'x080 z820', # correct
	'dark-green': 'x220 z820', # correct
	'brown': 'x080 z970', # correct
	'dark-grey': 'x220 z970', # correct
	'dark-red': 'x080 z420', # correct
	'light-red': 'x220 z420', # correct
}
paper_x_start = 430
paper_x_end = 999
paper_z_start = 800
paper_z_end = 380

MAX_ANGLE_SHARPNESS = math.pi/6
MAX_TRAVEL_PER_STEP = 10

# Rotation
steps_per_circle = 400


class FakeSerial:
	def __init__(self):
		self.i = True;
		self.position = [0,0,0,0,0]

	def readline(self):
		self.i = not self.i
		if self.i:
			return "Command finished"
		else:
			return ' '.join([str(i) for i in self.position])

	def write(self, new_location):
		print(new_location)
		locations = new_location.rstrip().split(" ")
		for location in locations:
			dim = {'x': 0, 'y': 1, 'z': 2, 'r': 3, 's': 4}[location[0]]
			num = int(location[1:])
			self.position[dim] = num

def send(text):
	ser.write(text + '\n')     # write a string
	print('Sent command ' + text)
	while(ser.readline().rstrip() != "Command finished"):
		pass
	new_position = [abs(int(x)) for x in ser.readline().rstrip().split(' ')]
	for i in range(5):
		current_position[i] = new_position[i]

def clean():
	send(carry_position + " y" + to_command(brush_height) + " r" + to_command(steps_per_circle))
	send("z100 x420")
	send("y" + to_command(sponge_height + brush_height))
	for i in range((800-420)/20+1):
		x = str(420 + i*20).zfill(3)
		if (i%2 == 0):
			s = "060"
		else:
			s = "110"
		send("x" + x + " s" + s)
	send("y" + to_command(brush_height))
	send(carry_position)

def to_command(num):
	return str(max(0, (min(999, int(num))))).zfill(3)

def scale_to_board(x_img, z_img):
	x_board = x_img*(paper_x_end-paper_x_start)/100+paper_x_start
	z_board = z_img*(paper_z_end-paper_z_start)/100+paper_z_start
	return x_board, z_board

def rotation_to_travel_angle(rotation):
	rotation_angle = rotation*(2*math.pi)/steps_per_circle
	return rotation_angle - math.pi/2

def travel_angle_to_rotation(angle):
	rotation_angle = angle + math.pi/2
	return (rotation_angle*steps_per_circle/(2*math.pi))

def start_at(x_img, z_img, x_target, z_target):
	x_board, z_board = scale_to_board(x_img, z_img)
	destination_angle = math.atan2(z_board-current_position[2],x_board-current_position[0])
	x_str = to_command(x_board)
	z_str = to_command(z_board)
	r_str = to_command(travel_angle_to_rotation(destination_angle))
	send("x" + x_str + " z" + z_str)
	send("r" + r_str)
	send("s090")
	send("y" + to_command(paper_height + brush_height))

def move_to(x_img, z_img):
	x_board, z_board = scale_to_board(x_img, z_img)
	current_angle = rotation_to_travel_angle(current_position[3])
	destination_angle = math.atan2(z_board-current_position[2],x_board-current_position[0])
	while abs(current_angle - destination_angle) > math.pi:
		if current_angle - destination_angle > math.pi:
			destination_angle += math.pi*2
		else:
			destination_angle -= math.pi*2
	angle_change = destination_angle - current_angle
	if abs(angle_change) > MAX_ANGLE_SHARPNESS:
		angle_change = angle_change/abs(angle_change)*MAX_ANGLE_SHARPNESS
	print(angle_change)
	travel_angle = current_angle + angle_change
	distance_to_destination = ((current_position[0]-x_board)**2 + (current_position[2]-z_board)**2)**0.5
	travel_distance = min(MAX_TRAVEL_PER_STEP, distance_to_destination)
	destination_x = current_position[0] + travel_distance*math.cos(travel_angle)
	destination_z = current_position[2] + travel_distance*math.sin(travel_angle)
	x_str = to_command(destination_x)
	z_str = to_command(destination_z)
	r_str = to_command(travel_angle_to_rotation(travel_angle))
	send("x" + x_str + " z" + z_str + " r" + r_str)
	if (abs(current_position[0] - x_board) > 4) or (abs(current_position[2]-z_board) > 4):
		move_to(x_img, z_img) 

def end_line():
	send("y" + to_command(brush_height))
	send(carry_position)

def load_color(color):
	send("y" + to_command(brush_height))
	location = color_locations[color]
	send(location + ' r' + to_command(steps_per_circle) + ' ' + carry_position)
	for i in range(3):
		send(color_load_start)
		send(color_load_end)
	send(carry_position)

def reset():
	send(carry_position)
	send("r000 y000")
	send("s000")
	send("x000 z000")
	print("RESET")

def switch_brush(new_brush):
	send("y000")
	send("z999 x500")
	send("r" + to_command(steps_per_circle))
	print("Switch to brush " + str(new_brush))
	global brush_height
	brush_height = brush_lengths[new_brush]
	raw_input()

def house():
	clean()
	load_color('dark-green')
	start_at(0,70,100,70)
	move_to(100,70)
	end_line()
	clean()
	load_color('brown')
	start_at(40,30,40,60)
	move_to(40,60)
	move_to(60,60)
	move_to(60,30)
	move_to(40,30)
	clean()
	reset()


ser = FakeSerial() #serial.Serial('/dev/cu.usbmodem1411') # FakeSerial()
print(ser.readline())
current_position = [0,0,0,0,0]
send(carry_position + " z100" + " r" + to_command(steps_per_circle)) # load initial position
