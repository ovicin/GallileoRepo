void setup() {
  // put your setup code here, to run once:
  system("telnetd -l /bin/sh");
  system("ifconfig eth0 169.254.1.1 netmask 255.255.0.0 up");

}

void loop() {
  // put your main code here, to run repeatedly: 
  
}
