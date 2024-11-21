#include <SD.h>
#include "RTClib.h"

#define SD_CS_PIN 5  // Defina o pino CS para o cartão SD

// ======================== CONFIGURAÇÕES ======================== //

// Instância do RTC
RTC_DS1307 rtc;

// Pinos dos Componentes
const int LDR_PIN = 14;               // Pino do sensor de luminosidade (LDR)
const int MMWAVE_C1_PIN = 32;         // Pino do sensor de presença mmWave do Cômodo 1
const int RELAY_C1_PIN = 17;          // Pino do relé da lâmpada do Cômodo 1
const int MMWAVE_C2_PIN = 16;         // Pino do sensor de presença mmWave do Cômodo 2 (alterado)
const int RELAY_C2_PIN = 4;           // Pino do relé da lâmpada do Cômodo 2 (alterado)
const int MMWAVE_EXT_PIN = 33;        // Pino do sensor de presença mmWave da Área Externa
const int RELAY_EXT1_PIN = 27;        // Pino do relé da lâmpada externa 1 (sempre acesa à noite)
const int RELAY_EXT2_PIN = 25;        // Pino do relé da lâmpada externa 2 (ativa com movimento)
// Definição dos pinos I2C para o ESP32
const int SDA_PIN = 21;  // Pino SDA do ESP32
const int SCL_PIN = 22;  // Pino SCL do ESP32

// Constantes e Configurações
const float CONSUMO_C1 = 15.0;        // Consumo da lâmpada no Cômodo 1 (em watts)
const float CONSUMO_C2 = 15.0;        // Consumo da lâmpada no Cômodo 2 (em watts)
const float CONSUMO_EXT1 = 15.0;      // Consumo da lâmpada externa 1 (em watts)
const float CONSUMO_EXT2 = 15.0;      // Consumo da lâmpada externa 2 (em watts)
// LDR Characteristics
const float GAMMA = 0.7065;           // GAMMA: Constante que define a sensibilidade do LDR a mudanças de luminosidade.
const float RL10 = 85.0;              // RL10: Resistência do LDR em condições de 10 lux.
float ldrValue = 0;                   // Valor de Lux lido do sensor
const int LDR_THRESHOLD = 500;        // Valor mínimo do LDR para considerar "noite"
const unsigned long REPORT_INTERVAL = 5000; // Intervalo de envio de dados (em ms)
const unsigned long MOTION_DELAY = 2000;    // Tempo para resetar detecção de movimento (ms)

// ======================== VARIÁVEIS GLOBAIS ======================== //

// Estados de Sensores
bool isNight = false;                 // Flag para indicar se é noite
bool motionDetectedC1 = false;        // Movimento detectado no Cômodo 1
bool motionDetectedC2 = false;        // Movimento detectado no Cômodo 2
bool motionDetectedExt = false;       // Movimento detectado na Área Externa

// Estados Anteriores (para detectar mudanças)
bool prevMotionDetectedC1 = false;
bool prevMotionDetectedC2 = false;
bool prevMotionDetectedExt = false;
bool prevIsNight = false;

// Temporizadores
unsigned long lastC1MotionTime = 0;   // Última detecção no Cômodo 1
unsigned long lastC2MotionTime = 0;   // Última detecção no Cômodo 2
unsigned long lastExtMotionTime = 0;  // Última detecção na Área Externa
unsigned long lastReportTime = 0;     // Última vez que os dados foram enviados

// Consumo acumulado (em watts-segundos)
float consumoTotalC1 = 0.0;           // Consumo acumulado da lâmpada do Cômodo 1
float consumoTotalC2 = 0.0;           // Consumo acumulado da lâmpada do Cômodo 2
float consumoTotalExt1 = 0.0;         // Consumo acumulado da lâmpada externa 1
float consumoTotalExt2 = 0.0;         // Consumo acumulado da lâmpada externa 2

// IDs dos dispositivos (de acordo com o banco de dados)
const int DEVICE_ID_LDR = 1;
const int DEVICE_ID_MMWAVE_C1 = 2;
const int DEVICE_ID_MMWAVE_C2 = 3;
const int DEVICE_ID_MMWAVE_EXT = 4;
const int DEVICE_ID_RELAY_C1 = 5;
const int DEVICE_ID_RELAY_C2 = 6;
const int DEVICE_ID_RELAY_EXT1 = 7;
const int DEVICE_ID_RELAY_EXT2 = 8;

// ======================== FUNÇÕES AUXILIARES ======================== //

/**
 * Inicializa o RTC DS1307.
 */
void setupRTC() {
  if (!rtc.begin()) {
    Serial.println("Não foi possível encontrar o RTC");
    while (1);
  }

  if (!rtc.isrunning()) {
    Serial.println("O RTC não está funcionando, ajustando a data e hora...");
    // Ajuste o RTC para a data e hora atuais (substitua pela data/hora corretas)
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

/**
 * Função para obter o timestamp atual em formato ISO8601.
 */
String getCurrentTimestamp() {
  DateTime now = rtc.now();

  char timestamp[25];
  sprintf(timestamp, "%04d-%02d-%02dT%02d:%02d:%02dZ",
          now.year(), now.month(), now.day(),
          now.hour(), now.minute(), now.second());

  return String(timestamp);
}

/**
 * Configura os pinos dos sensores, relés e inicializa as lâmpadas desligadas.
 */
void setupPins() {
  // Inicializa a comunicação I2C com os pinos especificados
  Wire.begin(SDA_PIN, SCL_PIN);

  // Configuração dos pinos dos sensores e atuadores
  pinMode(LDR_PIN, INPUT);                  // Pino do sensor LDR
  pinMode(MMWAVE_C1_PIN, INPUT_PULLUP);     // Sensor mmWave do Cômodo 1
  pinMode(RELAY_C1_PIN, OUTPUT);            // Relé da lâmpada do Cômodo 1
  pinMode(MMWAVE_C2_PIN, INPUT_PULLUP);     // Sensor mmWave do Cômodo 2
  pinMode(RELAY_C2_PIN, OUTPUT);            // Relé da lâmpada do Cômodo 2
  pinMode(MMWAVE_EXT_PIN, INPUT_PULLUP);    // Sensor mmWave da Área Externa
  pinMode(RELAY_EXT1_PIN, OUTPUT);          // Relé da lâmpada externa 1
  pinMode(RELAY_EXT2_PIN, OUTPUT);          // Relé da lâmpada externa 2

  // Inicializa todas as lâmpadas desligadas
  digitalWrite(RELAY_C1_PIN, HIGH);
  digitalWrite(RELAY_C2_PIN, HIGH);
  digitalWrite(RELAY_EXT1_PIN, HIGH);
  digitalWrite(RELAY_EXT2_PIN, HIGH);

  motionDetectedC1 = false; // Garante que a variável começa como falsa no Cômodo 1
  motionDetectedC2 = false; // Garante que a variável começa como falsa no Cômodo 2
  motionDetectedExt = false; // Garante que a variável começa como falsa na Área Externa
}

/**
 * Envia um evento em formato JSON para o Serial Monitor e salva no cartão SD.
 * @param jsonString String contendo o JSON do evento.
 */
void sendEvent(String jsonString) {
  Serial.println(jsonString);

  // Abre o arquivo para adicionar (append)
  File dataFile = SD.open("/events.txt", FILE_APPEND);
  if (dataFile) {
    dataFile.println(jsonString);
    dataFile.close();

    // Lista os arquivos após escrever
    listFilesInSD();
  } else {
    Serial.println("Erro ao abrir events.txt para escrita!");
  }
}

/**
 * Lista os arquivos presentes no cartão SD.
 */
void listFilesInSD() {
  File root = SD.open("/");
  Serial.println("Arquivos no cartão SD:");
  printDirectory(root, 0);
  root.close();
}

/**
 * Função auxiliar para imprimir o diretório.
 */
void printDirectory(File dir, int numTabs) {
  while (true) {
    File entry = dir.openNextFile();
    if (!entry) {
      // Sem mais arquivos
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      Serial.print('\t');
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      printDirectory(entry, numTabs + 1);
    } else {
      // Arquivos têm tamanhos, diretórios não
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
    }
    entry.close();
  }
}

/**
 * Atualiza o estado do LDR e verifica se é noite.
 */
void updateLdrStatus() {
  // Lê o valor analógico do LDR (0-4095 no ESP32)
  int analogValue = analogRead(LDR_PIN);

  // Converte o valor analógico para tensão (0-3.3V)
  float voltage = analogValue / 4095.0 * 3.3;

  // Calcula a resistência do LDR com base na divisão de tensão
  float resistance = 5000 * voltage / (1 - voltage / 3.3);

  // Calcula o valor em Lux usando a fórmula baseada em GAMMA e RL10
  ldrValue = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));

  // Verifica se o valor calculado é válido
  if (isnan(ldrValue)) {
    Serial.println(F("Erro na leitura do LDR!"));
    return; // Sai da função caso o valor seja inválido
  }

  // Define se é noite com base no limiar de Lux
  isNight = (ldrValue < LDR_THRESHOLD);

  // Verifica se houve mudança significativa na luminosidade
  static float prevLdrValue = 0;
  if (abs(ldrValue - prevLdrValue) > 50) { // Threshold de variação
    // Gera evento JSON para o LDR
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_LDR) + ",";
    json += "\"type\":\"sensor-reading\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + String(ldrValue, 2) + " lux\",";
    json += "\"numeric_value\":" + String(ldrValue, 2);
    json += "}";

    sendEvent(json);
    prevLdrValue = ldrValue;
  }
}

/**
 * Verifica a detecção de movimento em cada sensor mmWave.
 */
void checkMotionDetectors() {
  // Cômodo 1
  if (digitalRead(MMWAVE_C1_PIN) == LOW) {
    motionDetectedC1 = true;
    lastC1MotionTime = millis();
  } else if (millis() - lastC1MotionTime > MOTION_DELAY) {
    motionDetectedC1 = false;
  }

  // Verifica mudança de estado no sensor do Cômodo 1
  if (motionDetectedC1 != prevMotionDetectedC1) {
    String status = motionDetectedC1 ? "Movimento detectado" : "Movimento cessado";
    int numericValue = motionDetectedC1 ? 1 : 0;

    // Gera evento JSON para o sensor de presença
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_MMWAVE_C1) + ",";
    json += "\"type\":\"sensor-reading\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevMotionDetectedC1 = motionDetectedC1;
  }

  // Cômodo 2
  if (digitalRead(MMWAVE_C2_PIN) == LOW) {
    motionDetectedC2 = true;
    lastC2MotionTime = millis();
  } else if (millis() - lastC2MotionTime > MOTION_DELAY) {
    motionDetectedC2 = false;
  }

  // Verifica mudança de estado no sensor do Cômodo 2
  if (motionDetectedC2 != prevMotionDetectedC2) {
    String status = motionDetectedC2 ? "Movimento detectado" : "Movimento cessado";
    int numericValue = motionDetectedC2 ? 1 : 0;

    // Gera evento JSON para o sensor de presença
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_MMWAVE_C2) + ",";
    json += "\"type\":\"sensor-reading\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevMotionDetectedC2 = motionDetectedC2;
  }

  // Área Externa
  if (digitalRead(MMWAVE_EXT_PIN) == LOW) {
    motionDetectedExt = true;
    lastExtMotionTime = millis();
  } else if (millis() - lastExtMotionTime > MOTION_DELAY) {
    motionDetectedExt = false;
  }

  // Verifica mudança de estado no sensor da Área Externa
  if (motionDetectedExt != prevMotionDetectedExt) {
    String status = motionDetectedExt ? "Movimento detectado" : "Movimento cessado";
    int numericValue = motionDetectedExt ? 1 : 0;

    // Gera evento JSON para o sensor de presença
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_MMWAVE_EXT) + ",";
    json += "\"type\":\"sensor-reading\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevMotionDetectedExt = motionDetectedExt;
  }
}

/**
 * Controla o estado das lâmpadas com base no LDR e nos sensores de presença.
 */
void controlLights() {
  // Cômodo 1: Liga/desliga a lâmpada dependendo da noite e do movimento
  bool lampStateC1 = (isNight && motionDetectedC1);
  digitalWrite(RELAY_C1_PIN, lampStateC1 ? LOW : HIGH);

  // Verifica mudança de estado no relé do Cômodo 1
  static bool prevLampStateC1 = false;
  if (lampStateC1 != prevLampStateC1) {
    String status = lampStateC1 ? "Ativado" : "Desativado";
    int numericValue = lampStateC1 ? 1 : 0;

    // Gera evento JSON para o relé
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_C1) + ",";
    json += "\"type\":\"state-change\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevLampStateC1 = lampStateC1;
  }

  // Cômodo 2: Liga/desliga a lâmpada dependendo da noite e do movimento
  bool lampStateC2 = (isNight && motionDetectedC2);
  digitalWrite(RELAY_C2_PIN, lampStateC2 ? LOW : HIGH);

  // Verifica mudança de estado no relé do Cômodo 2
  static bool prevLampStateC2 = false;
  if (lampStateC2 != prevLampStateC2) {
    String status = lampStateC2 ? "Ativado" : "Desativado";
    int numericValue = lampStateC2 ? 1 : 0;

    // Gera evento JSON para o relé
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_C2) + ",";
    json += "\"type\":\"state-change\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevLampStateC2 = lampStateC2;
  }

  // Área Externa 1: Sempre acesa à noite
  bool lampStateExt1 = isNight;
  digitalWrite(RELAY_EXT1_PIN, lampStateExt1 ? LOW : HIGH);

  // Verifica mudança de estado no relé da Área Externa 1
  static bool prevLampStateExt1 = false;
  if (lampStateExt1 != prevLampStateExt1) {
    String status = lampStateExt1 ? "Ativado" : "Desativado";
    int numericValue = lampStateExt1 ? 1 : 0;

    // Gera evento JSON para o relé
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_EXT1) + ",";
    json += "\"type\":\"state-change\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevLampStateExt1 = lampStateExt1;
  }

  // Área Externa 2: Liga/desliga com movimento à noite
  bool lampStateExt2 = (isNight && motionDetectedExt);
  digitalWrite(RELAY_EXT2_PIN, lampStateExt2 ? LOW : HIGH);

  // Verifica mudança de estado no relé da Área Externa 2
  static bool prevLampStateExt2 = false;
  if (lampStateExt2 != prevLampStateExt2) {
    String status = lampStateExt2 ? "Ativado" : "Desativado";
    int numericValue = lampStateExt2 ? 1 : 0;

    // Gera evento JSON para o relé
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_EXT2) + ",";
    json += "\"type\":\"state-change\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + status + "\",";
    json += "\"numeric_value\":" + String(numericValue);
    json += "}";

    sendEvent(json);
    prevLampStateExt2 = lampStateExt2;
  }
}

/**
 * Calcula o consumo acumulado das lâmpadas ligadas.
 * @param deltaTime Tempo desde a última atualização (em milissegundos)
 */
void updateConsumption(unsigned long deltaTime) {
  if (digitalRead(RELAY_C1_PIN) == LOW) {
    float consumo = CONSUMO_C1 * (deltaTime / 1000.0);
    consumoTotalC1 += consumo;

    // Gera evento JSON para consumo de energia
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_C1) + ",";
    json += "\"type\":\"energy-consumption\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + String(consumo, 2) + " W\",";
    json += "\"numeric_value\":" + String(consumo, 2);
    json += "}";

    sendEvent(json);
  }

  if (digitalRead(RELAY_C2_PIN) == LOW) {
    float consumo = CONSUMO_C2 * (deltaTime / 1000.0);
    consumoTotalC2 += consumo;

    // Gera evento JSON para consumo de energia
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_C2) + ",";
    json += "\"type\":\"energy-consumption\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + String(consumo, 2) + " W\",";
    json += "\"numeric_value\":" + String(consumo, 2);
    json += "}";

    sendEvent(json);
  }

  if (digitalRead(RELAY_EXT1_PIN) == LOW) {
    float consumo = CONSUMO_EXT1 * (deltaTime / 1000.0);
    consumoTotalExt1 += consumo;

    // Gera evento JSON para consumo de energia
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_EXT1) + ",";
    json += "\"type\":\"energy-consumption\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + String(consumo, 2) + " W\",";
    json += "\"numeric_value\":" + String(consumo, 2);
    json += "}";

    sendEvent(json);
  }

  if (digitalRead(RELAY_EXT2_PIN) == LOW) {
    float consumo = CONSUMO_EXT2 * (deltaTime / 1000.0);
    consumoTotalExt2 += consumo;

    // Gera evento JSON para consumo de energia
    String json = "{";
    json += "\"device_id\":" + String(DEVICE_ID_RELAY_EXT2) + ",";
    json += "\"type\":\"energy-consumption\",";
    json += "\"timestamp\":\"" + getCurrentTimestamp() + "\",";
    json += "\"value\":\"" + String(consumo, 2) + " W\",";
    json += "\"numeric_value\":" + String(consumo, 2);
    json += "}";

    sendEvent(json);
  }
}

// ======================== FUNÇÕES PRINCIPAIS ======================== //

/**
 * Configura os pinos, inicializa o sistema.
 */
void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  setupPins();
  setupRTC();  // Inicializa o RTC

  // Inicializa o cartão SD
  Serial.print("Inicializando o cartão SD... ");
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Falha na inicialização do cartão SD!");
    while (1);
  }
  Serial.println("Cartão SD inicializado com sucesso.");
}

/**
 * Loop principal que atualiza sensores, controla lâmpadas e calcula consumo.
 */
void loop() {
  unsigned long currentTime = millis(); // Obtém o tempo atual

  // Atualiza estado do LDR (lux e noite)
  updateLdrStatus();

  // Verifica movimento nos sensores mmWave
  checkMotionDetectors();

  // Controla as lâmpadas com base nos sensores
  controlLights();

  // Atualiza e reporta o consumo periodicamente
  if (currentTime - lastReportTime >= REPORT_INTERVAL) {
    unsigned long deltaTime = currentTime - lastReportTime;
    updateConsumption(deltaTime);
    lastReportTime = currentTime;
  }

  delay(300); // Ajuste do delay conforme necessário
}
