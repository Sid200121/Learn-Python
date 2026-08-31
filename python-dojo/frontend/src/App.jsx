import { useEffect, useState } from 'react'
import './app.css'
import { api } from './api'
import LevelRail from './components/LevelRail'
import LevelView from './components/LevelView'

export default function App() {
  const [levels, setLevels] = useState([])
  const [activeLevelId, setActiveLevelId] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  async function refresh() {
    try {
      const data = await api.getDashboard()
      setLevels(data.levels)
      if (activeLevelId == null) {
        const firstOpen = data.levels.find((l) => l.status !== 'locked')
        setActiveLevelId(firstOpen ? firstOpen.id : data.levels[0]?.id)
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (loading) {
    return (
      <div className="app-shell">
        <p className="loading">Loading your workshop…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app-shell">
        <p className="error">
          Couldn't reach the backend: {error}. Check that it's running and VITE_API_URL is set.
        </p>
      </div>
    )
  }

  const activeLevel = levels.find((l) => l.id === activeLevelId)

  return (
    <div className="app-shell">
      <LevelRail levels={levels} activeLevelId={activeLevelId} onSelect={setActiveLevelId} />
      {activeLevel && <LevelView level={activeLevel} onProgressChange={refresh} />}
    </div>
  )
}
