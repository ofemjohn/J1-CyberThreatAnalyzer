import React, { useState } from 'react';
import './App.css';

interface ThreatAnalysisResult {
  threat_detected: boolean;
  threat_type: string;
  confidence_score: number;
  risk_level: string;
  analysis_details: string;
  recommendations: string[];
}

function App() {
  const [content, setContent] = useState('');
  const [contentType, setContentType] = useState('email');
  const [analysisType, setAnalysisType] = useState('phishing');
  const [result, setResult] = useState<ThreatAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeThreat = async () => {
    if (!content.trim()) {
      setError('Please enter content to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          content_type: contentType,
          analysis_type: analysisType,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        setError(`Error: ${response.status} - ${response.statusText}`);
      }
    } catch (err) {
      setError('Failed to connect to the analysis service. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const loadSampleData = (type: string) => {
    const samples = {
      phishing: `Subject: URGENT: Your Account Will Be Suspended
From: security@amazon-support.com
Content: Dear Customer, Your account has been flagged for suspicious activity. Click here immediately to verify your identity or your account will be suspended within 24 hours. This is your final warning!`,
      malware: `Event: Malware signature detected
Details: File 'document.pdf.exe' downloaded from suspicious domain contains trojan horse signature
Severity: critical`,
      anomaly: `Event: Multiple failed login attempts detected
Details: User 'admin' attempted 15 failed logins from IP 192.168.1.100 within 5 minutes
Severity: high`
    };
    
    setContent(samples[type as keyof typeof samples] || '');
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'critical': return '#dc3545';
      case 'high': return '#fd7e14';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ J1-CyberThreatAnalyzer</h1>
        <p>AI-powered cybersecurity threat analysis tool</p>
      </header>

      <main className="App-main">
        <div className="analysis-form">
          <h2>Threat Analysis</h2>
          
          <div className="form-group">
            <label htmlFor="contentType">Content Type:</label>
            <select
              id="contentType"
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
            >
              <option value="email">Email</option>
              <option value="log">Security Log</option>
              <option value="file">File Analysis</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="analysisType">Analysis Type:</label>
            <select
              id="analysisType"
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value)}
            >
              <option value="phishing">Phishing Detection</option>
              <option value="malware">Malware Detection</option>
              <option value="anomaly">Anomaly Detection</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="content">Content to Analyze:</label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter the content you want to analyze for threats..."
              rows={8}
            />
          </div>

          <div className="sample-buttons">
            <button onClick={() => loadSampleData('phishing')} className="sample-btn">
              📧 Load Phishing Sample
            </button>
            <button onClick={() => loadSampleData('malware')} className="sample-btn">
              🦠 Load Malware Sample
            </button>
            <button onClick={() => loadSampleData('anomaly')} className="sample-btn">
              🔍 Load Anomaly Sample
            </button>
          </div>

          <button 
            onClick={analyzeThreat} 
            disabled={loading}
            className="analyze-btn"
          >
            {loading ? '🔄 Analyzing...' : '🛡️ Analyze Threat'}
          </button>

          {error && <div className="error-message">{error}</div>}
        </div>

        {result && (
          <div className="analysis-result">
            <h2>Analysis Results</h2>
            
            <div className="result-summary">
              <div className={`threat-status ${result.threat_detected ? 'threat-detected' : 'no-threat'}`}>
                {result.threat_detected ? '🚨 THREAT DETECTED' : '✅ NO THREAT DETECTED'}
              </div>
              
              <div className="result-details">
                <div className="detail-item">
                  <strong>Threat Type:</strong> {result.threat_type}
                </div>
                <div className="detail-item">
                  <strong>Confidence Score:</strong> {result.confidence_score}%
                </div>
                <div className="detail-item">
                  <strong>Risk Level:</strong> 
                  <span style={{ color: getRiskColor(result.risk_level) }}>
                    {result.risk_level.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>

            <div className="analysis-details">
              <h3>Analysis Details:</h3>
              <p>{result.analysis_details}</p>
            </div>

            <div className="recommendations">
              <h3>Recommendations:</h3>
              <ul>
                {result.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Built with FastAPI, React, and Ollama LLM</p>
        <p>Enterprise AI Applications - Kennesaw State University</p>
      </footer>
    </div>
  );
}

export default App;