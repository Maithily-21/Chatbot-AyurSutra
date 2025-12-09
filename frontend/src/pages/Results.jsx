import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DoshaResult from '../components/Assessment/DoshaResult'
import TherapyCard from '../components/Assessment/TherapyCard'
import useChatStore from '../store/chatStore'
import './Results.css'

const Results = () => {
  const navigate = useNavigate()
  const { doshaResults, panchakarmaRecs, userProfile } = useChatStore()
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState(null)

  const handleDownloadPDF = async () => {
    setDownloading(true)
    setDownloadError(null)

    try {
      // Prepare data for PDF generation
      const pdfRequestData = {
        user_data: {
          name: userProfile?.name || 'User',
          email: userProfile?.email || '',
          age: userProfile?.age || '',
          gender: userProfile?.gender || ''
        },
        dosha_results: doshaResults || {},
        panchakarma_recs: panchakarmaRecs || {}
      }

      // Call the PDF generation endpoint
      const response = await fetch('http://127.0.0.1:8000/api/pdf/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(pdfRequestData)
      })

      if (!response.ok) {
        throw new Error('Failed to generate PDF')
      }

      // Get the PDF blob
      const blob = await response.blob()
      
      // Extract filename from response headers
      const contentDisposition = response.headers.get('content-disposition')
      let filename = 'AyurSutra_Report.pdf'
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }

      // Create download link
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      
      // Cleanup
      window.URL.revokeObjectURL(url)
      document.body.removeChild(link)

    } catch (error) {
      console.error('PDF download error:', error)
      setDownloadError(error.message)
    } finally {
      setDownloading(false)
    }
  }

  if (!doshaResults) {
    return (
      <div className="results-page">
        <main className="results-main">
          <div className="no-results">
            <h2>No assessment results found</h2>
            <p>Please complete the assessment first.</p>
            <button onClick={() => navigate('/chat')} className="cta-button">
              Start Assessment
            </button>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="results-page">
      <main className="results-main">
        {/* Results Header with Download Button */}
        <div className="results-header">
          <div className="header-content">
            <h1 className="page-title">Your Ayurvedic Assessment Results</h1>
            <p className="page-subtitle">
              Based on your responses, here are your personalized Dosha analysis and Panchakarma recommendations
            </p>
          </div>
          
          <button 
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="download-pdf-btn"
          >
            {downloading ? (
              <>
                <span className="download-spinner"></span>
                Generating PDF...
              </>
            ) : (
              <>
                <svg 
                  className="download-icon" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2"
                >
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download PDF Report
              </>
            )}
          </button>
        </div>

        {/* Download Error Message */}
        {downloadError && (
          <div className="download-error">
            <strong>Error:</strong> {downloadError}
            <button 
              onClick={() => setDownloadError(null)}
              className="error-dismiss"
            >
              ×
            </button>
          </div>
        )}

        {/* PDF Preview Info */}
        <div className="pdf-preview-info">
          <div className="pdf-info-card">
            <h3>📋 Your PDF Report Includes:</h3>
            <ul>
              <li>Complete Dosha analysis with percentages</li>
              <li>Detailed Panchakarma therapy recommendations</li>
              <li>Personalized dietary guidelines (Ahara)</li>
              <li>Lifestyle modifications (Vihara)</li>
              <li>Yoga and Pranayama suggestions</li>
              <li>Important precautions and disclaimers</li>
            </ul>
          </div>
        </div>

        {/* Dosha Results */}
        <div className="dosha-section">
          <h2 className="section-title">Your Dosha Analysis</h2>
          <DoshaResult doshaResults={doshaResults} />
        </div>

        {/* Panchakarma Therapies */}
        {panchakarmaRecs && (
          <div className="therapies-section">
            <h2 className="section-title">Recommended Panchakarma Therapies</h2>
            <div className="therapy-grid">
              {panchakarmaRecs.therapy_details?.map((therapy, index) => (
                <TherapyCard key={index} therapy={therapy} />
              ))}
            </div>
          </div>
        )}

        {/* Additional Recommendations */}
        {panchakarmaRecs && (
          <div className="additional-recommendations">
            <div className="recommendation-column">
              <h3>🍽️ Dietary Recommendations (Ahara)</h3>
              <div className="diet-section">
                <h4>Foods to Favor:</h4>
                <ul>
                  {panchakarmaRecs.dietary?.favor?.map((item, index) => (
                    <li key={index}>{item}</li>
                  )) || <li>No specific dietary recommendations</li>}
                </ul>
              </div>
              <div className="diet-section">
                <h4>Foods to Avoid:</h4>
                <ul>
                  {panchakarmaRecs.dietary?.avoid?.map((item, index) => (
                    <li key={index}>{item}</li>
                  )) || <li>No specific restrictions</li>}
                </ul>
              </div>
            </div>

            <div className="recommendation-column">
              <h3>🧘 Lifestyle Modifications (Vihara)</h3>
              <div className="lifestyle-section">
                <h4>Daily Routine:</h4>
                <p>{panchakarmaRecs.lifestyle?.routine || 'Follow a balanced daily routine'}</p>
                
                <h4>Yoga Practices:</h4>
                <p>{panchakarmaRecs.lifestyle?.yoga || 'Gentle yoga appropriate for your dosha'}</p>
                
                <h4>Pranayama:</h4>
                <p>{panchakarmaRecs.lifestyle?.pranayama || 'Deep breathing exercises'}</p>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="action-buttons">
          <button 
            onClick={() => navigate('/chat')}
            className="action-btn chat-btn"
          >
            <svg className="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
            </svg>
            Chat with AyurSutra
          </button>
          
          <button 
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="action-btn download-btn"
          >
            {downloading ? (
              <>
                <span className="btn-spinner"></span>
                Generating...
              </>
            ) : (
              <>
                <svg className="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download Full Report
              </>
            )}
          </button>
        </div>
      </main>
    </div>
  )
}

export default Results