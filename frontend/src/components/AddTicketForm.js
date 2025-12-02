import React, { useState } from 'react'
import api from '../api/client'

export default function AddTicketForm({ onCreated }){
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [attachments, setAttachments] = useState([]) // not used by backend create yet
  const [priority, setPriority] = useState('medium')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [ai, setAi] = useState(null) // predicted fields

  function handleFiles(e){
    setAttachments(Array.from(e.target.files || []))
  }

  async function handleSubmit(e){
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAi(null)
    try{
      // Backend expects JSON: { title, description, priority }
      const payload = { title, description, priority }
      const res = await api.post('/tickets', payload)
      const created = res.data.data?.ticket || res.data.data
      setAi({
        predicted_priority: created?.predicted_priority,
        predicted_sentiment: created?.sentiment_label,
        keywords: created?.keywords,
        sentiment_score: created?.sentiment_score
      })
      onCreated && onCreated(created)
      setTitle('')
      setDescription('')
      setAttachments([])
    }catch(err){
      setError(err.response?.data?.error || 'Failed to create ticket')
    }finally{setLoading(false)}
  }

  return (
    <div className="card">
      <h3>Create Ticket</h3>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit} className="form-grid">
        <input placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} required />
        <textarea placeholder="Describe your issue" value={description} onChange={e=>setDescription(e.target.value)} rows={4} required />
        <select value={priority} onChange={e=>setPriority(e.target.value)}>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <input type="file" multiple onChange={handleFiles} />
        <button type="submit" className="btn btn-primary" disabled={loading}>{loading? 'Submitting...' : 'Submit ticket'}</button>
      </form>
      {ai && (
        <div className="ai-insights">
          <h4>🤖 AI Predictions</h4>
          <div className="ai-grid">
            <div className="ai-card">
              <span className="ai-label">Priority</span>
              <span className={`ai-badge priority-${ai.predicted_priority}`}>{ai.predicted_priority || '—'}</span>
            </div>
            <div className="ai-card">
              <span className="ai-label">Sentiment</span>
              <span className={`ai-badge sentiment-${ai.predicted_sentiment}`}>{ai.predicted_sentiment || '—'}</span>
            </div>
            <div className="ai-card">
              <span className="ai-label">Keywords</span>
              <span className="ai-value">{(ai.keywords || []).slice(0,3).join(', ') || '—'}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
