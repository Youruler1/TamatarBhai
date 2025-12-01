#!/usr/bin/env node
/**
 * Simple frontend validation test without external dependencies
 */

const fs = require('fs');
const path = require('path');

function testPackageJson() {
    console.log('🧪 Testing Frontend Package Configuration...');
    
    try {
        const packagePath = path.join('frontend', 'package.json');
        const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
        
        // Check required dependencies
        const requiredDeps = [
            'react',
            'react-dom', 
            'axios',
            'lucide-react',
            'clsx',
            'date-fns'
        ];
        
        for (const dep of requiredDeps) {
            if (!packageJson.dependencies[dep]) {
                throw new Error(`Missing dependency: ${dep}`);
            }
        }
        
        // Check required dev dependencies
        const requiredDevDeps = [
            '@types/react',
            '@types/react-dom',
            '@vitejs/plugin-react',
            'typescript',
            'vite',
            'tailwindcss'
        ];
        
        for (const dep of requiredDevDeps) {
            if (!packageJson.devDependencies[dep]) {
                throw new Error(`Missing dev dependency: ${dep}`);
            }
        }
        
        // Check scripts
        const requiredScripts = ['dev', 'build', 'preview'];
        for (const script of requiredScripts) {
            if (!packageJson.scripts[script]) {
                throw new Error(`Missing script: ${script}`);
            }
        }
        
        console.log('✅ Package.json configuration is valid');
        return true;
        
    } catch (error) {
        console.log(`❌ Package.json test failed: ${error.message}`);
        return false;
    }
}

function testComponentStructure() {
    console.log('\n🧪 Testing Component Structure...');
    
    try {
        const requiredFiles = [
            'frontend/src/App.tsx',
            'frontend/src/main.tsx',
            'frontend/src/App.css',
            'frontend/src/services/api.ts',
            'frontend/src/components/LoadingSkeleton.tsx',
            'frontend/src/components/ImageWithFallback.tsx',
            'frontend/src/components/ErrorBoundary.tsx',
            'frontend/src/pages/DailyPreview.tsx',
            'frontend/src/pages/SwitchupDiff.tsx',
            'frontend/src/pages/WeeklySnapshot.tsx'
        ];
        
        for (const file of requiredFiles) {
            if (!fs.existsSync(file)) {
                throw new Error(`Missing file: ${file}`);
            }
        }
        
        console.log('✅ All required components exist');
        return true;
        
    } catch (error) {
        console.log(`❌ Component structure test failed: ${error.message}`);
        return false;
    }
}

function testApiService() {
    console.log('\n🧪 Testing API Service...');
    
    try {
        const apiPath = path.join('frontend', 'src', 'services', 'api.ts');
        const apiContent = fs.readFileSync(apiPath, 'utf8');
        
        // Check required API functions
        const requiredFunctions = [
            'generatePreview',
            'compareDishes', 
            'getWeeklySnapshot',
            'getDishes',
            'healthCheck'
        ];
        
        for (const func of requiredFunctions) {
            if (!apiContent.includes(func)) {
                throw new Error(`Missing API function: ${func}`);
            }
        }
        
        // Check required interfaces
        const requiredInterfaces = [
            'PreviewRequest',
            'PreviewResponse',
            'CompareRequest',
            'CompareResponse',
            'WeeklyResponse'
        ];
        
        for (const interface of requiredInterfaces) {
            if (!apiContent.includes(interface)) {
                throw new Error(`Missing interface: ${interface}`);
            }
        }
        
        // Check error handling
        if (!apiContent.includes('interceptors')) {
            throw new Error('Missing axios interceptors for error handling');
        }
        
        console.log('✅ API service is properly structured');
        return true;
        
    } catch (error) {
        console.log(`❌ API service test failed: ${error.message}`);
        return false;
    }
}

function testErrorHandling() {
    console.log('\n🧪 Testing Error Handling...');
    
    try {
        // Check ErrorBoundary component
        const errorBoundaryPath = path.join('frontend', 'src', 'components', 'ErrorBoundary.tsx');
        const errorBoundaryContent = fs.readFileSync(errorBoundaryPath, 'utf8');
        
        if (!errorBoundaryContent.includes('componentDidCatch')) {
            throw new Error('ErrorBoundary missing componentDidCatch');
        }
        
        if (!errorBoundaryContent.includes('getDerivedStateFromError')) {
            throw new Error('ErrorBoundary missing getDerivedStateFromError');
        }
        
        // Check page components have error handling
        const pageFiles = [
            'frontend/src/pages/DailyPreview.tsx',
            'frontend/src/pages/SwitchupDiff.tsx',
            'frontend/src/pages/WeeklySnapshot.tsx'
        ];
        
        for (const pageFile of pageFiles) {
            const content = fs.readFileSync(pageFile, 'utf8');
            
            if (!content.includes('catch') || !content.includes('error')) {
                throw new Error(`${pageFile} missing error handling`);
            }
            
            if (!content.includes('setError')) {
                throw new Error(`${pageFile} missing error state management`);
            }
        }
        
        console.log('✅ Error handling is properly implemented');
        return true;
        
    } catch (error) {
        console.log(`❌ Error handling test failed: ${error.message}`);
        return false;
    }
}

function testLoadingStates() {
    console.log('\n🧪 Testing Loading States...');
    
    try {
        // Check LoadingSkeleton component
        const skeletonPath = path.join('frontend', 'src', 'components', 'LoadingSkeleton.tsx');
        const skeletonContent = fs.readFileSync(skeletonPath, 'utf8');
        
        const requiredTypes = ['card', 'chart', 'text', 'image'];
        for (const type of requiredTypes) {
            if (!skeletonContent.includes(`'${type}'`)) {
                throw new Error(`LoadingSkeleton missing type: ${type}`);
            }
        }
        
        // Check page components use loading states
        const pageFiles = [
            'frontend/src/pages/DailyPreview.tsx',
            'frontend/src/pages/SwitchupDiff.tsx', 
            'frontend/src/pages/WeeklySnapshot.tsx'
        ];
        
        for (const pageFile of pageFiles) {
            const content = fs.readFileSync(pageFile, 'utf8');
            
            if (!content.includes('LoadingSkeleton')) {
                throw new Error(`${pageFile} missing LoadingSkeleton usage`);
            }
            
            if (!content.includes('isLoading')) {
                throw new Error(`${pageFile} missing loading state`);
            }
        }
        
        console.log('✅ Loading states are properly implemented');
        return true;
        
    } catch (error) {
        console.log(`❌ Loading states test failed: ${error.message}`);
        return false;
    }
}

function main() {
    console.log('🍅 Tamatar-Bhai Frontend Tests');
    console.log('=' .repeat(40));
    
    const tests = [
        testPackageJson,
        testComponentStructure,
        testApiService,
        testErrorHandling,
        testLoadingStates
    ];
    
    let passed = 0;
    const total = tests.length;
    
    for (const test of tests) {
        try {
            if (test()) {
                passed++;
            }
        } catch (error) {
            console.log(`❌ Test failed with exception: ${error.message}`);
        }
    }
    
    console.log('\n' + '='.repeat(40));
    console.log(`📊 Test Results: ${passed}/${total} tests passed`);
    
    if (passed === total) {
        console.log('🎉 All frontend tests passed! Ready for deployment.');
        return true;
    } else {
        console.log('⚠️  Some tests failed. Check the issues above.');
        return false;
    }
}

if (require.main === module) {
    const success = main();
    process.exit(success ? 0 : 1);
}