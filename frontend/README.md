# Tamatar-Bhai Frontend

React + TypeScript + Vite frontend for the Tamatar-Bhai MVP application.

---

## 🏗️ Architecture

### Tech Stack
- **React 19.1.1**: UI framework
- **TypeScript 5.8.3**: Type safety
- **Vite 7.1.2**: Build tool and dev server
- **TailwindCSS 4.1.17**: Utility-first CSS
- **Axios 1.13.2**: HTTP client
- **date-fns 4.1.0**: Date manipulation
- **lucide-react 0.555.0**: Icon library

### Project Structure
```
src/
├── components/       # Reusable UI components
│   ├── ErrorBoundary.tsx
│   ├── ImageWithFallback.tsx
│   ├── LoadingSkeleton.tsx
│   ├── TabNavigation.tsx
│   └── index.ts
├── pages/           # Feature pages
│   ├── DailyPreview.tsx
│   ├── SwitchupDiff.tsx
│   ├── WeeklySnapshot.tsx
│   └── index.ts
├── services/        # API client
│   └── api.ts
├── types/           # TypeScript definitions
│   ├── api.ts
│   └── components.ts
├── App.tsx          # Main app component
├── App.css          # App-specific styles
├── main.tsx         # Entry point
└── index.css        # Global styles
```

---

## 🚀 Development

### Prerequisites
- Node.js 20+ 
- npm or yarn

### Setup
```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start dev server
npm run dev
```

### Available Scripts
```bash
npm run dev          # Start development server (port 5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run build:css    # Build Tailwind CSS
```

---

## 📦 Components

### Shared Components

#### ErrorBoundary
Catches React errors and displays fallback UI.

```tsx
import { ErrorBoundary } from './components';

<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>
```

#### LoadingSkeleton
Animated loading placeholders.

```tsx
import { LoadingSkeleton } from './components';

<LoadingSkeleton type="card" count={2} />
<LoadingSkeleton type="chart" />
<LoadingSkeleton type="text" />
<LoadingSkeleton type="image" />
```

#### ImageWithFallback
Smart image component with loading and error states.

```tsx
import { ImageWithFallback } from './components';

<ImageWithFallback
  src="/path/to/image.jpg"
  alt="Description"
  fallbackSrc="/placeholder.png"
  className="w-full h-64"
/>
```

#### TabNavigation
Top-level navigation component.

```tsx
import { TabNavigation } from './components';

<TabNavigation
  activeTab={activeTab}
  onTabChange={setActiveTab}
/>
```

---

## 🔌 API Service

### Usage

```tsx
import api from './services/api';

// Generate preview
const preview = await api.generatePreview('aloo paratha', 'lunch');

// Compare dishes
const comparison = await api.compareDishes('rajma', 'dal tadka');

// Get weekly snapshot
const weekly = await api.getWeeklySnapshot('2024-11-25', '2024-12-01');

// Get all dishes
const dishes = await api.getDishes();

// Health check
const health = await api.healthCheck();
```

### Error Handling

```tsx
import { formatErrorMessage } from './services/api';

try {
  const result = await api.generatePreview(dish, meal);
} catch (error) {
  const message = formatErrorMessage(error);
  console.error(message);
}
```

---

## 🎨 Styling

### TailwindCSS Configuration

Custom tomato theme colors:
```js
colors: {
  tomato: {
    50: '#fef2f2',
    100: '#fee2e2',
    // ... through 900
  }
}
```

### CSS Custom Properties

Available in `index.css`:
```css
--color-tomato-500: #ef4444;
--spacing-md: 1rem;
--radius-md: 0.5rem;
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
```

### Responsive Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

---

## 🧪 Testing

### Manual Testing Checklist

**Daily Preview:**
- [ ] Enter dish name and select meal
- [ ] Verify image loads
- [ ] Check calorie display
- [ ] Verify bhai and formal captions
- [ ] Test error handling
- [ ] Test loading states

**Switch-up Diff:**
- [ ] Compare two dishes
- [ ] Verify calorie difference
- [ ] Check recommendation
- [ ] Test swap button
- [ ] Test validation

**Weekly Snapshot:**
- [ ] Select date range
- [ ] Verify chart displays
- [ ] Check statistics
- [ ] Test date validation
- [ ] Test quick select buttons

---

## 🐛 Troubleshooting

### Common Issues

**"Cannot connect to backend"**
- Check if backend is running on port 8000
- Verify `VITE_API_BASE_URL` in `.env`
- Check CORS configuration

**"Module not found"**
```bash
rm -rf node_modules package-lock.json
npm install
```

**"Build fails"**
```bash
npm run lint
npm run build
```

**"Styles not applying"**
```bash
npm run build:css
```

---

## 📝 Development Guidelines

### Code Style
- Use TypeScript for type safety
- Follow React hooks best practices
- Use functional components
- Keep components small and focused
- Extract reusable logic into hooks

### Naming Conventions
- Components: PascalCase (`DailyPreview.tsx`)
- Files: camelCase for utilities, PascalCase for components
- CSS classes: Tailwind utilities preferred
- Functions: camelCase (`formatErrorMessage`)

### Component Structure
```tsx
// 1. Imports
import { useState } from 'react';
import { SomeType } from '../types';

// 2. Component definition
const MyComponent = ({ prop1, prop2 }: Props) => {
  // 3. State and hooks
  const [state, setState] = useState();
  
  // 4. Event handlers
  const handleClick = () => {};
  
  // 5. Render
  return <div>...</div>;
};

// 6. Export
export default MyComponent;
```

---

## 🚢 Deployment

### Docker Build
```bash
docker build -t tamatar-bhai-frontend .
docker run -p 3000:80 tamatar-bhai-frontend
```

### Production Build
```bash
npm run build
# Output in dist/
```

### Environment Variables
```bash
# Development
VITE_API_BASE_URL=http://localhost:8000

# Production
VITE_API_BASE_URL=https://api.yourdomain.com
```

---

## 📚 Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Axios Documentation](https://axios-http.com/docs/intro)

---

## 🤝 Contributing

1. Follow the existing code style
2. Add TypeScript types for new code
3. Test your changes manually
4. Update documentation if needed
5. Keep components focused and reusable

---

**Built with ❤️ for the Tamatar-Bhai community**
