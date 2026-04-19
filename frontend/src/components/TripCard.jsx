import React from 'react'
import { MapPin, Clock, AlertCircle, CheckCircle, Gauge } from 'lucide-react'

function TripCard({ trip }) {
  const getRiskBadgeClass = (riskLevel) => {
    switch (riskLevel) {
      case 'green':
        return 'bg-green-900 text-green-200 border-green-500'
      case 'yellow':
        return 'bg-yellow-900 text-yellow-200 border-yellow-500'
      case 'orange':
        return 'bg-orange-900 text-orange-200 border-orange-500'
      case 'red':
        return 'bg-red-900 text-red-200 border-red-500'
      default:
        return 'bg-gray-700 text-gray-200 border-gray-500'
    }
  }

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'green':
        return 'border-green-500 bg-gradient-to-br from-green-950 to-gray-900'
      case 'yellow':
        return 'border-yellow-500 bg-gradient-to-br from-yellow-950 to-gray-900'
      case 'orange':
        return 'border-orange-500 bg-gradient-to-br from-orange-950 to-gray-900'
      case 'red':
        return 'border-red-500 bg-gradient-to-br from-red-950 to-gray-900'
      default:
        return 'border-gray-500 bg-gray-900'
    }
  }

  return (
    <div className={`card p-6 border-l-4 border-t-2 ${getRiskColor(trip.risk_level)} rounded-lg shadow-lg hover:shadow-xl transition-all`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4 pb-4 border-b border-gray-700">
        <div>
          <h3 className="font-bold text-white text-lg">Trip #{trip.id}</h3>
          {trip.bilty && (
            <p className="text-sm text-gray-400 mt-1">{trip.bilty.bilty_number}</p>
          )}
        </div>
        <span className={`risk-badge border ${getRiskBadgeClass(trip.risk_level)} px-3 py-1 rounded-full text-sm font-bold`}>
          {trip.risk_level.toUpperCase()}
        </span>
      </div>

      {/* Route */}
      {trip.bilty && trip.bilty.route && (
        <div className="flex items-center gap-2 text-sm text-gray-300 mb-4">
          <MapPin className="w-4 h-4 text-blue-400" />
          <span className="font-medium">{trip.bilty.route.origin_city}</span>
          <span className="text-gray-600">→</span>
          <span className="font-medium">{trip.bilty.route.destination_city}</span>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-gray-800 p-3 rounded-lg">
          <p className="text-xs text-gray-500 uppercase">Location</p>
          <p className="text-white font-semibold mt-1">{trip.current_location || 'In Transit'}</p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <p className="text-xs text-gray-500 uppercase">Progress</p>
          <p className="text-white font-semibold mt-1">{trip.km_completed.toFixed(0)} km</p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <p className="text-xs text-gray-500 uppercase">Delay</p>
          <p className={`font-semibold mt-1 ${trip.delay_hours > 2 ? 'text-orange-400' : 'text-green-400'}`}>
            {trip.delay_hours.toFixed(1)}h
          </p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <p className="text-xs text-gray-500 uppercase">Health</p>
          <p className={`font-semibold mt-1 ${trip.truck?.health_score > 80 ? 'text-green-400' : 'text-yellow-400'}`}>
            {trip.truck?.health_score.toFixed(0)}%
          </p>
        </div>
      </div>

      {/* Risk Indicator */}
      <div className="bg-gray-800 p-4 rounded-lg mb-4">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-orange-400" />
            <span className="text-sm text-gray-400">Delay Probability</span>
          </div>
          <span className="font-bold text-white">{(trip.delay_probability * 100).toFixed(0)}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full ${
              trip.delay_probability < 0.3 ? 'bg-green-500' :
              trip.delay_probability < 0.6 ? 'bg-yellow-500' :
              'bg-red-500'
            }`}
            style={{ width: `${trip.delay_probability * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Driver & Truck Info */}
      {(trip.driver || trip.truck) && (
        <div className="border-t border-gray-700 pt-3 space-y-2 text-sm">
          {trip.driver && (
            <div className="flex items-center justify-between text-gray-400">
              <span>Driver:</span>
              <span className="text-white font-medium">{trip.driver.name}</span>
            </div>
          )}
          {trip.truck && (
            <div className="flex items-center justify-between text-gray-400">
              <span>Truck:</span>
              <span className="text-white font-medium">{trip.truck.registration_number}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default TripCard
