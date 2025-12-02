import React, { useEffect, useState } from 'react'
import api from '../api/client'
import TicketCard from '../components/TicketCard'
import showToast from '../utils/toast'

export default function AgentDashboard(){
  const [tickets, setTickets] = useState([])
  const [agents, setAgents] = useState([])
  const [adding, setAdding] = useState(false)
  const [agentName, setAgentName] = useState('')
  const [agentEmail, setAgentEmail] = useState('')
  const [agentPassword, setAgentPassword] = useState('password123')
  

  // Assign modal state
  const [assignModalOpen, setAssignModalOpen] = useState(false)
  const [modalTicket, setModalTicket] = useState(null)
  const [modalAgentId, setModalAgentId] = useState('')
  const [createAgentModalOpen, setCreateAgentModalOpen] = useState(false)
  const [newAgentName, setNewAgentName] = useState('')
  const [newAgentEmail, setNewAgentEmail] = useState('')
  const [newAgentPassword, setNewAgentPassword] = useState('password123')

  useEffect(()=>{
    async function load(){
      try{
        const token = localStorage.getItem('sp_token')
        const res = await api.get('/tickets', { headers: { Authorization: `Bearer ${token}` } })
        setTickets(res.data.data?.tickets || [])
        // If user is admin, fetch agents list for assignment UI
        const role = localStorage.getItem('sp_role')
        if(role === 'admin'){
          try{
            const ares = await api.get('/users/agents')
            setAgents(ares.data.data?.agents || ares.data?.agents || [])
          }catch(e){
            console.warn('Failed to load agents', e)
          }
        }
      }catch(e){
        console.warn('Failed to load tickets', e)
      }
    }
    load()
  }, [])

  return (
    <div className="page">
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',gap:12}}>
        <h2 style={{margin:0}}>Assigned Tickets</h2>
        {localStorage.getItem('sp_role') === 'admin' && (
          <div style={{display:'flex',gap:8}}>
            <button className="btn" onClick={()=>{ setAssignModalOpen(true); setModalTicket(null); setModalAgentId('') }}>Assign Ticket</button>
            <button className="btn btn-primary" onClick={()=>setCreateAgentModalOpen(true)}>Create Agent</button>
          </div>
        )}
      </div>
      <div style={{display:'flex',gap:20,alignItems:'flex-start'}}>
        <div style={{flex:1}}>
          <div className="ticket-list">
                {tickets.length === 0 && <div>No tickets yet</div>}
                {tickets.map(t => (
                  <TicketCard
                    key={t.ticket_id || t.id}
                    ticket={t}
                    agents={agents}
                    onUpdated={() => { api.get('/tickets').then(r=>setTickets(r.data.data?.tickets || [])).catch(()=>{}) }}
                    openAssignModal={(tk)=>{ setModalTicket(tk); setAssignModalOpen(true)}}
                    showToast={showToast}
                  />
                ))}
          </div>
        </div>

        <aside style={{width:360}}>
          {localStorage.getItem('sp_role') === 'admin' && (
            <div className="card agent-panel">
              <h3>Agent Management</h3>
              <div style={{display:'grid',gap:8}}>
                <input placeholder="Name" value={agentName} onChange={e=>setAgentName(e.target.value)} />
                <input placeholder="Email" value={agentEmail} onChange={e=>setAgentEmail(e.target.value)} />
                <input placeholder="Password" value={agentPassword} onChange={e=>setAgentPassword(e.target.value)} />
                <div style={{display:'flex',gap:8,justifyContent:'flex-end'}}>
                  <button className="btn" onClick={async()=>{
                    setAdding(true)
                    try{
                      const payload = { name: agentName, email: agentEmail, password: agentPassword }
                      // use new create-agent endpoint which does not return a token
                      const res = await api.post('/auth/create-agent', payload)
                      showToast('Agent created', 'success')
                      // refresh agents
                      const ares = await api.get('/users/agents')
                      setAgents(ares.data.data?.agents || ares.data?.agents || [])
                      setAgentName('')
                      setAgentEmail('')
                    }catch(err){
                      console.warn('Agent create failed', err)
                      showToast(err.response?.data?.error || 'Failed to create agent', 'error')
                    }finally{setAdding(false)}
                  }}>{adding ? 'Adding...' : 'Add Agent'}</button>
                </div>
                
              </div>
              <hr style={{margin:'12px 0',borderColor:'rgba(255,255,255,0.04)'}} />
              <h4 style={{margin:'6px 0'}}>Agents</h4>
              <div style={{display:'grid',gap:8,maxHeight:260,overflow:'auto'}}>
                {agents.length === 0 && <div className="muted">No agents found</div>}
                {agents.map(a=> (
                  <div key={a.agent_id || a.user_id || a.id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:8}}>
                    <div>
                      <div style={{fontWeight:700}}>{a.name || a.email || (a.agent_id||a.user_id)}</div>
                      <div className="muted-xs">{a.email || ''}</div>
                    </div>
                    <div>
                      <button className="btn" onClick={() => {
                        // quick assign: assign first open ticket to this agent
                        const t = tickets.find(tt=>tt.status === 'open' || tt.status === 'pending')
                        if(!t) return alert('No open tickets')
                        if(!window.confirm(`Assign ticket "${t.title || t.name}" to ${a.name || a.email}?`)) return
                        api.post(`/tickets/${t.ticket_id || t.id}/assign`, { agent_id: a.agent_id || a.user_id || a.id }).then(()=>{
                          api.get('/tickets').then(r=>setTickets(r.data.data?.tickets || [])).catch(()=>{})
                          showToast('Assigned successfully', 'success')
                        }).catch(e=>{console.warn(e); showToast('Assign failed', 'error')})
                      }}>Assign</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </aside>
      </div>
      {/* Assign Modal */}
      {assignModalOpen && (
        <div className="modal-backdrop" onClick={()=>setAssignModalOpen(false)}>
          <div className="modal" onClick={e=>e.stopPropagation()}>
            <h3>Assign Ticket</h3>
            <div style={{marginTop:8}}><strong>{modalTicket?.title}</strong></div>
            <div style={{marginTop:12}}>
              <select value={modalAgentId} onChange={e=>setModalAgentId(e.target.value)} style={{width:'100%',padding:10,borderRadius:8}}>
                <option value="">Select agent...</option>
                {agents.map(a=> <option key={a.agent_id || a.user_id || a.id} value={a.agent_id || a.user_id || a.id}>{a.name || a.email}</option>)}
              </select>
            </div>
            <div style={{display:'flex',justifyContent:'flex-end',gap:8,marginTop:14}}>
              <button className="btn" onClick={()=>setAssignModalOpen(false)}>Cancel</button>
              <button className="btn" onClick={async()=>{
                // Resolve ticket quickly from the modal
                if(!modalTicket) return showToast('Select a ticket first', 'error')
                if(!window.confirm(`Mark ticket "${modalTicket?.title}" as resolved?`)) return
                try{
                  await api.put(`/tickets/${modalTicket.ticket_id || modalTicket.id}/status`, { status: 'resolved' })
                  setAssignModalOpen(false)
                  setModalAgentId('')
                  setModalTicket(null)
                  const r = await api.get('/tickets')
                  setTickets(r.data.data?.tickets || [])
                  showToast('Ticket resolved', 'success')
                }catch(err){
                  console.warn('Resolve failed', err)
                  showToast('Resolve failed', 'error')
                }
              }}>Resolve</button>
              <button className="btn btn-primary" onClick={async()=>{
                if(!modalAgentId) return showToast('Select an agent', 'error')
                if(!window.confirm(`Assign ticket "${modalTicket?.title}" to selected agent?`)) return
                try{
                  await api.post(`/tickets/${modalTicket.ticket_id || modalTicket.id}/assign`, { agent_id: modalAgentId })
                  setAssignModalOpen(false)
                  setModalAgentId('')
                  setModalTicket(null)
                  const r = await api.get('/tickets')
                  setTickets(r.data.data?.tickets || [])
                  showToast('Assigned successfully', 'success')
                }catch(err){
                  console.warn(err)
                  showToast('Assign failed', 'error')
                }
              }}>Assign</button>
            </div>
          </div>
        </div>
      )}

      
    </div>
  )
}
