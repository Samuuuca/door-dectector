# 👁️ Door Detect: Detecção de Pessoas + Alerta na Alexa

Este é um script em Python que utiliza a biblioteca Ultralytics (YOLOv8) e OpenCV para monitorar um feed de vídeo (RTSP ou webcam).

Ele detecta pessoas dentro de uma área de interesse pré-definida. Se uma pessoa permanecer nessa área por mais de 10 segundos, o script envia um gatilho para a **Amazon Alexa** através do **Voice Monkey**, fazendo-a falar um aviso.

---

## ✨ Funcionalidades

* **Monitoramento em Tempo Real:** Conecta-se a qualquer feed RTSP ou webcam local.
* **Detecção de Pessoas:** Utiliza o modelo YOLOv8n para detecção de alta performance.
* **Área de Interesse:** Permite definir coordenadas (x, y) de um retângulo na tela para monitoramento focado.
* **Controle de Permanência:** Um cronômetro é ativado quando uma pessoa entra na área e dispara um alerta após um tempo configurável.
* **Integração com Alexa:** Envia um alerta de voz para qualquer dispositivo Alexa na sua conta usando a Skill Voice Monkey.

---

## 🔧 Pré-requisitos

Antes de começar, você precisará de:

* [Python 3.12+](https://www.python.org/)
* Uma câmera com feed RTSP ou uma webcam.
* Um dispositivo Amazon Alexa (Ex: Echo Dot).
* Uma conta gratuita no [Voice Monkey](https://voicemonkey.io/).

---

## ⚙️ Configuração (Obrigatório)

Este projeto não funcionará sem a configuração correta das variáveis de ambiente e da Alexa.

### 1. Configuração da Alexa (Voice Monkey)

1.  **Ative a Skill:** No seu app Alexa, procure e ative a Skill "Voice Monkey".
2.  **Crie um "Device":**
    * Faça login no [painel do Voice Monkey](https://voicemonkey.io/dashboard).
    * Vá para "Manage Devices" e crie um novo dispositivo. Dê a ele um nome simples, como `sensor_porta`.
3.  **Descubra o Dispositivo:**
    * Diga ao seu dispositivo: **"Alexa, descobrir dispositivos"**.
    * Ela deve encontrar o "sensor_porta" (ele aparecerá como um sensor de movimento).
4.  **Crie a Rotina na Alexa:**
    * No app Alexa, vá em **Mais > Rotinas**.
    * Crie uma nova rotina:
        * **QUANDO:** "Casa Inteligente" -> Selecione seu dispositivo "sensor_porta".
        * **AÇÃO:** "Alexa diz" -> "Personalizado" -> Digite a frase que ela deve falar (ex: *Atenção, pessoa detectada na porta.*).

# Intalação e Execução

## Instalação
```
git clone "https://github.com/Samuuuca/door_detect git"
cd door_detect

# Crie o venv
python -m venv .venv

# Ative o venv
# Windows (PowerShell)
.venv\Scripts\Activate

# Linux ou macOS
source .venv/bin/activate

#Instale as dependências
pip install -r requirements.txt

```
## Execução
```
python door-detect.py
```