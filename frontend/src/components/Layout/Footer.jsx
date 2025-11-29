import React from 'react'
import { Link } from 'react-router-dom'
import './Footer.css'

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-top">
          <div className="footer-logo-section">
            <Link to="/" className="footer-logo">
              <div className="footer-logo-icon">
                <span className="footer-heart">❤️</span>
              </div>
              <div className="footer-logo-text">
                <span className="footer-logo-name">AYURSUTRA</span>
                <span className="footer-tagline">PANCHAKARMA EXCELLENCE</span>
              </div>
            </Link>
            <p className="footer-description">
              Transforming Ayurvedic healthcare with intelligent patient management, 
              seamless booking, and comprehensive wellness tracking.
            </p>
          </div>
        </div>

        <div className="footer-contact">
          <div className="contact-item">
            <span className="contact-icon">📞</span>
            <span className="contact-text">+91 98765 43210</span>
          </div>
          <div className="contact-item">
            <span className="contact-icon">✉️</span>
            <span className="contact-text">support@ayursutra.com</span>
          </div>
          <div className="contact-item">
            <span className="contact-icon">📍</span>
            <span className="contact-text">Mumbai, India</span>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-copyright">
            © 2025 AYURSUTRA. ALL RIGHTS RESERVED. | EMPOWERING AYURVEDIC HEALTHCARE
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
