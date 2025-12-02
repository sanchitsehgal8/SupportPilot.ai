import React, { useState } from 'react'
import api from '../api/client'
import showToast from '../utils/toast'

export default function TicketCard({ ticket, agents = [], onUpdated, openAssignModal }){
  const role = typeof window !== 'undefined' ? localStorage.getItem('sp_role') : null
  const [status, setStatus] = useState(ticket.status || 'open')
  const [assignTo, setAssignTo] = useState('')

  async function updateStatus(newStatus){
    try{
      // confirm when resolving/closing
      if((newStatus === 'resolved' || newStatus === 'closed') && !window.confirm(`Mark ticket \"${ticket.title || ticket.name}\" as ${newStatus}?`)) return
      setStatus(newStatus)
      await api.put(`/tickets/${ticket.ticket_id || ticket.id}/status`, { status: newStatus })
      showToast('Status updated', 'success')
      if(onUpdated) onUpdated()
    }catch(e){
      console.warn('Failed to update status', e)
      setStatus(ticket.status || 'open')
      showToast('Failed to update status', 'error')
    }
  }
  // decode JWT to get current user id for agent self-assign
  function getCurrentUserId(){
    try{
      const token = localStorage.getItem('sp_token') || ''
      const payload = token.split('.')[1]
      if(!payload) return null
      const json = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
      return json.user_id || json.sub || null
    }catch(e){return null}
  }

  async function assignToAgent(agentId){
    try{
      if(!agentId) return showToast('Select an agent', 'error')
      if(!window.confirm(`Assign ticket \"${ticket.title || ticket.name}\" to selected agent?`)) return
      await api.post(`/tickets/${ticket.ticket_id || ticket.id}/assign`, { agent_id: agentId })
      showToast('Assigned successfully', 'success')
      if(onUpdated) onUpdated()
    }catch(e){
      console.warn('Assign failed', e)
      showToast('Assign failed', 'error')
    }
  }
  return (
    <div className="ticket-card">
      <div className="ticket-header">
        <strong className="ticket-title">{ticket.title || ticket.name}</strong>
        <div className="ticket-badges">
          <span className={`badge status-${ticket.status}`}>{ticket.status || 'open'}</span>
          {ticket.predicted_priority && (
            <span className={`badge priority-${ticket.predicted_priority}`}>{ticket.predicted_priority}</span>
          )}
        </div>
      </div>
      <div className="ticket-body">{ticket.description}</div>
      <div className="ticket-footer">
        <div className="ticket-meta">
          {ticket.sentiment_label && (
            <span className={`sentiment-icon sentiment-${ticket.sentiment_label}`} title={`Sentiment: ${ticket.sentiment_label}`}>
              {ticket.sentiment_label === 'positive' ? '😊' : ticket.sentiment_label === 'negative' ? '😞' : '😐'}
            </span>
          )}
          {ticket.keywords && ticket.keywords.length > 0 && (
            <span className="keywords" title={ticket.keywords.join(', ')}>
              🏷️ {ticket.keywords.slice(0,2).join(', ')}
            </span>
          )}
        </div>
        {role === 'agent' && (
          <span style={{marginLeft:12, display:'flex', gap:8, alignItems:'center'}}>
            <select value={status} onChange={e=>updateStatus(e.target.value)}>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="pending">Pending</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
            <button className="btn" onClick={()=>{
              // resolve quickly
              updateStatus('resolved')
            }}>Resolve</button>
            <button className="btn" onClick={()=>{
              const me = getCurrentUserId()
              if(me) assignToAgent(me)
            }}>Assign to me</button>
          </span>
        )}
        {role === 'admin' && agents && agents.length > 0 && (
          <span style={{marginLeft:12,display:'flex',gap:8,alignItems:'center'}}>
            <select value={assignTo} onChange={e=>setAssignTo(e.target.value)}>
              <option value="">Assign to...</option>
              {agents.map(a=> (
                <option key={a.agent_id || a.user_id || a.id} value={a.agent_id || a.user_id || a.id}>{a.name || a.email || (a.agent_id||a.user_id)}</option>
              ))}
            </select>
            <button className="btn" onClick={()=>assignToAgent(assignTo)} disabled={!assignTo}>Assign</button>
            <button className="btn" onClick={()=>{ if(openAssignModal) openAssignModal(ticket); else showToast('Open assign modal not available','error') }}>Open Modal</button>
          </span>
        )}
      </div>
    </div>
  )
}
