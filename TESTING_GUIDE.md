# Tamatar-Bhai Testing Guide

**Complete step-by-step guide to test the application**

---

## 🚀 Step 1: Build and Start the Application

### Option A: Using Docker (Recommended)

```bash
# From project root directory
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d

# To view logs if running in detached mode
docker-compose logs -f
```

**Wait for**: Both services to show "healthy" status (30-60 seconds)

### Option B: Local Development (Without Docker)

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🔍 Step 2: Verify Services Are Running

### Check Backend Health
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-01T...",
  "service": "tamatar-bhai-api"
}
```

### Check Frontend
Open browser: http://localhost:3000

**Expected**: You should see the Tamatar-Bhai homepage with three tabs

### Check Docker Status (if using Docker)
```bash
docker-compose ps
```

**Expected**: Both `backend` and `frontend` services should be "Up" and "healthy"

---

## 🧪 Step 3: Test Each Feature

### Test 1: Daily Preview

1. **Navigate to**: http://localhost:3000 (should be on "Daily Preview" tab by default)

2. **Test with valid dish:**
   - Enter: `aloo paratha`
   - Select: `lunch`
   - Click: "Generate Preview"
   - **Expected**: 
     - Loading skeleton appears
     - After 5-10 seconds, see:
       - Dish image
       - Calorie count (320)
       - Bhai-style caption
       - Formal caption

3. **Test with another dish:**
   - Click "Reset"
   - Enter: `butter chicken`
   - Select: `dinner`
   - Click: "Generate Preview"
   - **Expected**: Similar results with different content

4. **Test error handling:**
   - Enter: `xyz123invalid`
   - Click: "Generate Preview"
   - **Expected**: Should still work (fuzzy matching or estimation)

5. **Test empty input:**
   - Clear the dish field
   - Click: "Generate Preview"
   - **Expected**: Error message "Please enter a dish name"

### Test 2: Switch-up Diff

1. **Navigate to**: Click "Switch-up Diff" tab

2. **Test comparison:**
   - First dish: `rajma`
   - Second dish: `dal tadka`
   - Click: "Compare Dishes"
   - **Expected**:
     - Loading skeleton
     - Two side-by-side cards
     - Green border on lighter dish
     - Calorie difference shown
     - Bhai-style recommendation

3. **Test swap button:**
   - Click: "⇄ Swap"
   - **Expected**: Dishes switch positions
   - Click: "Compare Dishes" again
   - **Expected**: Same results but dishes swapped

4. **Test same dish:**
   - Enter: `rajma` in both fields
   - Click: "Compare Dishes"
   - **Expected**: Error "Please enter two different dishes to compare"

5. **Test empty fields:**
   - Leave one field empty
   - Click: "Compare Dishes"
   - **Expected**: Error "Please enter both dish names"

### Test 3: Weekly Snapshot

1. **Navigate to**: Click "Weekly Snapshot" tab

2. **Test with default dates (last 7 days):**
   - Click: "Generate Snapshot"
   - **Expected**:
     - Loading skeleton
     - Three stat cards (Total, Average, Meals)
     - Chart image
     - Additional stats table
     - AI-generated summary
   - **Note**: If no data exists, you may see "no data" message

3. **Test quick select:**
   - Click: "Last 14 days"
   - Click: "Generate Snapshot"
   - **Expected**: Updated date range and results

4. **Test custom date range:**
   - Set start date: 7 days ago
   - Set end date: today
   - Click: "Generate Snapshot"
   - **Expected**: Results for that range

5. **Test date validation:**
   - Set end date before start date
   - Click: "Generate Snapshot"
   - **Expected**: Error "Start date must be before or equal to end date"

6. **Test future date:**
   - Set end date to tomorrow
   - Click: "Generate Snapshot"
   - **Expected**: Error "End date cannot be in the future"

---

## 🔄 Step 4: Test Navigation and UX

### Tab Navigation
1. Click through all three tabs
2. **Expected**: Smooth transitions, content changes

### Responsive Design
1. Resize browser window to mobile size (< 768px)
2. **Expected**: 
   - Layout stacks vertically
   - Buttons remain usable
   - Text remains readable

### Loading States
1. Trigger any API call
2. **Expected**: 
   - Loading skeleton appears immediately
   - Smooth transition to results

### Error Recovery
1. Stop the backend: `docker-compose stop backend`
2. Try to generate a preview
3. **Expected**: Error message with retry button
4. Restart backend: `docker-compose start backend`
5. Click retry
6. **Expected**: Should work now

---

## 🧰 Step 5: Test API Endpoints Directly

### Test Backend API (Optional)

```bash
# Test preview endpoint
curl -X POST http://localhost:8000/api/preview \
  -H "Content-Type: application/json" \
  -d '{"dish":"aloo paratha","meal":"lunch"}'

# Test compare endpoint
curl -X POST http://localhost:8000/api/compare \
  -H "Content-Type: application/json" \
  -d '{"dishA":"rajma","dishB":"dal tadka"}'

# Test weekly endpoint
curl "http://localhost:8000/api/weekly?start=2024-11-25&end=2024-12-01"

# List all dishes
curl http://localhost:8000/api/dishes

# View API docs
open http://localhost:8000/docs
```

---

## 📊 Step 6: Check Logs

### Docker Logs
```bash
# View all logs
docker-compose logs

# View backend logs only
docker-compose logs backend

# View frontend logs only
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

### Look for:
- ✅ No error messages
- ✅ Successful API calls
- ✅ 200 status codes
- ❌ Any 500 errors or exceptions

---

## 🛑 Step 7: Stop the Application

### Docker
```bash
# Stop services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# Stop but keep containers
docker-compose stop
```

### Local Development
- Press `Ctrl+C` in both terminal windows

---

## ✅ Success Criteria Checklist

### Functional Tests
- [ ] Daily Preview generates image and captions
- [ ] Switch-up Diff compares dishes correctly
- [ ] Weekly Snapshot shows chart and summary
- [ ] Tab navigation works smoothly
- [ ] All forms validate input properly
- [ ] Error messages are clear and helpful
- [ ] Loading states appear during API calls
- [ ] Reset buttons clear forms

### Visual Tests
- [ ] Layout looks clean and organized
- [ ] Colors match tomato theme (red accents)
- [ ] Text is readable
- [ ] Images load properly
- [ ] Responsive design works on mobile
- [ ] Buttons are clickable and styled
- [ ] Cards have proper shadows and borders

### Technical Tests
- [ ] Backend health check returns 200
- [ ] Frontend loads without console errors
- [ ] API calls complete successfully
- [ ] Docker containers are healthy
- [ ] No memory leaks or crashes
- [ ] Images are cached properly

---

## 🐛 Common Issues and Solutions

### Issue: "Cannot connect to backend"
**Solution:**
```bash
# Check if backend is running
docker-compose ps
# Or
curl http://localhost:8000/health

# Restart backend
docker-compose restart backend
```

### Issue: "Port already in use"
**Solution:**
```bash
# Find process using port 3000 or 8000
lsof -i :3000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Issue: "Frontend shows blank page"
**Solution:**
1. Check browser console for errors (F12)
2. Verify API URL in .env file
3. Clear browser cache
4. Rebuild: `docker-compose up --build`

### Issue: "Images not loading"
**Solution:**
1. Check if StabilityAI API key is set
2. Check backend logs for errors
3. Verify `/data/images/` directory exists
4. Check nginx proxy configuration

### Issue: "No data for weekly snapshot"
**Solution:**
1. Add some meals first using Daily Preview
2. Or use admin endpoint to add test data:
```bash
curl -X POST http://localhost:8000/admin/user_meal \
  -H "Content-Type: application/json" \
  -d '{
    "dish_name": "Aloo Paratha",
    "meal_type": "lunch",
    "calories": 320
  }'
```

---

## 📸 Expected Screenshots

### Daily Preview
- Header with tomato logo
- Form with dish input and meal selector
- Large calorie count display
- Orange/red card for bhai caption
- Blue card for formal caption

### Switch-up Diff
- Two input fields side by side
- Swap button between them
- Two comparison cards
- Green border on lighter dish
- Orange recommendation card

### Weekly Snapshot
- Date pickers
- Quick select buttons
- Three stat cards (red, blue, green)
- Chart image
- Stats table
- Blue summary card

---

## 🎯 Performance Benchmarks

### Expected Response Times
- Daily Preview: 5-15 seconds (image generation is slow)
- Switch-up Diff: 2-5 seconds
- Weekly Snapshot: 3-8 seconds (chart generation)
- Tab switching: < 100ms
- Page load: < 2 seconds

### Resource Usage
- Backend memory: ~200-300 MB
- Frontend memory: ~50-100 MB
- Docker total: ~500 MB

---

## 📝 Test Report Template

```markdown
# Test Report - Tamatar-Bhai MVP

**Date**: [Date]
**Tester**: [Name]
**Environment**: Docker / Local

## Test Results

### Daily Preview
- [ ] Pass / [ ] Fail
- Notes: 

### Switch-up Diff
- [ ] Pass / [ ] Fail
- Notes:

### Weekly Snapshot
- [ ] Pass / [ ] Fail
- Notes:

### Navigation
- [ ] Pass / [ ] Fail
- Notes:

### Responsive Design
- [ ] Pass / [ ] Fail
- Notes:

## Issues Found
1. 
2. 
3. 

## Overall Status
- [ ] Ready for demo
- [ ] Needs fixes
- [ ] Blocked

## Recommendations
1. 
2. 
3. 
```

---

## 🎉 Next Steps After Testing

1. **If all tests pass**: Application is ready for demo!
2. **If issues found**: Document them and prioritize fixes
3. **Performance issues**: Check logs and optimize
4. **UI improvements**: Gather feedback and iterate

---

**Happy Testing! 🍅**

*"Bhai, test karo aur bugs dhundo!" 🐛*
