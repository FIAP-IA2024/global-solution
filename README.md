# Global Solution

Este projeto tem como objetivo fornecer uma solução para o **gerenciamento e otimização do consumo energético** em residências, utilizando **Streamlit** para visualização, **MQTT** para comunicação e **SQLite** como banco de dados para armazenar os dados gerados. A aplicação monitora, em tempo real, o consumo de energia, as tarifas de energia, e gera relatórios de eficiência energética. O sistema permite a análise do consumo por zona e dispositivo, além de possibilitar a visualização de gráficos detalhados.

---

## Funcionalidades

- **Métricas em tempo real**: Exibe o consumo atual de energia, a tarifa de energia e o custo total em tempo real.
- **Relatórios de Eficiência**: Exibe o custo total por zona e dispositivo, além de gráficos interativos de consumo por zona e dispositivo.
- **Filtros interativos**: Permite selecionar zonas, dispositivos e períodos específicos para visualizar os dados.
- **Simulação de eventos**: O arquivo `mqtt.py` simula uma conexão entre um microcontrolador e a aplicação Python, enviando eventos dos dispositivos registrados, como leituras de sensores e consumo de energia.
- **Análise histórica do consumo de energia elétrica no Brasil**: A aplicação inclui gráficos e relatórios baseados em dados históricos de consumo, utilizando fontes confiáveis, como a **Base dos Dados**.

---

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```bash
cds/
├── data-source/
│   └── br_mme_consumo_energia_eletrica.csv  # Dados históricos do consumo de energia no Brasil
├── database/
│   ├── init.sql                             # Script SQL para inicializar o banco de dados
│   └── data.db                              # Banco de dados SQLite (gerado automaticamente)
├── database.py                              # Funções para interação com o banco de dados
└── main.py                                  # Análise histórica e relatórios do consumo de energia no Brasil

ctwp/
├── database/
│   ├── init.sql                             # Script SQL para inicializar o banco de dados
│   └── data.db                              # Banco de dados SQLite (gerado automaticamente)
├── database.py                              # Funções para interação com o banco de dados
├── main.py                                  # Aplicação principal do Streamlit para eficiência energética
└── mqtt.py                                  # Simulação de comunicação via MQTT

dashboard.py                                 # Dashboard unificado para CTWP e CDS
requirements.txt                             # Dependências do projeto
```

---

## Tecnologias Utilizadas

- **Streamlit**: Para criar a interface de usuário interativa.
- **Paho MQTT**: Para simulação de comunicação entre a aplicação e dispositivos.
- **SQLite**: Para armazenamento dos dados do consumo energético e eventos dos dispositivos.
- **Plotly**: Para criação de gráficos interativos.
- **Python 3.x**: Linguagem de programação utilizada para implementar toda a lógica do sistema.

---

## Requisitos

Certifique-se de ter o Python 3.x instalado. Instale as dependências do projeto com o seguinte comando:

```bash
pip install -r requirements.txt
```

---

## Instruções para Execução

### 1. Configuração do Banco de Dados

Os bancos de dados SQLite para **CDS** e **CTWP** são inicializados automaticamente ao executar os respectivos módulos (`cds/main.py` ou `ctwp/main.py`). O arquivo `init.sql` contém os comandos necessários para criar as tabelas e dados iniciais.

---

### 2. Executando o MQTT

O arquivo **`mqtt.py`** simula a comunicação entre dispositivos (como microcontroladores) e a aplicação Python. Ele publica eventos no **MQTT Broker** (usando o broker público `test.mosquitto.org`).

**Para executar:**

```bash
python ctwp/mqtt.py
```

Os eventos simulados incluem:

```json
{
  "device_id": 1,
  "type": "sensor-reading",
  "timestamp": "2024-11-20T10:30:00Z",
  "value": "345.78",
  "numeric_value": 345.78
}
```

---

### 3. Executando o Dashboard

Para iniciar o dashboard unificado, execute:

```bash
streamlit run dashboard.py
```

O dashboard oferece:
- **CTWP**: Interface para gerenciamento e otimização de consumo energético em residências.
- **CDS**: Análise histórica do consumo de energia elétrica no Brasil.

---

### 4. Fluxo de Dados

1. **MQTT**: O script `mqtt.py` envia eventos simulados para o broker MQTT.
2. **Banco de Dados**: Os eventos são salvos no SQLite para análise.
3. **Interface**: O Streamlit exibe as métricas, gráficos e relatórios com base nos dados coletados.

---

## Conclusão

Este sistema foi projetado para otimizar o consumo de energia em residências, monitorar dados históricos e oferecer análises detalhadas. Ele combina tecnologia moderna (MQTT, Streamlit) com visualizações interativas para proporcionar insights práticos e eficientes. Ideal para residências ou pequenos negócios interessados em reduzir custos e melhorar a eficiência energética.
