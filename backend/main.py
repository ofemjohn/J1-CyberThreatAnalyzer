from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from typing import List, Dict, Optional
import re

app = FastAPI(title="J1-CyberThreatAnalyzer", description="AI-powered cybersecurity threat analysis tool")

# Request models
class ThreatAnalysisRequest(BaseModel):
    content: str
    content_type: str  # "email", "log", "file"
    analysis_type: str  # "phishing", "malware", "anomaly"

class ThreatAnalysisResponse(BaseModel):
    threat_detected: bool
    threat_type: str
    confidence_score: int
    risk_level: str
    analysis_details: str
    recommendations: List[str]

# Sample threat patterns for analysis
THREAT_PATTERNS = {
    "phishing": [
        "urgent action required",
        "click here immediately",
        "verify your account",
        "suspended account",
        "limited time offer",
        "congratulations you won",
        "act now or lose access"
    ],
    "malware": [
        "executable file",
        "suspicious download",
        "unknown process",
        "system compromise",
        "backdoor detected",
        "trojan horse",
        "rootkit installation"
    ],
    "anomaly": [
        "multiple failed logins",
        "unusual access pattern",
        "privilege escalation",
        "suspicious network traffic",
        "data exfiltration",
        "unauthorized access"
    ]
}

def analyze_with_llm(content: str, analysis_type: str) -> Dict:
    """Analyze content using Ollama LLM"""
    try:
        # Prepare the prompt for cybersecurity analysis
        prompt = f"""
        Analyze the following {analysis_type} content for security threats. 
        Provide a JSON response with:
        - threat_detected: boolean
        - threat_type: string
        - confidence_score: integer (0-100)
        - risk_level: string (low/medium/high/critical)
        - analysis_details: string
        - recommendations: array of strings
        
        Content to analyze:
        {content}
        
        Focus on detecting: phishing attempts, malware indicators, suspicious activities, or security anomalies.
        """
        
        # Call Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 30,
                    "num_predict": 256
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # Fallback: create structured response from text
                    return create_fallback_response(response_text, analysis_type)
            except json.JSONDecodeError:
                return create_fallback_response(response_text, analysis_type)
        else:
            raise HTTPException(status_code=500, detail="LLM service unavailable")
            
    except requests.exceptions.RequestException:
        # Fallback to rule-based analysis
        return rule_based_analysis(content, analysis_type)

def create_fallback_response(response_text: str, analysis_type: str) -> Dict:
    """Create structured response from LLM text output"""
    threat_detected = any(keyword in response_text.lower() for keyword in ["threat", "suspicious", "malicious", "phishing"])
    confidence_score = 75 if threat_detected else 25
    
    return {
        "threat_detected": threat_detected,
        "threat_type": analysis_type,
        "confidence_score": confidence_score,
        "risk_level": "high" if confidence_score > 70 else "medium" if confidence_score > 40 else "low",
        "analysis_details": response_text[:200] + "..." if len(response_text) > 200 else response_text,
        "recommendations": [
            "Review the content carefully",
            "Consider additional verification",
            "Monitor for similar patterns"
        ]
    }

def rule_based_analysis(content: str, analysis_type: str) -> Dict:
    """Fallback rule-based analysis when LLM is unavailable"""
    content_lower = content.lower()
    threat_detected = False
    confidence_score = 0
    threat_type = "unknown"
    
    # Check for threat patterns
    for threat_category, patterns in THREAT_PATTERNS.items():
        for pattern in patterns:
            if pattern in content_lower:
                threat_detected = True
                threat_type = threat_category
                confidence_score += 20
    
    confidence_score = min(confidence_score, 100)
    
    return {
        "threat_detected": threat_detected,
        "threat_type": threat_type,
        "confidence_score": confidence_score,
        "risk_level": "high" if confidence_score > 70 else "medium" if confidence_score > 40 else "low",
        "analysis_details": f"Rule-based analysis detected {threat_type} patterns in the content.",
        "recommendations": [
            "Review content for suspicious patterns",
            "Verify sender authenticity",
            "Check for additional security indicators"
        ]
    }

@app.get("/")
async def root():
    return {"message": "J1-CyberThreatAnalyzer API", "status": "running"}

@app.post("/analyze", response_model=ThreatAnalysisResponse)
async def analyze_threat(request: ThreatAnalysisRequest):
    """Analyze content for cybersecurity threats"""
    try:
        result = analyze_with_llm(request.content, request.analysis_type)
        
        return ThreatAnalysisResponse(
            threat_detected=result["threat_detected"],
            threat_type=result["threat_type"],
            confidence_score=result["confidence_score"],
            risk_level=result["risk_level"],
            analysis_details=result["analysis_details"],
            recommendations=result["recommendations"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Ollama connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return {"status": "healthy", "ollama": "connected"}
        else:
            return {"status": "degraded", "ollama": "disconnected"}
    except:
        return {"status": "degraded", "ollama": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
