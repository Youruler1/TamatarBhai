# Implementation Plan

- [x] 1. Set up project structure and core configuration


  - Create directory structure for backend/, frontend/, data/ folders
  - Set up Docker configuration files (Dockerfiles, docker-compose.yml)
  - Create environment configuration files (.env.example)
  - Initialize package.json for frontend and requirements.txt for backend
  - _Requirements: 6.1, 6.2, 6.3, 7.6, 11.1, 11.2, 11.3_

- [x] 2. Create nutrition lookup data and database schema


  - Generate nutrition_lookup.csv with 50+ Indian dishes and calorie data
  - Create SQLite database schema with dishes, cache, and user_meals tables
  - Implement database initialization scripts
  - Set up data directory structure with images/ subdirectory
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 3. Implement backend API foundation


  - Set up FastAPI application with basic configuration
  - Create model_routes.json configuration file for external API routing
  - Implement database connection and ORM models using SQLAlchemy
  - Create basic API endpoint structure with proper error handling
  - _Requirements: 6.2, 7.6, 10.4_

- [x] 4. Build external API integration services


  - Implement OpenAI service class with gpt-4o-mini integration
  - Create StabilityAI service class with stable-diffusion-2 integration
  - Implement proper API key management from environment variables
  - Add fallback mechanisms for API failures
  - _Requirements: 6.5, 6.6, 7.7, 10.1, 10.2, 10.3_

- [x] 5. Implement "bhai style" caption generation

  - Create explicit bhai style persona definition for OpenAI prompts
  - Implement bhai-style caption generation with few-shot prompting
  - Implement formal caption generation
  - Test and validate bhai style output matches requirements
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 6. Build nutrition lookup and caching system


  - Implement fuzzy string matching for dish name lookup
  - Create caching manager for storing generated content
  - Implement cache invalidation and TTL management
  - Add database operations for cache management
  - _Requirements: 8.4, 8.5, 2.6_

- [x] 7. Implement Daily Preview API endpoint


  - Create POST /api/preview endpoint with request/response models
  - Integrate image generation with StabilityAI
  - Implement image saving to data/images/ directory
  - Add calorie lookup with fuzzy matching
  - Generate both bhai and formal captions
  - Implement caching for complete preview responses
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 7.1_

- [x] 8. Implement Switch-up Diff API endpoint


  - Create POST /api/compare endpoint with request/response models
  - Implement calorie retrieval for both dishes
  - Generate bhai-style comparison suggestion using OpenAI
  - Add proper error handling and validation
  - _Requirements: 2.1, 2.2, 2.3, 7.3_

- [x] 9. Implement Weekly Snapshot API endpoint


  - Create GET /api/weekly endpoint with date range parameters
  - Implement calorie calculation for date ranges
  - Create matplotlib chart generation for weekly data
  - Generate formal summary using OpenAI
  - Save charts as PNG files and return URLs
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 6.7, 7.4_

- [x] 10. Implement admin management endpoints

  - Create POST /admin/dish endpoint for adding/editing dishes
  - Implement POST /admin/cache/clear endpoint for cache management
  - Add proper validation and error handling for admin operations
  - Provide confirmation feedback for admin actions
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 7.5_

- [x] 11. Build React frontend foundation



  - Initialize React + Vite project with TypeScript
  - Set up component structure and routing
  - Implement tab-based navigation (Daily Preview, Switch-up, Weekly)
  - Create shared components (LoadingSkeleton, ErrorBoundary, ImageWithFallback)
  - Add basic styling with CSS or Tailwind
  - _Requirements: 6.1, 9.1, 9.2_

- [x] 12. Implement Daily Preview frontend component



  - Create DailyPreview component with dish and meal input forms
  - Implement API integration for preview generation
  - Add loading skeletons during API calls
  - Display generated image, calories, and both caption styles
  - Handle error states and fallback content
  - _Requirements: 1.7, 9.3, 10.1_

- [x] 13. Implement Switch-up Diff frontend component




  - Create SwitchupDiff component with two dish input fields
  - Implement API integration for dish comparison
  - Display calories for both dishes and bhai-style suggestion
  - Add loading states and error handling
  - _Requirements: 2.3, 9.3_




- [ ] 14. Implement Weekly Snapshot frontend component
  - Create WeeklySnapshot component with date range picker
  - Implement API integration for weekly data retrieval
  - Display generated chart and formal summary



  - Add loading states and proper error handling
  - _Requirements: 3.5, 9.3_

- [x] 15. Add API attribution and loading states



  - Include "Generated by OpenAI / StabilityAI" footnotes on all generated content
  - Implement comprehensive loading skeletons for all API operations
  - Add proper error messages and retry mechanisms
  - Ensure graceful degradation when APIs are unavailable
  - _Requirements: 9.4, 9.3, 10.1, 10.2, 10.3_



- [x] 16. Implement Docker containerization

  - Create Dockerfile for backend with FastAPI and dependencies
  - Create Dockerfile for frontend with React build process
  - Configure docker-compose.yml with proper service dependencies
  - Set up volume mounting for data persistence


  - Test container builds and inter-service communication
  - _Requirements: 6.4, 11.2, 11.6_



- [ ] 17. Create demo script and documentation
  - Write comprehensive README.md with setup instructions
  - Create run_demo.sh script for easy application startup

  - Document API endpoints and usage examples
  - Include demo flow instructions for testing all features
  - Add troubleshooting section for common issues


  - _Requirements: 11.4, 11.5_

- [ ] 18. Implement comprehensive error handling and testing
  - Add proper error handling for all API endpoints
  - Implement fallback mechanisms for external API failures
  - Create unit tests for critical backend functions


  - Test frontend components with mock API responses
  - Verify application works without crashes when APIs fail
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 19. Final integration testing and optimization
  - Test complete application flow from docker-compose up



  - Verify all features work end-to-end
  - Test with actual OpenAI and StabilityAI API calls
  - Optimize performance and loading times
  - Ensure application is accessible at http://localhost:3000
  - _Requirements: 11.6, 9.5_

- [ ] 20. Polish UI and prepare for demo
  - Apply final styling and ensure clean card-based design
  - Test responsive design on different screen sizes
  - Verify all loading states and error messages are user-friendly
  - Ensure smooth navigation between tabs
  - Prepare sample data and demo scenarios
  - _Requirements: 9.1, 9.2, 9.3, 9.4_