bool standby = true;
bool record = false;
bool b1 = false;
bool b2 = false;
bool b3 = false;
bool b4 = false;
bool b5 = false;
bool b6 = false;

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
    starttime = senddata(starttime,1234.5678,69,17,25.49,128.6,438.80125,1,1,1,1,1,1);
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
