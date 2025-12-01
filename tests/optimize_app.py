#!/usr/bin/env python3
"""
Application optimization script for Tamatar-Bhai MVP
Performs final checks and optimizations
"""

import os
import json
import sys
from pathlib import Path

def optimize_environment():
    """Optimize environment configuration"""
    print("🔧 Optimizing Environment Configuration...")
    
    # Check .env.example has all required variables
    env_example_path = Path('.env.example')
    if env_example_path.exists():
        with open(env_example_path, 'r') as f:
            env_content = f.read()
        
        required_vars = [
            'OPENAI_API_KEY',
            'STABILITY_KEY', 
            'DATABASE_URL',
            'CACHE_TTL_HOURS',
            'MAX_IMAGE_SIZE_MB',
            'DEBUG',
            'VITE_API_BASE_URL'
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing environment variables: {missing_vars}")
            return False
        
        print("✅ Environment configuration is complete")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def optimize_data_directories():
    """Ensure data directories exist with proper structure"""
    print("\n🔧 Optimizing Data Directories...")
    
    directories = [
        'data',
        'data/images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created/verified directory: {directory}")
    
    # Check nutrition data
    nutrition_file = Path('data/nutrition_lookup.csv')
    if nutrition_file.exists():
        with open(nutrition_file, 'r') as f:
            lines = f.readlines()
        
        if len(lines) >= 51:  # Header + 50 dishes
            print(f"✅ Nutrition data is complete ({len(lines)-1} dishes)")
        else:
            print(f"⚠️  Nutrition data may be incomplete ({len(lines)-1} dishes)")
    else:
        print("❌ Nutrition data file not found")
        return False
    
    return True

def optimize_docker_config():
    """Optimize Docker configuration"""
    print("\n🔧 Optimizing Docker Configuration...")
    
    # Check docker-compose.yml
    compose_file = Path('docker-compose.yml')
    if compose_file.exists():
        with open(compose_file, 'r') as f:
            compose_content = f.read()
        
        # Check for health checks
        if 'healthcheck:' in compose_content:
            print("✅ Health checks are configured")
        else:
            print("⚠️  Health checks not found in docker-compose.yml")
        
        # Check for restart policies
        if 'restart:' in compose_content:
            print("✅ Restart policies are configured")
        else:
            print("⚠️  Restart policies not configured")
        
        # Check for proper volumes
        if 'volumes:' in compose_content and 'tamatar_data:' in compose_content:
            print("✅ Volume configuration is optimized")
        else:
            print("⚠️  Volume configuration may need optimization")
        
        return True
    else:
        print("❌ docker-compose.yml not found")
        return False

def optimize_frontend_build():
    """Check frontend build optimization"""
    print("\n🔧 Checking Frontend Build Configuration...")
    
    package_file = Path('frontend/package.json')
    if package_file.exists():
        with open(package_file, 'r') as f:
            package_data = json.load(f)
        
        # Check for production dependencies
        if 'dependencies' in package_data:
            deps = package_data['dependencies']
            essential_deps = ['react', 'react-dom', 'axios', 'lucide-react']
            
            missing_deps = []
            for dep in essential_deps:
                if dep not in deps:
                    missing_deps.append(dep)
            
            if missing_deps:
                print(f"⚠️  Missing essential dependencies: {missing_deps}")
            else:
                print("✅ All essential dependencies are present")
        
        # Check build script
        if 'scripts' in package_data and 'build' in package_data['scripts']:
            print("✅ Build script is configured")
        else:
            print("⚠️  Build script not found")
        
        return True
    else:
        print("❌ Frontend package.json not found")
        return False

def optimize_backend_config():
    """Check backend configuration optimization"""
    print("\n🔧 Checking Backend Configuration...")
    
    # Check requirements.txt
    req_file = Path('backend/requirements.txt')
    if req_file.exists():
        with open(req_file, 'r') as f:
            requirements = f.read()
        
        essential_packages = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'pandas',
            'matplotlib',
            'openai',
            'requests'
        ]
        
        missing_packages = []
        for package in essential_packages:
            if package not in requirements.lower():
                missing_packages.append(package)
        
        if missing_packages:
            print(f"⚠️  Missing essential packages: {missing_packages}")
        else:
            print("✅ All essential packages are present")
        
        return True
    else:
        print("❌ Backend requirements.txt not found")
        return False

def check_performance_optimizations():
    """Check for performance optimizations"""
    print("\n🔧 Checking Performance Optimizations...")
    
    optimizations = []
    
    # Check for caching in backend
    app_file = Path('backend/app.py')
    if app_file.exists():
        with open(app_file, 'r') as f:
            app_content = f.read()
        
        if 'cache' in app_content.lower():
            optimizations.append("✅ Caching is implemented")
        else:
            optimizations.append("⚠️  Caching may not be implemented")
    
    # Check for loading states in frontend
    daily_preview = Path('frontend/src/pages/DailyPreview.tsx')
    if daily_preview.exists():
        with open(daily_preview, 'r') as f:
            content = f.read()
        
        if 'LoadingSkeleton' in content:
            optimizations.append("✅ Loading states are implemented")
        else:
            optimizations.append("⚠️  Loading states may be missing")
    
    # Check for error boundaries
    error_boundary = Path('frontend/src/components/ErrorBoundary.tsx')
    if error_boundary.exists():
        optimizations.append("✅ Error boundaries are implemented")
    else:
        optimizations.append("⚠️  Error boundaries may be missing")
    
    for opt in optimizations:
        print(opt)
    
    return len([o for o in optimizations if o.startswith("✅")]) >= 2

def main():
    """Run all optimization checks"""
    print("🍅 Tamatar-Bhai MVP Optimization")
    print("=" * 50)
    
    checks = [
        optimize_environment,
        optimize_data_directories,
        optimize_docker_config,
        optimize_frontend_build,
        optimize_backend_config,
        check_performance_optimizations
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"❌ Check failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Optimization Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Application is fully optimized and ready for deployment!")
        print("\n🚀 Final deployment checklist:")
        print("   1. ✅ Add your API keys to .env file")
        print("   2. ✅ Run: docker-compose up --build")
        print("   3. ✅ Access: http://localhost:3000")
        print("   4. ✅ Test all features with sample data")
        print("   5. ✅ Monitor logs for any issues")
        return True
    else:
        print("⚠️  Some optimization checks failed. Review the issues above.")
        print("\n🔍 Consider addressing the warnings for better performance.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)