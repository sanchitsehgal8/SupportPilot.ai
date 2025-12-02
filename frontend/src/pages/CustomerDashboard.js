import React, { useEffect, useState } from 'react'
import api from '../api/client'
import TicketCard from '../components/TicketCard'
import AddTicketForm from '../components/AddTicketForm'

export default function CustomerDashboard(){
  const [tickets, setTickets] = useState([])

  useEffect(()=>{
    async function load(){
      try{
        const token = localStorage.getItem('sp_token')
        const res = await api.get('/tickets', { headers: { Authorization: `Bearer ${token}` } })
        setTickets(res.data.data?.tickets || [])
      }catch(e){
        console.warn('Failed to load tickets', e)
      }
    }
    load()
  }, [])

  return (
    <div className="page">
      <div className="grid-2">
        <AddTicketForm onCreated={(t)=> setTickets(prev => [t, ...prev])} />
        <div>
          <h2>My Tickets</h2>
          <div className="ticket-list">
            {tickets.length === 0 && <div>No tickets yet</div>}
            {tickets.map(t => <TicketCard key={t.ticket_id || t.id} ticket={t} />)}
          </div>
        </div>
      </div>
    </div>
  )
}
