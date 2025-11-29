import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Header.css'

const Header = () => {
  const location = useLocation()
  
  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <div className="logo-icon-box">
            <span className="logo-heart">❤️</span>
          </div>
          <div className="logo-text-container">
            <span className="logo-text">AYURSUTRA</span>
            <span className="logo-tagline">PROFESSIONAL HEALTHCARE PLATFORM</span>
          </div>
        </Link>
        <nav className="nav">
          <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            HOME
          </Link>
          <Link to="/services" className={`nav-link ${location.pathname === '/services' ? 'active' : ''}`}>
            SERVICES
          </Link>
          <Link to="/about" className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}>
            ABOUT
          </Link>
        </nav>
      </div>
    </header>
  )
}

export default Header

