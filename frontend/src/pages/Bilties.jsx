import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { CheckCircle, AlertCircle, XCircle, Clock, FileText, Weight, Truck, MapPin } from 'lucide-react'

function Bilties() {
  const [bilties, setBilties] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [formData, setFormData] = useState({
    bilty_number: '',
    sender_name: '',
    receiver_name: '',
    goods_description: '',
    weight_kg: '',
    rate_per_km: ''
  })

  useEffect(() => {
    fetchBilties()
  }, [])

  const fetchBilties = async () => {
    try {
      const res = await axios.get('/api/bilty')
      setBilties(res.data)
    } catch (err) {
      console.error('Error fetching bilties:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // Note: This is a simplified version. Full implementation would handle all required fields
      await axios.post('/api/bilty/create', {
        ...formData,
        company_id: 1,
        route_id: 1,
        scheduled_pickup: new Date().toISOString(),
        scheduled_delivery: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
      })
      setFormData({
        bilty_number: '',
        sender_name: '',
        receiver_name: '',
        goods_description: '',
        weight_kg: '',
        rate_per_km: ''
      })
      fetchBilties()
    } catch (err) {
      console.error('Error creating bilty:', err)
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return { icon: <CheckCircle className="w-5 h-5" />, color: 'text-green-400', bg: 'bg-green-900' }
      case 'delayed':
        return { icon: <AlertCircle className="w-5 h-5" />, color: 'text-orange-400', bg: 'bg-orange-900' }
      case 'cancelled':
        return { icon: <XCircle className="w-5 h-5" />, color: 'text-red-400', bg: 'bg-red-900' }
      case 'active':
        return { icon: <Truck className="w-5 h-5" />, color: 'text-blue-400', bg: 'bg-blue-900' }
      default:
        return { icon: <Clock className="w-5 h-5" />, color: 'text-gray-400', bg: 'bg-gray-800' }
    }
  }

  const filteredBilties = filter === 'all' ? bilties : bilties.filter(b => b.status === filter)
  const statusCounts = {
    all: bilties.length,
    pending: bilties.filter(b => b.status === 'pending').length,
    active: bilties.filter(b => b.status === 'active').length,
    completed: bilties.filter(b => b.status === 'completed').length,
    delayed: bilties.filter(b => b.status === 'delayed').length
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 to-black rounded-lg p-8">
        <h2 className="text-4xl font-bold text-white mb-2">Transport Documents</h2>
        <p className="text-gray-400">Manage bilties and shipment information</p>
        <div className="flex gap-4 mt-4 text-sm">
          <div>
            <p className="text-gray-500">Total Bilties</p>
            <p className="text-white font-semibold text-lg">{statusCounts.all}</p>
          </div>
          <div>
            <p className="text-gray-500">In Transit</p>
            <p className="text-blue-400 font-semibold text-lg">{statusCounts.active}</p>
          </div>
          <div>
            <p className="text-gray-500">Completed</p>
            <p className="text-green-400 font-semibold text-lg">{statusCounts.completed}</p>
          </div>
        </div>
      </div>

      {/* Create Form */}
      <div className="bg-gradient-to-br from-gray-900 to-black rounded-lg p-8 border border-gray-800">
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <FileText className="w-6 h-6 text-blue-400" />
          Create New Bilty
        </h3>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-400 text-sm mb-2">Bilty Number</label>
            <input
              type="text"
              placeholder="BLT-2024-001"
              value={formData.bilty_number}
              onChange={(e) => setFormData({...formData, bilty_number: e.target.value})}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500"
              required
            />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Sender Name</label>
            <input
              type="text"
              placeholder="Sender Company"
              value={formData.sender_name}
              onChange={(e) => setFormData({...formData, sender_name: e.target.value})}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500"
              required
            />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Receiver Name</label>
            <input
              type="text"
              placeholder="Receiver Company"
              value={formData.receiver_name}
              onChange={(e) => setFormData({...formData, receiver_name: e.target.value})}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500"
              required
            />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Goods Description</label>
            <input
              type="text"
              placeholder="Electronics, Grains, etc."
              value={formData.goods_description}
              onChange={(e) => setFormData({...formData, goods_description: e.target.value})}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500"
            />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Weight (kg)</label>
            <input
              type="number"
              placeholder="1000"
              value={formData.weight_kg}
              onChange={(e) => setFormData({...formData, weight_kg: e.target.value})}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500"
            />
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Rate per km (₹)</label>
            <input
              type="number"
              placeholder="10"
              value={formData.rate_per_km}
              onChange={(e) => setFormData({...formData, rate_per_km: e.target.value})}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-500"
            />
          </div>
          <button type="submit" className="btn-primary md:col-span-2 py-3 text-base font-semibold">
            Create Bilty
          </button>
        </form>
      </div>

      {/* Status Filter */}
      <div className="flex gap-2 flex-wrap">
        {['all', 'pending', 'active', 'completed', 'delayed'].map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg transition-all ${
              filter === status
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)} ({statusCounts[status]})
          </button>
        ))}
      </div>

      {/* Bilties List */}
      <div>
        <h3 className="section-header">Bilty List</h3>
        {loading ? (
          <div className="text-center py-16">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
            <p className="mt-4 text-gray-400">Loading bilties...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredBilties.length === 0 ? (
              <div className="text-center py-16 bg-gray-900 rounded-lg border border-gray-800">
                <FileText className="w-12 h-12 text-gray-700 mx-auto mb-4" />
                <p className="text-gray-500 text-lg">No bilties found</p>
              </div>
            ) : (
              filteredBilties.map((bilty) => {
                const status = getStatusIcon(bilty.status)
                return (
                  <div key={bilty.id} className="card p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-start gap-3 flex-1">
                        <div className={`p-3 rounded-lg ${status.bg}`}>
                          <div className={status.color}>
                            {status.icon}
                          </div>
                        </div>
                        <div>
                          <h4 className="font-bold text-white text-lg">{bilty.bilty_number}</h4>
                          <p className="text-gray-400 text-sm capitalize">{bilty.status}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-white text-lg">₹{Math.round(bilty.total_amount).toLocaleString()}</p>
                        <p className="text-gray-500 text-sm">{bilty.weight_kg} kg</p>
                      </div>
                    </div>

                    {/* Route Information */}
                    <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg mb-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-gray-400 text-sm">
                          <MapPin className="w-4 h-4" />
                          <span>{bilty.sender_name}</span>
                        </div>
                        <div className="text-gray-600">→</div>
                        <div className="flex items-center gap-2 text-gray-400 text-sm">
                          <span>{bilty.receiver_name}</span>
                          <MapPin className="w-4 h-4" />
                        </div>
                      </div>
                    </div>

                    {/* Details Grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <p className="text-xs text-gray-500 uppercase">Goods</p>
                        <p className="text-white text-sm mt-1 font-medium">{bilty.goods_description || 'N/A'}</p>
                      </div>
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <p className="text-xs text-gray-500 uppercase">Weight</p>
                        <div className="flex items-center gap-1 mt-1">
                          <Weight className="w-3 h-3 text-blue-400" />
                          <p className="text-white text-sm font-medium">{bilty.weight_kg} kg</p>
                        </div>
                      </div>
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <p className="text-xs text-gray-500 uppercase">Rate/km</p>
                        <p className="text-white text-sm mt-1 font-medium">₹{bilty.rate_per_km}/km</p>
                      </div>
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <p className="text-xs text-gray-500 uppercase">Total</p>
                        <p className="text-green-400 text-sm mt-1 font-semibold">₹{Math.round(bilty.total_amount).toLocaleString()}</p>
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Bilties
