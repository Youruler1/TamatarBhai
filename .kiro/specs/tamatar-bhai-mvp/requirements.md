# Requirements Document

## Introduction

Tamatar-Bhai is a 1-day MVP web application that provides AI-powered food insights with a friendly "bhai style" personality. The app helps users get nutritional information, visual representations of dishes, and personalized recommendations using external AI APIs (OpenAI and StabilityAI). The application must be fully containerized and demoable on a local laptop.

## Requirements

### Requirement 1: Daily Preview Feature

**User Story:** As a user, I want to get AI-generated insights about a dish including image, calories, and captions, so that I can visualize and understand my meal better.

#### Acceptance Criteria

1. WHEN user inputs dish name and meal type THEN system SHALL generate a complete preview with image, calories, and dual captions
2. WHEN StabilityAI generates an image THEN system SHALL save it to data/images/ directory with proper caching
3. IF StabilityAI fails THEN system SHALL fallback to web image fetch or placeholder image
4. WHEN system looks up calories THEN system SHALL use fuzzy matching against nutrition_lookup.csv
5. WHEN generating captions THEN system SHALL create both "bhai style" and "formal" versions using OpenAI
6. WHEN preview is generated THEN system SHALL cache results in SQLite database
7. WHEN API calls are in progress THEN system SHALL show loading skeletons to user

### Requirement 2: Switch-up Diff Feature

**User Story:** As a user, I want to compare two dishes and get a recommendation, so that I can make better food choices.

#### Acceptance Criteria

1. WHEN user inputs two dish names THEN system SHALL retrieve calories for both dishes
2. WHEN comparison is requested THEN system SHALL generate a 1-line "bhai style" suggestion using OpenAI
3. WHEN comparison results are ready THEN system SHALL display calories and recommendation clearly

### Requirement 3: Weekly Snapshot Feature

**User Story:** As a user, I want to see my weekly calorie consumption with visual charts and summary, so that I can track my eating patterns.

#### Acceptance Criteria

1. WHEN user selects date range THEN system SHALL calculate total calories for the period
2. WHEN weekly data is processed THEN system SHALL generate a bar chart using matplotlib
3. WHEN chart is created THEN system SHALL save it as PNG file
4. WHEN summary is requested THEN system SHALL generate formal 3-4 sentence summary via OpenAI
5. WHEN weekly snapshot is displayed THEN system SHALL show both chart and text summary

### Requirement 4: Admin Management Feature

**User Story:** As an admin, I want to manage dishes and clear cache, so that I can maintain the application data.

#### Acceptance Criteria

1. WHEN admin accesses admin panel THEN system SHALL allow adding new dishes to SQLite
2. WHEN admin edits dish THEN system SHALL update dish information in database
3. WHEN admin clears cache THEN system SHALL remove cached data for specified dish
4. WHEN admin operations complete THEN system SHALL provide confirmation feedback

### Requirement 5: AI Integration with Bhai Style Personality

**User Story:** As a user, I want to receive responses in a friendly "bhai style" tone, so that the interaction feels personal and engaging.

#### Acceptance Criteria

1. WHEN system generates "bhai style" content THEN it SHALL use Hinglish (English + Hindi mix)
2. WHEN creating bhai responses THEN system SHALL sound like friendly Indian college student
3. WHEN generating bhai content THEN system SHALL use light humor and informal slang (no profanity)
4. WHEN bhai responses are created THEN they SHALL be short and punchy (1-2 lines max)
5. WHEN prompting OpenAI THEN system SHALL include explicit bhai style definition in few-shot prompts

### Requirement 6: Technical Architecture

**User Story:** As a developer, I want a containerized full-stack application, so that it can be easily deployed and demonstrated.

#### Acceptance Criteria

1. WHEN application is built THEN frontend SHALL use React + Vite
2. WHEN backend is implemented THEN it SHALL use FastAPI framework
3. WHEN data storage is needed THEN system SHALL use SQLite database
4. WHEN containerization is required THEN system SHALL use Docker + docker-compose
5. WHEN text generation is needed THEN system SHALL use OpenAI gpt-4o-mini
6. WHEN image generation is needed THEN system SHALL use StabilityAI stable-diffusion-2
7. WHEN charts are generated THEN system SHALL use matplotlib to create PNG files

### Requirement 7: API Endpoints and Configuration

**User Story:** As a system integrator, I want well-defined API endpoints and configuration, so that the application components can communicate effectively.

#### Acceptance Criteria

1. WHEN backend starts THEN it SHALL provide POST /api/preview endpoint
2. WHEN dishes are requested THEN system SHALL provide GET /api/dishes endpoint
3. WHEN comparison is needed THEN system SHALL provide POST /api/compare endpoint
4. WHEN weekly data is requested THEN system SHALL provide GET /api/weekly endpoint
5. WHEN admin functions are needed THEN system SHALL provide POST /admin/dish and POST /admin/cache/clear endpoints
6. WHEN model routing is configured THEN system SHALL use backend/model_routes.json file
7. WHEN external APIs are called THEN system SHALL use proper API keys from environment variables

### Requirement 8: Data Management and Caching

**User Story:** As a system user, I want fast responses and proper data management, so that the application performs efficiently.

#### Acceptance Criteria

1. WHEN nutrition data is needed THEN system SHALL use nutrition_lookup.csv with 50+ dishes
2. WHEN caching is implemented THEN system SHALL create SQLite tables for dishes and cache
3. WHEN images are generated THEN system SHALL save them in data/images/ directory
4. WHEN cache lookup occurs THEN system SHALL check for existing dish data before API calls
5. WHEN fuzzy matching is performed THEN system SHALL find closest dish match in nutrition database

### Requirement 9: User Interface and Experience

**User Story:** As a user, I want a clean and intuitive interface, so that I can easily navigate and use all features.

#### Acceptance Criteria

1. WHEN user accesses application THEN interface SHALL use top tab layout with Daily Preview, Switch-up, Weekly tabs
2. WHEN styling is applied THEN system SHALL use clean cards and minimal design
3. WHEN API calls are in progress THEN system SHALL show loading skeletons
4. WHEN content is generated THEN system SHALL include footnote "Generated by OpenAI / StabilityAI"
5. WHEN application loads THEN it SHALL be accessible at http://localhost:3000

### Requirement 10: Error Handling and Reliability

**User Story:** As a user, I want the application to work reliably even when external services fail, so that I can always get some response.

#### Acceptance Criteria

1. WHEN external APIs fail THEN system SHALL provide fallback responses or placeholders
2. WHEN StabilityAI is unavailable THEN system SHALL use web image fetch or placeholder images
3. WHEN OpenAI is unavailable THEN system SHALL provide default captions or cached responses
4. WHEN database operations fail THEN system SHALL handle errors gracefully without crashes
5. WHEN any component fails THEN system SHALL log errors and continue operating

### Requirement 11: Deployment and Documentation

**User Story:** As a developer or user, I want clear setup instructions and easy deployment, so that I can run the application locally.

#### Acceptance Criteria

1. WHEN repository is provided THEN it SHALL include complete backend/ and frontend/ directories
2. WHEN Docker setup is needed THEN system SHALL provide Dockerfiles and docker-compose.yml
3. WHEN environment setup is required THEN system SHALL include .env.example file
4. WHEN demo is needed THEN system SHALL provide run_demo.sh script
5. WHEN documentation is accessed THEN README.md SHALL contain detailed setup and demo instructions
6. WHEN application is started THEN command "docker-compose up --build" SHALL launch complete system