import React, { useState, useEffect } from 'react'
import axios from 'axios'
import SimulationCard from '../components/SimulationCard'
import Copilot from '../components/Copilot'

function Simulation() {
  const [trips, setTrips] = useState([])
  const [selectedTrip, setSelectedTrip] = useState(null)
  const [simulationData, setSimulationData] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchTrips()
  }, [])

  const fetchTrips = async () => {
    try {
      const res = await axios.get('/api/trips?limit=20')
      if (res.data && res.data.length > 0) {
        setTrips(res.data)
        setSelectedTrip(res.data[0].id)
      }
    } catch (err) {
      console.error('Error fetching trips:', err)
    }
  }

  const handleSimulate = async (tripId) => {
    try {
      setLoading(true)
      const res = await axios.post(`/api/simulation/${tripId}`)
      setSimulationData(res.data)
    } catch (err) {
      console.error('Error running simulation:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Simulation & Decision Support</h2>
        <p className="text-gray-600 mt-2">AI-powered recommendations for trip management</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Trip Selection */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-bold mb-4">Select Trip</h3>
            <div className="space-y-2">
              {trips.map((trip) => (
                <button
                  key={trip.id}
                  onClick={() => {
                    setSelectedTrip(trip.id)
                    handleSimulate(trip.id)
                  }}
                  className={`w-full text-left p-4 rounded-lg transition ${
                    selectedTrip === trip.id
                      ? 'bg-blue-100 border-2 border-blue-500'
                      : 'bg-gray-50 border border-gray-200 hover:bg-gray-100'
                  }`}
                >
                  <div className="font-bold">Trip #{trip.id}</div>
                  <div className="text-sm text-gray-600">Risk: {trip.risk_level}</div>
                  <div className="text-sm text-gray-600">Delay: {trip.delay_hours.toFixed(1)}h</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Simulation Options */}
        <div className="lg:col-span-2 space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">Running simulation...</p>
            </div>
          ) : simulationData ? (
            <>
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-xl font-bold mb-4">Current Risk Assessment</h3>
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-600">Risk Level</span>
                    <span className="font-bold text-2xl">{(simulationData.current_risk * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all ${
                        simulationData.current_risk < 0.3 ? 'bg-green-600' :
                        simulationData.current_risk < 0.6 ? 'bg-yellow-600' :
                        'bg-red-600'
                      }`}
                      style={{ width: `${simulationData.current_risk * 100}%` }}
                    ></div>
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <p className="text-sm text-blue-800">
                    <strong>Recommended Action:</strong> {simulationData.recommended.toUpperCase()}
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-bold">Action Options</h3>
                {simulationData.options.map((option, idx) => (
                  <SimulationCard key={idx} option={option} />
                ))}
              </div>

              <div>
                <Copilot tripId={simulationData.trip_id} riskLevel={
                  simulationData.current_risk < 0.3 ? 'green' :
                  simulationData.current_risk < 0.6 ? 'yellow' :
                  'red'
                } />
              </div>
            </>
          ) : (
            <div className="bg-gray-50 rounded-lg p-12 text-center text-gray-600">
              Select a trip to see simulation options
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Simulation
