// ===== Pines =====
const int PIN_POT_J1   = 34; // Potenciometro - rotacion base (joint_1)
const int PIN_POT_J2   = 35; // Potenciometro - hombro (joint_2)
const int PIN_POT_GRIP = 32; // Potenciometro - apertura pinza (dedos)


const float J1_MIN = -2.5, J1_MAX = 2.5;
const float J2_MIN = -2.0, J2_MAX = 2.0;
const float GRIP_MIN = 0.0, GRIP_MAX = 0.05;

const int ADC_MAX = 4095;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);       
  analogSetAttenuation(ADC_11db); 
}

float mapFloat(long x, long inMin, long inMax, float outMin, float outMax) {
  return outMin + (outMax - outMin) * ((float)(x - inMin) / (float)(inMax - inMin));
}

void loop() {
  int raw1 = analogRead(PIN_POT_J1);
  int raw2 = analogRead(PIN_POT_J2);
  int raw3 = analogRead(PIN_POT_GRIP);

  float j1   = mapFloat(raw1, 0, ADC_MAX, J1_MIN, J1_MAX);
  float j2   = mapFloat(raw2, 0, ADC_MAX, J2_MIN, J2_MAX);
  float grip = mapFloat(raw3, 0, ADC_MAX, GRIP_MIN, GRIP_MAX);

  Serial.print("j1:");    Serial.print(j1, 3);
  Serial.print(",j2:");   Serial.print(j2, 3);
  Serial.print(",grip:"); Serial.println(grip, 3);

  delay(50); 
}
