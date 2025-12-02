import React, { useState } from 'react'
import api from '../api/client'

export default function LoginPage(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleLogin(e){
    e.preventDefault()
    setLoading(true)
    setError(null)
    try{
      const res = await api.post('/auth/login', { email, password })
      // Save token & redirect based on role
      const data = res.data.data
      localStorage.setItem('sp_token', data.token)
      localStorage.setItem('sp_role', data.role)
      if(data.role === 'admin') window.location.href = '/admin'
      else if(data.role === 'agent') window.location.href = '/agent'
      else window.location.href = '/customer'
    }catch(err){
      setError(err.response?.data?.error || 'Login failed')
    }finally{setLoading(false)}
  }

  return (
    <div className="auth-page">
      <form className="auth-form" onSubmit={handleLogin}>
        <h2>SupportPilot — Login</h2>
        {error && <div className="error">{error}</div>}
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
        <div className="muted">Don't have an account? <a href="/signup">Sign up</a></div>
      </form>
    </div>
  )
}
