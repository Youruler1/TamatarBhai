#!/usr/bin/env python3
"""
Simple test script to validate backend components without running the server
"""

import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, 'backend')

def test_configuration():
    """Test configuration files"""
    print("🧪 Testing Configuration Files...")
    
    # Test model routes
    try:
        with open('backend/model_routes.json', 'r') as f:
            model_routes = json.load(f)
        
        assert 'caption' in model_routes
        assert 'image' in model_routes
        assert model_routes['caption']['external_config']['model'] == 'gpt-4o-mini'
        assert model_routes['image']['external_config']['engine'] == 'stable-diffusion-2'
        print("✅ Model routes configuration is valid")
        
    except Exception as e:
        print(f"❌ Model routes test failed: {e}")
        return False
    
    # Test nutrition data
    try:
        import pandas as pd
        df = pd.read_csv('data/nutrition_lookup.csv')
        
        assert len(df) >= 50, f"Expected at least 50 dishes, got {len(df)}"
        assert 'dish_name' in df.columns
        assert 'calories' in df.columns
        assert 'meal_type' in df.columns
        
        # Test some specific dishes
        aloo_paratha = df[df['dish_name'] == 'Aloo Paratha']
        assert len(aloo_paratha) == 1, "Aloo Paratha should exist"
        assert aloo_paratha.iloc[0]['calories'] == 320, "Aloo Paratha should have 320 calories"
        
        print(f"✅ Nutrition data is valid ({len(df)} dishes loaded)")
        
    except Exception as e:
        print(f"❌ Nutrition data test failed: {e}")
        return False
    
    return True

def test_nutrition_service():
    """Test nutrition service functionality"""
    print("\n🧪 Testing Nutrition Service...")
    
    try:
        from services.nutrition_service import NutritionService
        
        nutrition_service = NutritionService()
        
        # Test exact match
        result = nutrition_service.get_dish_info("Aloo Paratha")
        assert result['calories'] == 320
        assert result['confidence'] == 100
        print("✅ Exact match works")
        
        # Test fuzzy match
        result = nutrition_service.get_dish_info("alu paratha")  # Different spelling
        assert result['calories'] == 320
        assert result['confidence'] >= 70  # Should be high confidence
        print("✅ Fuzzy matching works")
        
        # Test fallback
        result = nutrition_service.get_dish_info("unknown dish xyz")
        assert result['calories'] > 0  # Should return estimated calories
        assert result['confidence'] == 0  # No match found
        print("✅ Fallback estimation works")
        
        # Test search
        results = nutrition_service.search_dishes("paratha", limit=5)
        assert len(results) > 0
        assert any('paratha' in r['name'].lower() for r in results)
        print("✅ Dish search works")
        
        return True
        
    except Exception as e:
        print(f"❌ Nutrition service test failed: {e}")
        return False

def test_service_manager():
    """Test service manager fallbacks"""
    print("\n🧪 Testing Service Manager...")
    
    try:
        from services.service_manager import ServiceManager
        
        service_manager = ServiceManager()
        
        # Test service status
        status = service_manager.get_service_status()
        print(f"📊 Service Status: {status}")
        
        # Test fallback captions (should work without API keys)
        bhai_caption = service_manager._fallback_bhai_caption("Aloo Paratha", 320)
        formal_caption = service_manager._fallback_formal_caption("Aloo Paratha", 320)
        
        assert len(bhai_caption) > 0
        assert len(formal_caption) > 0
        assert "bhai" in bhai_caption.lower() or "Bhai" in bhai_caption
        
        print("✅ Fallback captions work")
        
        # Test comparison fallback
        comparison = service_manager._fallback_comparison("Rajma", "Dal Tadka", 245, 180)
        assert len(comparison) > 0
        assert "bhai" in comparison.lower() or "Bhai" in comparison
        
        print("✅ Fallback comparison works")
        
        return True
        
    except Exception as e:
        print(f"❌ Service manager test failed: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    print("\n🧪 Testing Pydantic Models...")
    
    try:
        from models import PreviewRequest, PreviewResponse, CompareRequest, CompareResponse
        
        # Test PreviewRequest
        preview_req = PreviewRequest(dish="Aloo Paratha", meal="lunch")
        assert preview_req.dish == "Aloo Paratha"
        assert preview_req.meal == "lunch"
        print("✅ PreviewRequest model works")
        
        # Test PreviewResponse
        preview_resp = PreviewResponse(
            dish="Aloo Paratha",
            calories=320,
            image_url="/data/images/test.png",
            captions={"bhai": "Test bhai", "formal": "Test formal"},
            meta={"model": "test"}
        )
        assert preview_resp.calories == 320
        print("✅ PreviewResponse model works")
        
        # Test CompareRequest
        compare_req = CompareRequest(dishA="Rajma", dishB="Dal Tadka")
        assert compare_req.dishA == "Rajma"
        print("✅ CompareRequest model works")
        
        return True
        
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🍅 Tamatar-Bhai Backend Tests")
    print("=" * 40)
    
    tests = [
        test_configuration,
        test_nutrition_service,
        test_service_manager,
        test_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)