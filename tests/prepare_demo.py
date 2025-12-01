#!/usr/bin/env python3
"""
Demo preparation script for Tamatar-Bhai MVP
Prepares sample data and validates demo scenarios
"""

import json
import csv
from pathlib import Path
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample data for demo"""
    print("🎬 Preparing Demo Sample Data...")
    
    # Ensure data directory exists
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Create sample nutrition data if it doesn't exist
    nutrition_file = data_dir / 'nutrition_lookup.csv'
    if not nutrition_file.exists():
        print("📊 Creating sample nutrition database...")
        
        sample_dishes = [
            # Breakfast items
            ("Aloo Paratha", 320, "breakfast", 8, 45, 12, "Stuffed flatbread with spiced potatoes"),
            ("Poha", 180, "breakfast", 4, 35, 2, "Flattened rice with vegetables and spices"),
            ("Upma", 200, "breakfast", 5, 38, 3, "Semolina porridge with vegetables"),
            ("Idli Sambar", 150, "breakfast", 6, 28, 2, "Steamed rice cakes with lentil curry"),
            ("Masala Dosa", 280, "breakfast", 8, 50, 8, "Crispy crepe with spiced potato filling"),
            
            # Lunch items
            ("Rajma", 245, "lunch", 15, 35, 8, "Red kidney beans in spiced tomato gravy"),
            ("Dal Tadka", 180, "lunch", 12, 28, 4, "Tempered yellow lentils"),
            ("Butter Chicken", 400, "lunch", 25, 15, 28, "Creamy tomato-based chicken curry"),
            ("Chole Bhature", 450, "lunch", 18, 65, 15, "Spiced chickpeas with fried bread"),
            ("Biryani", 380, "lunch", 20, 55, 12, "Fragrant rice with meat or vegetables"),
            ("Palak Paneer", 220, "lunch", 14, 12, 16, "Spinach curry with cottage cheese"),
            ("Roti Sabzi", 250, "lunch", 8, 45, 6, "Flatbread with mixed vegetables"),
            
            # Dinner items
            ("Khichdi", 160, "dinner", 6, 32, 2, "Comfort food of rice and lentils"),
            ("Dal Chawal", 200, "dinner", 8, 38, 3, "Lentils with steamed rice"),
            ("Vegetable Curry", 180, "dinner", 5, 25, 8, "Mixed vegetables in spiced gravy"),
            ("Chicken Curry", 320, "dinner", 28, 8, 18, "Traditional spiced chicken curry"),
            ("Fish Curry", 280, "dinner", 25, 6, 16, "Fish in coconut-based curry"),
            
            # Snacks
            ("Samosa", 150, "snack", 4, 18, 8, "Fried pastry with savory filling"),
            ("Pakora", 120, "snack", 3, 12, 7, "Deep-fried vegetable fritters"),
            ("Dhokla", 100, "snack", 3, 18, 2, "Steamed fermented rice cake"),
            ("Chaat", 180, "snack", 5, 28, 6, "Savory street food snack"),
            ("Vada Pav", 250, "snack", 6, 35, 10, "Spiced potato fritter in bread bun"),
            
            # Regional specialties
            ("Pav Bhaji", 350, "lunch", 8, 48, 14, "Spiced vegetable mash with bread"),
            ("Misal Pav", 280, "breakfast", 10, 40, 8, "Spicy sprout curry with bread"),
            ("Thali", 450, "lunch", 18, 65, 15, "Complete meal with variety of dishes"),
            ("Paratha", 200, "breakfast", 6, 28, 8, "Layered flatbread"),
            ("Lassi", 120, "snack", 4, 18, 4, "Yogurt-based drink"),
            
            # South Indian
            ("Rasam Rice", 180, "lunch", 4, 35, 3, "Tangy tamarind soup with rice"),
            ("Sambhar Rice", 200, "lunch", 6, 38, 4, "Lentil curry with rice"),
            ("Coconut Rice", 220, "lunch", 4, 42, 6, "Rice cooked with coconut"),
            ("Lemon Rice", 190, "lunch", 3, 40, 4, "Tangy rice with lemon and spices"),
            
            # Sweets (occasional)
            ("Gulab Jamun", 180, "snack", 3, 25, 8, "Sweet milk dumplings in syrup"),
            ("Jalebi", 150, "snack", 2, 30, 5, "Crispy sweet pretzel in syrup"),
            ("Rasgulla", 120, "snack", 4, 20, 3, "Spongy cottage cheese balls in syrup"),
            
            # Healthy options
            ("Quinoa Salad", 160, "lunch", 6, 25, 6, "Protein-rich grain salad"),
            ("Sprout Salad", 120, "snack", 8, 18, 2, "Fresh sprouted legumes salad"),
            ("Vegetable Soup", 80, "dinner", 3, 15, 1, "Clear broth with mixed vegetables"),
            ("Fruit Chaat", 100, "snack", 2, 24, 1, "Mixed fruit salad with spices"),
            
            # Beverages
            ("Masala Chai", 60, "snack", 2, 8, 2, "Spiced tea with milk"),
            ("Fresh Lime Water", 25, "snack", 0, 6, 0, "Refreshing citrus drink"),
            ("Buttermilk", 80, "snack", 3, 8, 2, "Spiced yogurt drink"),
            
            # Street food
            ("Pani Puri", 120, "snack", 3, 20, 4, "Crispy shells with flavored water"),
            ("Bhel Puri", 150, "snack", 4, 25, 5, "Puffed rice snack mix"),
            ("Sev Puri", 140, "snack", 3, 22, 6, "Crispy base with chutneys and sev"),
            
            # Regional breakfast
            ("Medu Vada", 180, "breakfast", 6, 20, 10, "Fried lentil donuts"),
            ("Rava Idli", 120, "breakfast", 4, 22, 2, "Steamed semolina cakes"),
            ("Uttapam", 200, "breakfast", 6, 35, 5, "Thick pancake with vegetables"),
            
            # Comfort food
            ("Maggi", 220, "snack", 6, 32, 8, "Instant noodles with vegetables"),
            ("Bread Pakora", 180, "snack", 5, 22, 8, "Bread fritters with filling"),
            ("Aloo Tikki", 160, "snack", 4, 25, 6, "Spiced potato patties"),
            
            # Festive foods
            ("Puran Poli", 250, "snack", 6, 45, 6, "Sweet stuffed flatbread"),
            ("Modak", 140, "snack", 3, 28, 3, "Steamed rice flour dumplings"),
            ("Kheer", 180, "snack", 5, 30, 6, "Rice pudding with milk and nuts")
        ]
        
        with open(nutrition_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['dish_name', 'calories', 'meal_type', 'protein_g', 'carbs_g', 'fat_g', 'description'])
            writer.writerows(sample_dishes)
        
        print(f"✅ Created nutrition database with {len(sample_dishes)} dishes")
    else:
        print("✅ Nutrition database already exists")
    
    return True

def create_demo_scenarios():
    """Create demo scenario documentation"""
    print("\n🎬 Creating Demo Scenarios...")
    
    demo_scenarios = {
        "daily_preview_scenarios": [
            {
                "dish": "aloo paratha",
                "meal": "breakfast",
                "expected_calories": 320,
                "description": "Popular North Indian breakfast - stuffed flatbread"
            },
            {
                "dish": "butter chicken",
                "meal": "lunch", 
                "expected_calories": 400,
                "description": "Rich and creamy chicken curry"
            },
            {
                "dish": "dal tadka",
                "meal": "dinner",
                "expected_calories": 180,
                "description": "Simple and healthy lentil curry"
            }
        ],
        "comparison_scenarios": [
            {
                "dishA": "rajma",
                "dishB": "dal tadka",
                "expected_difference": 65,
                "lighter_dish": "dal tadka",
                "description": "Compare protein-rich rajma vs lighter dal"
            },
            {
                "dishA": "butter chicken", 
                "dishB": "palak paneer",
                "expected_difference": 180,
                "lighter_dish": "palak paneer",
                "description": "Compare rich butter chicken vs healthier palak paneer"
            },
            {
                "dishA": "biryani",
                "dishB": "khichdi", 
                "expected_difference": 220,
                "lighter_dish": "khichdi",
                "description": "Compare festive biryani vs comfort food khichdi"
            }
        ],
        "weekly_scenarios": [
            {
                "period": "last_7_days",
                "description": "Current week analysis",
                "sample_meals": [
                    {"day": "Monday", "dish": "aloo paratha", "calories": 320},
                    {"day": "Tuesday", "dish": "rajma", "calories": 245},
                    {"day": "Wednesday", "dish": "dal tadka", "calories": 180},
                    {"day": "Thursday", "dish": "butter chicken", "calories": 400},
                    {"day": "Friday", "dish": "biryani", "calories": 380},
                    {"day": "Saturday", "dish": "khichdi", "calories": 160},
                    {"day": "Sunday", "dish": "thali", "calories": 450}
                ]
            }
        ]
    }
    
    with open('demo_scenarios.json', 'w') as f:
        json.dump(demo_scenarios, f, indent=2)
    
    print("✅ Demo scenarios created")
    return True

def create_demo_checklist():
    """Create demo checklist"""
    print("\n📋 Creating Demo Checklist...")
    
    checklist = """
# 🍅 Tamatar-Bhai MVP Demo Checklist

## Pre-Demo Setup
- [ ] Ensure Docker Desktop is running
- [ ] API keys are configured in .env file
- [ ] Run `docker-compose up --build` 
- [ ] Wait for services to start (30-60 seconds)
- [ ] Verify frontend at http://localhost:3000
- [ ] Verify backend at http://localhost:8000/health

## Demo Flow

### 1. Daily Preview Feature (2-3 minutes)
- [ ] Navigate to Daily Preview tab
- [ ] Enter "aloo paratha" as dish name
- [ ] Select "breakfast" as meal type
- [ ] Click "Generate Preview"
- [ ] Show loading skeleton animation
- [ ] Highlight generated image (or fallback)
- [ ] Point out bhai-style caption: "Bhai, yeh aloo paratha..."
- [ ] Show formal caption for comparison
- [ ] Mention calorie information (320 cal)
- [ ] Show API attribution at bottom

**Key Points to Mention:**
- AI-generated content with fallback mechanisms
- Dual caption styles (bhai vs formal)
- Fuzzy matching for dish names
- Caching for performance

### 2. Switch-up Diff Feature (2-3 minutes)
- [ ] Navigate to Switch-up Diff tab
- [ ] Enter "butter chicken" in first field
- [ ] Enter "palak paneer" in second field
- [ ] Click "Compare Dishes"
- [ ] Show loading animation
- [ ] Highlight calorie comparison (400 vs 220)
- [ ] Read bhai-style recommendation aloud
- [ ] Show calorie difference indicator
- [ ] Demonstrate swap functionality

**Key Points to Mention:**
- Instant calorie comparison
- Bhai-style recommendations for better choices
- Visual comparison with color coding
- Helpful for making healthier decisions

### 3. Weekly Snapshot Feature (2-3 minutes)
- [ ] Navigate to Weekly Snapshot tab
- [ ] Use default current week dates
- [ ] Click "Generate Snapshot"
- [ ] Show chart loading skeleton
- [ ] Display generated calorie chart
- [ ] Read AI-generated summary
- [ ] Show statistics (total calories, avg per day)
- [ ] Try quick select buttons (Last 7 days, etc.)

**Key Points to Mention:**
- Visual analytics with matplotlib charts
- AI-generated insights and summaries
- Flexible date range selection
- Helps track eating patterns

### 4. Error Handling & Reliability (1 minute)
- [ ] Try invalid dish name to show fallback
- [ ] Demonstrate retry functionality
- [ ] Show loading states throughout
- [ ] Mention offline capabilities

**Key Points to Mention:**
- Graceful degradation when APIs fail
- Comprehensive error handling
- User-friendly error messages
- Retry mechanisms

## Technical Highlights
- [ ] Mention containerized deployment
- [ ] Show API documentation at /docs
- [ ] Highlight responsive design
- [ ] Mention security features (non-root containers)
- [ ] Show health check endpoints

## Q&A Preparation
**Common Questions:**
- How accurate are the calorie estimates? (Fuzzy matching + nutrition database)
- What happens if APIs are down? (Fallback mechanisms)
- Can it handle regional variations? (Yes, fuzzy matching)
- Is it production ready? (MVP scope, needs scaling for production)
- How does the bhai style work? (OpenAI with explicit persona prompts)

## Post-Demo
- [ ] Show docker-compose logs for transparency
- [ ] Demonstrate stopping with docker-compose down
- [ ] Mention GitHub repository and documentation
- [ ] Provide setup instructions for local testing

## Backup Plans
- [ ] Have screenshots ready if live demo fails
- [ ] Prepare sample API responses
- [ ] Know how to restart services quickly
- [ ] Have fallback dishes that work well

## Demo Tips
- Keep energy high and engaging
- Explain the "bhai" personality concept early
- Show both success and error scenarios
- Emphasize the 1-day MVP scope
- Highlight the AI integration aspects
- Be prepared for technical questions
"""
    
    with open('DEMO_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("✅ Demo checklist created")
    return True

def validate_demo_readiness():
    """Validate that everything is ready for demo"""
    print("\n🔍 Validating Demo Readiness...")
    
    checks = []
    
    # Check required files
    required_files = [
        'docker-compose.yml',
        '.env.example', 
        'run_demo.sh',
        'README.md',
        'data/nutrition_lookup.csv'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            checks.append(f"✅ {file_path} exists")
        else:
            checks.append(f"❌ {file_path} missing")
    
    # Check frontend components
    frontend_components = [
        'frontend/src/pages/DailyPreview.tsx',
        'frontend/src/pages/SwitchupDiff.tsx', 
        'frontend/src/pages/WeeklySnapshot.tsx',
        'frontend/src/components/TabNavigation.tsx'
    ]
    
    for component in frontend_components:
        if Path(component).exists():
            checks.append(f"✅ {component} ready")
        else:
            checks.append(f"❌ {component} missing")
    
    # Check backend files
    backend_files = [
        'backend/app.py',
        'backend/models.py',
        'backend/requirements.txt'
    ]
    
    for file_path in backend_files:
        if Path(file_path).exists():
            checks.append(f"✅ {file_path} ready")
        else:
            checks.append(f"❌ {file_path} missing")
    
    # Print results
    for check in checks:
        print(check)
    
    success_count = len([c for c in checks if c.startswith("✅")])
    total_count = len(checks)
    
    print(f"\n📊 Demo Readiness: {success_count}/{total_count} checks passed")
    
    if success_count == total_count:
        print("🎉 Demo is ready! All components are in place.")
        return True
    else:
        print("⚠️  Some components are missing. Check the issues above.")
        return False

def main():
    """Prepare everything for demo"""
    print("🍅 Tamatar-Bhai MVP Demo Preparation")
    print("=" * 50)
    
    steps = [
        create_sample_data,
        create_demo_scenarios,
        create_demo_checklist,
        validate_demo_readiness
    ]
    
    success_count = 0
    for step in steps:
        try:
            if step():
                success_count += 1
        except Exception as e:
            print(f"❌ Step failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Demo Preparation: {success_count}/{len(steps)} steps completed")
    
    if success_count == len(steps):
        print("🎉 Demo preparation complete!")
        print("\n🚀 Ready to demo Tamatar-Bhai MVP!")
        print("   1. Start services: ./run_demo.sh")
        print("   2. Follow DEMO_CHECKLIST.md")
        print("   3. Use demo_scenarios.json for test cases")
        return True
    else:
        print("⚠️  Demo preparation incomplete. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)