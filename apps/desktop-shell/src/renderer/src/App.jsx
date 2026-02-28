import React, { useState, useEffect } from 'react'
import orbImage from './assets/orb.png'

const ORB_API = 'http://127.0.0.1:7777/v1/orb/state'

function App() {
  const [orbState, setOrbState] = useState('idle')

  useEffect(() => {
    const poll = async () => {
      try {
        const res = await fetch(ORB_API)
        const data = await res.json()
        setOrbState(data.orb_state || 'idle')
      } catch {
        setOrbState('idle')
      }
    }
    poll()
    const interval = setInterval(poll, 400)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="container">
      <div className={`orb-wrapper ${orbState}`}>
        <img src={orbImage} alt="JARVIS Orb" className="orb-image" draggable="false" />
        <div className="orb-glow"></div>
      </div>
      <div className="state-label">{orbState.toUpperCase()}</div>
    </div>
  )
}

export default App
