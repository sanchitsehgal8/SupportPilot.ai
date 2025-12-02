import React, { useState } from 'react'
import api from '../api/client'

export default function SignupPage(){
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('customer')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSignup(e){
    e.preventDefault()
    setLoading(true)
    setError(null)
    try{
      const res = await api.post('/auth/register', { email, password, name, role })
      const data = res.data.data
      localStorage.setItem('sp_token', data.token)
      localStorage.setItem('sp_role', data.role || role)
      if ((data.role || role) === 'admin') window.location.href = '/admin'
      else if ((data.role || role) === 'agent') window.location.href = '/agent'
      else window.location.href = '/customer'
    }catch(err){
      setError(err.response?.data?.error || 'Signup failed')
    }finally{setLoading(false)}
  }

  return (
    <div className="auth-page">
      <form className="auth-form" onSubmit={handleSignup}>
        <h2>Create an account</h2>
        {error && <div className="error">{error}</div>}
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <select value={role} onChange={e=>setRole(e.target.value)}>
          <option value="customer">Customer</option>
          <option value="agent">Agent</option>
          <option value="admin">Admin</option>
        </select>
        <button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
        <div className="muted">Already have an account? <a href="/login">Login</a></div>
      </form>
    </div>
  )
}
