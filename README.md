# 🛠️ Laboratório de Engenharia: Automação, Visão Computacional e Dados

Este repositório reúne meus estudos, experimentos e códigos práticos focados no ecossistema de Automação Industrial, Robótica e Integração de Sistemas (Hardware/Software).

## 🚀 Estrutura do Repositório e Recursos Desenvolvidos

O projeto está estruturado em módulos práticos que resolvem problemas reais de engenharia de controle e sistemas autônomos:

### 👁️ [Módulo 01: Visão Computacional (OpenCV)](./01-visao-computacional-opencv)
Algoritmos focados em processamento de imagem em tempo real, inteligência visual e navegação:
* **Segurança e Detecção de Riscos:** Identificação e isolamento de focos de incêndio através de filtros de cor (`opencv_aula7_detectar_cor_fogo.py`).
* **Sistemas de Navegação e Alvos:** Rastreamento robusto de alvos por cor, detecção de contornos/centro de massa e leitura de setas direcionais para orientação de robôs móveis.
* **Assistência e Manobra:** Desenvolvimento de guias visuais dinâmicas para sistemas de câmera de ré e auxílio em estacionamento.

### 📊 [Módulo 02: Análise de Dados Industriais (Pandas)](./02-analise-dados-pandas)
Manipulação e tratamento de dados aplicados à automação. Aprendizado focado na criação de estruturas de dados (DataFrames) e tratamento de tabelas para processar logs de produção e medições de sensores.

### 🔌 [Módulo 03: Integração Python + Arduino](./03-integracao-arduino-python)
Arquivos de firmware e scripts de alto nível operando em conjunto via comunicação serial (UART):
* **Controle de Movimento Suave:** Integração de sistemas de tracking de vídeo (OpenCV) com atuadores físicos (Servos), aplicando lógicas de aceleração e desaceleração suave para mitigar impactos mecânicos e desgaste no hardware.

---
## 🛠️ Ferramentas e Tecnologias
* **Linguagens:** Python 3.x, C/C++ (Embedded)
* **Bibliotecas & Ecossistema:** OpenCV, Pandas, PySerial, Arduino IDE