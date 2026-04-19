import React from 'react'
import { TrendingDown, TrendingUp, Zap, Shield, ArrowRight } from 'lucide-react'

function SimulationCard({ option, onClick }) {
  const isReduction = option.risk_reduction > 0
  const impactPercent = Math.abs((option.estimated_impact * 100).toFixed(1))
  const riskPercent = Math.abs((option.risk_reduction * 100).toFixed(1))

  const actionColorMap = {
    'continue': 'from-blue-900 via-gray-900 to-gray-800 border-blue-500',
    'reroute': 'from-purple-900 via-gray-900 to-gray-800 border-purple-500',
    'hold': 'from-orange-900 via-gray-900 to-gray-800 border-orange-500',
    'speedup': 'from-green-900 via-gray-900 to-gray-800 border-green-500'
  }

  const actionIconColorMap = {
    'continue': 'text-blue-400',
    'reroute': 'text-purple-400',
    'hold': 'text-orange-400',
    'speedup': 'text-green-400'
  }

  const actionBadgeMap = {
    'continue': 'bg-blue-900 text-blue-200 border-blue-500',
    'reroute': 'bg-purple-900 text-purple-200 border-purple-500',
    'hold': 'bg-orange-900 text-orange-200 border-orange-500',
    'speedup': 'bg-green-900 text-green-200 border-green-500'
  }

  const actionLower = option.action.toLowerCase()
  const colorClass = actionColorMap[actionLower] || actionColorMap['continue']
  const iconColor = actionIconColorMap[actionLower] || actionIconColorMap['continue']
  const badgeClass = actionBadgeMap[actionLower] || actionBadgeMap['continue']

  return (
    <div
      onClick={onClick}
      className={`card p-6 border-2 border-l-4 bg-gradient-to-br ${colorClass} rounded-lg shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105 hover:translate-y-[-2px]`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg bg-opacity-10`}>
          <div className={iconColor}>
            <Zap className="w-6 h-6" />
          </div>
        </div>
        <span className={`border px-3 py-1 rounded-full text-sm font-bold ${badgeClass}`}>
          {option.action.toUpperCase()}
        </span>
      </div>

      {/* Description */}
      <div className="mb-4">
        <h3 className="text-xl font-bold text-white capitalize">{option.action}</h3>
        <p className="text-gray-400 text-sm mt-2 leading-relaxed">{option.description}</p>
      </div>

      {/* Metrics */}
      <div className="space-y-3 bg-gray-800 bg-opacity-50 p-4 rounded-lg mb-4">
        {/* Impact */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-blue-400" />
              Impact
            </span>
            <span className="font-bold text-white">{impactPercent}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-blue-400"
              style={{ width: `${Math.min(impactPercent, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Risk Reduction */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm flex items-center gap-2">
              <Shield className="w-4 h-4 text-green-400" />
              Risk Reduction
            </span>
            <span className={`font-bold ${isReduction ? 'text-green-400' : 'text-orange-400'}`}>
              {isReduction ? '+' : ''}{riskPercent}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${isReduction ? 'bg-gradient-to-r from-green-500 to-green-400' : 'bg-gradient-to-r from-orange-500 to-orange-400'}`}
              style={{ width: `${Math.min(riskPercent, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* CTA Button */}
      <button className="w-full px-4 py-2 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg transition font-medium flex items-center justify-center gap-2 border border-gray-600">
        <span>Execute</span>
        <ArrowRight className="w-4 h-4" />
      </button>
    </div>
  )
}

export default SimulationCard
