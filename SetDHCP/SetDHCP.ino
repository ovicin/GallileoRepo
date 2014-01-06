void setup() {
  // put your setup code here, to run once:
  
  system("telnetd -l /bin/sh");
  system("udhcpc -i eth0"); /*restart the dhcp client*/


}

void loop() {
  // put your main code here, to run repeatedly: 
  system("ifconfig eth0 > /dev/ttyGS0");
}
