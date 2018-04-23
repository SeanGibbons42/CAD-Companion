<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
#include "CurieIMU.h"

bool standby = false;
bool record = true;
=======
bool standby = true;
bool record = false;
>>>>>>> parent of 56e7b1f... Buttons - Arduino - Graph
=======
bool standby = true;
bool record = false;
>>>>>>> parent of 56e7b1f... Buttons - Arduino - Graph
bool b1 = false;
bool b2 = false;
bool b3 = false;
bool b4 = false;
bool b5 = false;
bool b6 = false;
<<<<<<< HEAD
=======
bool standby = true;
bool record = false;
int b1 = 0;
int b2 = 0;
int b3 = 0;
int b4 = 0;
int b5 = 0;
int b6 = 0;
>>>>>>> 684ec3f74acc220ed1c39547f896df7c79f5c95f
=======
>>>>>>> parent of 56e7b1f... Buttons - Arduino - Graph

unsigned long starttime = millis();

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(19200);
}

void loop()
{
  // First check to see if there is a new message
  if (Serial.available())
  {

    String message = Serial.readString();
    //Check message to see if we need to change mode
    if (message.equals("r\n"))
    {
      standby = false;
      record = true;
    }
    else if (message.equals("s\n"))
    {
      standby = true;
      record = false;
    }
    else if (message.equals("c\n"))
    {
      calibrate();
    }
  }

  //if we are in record mode we will send some data to the computer
  if(record)
  {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    for(byte button = 0; button < 4; button++){but_vals[button] = digitalRead(but_pins[button]);}
    double imudat[6];
    
    poll_imu(&imudat[0]);    
    starttime = senddata(starttime,imudat[0],imudat[1],imudat[2],imudat[3],imudat[4],imudat[5],but_vals[0],but_vals[1],but_vals[2],but_vals[3],1,1);
    //starttime = senddata(starttime,1234.5678,69,17,25.49,128.6,438.80125,but_vals[0],but_vals[0],but_vals[0],but_vals[0],1,1);
=======
    //buttons attached to pins 13-8
    b1 = digitalRead(13);
    b2 = digitalRead(12);
    b3 = digitalRead(11);
    b4 = digitalRead(10);
    b5 = digitalRead(9);
    b6 = digitalRead(8);
    starttime = senddata(starttime,1234.5678,69,17,25.49,128.6,438.80125,b1,b2,b3,b4,b5,b6);
>>>>>>> 684ec3f74acc220ed1c39547f896df7c79f5c95f
=======
    starttime = senddata(starttime,1234.5678,69,17,25.49,128.6,438.80125,1,1,1,1,1,1);
>>>>>>> parent of 56e7b1f... Buttons - Arduino - Graph
=======
    starttime = senddata(starttime,1234.5678,69,17,25.49,128.6,438.80125,1,1,1,1,1,1);
>>>>>>> parent of 56e7b1f... Buttons - Arduino - Graph
  }
  //no matter what mode we are in we want to wait a bit
  delay(100);
}

void calibrate()
{
  //idk what to do here
}

void printeight(double b)
{
  //move the first four decimal places in front of the decimal
  int a = b*10000;

  int digits[8] = {0,0,0,0,0,0,0,0};
  for(int i=7;i>=0;i--)
  {
    //we assemble the array in reverse order, since a%10 returns the ones digit
    digits[i] = a%10;
    a = a/10;
  }
  for(int i=0;i<8;i++)
  {
    //since we assembled backwards, we can print going forwards
    Serial.print(digits[i]);
  }
}

void printfour(unsigned long b)
{
  //turn our unsigned long into an integer (pretty sure this wont cause issues)
  int a = b;
  int digits[4] = {0,0,0,0};
  for(int i=3;i>=0;i--)
  {
    digits[i] = a%10;
    a = a/10;
  }
  for(int i=0;i<4;i++)
  {
    Serial.print(digits[i]);
  }
}

int senddata(unsigned long lasttime, double ax, double ay, double az, double gx, double gy, double gz, bool b1, bool b2, bool b3, bool b4, bool b5, bool b6)
{
  //get the current time
  unsigned long currenttime = millis();

  unsigned long deltat = (double)(currenttime - lasttime);

  printfour(deltat);

  Serial.print('A');

  printeight(ax);
  Serial.print('#');

  printeight(ay);
  Serial.print('#');

  printeight(az);
  Serial.print("#G");

  printeight(gx);
  Serial.print('#');

  printeight(gy);
  Serial.print('#');

  printeight(gz);
  Serial.print("#B");

  Serial.print(b1);
  Serial.print('#');

  Serial.print(b2);
  Serial.print('#');

  Serial.print(b3);
  Serial.print('#');

  Serial.print(b4);
  Serial.print('#');

  Serial.print(b5);
  Serial.print('#');

  Serial.print(b6);
  Serial.print("#\n");

  return currenttime;
}
