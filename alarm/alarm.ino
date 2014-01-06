
typedef enum{
  INACTIVE = 0,
  ACTIVE
}enAlarmState;

// digital pin 2 has the alarm zone 1 attached
int alarmZone1 = 2;
enAlarmState alarmZone1State;



// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(alarmZone1, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  pollAlarmInput();
  
  // print out the state of the alarm:
  //Serial.println(alarmZone1State);
  delay(1);        // delay in between reads for stability
}

void pollAlarmInput(void)  {
  enAlarmState oldalarmZone1State = alarmZone1State;
  alarmZone1State = (enAlarmState)digitalRead(alarmZone1);
  
  if (alarmZone1State != oldalarmZone1State) //alarm state changed
    if (alarmZone1State)
      Zone1IntrusionCallback();
}

void Zone1IntrusionCallback(void){
  /* send email */
  system("python /home/root/python_scripts/send_mail.py");
  Serial.println(alarmZone1State);
}


