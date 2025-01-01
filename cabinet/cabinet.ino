#include <Keypad.h>
#include <Servo.h>
#include <SoftwareSerial.h>


const int REED_PIN = 13;  
const int red_led = 12;
const int green_led = 11;
const int blue_led = 10;
String str;
Servo myservo;

bool lockstate=true;



const byte ROWS = 4; 
const byte COLS = 3; 
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {8, 7, 6,5}; 
byte colPins[COLS] = {4, 3,2}; 
//Create an object of keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );



void setup() {
  pinMode(REED_PIN, INPUT_PULLUP); 
  pinMode(red_led, OUTPUT);
  pinMode(green_led, OUTPUT);
  pinMode(blue_led, OUTPUT);
  myservo.attach(9);
  myservo.write(0);

  Serial.begin(9600);
  digitalWrite(red_led, LOW);  
  digitalWrite(green_led, HIGH); 
  digitalWrite(blue_led, LOW);  
}




void blink() {
    digitalWrite(red_led, HIGH);
    digitalWrite(green_led, LOW);
    digitalWrite(blue_led, LOW);
    delay(100);
    digitalWrite(red_led, LOW);
    digitalWrite(green_led, HIGH);
    digitalWrite(blue_led, LOW);
    delay(100);
}

void turn_on() {
  myservo.write(0);
  digitalWrite(red_led, LOW);
  digitalWrite(green_led, HIGH);
  digitalWrite(blue_led, LOW);
}

void turn_off() {
  myservo.write(90);
  digitalWrite(red_led, HIGH);
  digitalWrite(green_led, LOW);
  digitalWrite(blue_led, LOW);
}

void read_keyboard() {
  String key_string = ""; 
    char key = keypad.getKey();
    if (key=='*'){
      while (true) {
        key = keypad.getKey(); 
        if (key) { 
            if (key == '#') { 
                break;
            }
            key_string += key;
      }
    }
  }


    if (key_string.length() > 0) {
        Serial.println(key_string);
    }
}

void loop() {
  read_keyboard();


 if (Serial.available()) {
    str = Serial.readStringUntil('\n');
    str.trim(); 

    if (str == "turn_on") {       
        turn_on();
        lockstate = true;
    } 
    else if (str == "turn_off") {
        turn_off();
        lockstate = false;
    }
    else if (str == "not pass") {
        blink();
        lockstate = false;
    }
}

}

