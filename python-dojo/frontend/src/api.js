const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

export const api = {
  getDashboard: () => request('/dashboard'),
  completeLesson: (lessonId) =>
    request(`/lessons/${lessonId}/complete`, { method: 'POST' }),
  getLevelProject: (levelId) => request(`/levels/${levelId}/project`),
  submit: (levelId, code) =>
    request('/submit', {
      method: 'POST',
      body: JSON.stringify({ level_id: levelId, code }),
    }),
}
