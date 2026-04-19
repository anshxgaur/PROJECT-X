import React from 'react'
import TripCard from './TripCard'

function TripFeed({ trips }) {
  if (!trips || trips.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No trips available</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {trips.map((trip) => (
        <TripCard key={trip.id} trip={trip} />
      ))}
    </div>
  )
}

export default TripFeed
