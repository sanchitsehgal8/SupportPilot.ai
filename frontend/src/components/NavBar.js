import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'

export default function NavBar(){
  const navigate = useNavigate()
  const token = typeof window !== 'undefined' ? localStorage.getItem('sp_token') : null
  const role = typeof window !== 'undefined' ? localStorage.getItem('sp_role') : null

  function logout(){
    localStorage.removeItem('sp_token')
    navigate('/login')
  }

  return (
    <header className="navbar">
      <div className="nav-left">
        {token && (
          <nav className="nav-links">
            {(role === 'customer' || role === 'admin' || role === 'agent') && (
              <NavLink to="/customer" className={({isActive})=>isActive?'active':''}>Dashboard</NavLink>
            )}
            {(role === 'agent' || role === 'admin') && (
              <NavLink to="/agent" className={({isActive})=>isActive?'active':''}>Agent</NavLink>
            )}
            {role === 'admin' && (
              <NavLink to="/admin" className={({isActive})=>isActive?'active':''}>Admin</NavLink>
            )}
          </nav>
        )}
      </div>
      <div className="brand-center">
        <span className="logo">🚀</span>
        <span className="brand-text">SupportPilot</span>
      </div>
      <div className="nav-right">
        {token ? (
          <button className="btn btn-logout" onClick={logout}>Logout</button>
        ) : (
          <div className="auth-links">
            <NavLink to="/login" className="btn-link">Login</NavLink>
            <NavLink to="/signup" className="btn btn-primary">Sign up</NavLink>
          </div>
        )}
      </div>
    </header>
  )
}
