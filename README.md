# J1-CyberThreatAnalyzer 🛡️

An AI-powered cybersecurity threat analysis tool built with Large Language Models (LLMs) for detecting phishing, malware, and suspicious activities in security logs and emails.

## 🌟 Features

- **Local LLM Integration**: Uses Ollama with Llama 3.2 (3B parameters) for privacy and control
- **Threat Detection**: Identifies phishing attempts, malware indicators, and suspicious activities
- **Security Log Analysis**: Processes various log formats for anomaly detection
- **Email Security**: Analyzes emails for phishing and social engineering attempts
- **Real-time Scoring**: Provides threat confidence scores and risk assessments
- **Enterprise-Ready**: Built with security and scalability in mind

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Security      │    │   FastAPI       │    │   Ollama        │
│   Logs/Emails   │◄──►│   Backend       │◄──►│   LLM Engine    │
│   (Input)       │    │   (Port 8000)   │    │   (Local)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Ollama installed locally
- Llama 3.2:3b model

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ofemjohn/J1-CyberThreatAnalyzer.git
   cd J1-CyberThreatAnalyzer
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install and Run Ollama**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull the model
   ollama pull llama3.2:3b
   ```

4. **Run the Application**
   ```bash
   # Terminal 1: Start Ollama
   ollama serve
   
   # Terminal 2: Start Backend
   cd backend
   source venv/bin/activate
   python main.py
   ```

5. **Access the Application**
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🛡️ Threat Detection Capabilities

- **Phishing Detection**: Identifies suspicious email patterns and social engineering attempts
- **Malware Indicators**: Detects potential malware signatures and suspicious file activities
- **Anomaly Detection**: Identifies unusual patterns in security logs
- **Risk Assessment**: Provides confidence scores for threat likelihood
- **False Positive Reduction**: Advanced filtering to minimize false alarms

## 📊 Analysis Features

The system includes comprehensive threat analysis with:
- **Threat Classification**: Categorizes detected threats by type and severity
- **Confidence Scoring**: Provides risk assessment scores (0-100)
- **Pattern Recognition**: Identifies common attack vectors and techniques
- **Log Correlation**: Analyzes multiple log sources for comprehensive threat detection

## 🧪 Test Scenarios

The tool is tested with various threat scenarios:
- **Phishing Emails**: Suspicious sender patterns, malicious links, social engineering
- **Malware Indicators**: Suspicious file activities, unusual network traffic
- **Security Log Anomalies**: Failed login attempts, privilege escalation attempts
- **Social Engineering**: Suspicious communication patterns and requests

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.12
- **LLM**: Ollama with Llama 3.2:3b
- **Analysis**: Custom threat detection algorithms
- **Data Processing**: JSON, CSV log parsing
- **Security**: Local processing for privacy

## 📝 Configuration

### LLM Parameters
- **Temperature**: 0.2 (optimized for security analysis accuracy)
- **Top P**: 0.8 (focused threat detection)
- **Top K**: 30 (controlled analysis diversity)
- **Max Tokens**: 256 (concise threat assessments)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**John Ofem**
- Enterprise AI Applications XLS Group 504
- Kennesaw State University

## 🙏 Acknowledgments

- Ollama team for the local LLM platform
- Meta for the Llama 3.2 model
- FastAPI community for excellent framework
- Cybersecurity community for threat intelligence

---

⭐ **Star this repository if you found it helpful!**
