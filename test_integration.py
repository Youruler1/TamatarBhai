#!/usr/bin/env python3
"""
Integration test script for Tamatar-Bhai MVP
Tests the complete application flow from docker-compose up
"""

import requests
import time
import json
import sys
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
TIMEOUT = 30
RETRY_DELAY = 2

def wait_for_service(url, service_name, max_retries=15):
    """Wait for a service to become available"""
    print(f"⏳ Waiting for {service_name} at {url}...")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if attempt < max_retries - 1:
            print(f"   Attempt {attempt + 1}/{max_retries} failed, retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
    
    print(f"❌ {service_name} failed to start after {max_retries} attempts")
    return False

def test_health_endpoints():
    """Test health check endpoints"""
    print("\n🧪 Testing Health Endpoints...")
    
    try:
        # Backend health
        response = requests.get(f"{BACKEND_URL}/health", timeout=TIMEOUT)
        assert response.status_code == 200
        health_data = response.json()
        assert "status" in health_data
        print("✅ Backend health check passed")
        
        # Frontend availability
        response = requests.get(FRONTEND_URL, timeout=TIMEOUT)
        assert response.status_code == 200
        print("✅ Frontend is accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Health endpoints test failed: {e}")
        return False

def test_daily_preview_api():
    """Test daily preview API endpoint"""
    print("\n🧪 Testing Daily Preview API...")
    
    try:
        # Test valid request
        payload = {
            "dish": "aloo paratha",
            "meal": "lunch"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/preview",
            json=payload,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        required_fields = ["dish", "calories", "image_url", "captions", "meta"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        assert "bhai" in data["captions"]
        assert "formal" in data["captions"]
        assert isinstance(data["calories"], int)
        assert data["calories"] > 0
        
        print("✅ Daily preview API works correctly")
        
        # Test error handling with invalid input
        invalid_payload = {"dish": "", "meal": "lunch"}
        response = requests.post(
            f"{BACKEND_URL}/api/preview",
            json=invalid_payload,
            timeout=TIMEOUT
        )
        
        # Should handle gracefully (either 400 or fallback response)
        assert response.status_code in [200, 400, 422]
        print("✅ Daily preview API handles invalid input")
        
        return True
        
    except Exception as e:
        print(f"❌ Daily preview API test failed: {e}")
        return False

def test_compare_api():
    """Test dish comparison API endpoint"""
    print("\n🧪 Testing Compare API...")
    
    try:
        payload = {
            "dishA": "rajma",
            "dishB": "dal tadka"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/compare",
            json=payload,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        required_fields = ["dishA", "dishB", "suggestion", "meta"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        assert "calories" in data["dishA"]
        assert "calories" in data["dishB"]
        assert isinstance(data["suggestion"], str)
        assert len(data["suggestion"]) > 0
        
        print("✅ Compare API works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Compare API test failed: {e}")
        return False

def test_weekly_api():
    """Test weekly snapshot API endpoint"""
    print("\n🧪 Testing Weekly API...")
    
    try:
        # Use last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        
        params = {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d")
        }
        
        response = requests.get(
            f"{BACKEND_URL}/api/weekly",
            params=params,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        required_fields = ["total_calories", "chart_url", "summary", "date_range", "meta"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        assert isinstance(data["total_calories"], int)
        assert isinstance(data["summary"], str)
        assert "start" in data["date_range"]
        assert "end" in data["date_range"]
        
        print("✅ Weekly API works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Weekly API test failed: {e}")
        return False

def test_dishes_api():
    """Test dishes listing API endpoint"""
    print("\n🧪 Testing Dishes API...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/dishes", timeout=TIMEOUT)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first dish structure
        dish = data[0]
        required_fields = ["id", "name", "calories", "meal_type"]
        for field in required_fields:
            assert field in dish, f"Missing field in dish: {field}"
        
        print(f"✅ Dishes API works correctly ({len(data)} dishes)")
        return True
        
    except Exception as e:
        print(f"❌ Dishes API test failed: {e}")
        return False

def test_error_handling():
    """Test API error handling"""
    print("\n🧪 Testing Error Handling...")
    
    try:
        # Test invalid endpoint
        response = requests.get(f"{BACKEND_URL}/api/nonexistent", timeout=TIMEOUT)
        assert response.status_code == 404
        print("✅ 404 handling works")
        
        # Test malformed JSON
        response = requests.post(
            f"{BACKEND_URL}/api/preview",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code in [400, 422]
        print("✅ Malformed JSON handling works")
        
        # Test missing required fields
        response = requests.post(
            f"{BACKEND_URL}/api/preview",
            json={"dish": "test"},  # Missing meal field
            timeout=TIMEOUT
        )
        assert response.status_code in [400, 422]
        print("✅ Missing field validation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_frontend_pages():
    """Test frontend page accessibility"""
    print("\n🧪 Testing Frontend Pages...")
    
    try:
        # Test main page loads
        response = requests.get(FRONTEND_URL, timeout=TIMEOUT)
        assert response.status_code == 200
        
        content = response.text
        assert "Tamatar-Bhai" in content
        assert "Daily Preview" in content or "preview" in content.lower()
        
        print("✅ Frontend pages are accessible")
        return True
        
    except Exception as e:
        print(f"❌ Frontend pages test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🍅 Tamatar-Bhai Integration Tests")
    print("=" * 50)
    
    # Wait for services to start
    if not wait_for_service(f"{BACKEND_URL}/health", "Backend"):
        print("❌ Backend service failed to start")
        return False
    
    if not wait_for_service(FRONTEND_URL, "Frontend"):
        print("❌ Frontend service failed to start")
        return False
    
    # Run tests
    tests = [
        test_health_endpoints,
        test_daily_preview_api,
        test_compare_api,
        test_weekly_api,
        test_dishes_api,
        test_error_handling,
        test_frontend_pages
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! Application is working correctly.")
        print("\n🚀 Ready for production deployment!")
        return True
    else:
        print("⚠️  Some integration tests failed. Check the issues above.")
        print("\n🔍 Debugging tips:")
        print("   - Check service logs: docker-compose logs -f")
        print("   - Verify API keys in .env file")
        print("   - Ensure all services are running: docker-compose ps")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)