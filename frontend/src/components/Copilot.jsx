import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, MessageCircle, Zap, X } from 'lucide-react'

function Copilot({ tripId, riskLevel }) {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'I\'m your AI logistics assistant. How can I help optimize this trip?',
      actions: ['Ask about delay risks', 'Get routing suggestions', 'Check truck health']
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    // Add user message
    setMessages(prev => [...prev, { type: 'user', text: input }])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/copilot/chat', {
        trip_id: tripId,
        message: input
      })

      const advice = response.data.advice
      const priority = response.data.priority

      setMessages(prev => [...prev, {
        type: 'bot',
        text: advice,
        priority: priority,
        actions: response.data.actions
      }])
    } catch (err) {
      console.error('Error:', err)
      setMessages(prev => [...prev, {
        type: 'bot',
        text: 'I encountered a temporary issue. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = () => {
    switch (riskLevel) {
      case 'red':
        return 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800'
      case 'orange':
        return 'bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800'
      case 'yellow':
        return 'bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-700 hover:to-yellow-800'
      default:
        return 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800'
    }
  }

  const getChatHeaderColor = () => {
    switch (riskLevel) {
      case 'red':
        return 'from-red-900 to-red-800'
      case 'orange':
        return 'from-orange-900 to-orange-800'
      default:
        return 'from-blue-900 to-blue-800'
    }
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 max-w-[calc(100%-1.5rem)]">
      {/* Floating Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className={`w-16 h-16 rounded-full flex items-center justify-center text-white shadow-2xl hover:shadow-3xl transition transform hover:scale-110 ${getRiskColor()}`}
        >
          <Zap className="w-8 h-8" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="bg-gray-950 rounded-lg shadow-2xl border border-gray-800 flex flex-col h-96 overflow-hidden">
          {/* Header */}
          <div className={`bg-gradient-to-r ${getChatHeaderColor()} text-white p-5 flex items-center justify-between flex-shrink-0`}>
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5" />
              <div>
                <h3 className="font-bold text-base">AI Copilot</h3>
                <p className="text-xs text-gray-300">Logistics Intelligence</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900 bg-opacity-50">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-3 rounded-lg ${
                    msg.type === 'user'
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-br-none shadow-lg'
                      : 'bg-gray-800 text-gray-100 rounded-bl-none border border-gray-700'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{msg.text}</p>
                  {msg.actions && msg.actions.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {msg.actions.map((action, i) => (
                        <div
                          key={i}
                          className={`text-xs p-2 rounded cursor-pointer transition ${
                            msg.type === 'user'
                              ? 'bg-blue-500 bg-opacity-30 hover:bg-opacity-50'
                              : 'bg-gray-700 hover:bg-gray-600'
                          }`}
                          onClick={() => setInput(action)}
                        >
                          • {action}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-800 px-4 py-3 rounded-lg rounded-bl-none border border-gray-700">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-800 p-4 flex-shrink-0 bg-gray-900">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask anything..."
                className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-100 placeholder-gray-500"
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={loading}
                className="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">Press Enter to send messages</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Copilot
