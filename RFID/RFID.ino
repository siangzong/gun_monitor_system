#include <Adafruit_Fingerprint.h>
#include <Servo.h>
#include <SoftwareSerial.h>

// 定義引腳
const int REED_PIN = 4;  // 干簧管
const int RED_LED = 7;
const int GREEN_LED = 6;
const int BLUE_LED = 5;
Servo myservo;

// 指紋模組的串口，使用 Pin 8 (RX) 和 Pin 9 (TX)
SoftwareSerial mySerial(8, 9); // RX -> Pin 8, TX -> Pin 9
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

bool lockEngaged = false;  // 門鎖是否上鎖的狀態
bool forceOpenWarning = false; // 是否處於強行開啟警告狀態
bool fingerprintScanningEnabled = true; // 是否啟用指紋掃描
unsigned long unlockStartTime; // 解鎖開始的時間
const unsigned long unlockDuration = 30000; // 解鎖持續時間 30 秒

// 函數前置宣告
void blinkLED(int led1, int led2 = -1);
void handleReedSwitch();
void processFingerprint();

void setup() {
  // 初始化 LED 和舵機
  pinMode(REED_PIN, INPUT_PULLUP);  // 干簧管使用上拉電阻
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  myservo.attach(3);
  myservo.write(90); // 初始為鎖上狀態

  // 初始化串口通信
  Serial.begin(9600);
  Serial.println("初始化指紋模組...");
 
  // 初始化指紋模組
  finger.begin(57600);
  if (finger.verifyPassword()) {
    Serial.println("指紋模組已成功連接");
  } else {
    Serial.println("指紋模組連接失敗，請檢查連接");
    while (1); // 如果連接失敗，停止執行
  }

  // 初始 LED 狀態
  digitalWrite(RED_LED, HIGH);  // 紅燈亮，表示門已上鎖
  digitalWrite(GREEN_LED, LOW); // 綠燈熄滅
  digitalWrite(BLUE_LED, LOW);  // 藍燈熄滅
}

void loop() {
  handleReedSwitch();
  processFingerprint();
}

// 處理干簧管邏輯
void handleReedSwitch() {
  int reedState = digitalRead(REED_PIN);

  // 強行開啟警告狀態
  if (forceOpenWarning) {
    blinkLED(RED_LED, BLUE_LED);  // 閃爍紅藍燈

    // 如果干簧管重新觸發（門被鎖上），停止警告
    if (reedState == LOW) {
      forceOpenWarning = false;  // 停止警告
      lockEngaged = true;  // 門鎖回到上鎖狀態
      myservo.write(90);  // 鎖上門
      digitalWrite(RED_LED, HIGH);  // 紅燈亮，表示門已上鎖
      digitalWrite(BLUE_LED, LOW);  // 藍燈熄滅
      digitalWrite(GREEN_LED, LOW); // 綠燈熄滅
    }
  } else if (reedState == HIGH && lockEngaged) {
    // 如果門鎖上鎖且干簧管觸發，表示門可能被強行打開
    forceOpenWarning = true;  // 啟動強行開啟警告
    Serial.println("警告：門鎖被強行打開！");
  }
}

// 處理指紋識別邏輯
void processFingerprint() {
  if (fingerprintScanningEnabled && digitalRead(REED_PIN) == LOW) {
    // 嘗試讀取指紋
    int fingerID = getFingerprintID();
    if (fingerID != -1) {
      Serial.print("指紋匹配成功，ID: ");
      Serial.println(fingerID);
      
      // 解鎖門鎖
      myservo.write(0);  // 打開門鎖
      lockEngaged = false;
      digitalWrite(RED_LED, LOW);  // 紅燈熄滅
      digitalWrite(GREEN_LED, HIGH);  // 綠燈亮，表示成功
      
      // 設定解鎖開始時間
      unlockStartTime = millis();
      fingerprintScanningEnabled = false;
    } else {
      Serial.println("指紋匹配失敗");
      digitalWrite(RED_LED, HIGH);  // 紅燈閃爍
    }
  }

  // 解鎖計時
  if (!lockEngaged && (millis() - unlockStartTime < unlockDuration)) {
    unsigned long remainingTime = unlockDuration - (millis() - unlockStartTime);

    // 剩餘時間小於 10 秒，綠燈閃爍
    if (remainingTime < 10000) {
      if ((remainingTime / 500) % 2 == 0) {
        digitalWrite(GREEN_LED, HIGH);
      } else {
        digitalWrite(GREEN_LED, LOW);
      }
    }
  } else if (!lockEngaged && millis() - unlockStartTime >= unlockDuration) {
    // 解鎖時間結束，鎖上門
    myservo.write(90);
    lockEngaged = true;
    digitalWrite(RED_LED, HIGH);  // 紅燈亮，表示門已上鎖
    digitalWrite(GREEN_LED, LOW); // 綠燈熄滅
    digitalWrite(BLUE_LED, LOW);  // 藍燈熄滅
    fingerprintScanningEnabled = true;  // 重新啟用指紋掃描
  }
}

// 指紋識別函數
int getFingerprintID() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK) return -1;

  return finger.fingerID;
}

// LED 閃爍函數
void blinkLED(int led1, int led2) {
  digitalWrite(led1, HIGH);
  if (led2 != -1) digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led1, LOW);
  if (led2 != -1) digitalWrite(led2, LOW);
  delay(200);
}