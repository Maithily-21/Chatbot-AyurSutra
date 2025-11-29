import React from 'react'
import { Link } from 'react-router-dom'
import Header from '../components/Layout/Header'
import Footer from '../components/Layout/Footer'
import './Services.css'

const Services = () => {
  return (
    <div className="services-page">
      <Header />
      <main className="services-main">
        <div className="services-container">
          <h1 className="services-title">Our Services</h1>
          <div className="title-underline"></div>
          
          <div className="services-grid">
            <div className="service-card">
              <div className="service-icon">🧘</div>
              <h3 className="service-name">Dosha Assessment</h3>
              <p className="service-description">
                Discover your unique mind-body constitution (Prakriti) through our comprehensive 
                AI-powered assessment. Understand your Vata, Pitta, and Kapha balance.
              </p>
              <Link to="/chat" className="service-button">
                Get Started
              </Link>
            </div>
            
            <div className="service-card">
              <div className="service-icon">🌱</div>
              <h3 className="service-name">Panchakarma Therapy</h3>
              <p className="service-description">
                Receive personalized recommendations for traditional Ayurvedic treatments 
                including Vamana, Virechana, Basti, Nasya, and Raktamokshana.
              </p>
              <Link to="/chat" className="service-button">
                Learn More
              </Link>
            </div>
            
            <div className="service-card">
              <div className="service-icon">📋</div>
              <h3 className="service-name">Detailed Reports</h3>
              <p className="service-description">
                Download comprehensive PDF reports with your assessment results, therapy 
                recommendations, dietary guidelines, and lifestyle modifications.
              </p>
              <Link to="/chat" className="service-button">
                View Reports
              </Link>
            </div>
            
            <div className="service-card">
              <div className="service-icon">💬</div>
              <h3 className="service-name">AI Chatbot Consultation</h3>
              <p className="service-description">
                Interact with our intelligent chatbot that combines ancient Ayurvedic wisdom 
                with modern machine learning for personalized health guidance.
              </p>
              <Link to="/chat" className="service-button">
                Start Chat
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}

export default Services

