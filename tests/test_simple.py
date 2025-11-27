#!/usr/bin/env python3
"""
Simple validation test without external dependencies
"""

import json
import os
from pathlib import Path

def test_project_structure():
    """Test that all required files exist"""
    print("🧪 Testing Project Structure...")
    
    required_files = [
        'backend/app.py',
        'backend/models.py', 
        'backend/database.py',
        'backend/Dockerfile',
        'backend/requirements.txt',
        'backend/model_routes.json',
        'frontend/package.json',
        'frontend/Dockerfile',
        'frontend/src/App.tsx',
        'frontend/src/services/api.ts',
        'data/nutrition_lookup.csv',
        'docker-compose.yml',
        '.env.example',
        'README.md',
        'run_demo.sh'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files exist")
    return True

def test_configuration_files():
    """Test configuration file contents"""
    print("\n🧪 Testing Configuration Files...")
    
    # Test model_routes.json
    try:
        with open('backend/model_routes.json', 'r') as f:
            model_routes = json.load(f)
        
        assert 'caption' in model_routes
        assert 'image' in model_routes
        print("✅ model_routes.json is valid")
    except Exception as e:
        print(f"❌ model_routes.json test failed: {e}")
        return False
    
    # Test package.json
    try:
        with open('frontend/package.json', 'r') as f:
            package_json = json.load(f)
        
        assert 'dependencies' in package_json
        assert 'react' in package_json['dependencies']
        assert 'vite' in package_json['devDependencies']
        print("✅ package.json is valid")
    except Exception as e:
        print(f"❌ package.json test failed: {e}")
        return False
    
    # Test docker-compose.yml exists and has basic structure
    try:
        with open('docker-compose.yml', 'r') as f:
            content = f.read()
        
        assert 'backend:' in content
        assert 'frontend:' in content
        assert '8000:8000' in content
        assert '3000:3000' in content
        print("✅ docker-compose.yml is valid")
    except Exception as e:
        print(f"❌ docker-compose.yml test failed: {e}")
        return False
    
    return True

def test_nutrition_data():
    """Test nutrition data file"""
    print("\n🧪 Testing Nutrition Data...")
    
    try:
        with open('data/nutrition_lookup.csv', 'r') as f:
            lines = f.readlines()
        
        # Check header
        header = lines[0].strip()
        expected_columns = ['dish_name', 'calories', 'meal_type', 'protein_g', 'carbs_g', 'fat_g', 'description']
        
        for col in expected_columns:
            assert col in header, f"Missing column: {col}"
        
        # Check we have enough dishes
        data_lines = len(lines) - 1  # Exclude header
        assert data_lines >= 50, f"Expected at least 50 dishes, got {data_lines}"
        
        # Check a few sample lines have the right format
        sample_line = lines[1].strip().split(',')
        assert len(sample_line) >= 7, "Each line should have at least 7 columns"
        
        # Check calories are numeric
        calories = sample_line[1]
        assert calories.isdigit(), f"Calories should be numeric, got: {calories}"
        
        print(f"✅ Nutrition data is valid ({data_lines} dishes)")
        return True
        
    except Exception as e:
        print(f"❌ Nutrition data test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint definitions"""
    print("\n🧪 Testing API Endpoint Definitions...")
    
    try:
        with open('backend/app.py', 'r') as f:
            content = f.read()
        
        # Check required endpoints exist
        required_endpoints = [
            '@app.post("/api/preview"',
            '@app.get("/api/dishes"',
            '@app.post("/api/compare"',
            '@app.get("/api/weekly"',
            '@app.post("/admin/dish"',
            '@app.post("/admin/cache/clear"'
        ]
        
        for endpoint in required_endpoints:
            assert endpoint in content, f"Missing endpoint: {endpoint}"
        
        print("✅ All required API endpoints are defined")
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def test_frontend_structure():
    """Test frontend component structure"""
    print("\n🧪 Testing Frontend Structure...")
    
    try:
        # Check main App component
        with open('frontend/src/App.tsx', 'r') as f:
            app_content = f.read()
        
        assert 'TabNavigation' in app_content
        assert 'DailyPreview' in app_content
        assert 'SwitchupDiff' in app_content
        assert 'WeeklySnapshot' in app_content
        
        # Check API service
        with open('frontend/src/services/api.ts', 'r') as f:
            api_content = f.read()
        
        assert 'generatePreview' in api_content
        assert 'compareDishes' in api_content
        assert 'getWeeklySnapshot' in api_content
        
        print("✅ Frontend structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ Frontend structure test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🍅 Tamatar-Bhai MVP Validation")
    print("=" * 40)
    
    tests = [
        test_project_structure,
        test_configuration_files,
        test_nutrition_data,
        test_api_endpoints,
        test_frontend_structure
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
    print(f"📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validations passed! Project structure is complete.")
        print("\n🚀 Ready for deployment with Docker!")
        print("   1. Add your API keys to .env file")
        print("   2. Run: docker-compose up --build")
        print("   3. Access: http://localhost:3000")
        return True
    else:
        print("⚠️  Some validations failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)