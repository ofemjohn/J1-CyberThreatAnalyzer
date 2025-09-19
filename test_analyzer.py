#!/usr/bin/env python3
"""
Test script for J1-CyberThreatAnalyzer
Tests the threat analysis functionality with sample data
"""

import requests
import json
import time

def test_threat_analysis():
    """Test the threat analysis API with sample data"""
    
    # Load sample data
    with open('data/sample_logs.json', 'r') as f:
        sample_data = json.load(f)
    
    base_url = "http://localhost:8000"
    
    print("🛡️  J1-CyberThreatAnalyzer Test Suite")
    print("=" * 50)
    
    # Test 1: Phishing Email Analysis
    print("\n📧 Test 1: Phishing Email Analysis")
    phishing_email = sample_data['email_samples'][0]
    
    payload = {
        "content": f"Subject: {phishing_email['subject']}\nFrom: {phishing_email['sender']}\nContent: {phishing_email['content']}",
        "content_type": "email",
        "analysis_type": "phishing"
    }
    
    try:
        response = requests.post(f"{base_url}/analyze", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Threat Detected: {result['threat_detected']}")
            print(f"🎯 Threat Type: {result['threat_type']}")
            print(f"📊 Confidence Score: {result['confidence_score']}%")
            print(f"⚠️  Risk Level: {result['risk_level']}")
            print(f"📝 Analysis: {result['analysis_details']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test 2: Security Log Analysis
    print("\n🔍 Test 2: Security Log Analysis")
    security_log = sample_data['security_logs'][0]
    
    payload = {
        "content": f"Event: {security_log['event']}\nDetails: {security_log['details']}\nSeverity: {security_log['severity']}",
        "content_type": "log",
        "analysis_type": "anomaly"
    }
    
    try:
        response = requests.post(f"{base_url}/analyze", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Threat Detected: {result['threat_detected']}")
            print(f"🎯 Threat Type: {result['threat_type']}")
            print(f"📊 Confidence Score: {result['confidence_score']}%")
            print(f"⚠️  Risk Level: {result['risk_level']}")
            print(f"📝 Analysis: {result['analysis_details']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test 3: Malware Detection
    print("\n🦠 Test 3: Malware Detection")
    malware_log = sample_data['security_logs'][2]
    
    payload = {
        "content": f"Event: {malware_log['event']}\nDetails: {malware_log['details']}\nSeverity: {malware_log['severity']}",
        "content_type": "file",
        "analysis_type": "malware"
    }
    
    try:
        response = requests.post(f"{base_url}/analyze", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Threat Detected: {result['threat_detected']}")
            print(f"🎯 Threat Type: {result['threat_type']}")
            print(f"📊 Confidence Score: {result['confidence_score']}%")
            print(f"⚠️  Risk Level: {result['risk_level']}")
            print(f"📝 Analysis: {result['analysis_details']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test Health Check
    print("\n🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Status: {health['status']}")
            print(f"🔗 Ollama: {health['ollama']}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")

if __name__ == "__main__":
    print("Starting threat analysis tests...")
    print("Make sure the backend is running on http://localhost:8000")
    print("And Ollama is running with llama3.2:3b model")
    print("\nPress Enter to continue...")
    input()
    
    test_threat_analysis()
    print("\n🎉 Test suite completed!")
