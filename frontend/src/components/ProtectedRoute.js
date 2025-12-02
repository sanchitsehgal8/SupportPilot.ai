import React from 'react'
import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children, roles }){
  const token = typeof window !== 'undefined' ? localStorage.getItem('sp_token') : null
  const role = typeof window !== 'undefined' ? localStorage.getItem('sp_role') : null
  if (!token) return <Navigate to="/login" replace />
  if (roles && role && !roles.includes(role)) return <Navigate to="/login" replace />
  return children
}
