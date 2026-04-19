import React from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

function KPICard({ title, value, icon, color, trend, description }) {
  const colorClasses = {
    blue: 'border-blue-500 bg-gradient-to-br from-blue-900 via-gray-900 to-gray-800',
    red: 'border-red-500 bg-gradient-to-br from-red-900 via-gray-900 to-gray-800',
    yellow: 'border-yellow-500 bg-gradient-to-br from-yellow-900 via-gray-900 to-gray-800',
    green: 'border-green-500 bg-gradient-to-br from-green-900 via-gray-900 to-gray-800'
  }

  const iconColors = {
    blue: 'text-blue-400',
    red: 'text-red-400',
    yellow: 'text-yellow-400',
    green: 'text-green-400'
  }

  return (
    <div className={`card p-6 border-2 border-l-4 ${colorClasses[color]} rounded-lg shadow-lg hover:shadow-xl transition-all`}>
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg bg-opacity-10 ${colorClasses[color]}`}>
          <div className={iconColors[color]}>
            {icon}
          </div>
        </div>
        {trend && (
          <div className={`flex items-center gap-1 text-sm ${trend > 0 ? 'text-green-400' : 'text-red-400'}`}>
            {trend > 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            <span>{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
      
      <div>
        <p className="text-sm font-medium text-gray-400 uppercase tracking-wide">{title}</p>
        <p className="text-4xl font-bold text-white mt-2">{value}</p>
        {description && (
          <p className="text-xs text-gray-500 mt-2">{description}</p>
        )}
      </div>
    </div>
  )
}

export default KPICard
