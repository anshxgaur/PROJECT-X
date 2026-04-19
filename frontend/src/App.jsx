import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Bilties from './pages/Bilties'
import Simulation from './pages/Simulation'
import { Truck } from 'lucide-react'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black">
        {/* Header */}
        <header className="bg-gray-900 shadow-sm border-b border-gray-800">
          <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2">
              <Truck className="w-8 h-8 text-blue-400" />
              <h1 className="text-2xl font-bold text-white">BiltyBook Intelligence</h1>
            </Link>
            <nav className="flex gap-6">
              <Link to="/" className="text-gray-300 hover:text-white transition">Dashboard</Link>
              <Link to="/bilties" className="text-gray-300 hover:text-white transition">Bilties</Link>
              <Link to="/simulation" className="text-gray-300 hover:text-white transition">Simulation</Link>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/bilties" element={<Bilties />} />
            <Route path="/simulation" element={<Simulation />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-gray-900 border-t border-gray-800 mt-20">
          <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
            <p className="text-center text-gray-400 text-sm">
              &copy; 2024 BiltyBook Intelligence. AI-powered transport optimization.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
