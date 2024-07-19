#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_camera.h>

// WiFi credentials
const char* ssid = "your_ssid";
const char* password = "your_password";

// Flask server URLs
const char* SERVER_URL = "http://127.0.0.1:5919/"
const char* upload_url = SERVER_URL+"upload";  // Replace with your Flask server IP and port
const char* receive_url = SERVER_URL+"receive";  // Replace with your Flask server IP and port

// Buzzer pin
int buzzerPin = 13;  // Adjust this pin number as needed

// Camera settings
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     21
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       19
#define Y4_GPIO_NUM       18
#define Y3_GPIO_NUM       5
#define Y2_GPIO_NUM       4
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() {
  Serial.begin(115200);
  pinMode(buzzerPin, OUTPUT);

  // Initialize the camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  
  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Capture and send image
  captureAndSendImage();

  // Get frequency from the server
  int frequency = getFrequency();

  // Play frequency
  if (frequency > 0) {
    Serial.printf("Playing frequency: %d Hz\n", frequency);
    tone(buzzerPin, frequency, 1000);  // Play the frequency for 1 second
    delay(1000);  // Wait for the tone to finish
  }

  delay(10000);  // Wait for 10 seconds before the next iteration
}

void captureAndSendImage() {
  // Capture image
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  
  // Send image to server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(upload_url);
    http.addHeader("Content-Type", "image/jpeg");
    
    int httpResponseCode = http.POST(fb->buf, fb->len);
    
    if (httpResponseCode == HTTP_CODE_OK || httpResponseCode == HTTP_CODE_FOUND) {
      Serial.println("Image sent successfully");
    } else {
      Serial.printf("Error in sending POST: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
  
  esp_camera_fb_return(fb);
}

int getFrequency() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(receive_url);
    
    int httpResponseCode = http.GET();
    
    if (httpResponseCode == HTTP_CODE_OK) {
      String response = http.getString();
      Serial.println("Response received: " + response);
      
      // Parse the response (assuming it's a JSON with a "frequency" field)
      int frequency = parseFrequency(response);
      http.end();
      return frequency;
    } else {
      Serial.printf("Error in GET request: %s\n", http.errorToString(httpResponseCode).c_str());
      http.end();
      return 0;
    }
  } else {
    Serial.println("WiFi Disconnected");
    return 0;
  }
}

int parseFrequency(String response) {
  // Simple JSON parsing (assuming response is in format {"frequency": 15000})
  int freqIndex = response.indexOf("\"frequency\":");
  if (freqIndex != -1) {
    int startIndex = response.indexOf(":", freqIndex) + 1;
    int endIndex = response.indexOf("}", startIndex);
    String freqString = response.substring(startIndex, endIndex);
    return freqString.toInt();
  }
  return 0;  // Default to 0 if parsing fails
}
