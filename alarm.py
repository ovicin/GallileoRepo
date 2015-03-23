import smtplib
import mraa
import time, threading

ZONE_INPUT_PIN = 6
RELAY_OUTPUT_PIN = 8
ALARM_LED_PIN = 8
ALARM_SW_PIN = 7

def zoneInputISR():
	print("Zone Input ISR")
	a.UpdateZoneInputState()
	
def buttonISR():
	print("Button ISR")
	if a.GetArmedState():
		a.Disarm()
	else:
		a.Arm()
	
class Alarm:
	def __init__(self):
		
		self.armed = 0
		self.arming = 0
		self.inputState = 0
		self.relayState = 0
		self.ledState = 0
		self.alarmState = 0
	
		#configure zone input pin
		self.zoneInput = mraa.Gpio(ZONE_INPUT_PIN) 
		self.zoneInput.dir(mraa.DIR_IN)
		self.zoneInput.isr(mraa.EDGE_BOTH, zoneInputISR, zoneInputISR)
		
		#configure led pin 
		self.led = mraa.Gpio(ALARM_LED_PIN)
		self.led.dir(mraa.DIR_OUT)

		#configure button pin
		self.button = mraa.Gpio(ALARM_SW_PIN)
		self.button.dir(mraa.DIR_IN)
		self.button.isr(mraa.EDGE_BOTH, buttonISR, buttonISR)
		
		#configure relay pin
		self.relay = mraa.Gpio(RELAY_OUTPUT_PIN)
		self.relay.dir(mraa.DIR_OUT)
		
	def GetArmedState(self):
		return self.armed
	
	def SetArmedState(self):
		print("Armed")
		self.armed = 1
		self.arming = 0
	
	def Disarm(self):
		print("Disarmed")
		self.alarmState = 0
		self.armed = 0
	
	def Arm(self):
		#start arm timer
		print("Arm Alarm in 10s")
		self.arming = 1
		threading.Timer(10, self.SetArmedState).start()
	
	def UpdateZoneInputState(self):
		self.inputState = self.zoneInput.read()
		
	def Process(self):
		print("Armed " + str(self.armed))
		print("InputState " + str(self.inputState))
		
		if self.armed:
			#Toogle LED
			self.ledState = not self.ledState
			if (self.inputState and not self.alarmState):
				#we are armed and we have an alarm
				#activate the output relay
				self.relayState = 1
				#self.send_email()
				self.alarmState = 1
		else:
			self.relayState = 0
			if self.arming:
				#if arming turn the led on
				self.ledState = 1
			else:
				#if not arming turn the led off
				self.ledState = 0
				
		self.led.write(self.ledState)
		self.relay.write(self.relayState)
		
		#Process calls itself each 1s
		threading.Timer(1, self.Process).start()
	
	def send_email():
		gmail_user = "xxx@gmail.com"
		gmail_pwd = "xxx"
		FROM = 'xx@gmail.com'
		TO = ['xx@yahoo.com'] #must be a list
		SUBJECT = "Testing sending using gmail"
		TEXT = "Testing sending mail using gmail servers"
		# Prepare actual message
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
		""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
		try:
			#server = smtplib.SMTP(SERVER) 
			server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
			server.ehlo()
			server.starttls()
			server.login(gmail_user, gmail_pwd)
			server.sendmail(FROM, TO, message)
			#server.quit()
			server.close()
			print 'successfully sent the mail'
		except:
			print "failed to send mail"
		
a = Alarm()
a.Process()


time.sleep(500)
	

