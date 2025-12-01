# Tamatar-Bhai Quick Start Guide

**Get up and running in 5 minutes!** ⚡

---

## 🚀 Fastest Way to Start

```bash
# 1. Make demo script executable
chmod +x run_demo.sh

# 2. Run it!
./run_demo.sh
```

That's it! The script will:
- ✅ Check prerequisites
- ✅ Build and start services
- ✅ Open your browser
- ✅ Show you the application

---

## 🎯 Manual Start (Alternative)

### Step 1: Start Services
```bash
docker-compose up --build -d
```

### Step 2: Wait 30-60 seconds
Services need time to become healthy.

### Step 3: Open Browser
```
http://localhost:3000
```

---

## 🧪 Quick Test

### Test 1: Daily Preview
1. Enter: `aloo paratha`
2. Select: `lunch`
3. Click: "Generate Preview"
4. Wait 5-10 seconds
5. See results!

### Test 2: Compare Dishes
1. Click: "Switch-up Diff" tab
2. Enter: `rajma` and `dal tadka`
3. Click: "Compare Dishes"
4. See comparison!

### Test 3: Weekly View
1. Click: "Weekly Snapshot" tab
2. Click: "Last 7 days"
3. Click: "Generate Snapshot"
4. See chart and stats!

---

## 🛑 Stop Services

```bash
docker-compose down
```

---

## 📊 Check Status

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Check backend health
curl http://localhost:8000/health
```

---

## 🐛 Quick Troubleshooting

### Problem: Port already in use
```bash
# Find and kill process on port 3000
lsof -i :3000
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Problem: Services not starting
```bash
# Check logs
docker-compose logs

# Restart
docker-compose restart

# Clean rebuild
docker-compose down -v
docker-compose up --build
```

### Problem: API keys not set
```bash
# Edit .env file
nano .env

# Add your keys:
OPENAI_API_KEY=your_key_here
STABILITY_KEY=your_key_here

# Restart
docker-compose restart
```

---

## 📚 More Information

- **Full Testing Guide**: `TESTING_GUIDE.md`
- **Demo Script**: `DEMO_FLOW.md`
- **Build Summary**: `FRONTEND_BUILD_SUMMARY.md`
- **Component Docs**: `frontend/README.md`

---

## 🎉 You're Ready!

The application is now running at:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Enjoy exploring Tamatar-Bhai!** 🍅

*"Bhai, ab maza aayega!" 😄*
