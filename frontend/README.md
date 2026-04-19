# BiltyBook Intelligence - Frontend

Modern React dashboard for real-time transport monitoring and AI-powered decision support.

## Architecture

### Pages
- **Dashboard**: Live KPI cards, trip feed with risk visualization
- **Bilties**: Create and manage transport documents
- **Simulation**: Decision support with AI recommendations

### Components
- **KPICard**: Key metric displays (Active Trips, At Risk, Delayed, Net Profit)
- **TripCard**: Individual trip card with risk color-coding
- **TripFeed**: Grid view of all active trips
- **SimulationCard**: Action option cards (Continue, Reroute, Hold, SpeedUp)
- **Copilot**: Floating AI assistant with chat interface

### Features
✅ Real-time trip tracking with live updates
✅ ML-based risk prediction (Green/Yellow/Orange/Red)
✅ AI-powered decision simulation
✅ Conversational copilot assistant
✅ Responsive design for desktop/tablet/mobile
✅ Live KPI dashboard with metrics
✅ Bilty document management

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons

## Setup

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend running at `http://localhost:8000`

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Setup environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   VITE_API_URL=http://localhost:8000
   ```

## Development

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`

Vite proxy automatically forwards `/api` requests to backend.

## Building

```bash
npm run build
```

Creates optimized production build in `dist/` directory.

## File Structure

```
src/
├── pages/
│   ├── Dashboard.jsx      # Main dashboard with KPIs and trip feed
│   ├── Bilties.jsx        # Bilty CRUD management
│   └── Simulation.jsx     # Decision support interface
├── components/
│   ├── KPICard.jsx        # KPI display component
│   ├── TripFeed.jsx       # Trip grid view
│   ├── TripCard.jsx       # Individual trip card
│   ├── SimulationCard.jsx # Action option card
│   └── Copilot.jsx        # AI assistant chat
├── App.jsx                # Main router
├── main.jsx               # Entry point
└── index.css              # Global styles + Tailwind
```

## Risk Level Color Coding

The dashboard uses color-coded risk indicators:

- **Green** (✓ Safe): Delay probability < 20%
- **Yellow** (⚠ Watch): Delay probability 20-40%
- **Orange** (⚠ Alert): Delay probability 40-60%
- **Red** (🚨 Critical): Delay probability > 60%

## API Integration

### Dashboard Endpoints
```javascript
// Fetch trips
GET /api/trips?limit=20

// Initialize demo data
POST /api/demo/init
```

### Bilty Endpoints
```javascript
// Create bilty
POST /api/bilty/create

// List bilties
GET /api/bilty

// Get bilty
GET /api/bilty/{id}

// Update bilty
PUT /api/bilty/{id}

// Delete bilty
DELETE /api/bilty/{id}
```

### Simulation & Copilot
```javascript
// Get simulation options
POST /api/simulation/{trip_id}

// Chat with copilot
POST /api/copilot/chat
```

## State Management

Uses React hooks (useState, useEffect) with Axios for API calls. Can be upgraded to Redux/Zustand for complex state.

## Performance

- Code splitting with React Router
- Lazy loading of components
- Optimized bundle size (~100KB gzipped)
- CSS-in-JS with Tailwind (purged)

## Features Implemented

### Dashboard Page
- [x] 4 KPI cards (Active Trips, At Risk, Delayed, Net Profit)
- [x] Live trip feed with color-coded risk levels
- [x] Auto-refresh every 30 seconds
- [x] Real-time metric updates

### Bilty Management
- [x] Create new bilty form
- [x] List all bilties
- [x] Display bilty status (pending, active, completed, delayed, cancelled)
- [x] Show sender, receiver, weight, amount

### Simulation & Copilot
- [x] Trip selection dropdown
- [x] Risk level progress bar
- [x] Recommended action display
- [x] Action option cards (Continue, Reroute, Hold, SpeedUp)
- [x] Risk reduction indicators
- [x] Floating Copilot AI assistant
- [x] Chat interface for logistics advice
- [x] Message history in conversation
- [x] Loading states

## Customization

### Adding a New Page

1. Create `src/pages/YourPage.jsx`
2. Add route in `App.jsx`:
   ```jsx
   <Route path="/your-path" element={<YourPage />} />
   ```
3. Add navigation link in header

### Styling

All styling uses Tailwind CSS. Customize in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      risk: {
        green: '#10b981',
        yellow: '#f59e0b',
        orange: '#f97316',
        red: '#ef4444',
      }
    },
  },
}
```

## Troubleshooting

### CORS errors
Ensure backend proxy is configured in `vite.config.js` and backend CORS is enabled.

### API not responding
1. Check backend is running at `http://localhost:8000`
2. Verify `VITE_API_URL` in `.env`
3. Check browser console for errors

### Styles not loading
Run `npm install` again and restart dev server.

## Production Deployment

1. Build: `npm run build`
2. Deploy `dist/` folder to CDN or static hosting
3. Configure API base URL for production backend

## Future Enhancements

- Advanced analytics dashboard
- Export reports (PDF/Excel)
- Real-time notifications with WebSocket
- Mobile app with React Native
- Advanced route optimization visualization
- Integration with payment systems
- Multi-language support
- Dark mode theme
