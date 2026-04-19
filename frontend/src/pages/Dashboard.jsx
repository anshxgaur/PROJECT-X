import React, { useState, useEffect } from 'react'
import axios from 'axios'
import KPICard from '../components/KPICard'
import TripFeed from '../components/TripFeed'
import { AlertTriangle, Truck, Clock, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'

function Dashboard() {
  const [kpis, setKpis] = useState({
    activeTrips: 0,
    atRisk: 0,
    delayed: 0,
    netProfit: 0
  })
  const [trips, setTrips] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Initialize demo data
        await axios.post('/api/demo/init')
        
        // Fetch trips
        const tripsRes = await axios.get('/api/trips?limit=20')
        const tripsData = tripsRes.data || []
        setTrips(tripsData)
        
        // Calculate KPIs
        const activeCount = tripsData.length
        const atRiskCount = tripsData.filter(t => ['orange', 'red'].includes(t.risk_level)).length
        const delayedCount = tripsData.filter(t => t.delay_hours > 2).length
        const netProfit = activeCount * 500 // Mock calculation
        
        setKpis({
          activeTrips: activeCount,
          atRisk: atRiskCount,
          delayed: delayedCount,
          netProfit: netProfit
        })
      } catch (err) {
        console.error('Error fetching data:', err)
        setError('Failed to load dashboard data')
        // Set fallback data
        setKpis({
          activeTrips: 12,
          atRisk: 3,
          delayed: 2,
          netProfit: 6000
        })
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    
    // Polling interval
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  const highRiskTrips = trips.filter(t => t.risk_level === 'red')
  const completionRate = trips.length > 0 ? (trips.filter(t => t.km_completed > 0).length / trips.length * 100).toFixed(1) : 0

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 to-black rounded-lg p-8">
        <h2 className="text-4xl font-bold text-white mb-2">Transport Dashboard</h2>
        <p className="text-gray-400">Real-time fleet monitoring and AI-powered risk assessment</p>
        <div className="flex gap-4 mt-4">
          <div className="text-sm">
            <p className="text-gray-500">Last Updated</p>
            <p className="text-white font-semibold">{new Date().toLocaleString()}</p>
          </div>
          <div className="text-sm">
            <p className="text-gray-500">System Status</p>
            <p className="text-green-400 font-semibold">✓ Operational</p>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <KPICard
          title="Active Trips"
          value={kpis.activeTrips}
          icon={<Truck className="w-6 h-6" />}
          color="blue"
          trend={3}
          description="Currently in transit"
        />
        <KPICard
          title="At Risk"
          value={kpis.atRisk}
          icon={<AlertTriangle className="w-6 h-6" />}
          color="red"
          trend={-5}
          description="Orange & Red levels"
        />
        <KPICard
          title="Delayed"
          value={kpis.delayed}
          icon={<Clock className="w-6 h-6" />}
          color="yellow"
          trend={10}
          description="> 2 hours delay"
        />
        <KPICard
          title="Net Profit"
          value={`₹${kpis.netProfit.toLocaleString()}`}
          icon={<TrendingUp className="w-6 h-6" />}
          color="green"
          trend={8}
          description="Today's revenue"
        />
      </div>

      {/* Alerts & Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Critical Alerts */}
        <div className="lg:col-span-1 bg-gradient-to-br from-gray-900 to-black rounded-lg p-6 border border-gray-800">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-400" />
            Critical Alerts
          </h3>
          {highRiskTrips.length > 0 ? (
            <div className="space-y-3">
              {highRiskTrips.slice(0, 3).map((trip) => (
                <div key={trip.id} className="bg-red-900 bg-opacity-30 border border-red-800 rounded p-3">
                  <p className="text-red-300 text-sm font-semibold">Trip #{trip.id}</p>
                  <p className="text-gray-400 text-xs mt-1">{(trip.delay_probability * 100).toFixed(0)}% delay risk</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">No critical alerts</p>
          )}
        </div>

        {/* Performance Metrics */}
        <div className="lg:col-span-1 bg-gradient-to-br from-gray-900 to-black rounded-lg p-6 border border-gray-800">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-400" />
            Performance
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-400 text-sm">Completion Rate</span>
                <span className="text-white font-semibold">{completionRate}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: `${completionRate}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-400 text-sm">Fleet Health</span>
                <span className="text-white font-semibold">85%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '85%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-400 text-sm">On-Time Delivery</span>
                <span className="text-white font-semibold">78%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '78%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="lg:col-span-1 bg-gradient-to-br from-gray-900 to-black rounded-lg p-6 border border-gray-800">
          <h3 className="text-lg font-bold text-white mb-4">System Information</h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Total Fleet</span>
              <span className="text-white font-semibold">24 trucks</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Active Drivers</span>
              <span className="text-white font-semibold">18 drivers</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Avg Trip Duration</span>
              <span className="text-white font-semibold">8.5 hours</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">ML Predictions</span>
              <span className="text-white font-semibold">98% accurate</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">API Response</span>
              <span className="text-white font-semibold">100ms</span>
            </div>
          </div>
        </div>
      </div>

      {/* Live Trip Feed */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-6">Live Trip Feed</h3>
        {error && (
          <div className="bg-red-900 bg-opacity-30 border border-red-800 rounded-lg p-4 mb-6">
            <p className="text-red-300 text-sm">{error}</p>
          </div>
        )}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
            <p className="mt-4 text-gray-400">Loading live trips...</p>
          </div>
        ) : (
          <TripFeed trips={trips} />
        )}
      </div>
    </div>
  )
}

export default Dashboard

