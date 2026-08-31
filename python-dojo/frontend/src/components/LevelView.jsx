import { useEffect, useState } from 'react'
import Markdown from './Markdown'
import { api } from '../api'

export default function LevelView({ level, onProgressChange }) {
  const [lessonIndex, setLessonIndex] = useState(0)
  const [project, setProject] = useState(null)
  const [code, setCode] = useState('')
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const lessons = level.lessons || []
  const currentLesson = lessons[lessonIndex]
  const allLessonsDone = level.lessons_done

  useEffect(() => {
    setLessonIndex(lessons.findIndex((l) => !l.completed))
    setProject(null)
    setResult(null)
    setCode('')
    setError(null)
  }, [level.id])

  async function markDoneAndAdvance() {
    await api.completeLesson(currentLesson.id)
    onProgressChange()
    const next = lessons.findIndex((l, idx) => idx > lessonIndex && !l.completed)
    if (next === -1) {
      loadProject()
    } else {
      setLessonIndex(next)
    }
  }

  function goToPreviousLesson() {
    setLessonIndex((idx) => Math.max(idx - 1, 0))
  }

  async function loadProject() {
    setError(null)
    try {
      const data = await api.getLevelProject(level.id)
      setProject(data)
    } catch (e) {
      setError(e.message)
    }
  }

  async function handleSubmit() {
    if (!code.trim()) return
    setSubmitting(true)
    setError(null)
    try {
      const data = await api.submit(level.id, code)
      setResult(data)
      onProgressChange()
    } catch (e) {
      setError(e.message)
    } finally {
      setSubmitting(false)
    }
  }

  // ---- lessons phase ----
  if (!allLessonsDone && !project && currentLesson) {
    return (
      <div className="main">
        <div className="mono eyebrow">
          LEVEL {String(level.id).padStart(2, '0')} · LESSON {lessonIndex + 1} OF {lessons.length}
        </div>
        <h2 className="title">{currentLesson.name}</h2>
        <Markdown text={currentLesson.lesson_md} />
        <div className="btn-row">
          <button className="btn ghost" onClick={goToPreviousLesson} disabled={lessonIndex === 0}>
            Back
          </button>
          <button className="btn" onClick={markDoneAndAdvance}>
            {lessonIndex + 1 === lessons.length ? "Done — see the level project" : 'Got it — next lesson'}
          </button>
        </div>
        {error && <p className="error">{error}</p>}
      </div>
    )
  }

  if (allLessonsDone && !project && !result) {
    // lessons finished on a previous visit — surface the project entry point
    return (
      <div className="main">
        <div className="mono eyebrow">LEVEL {String(level.id).padStart(2, '0')}</div>
        <h2 className="title">All lessons done</h2>
        <p className="lede">Time to put it together in one project.</p>
        <button className="btn" onClick={loadProject}>
          View the project brief
        </button>
        {error && <p className="error">{error}</p>}
      </div>
    )
  }

  // ---- project phase ----
  return (
    <div className="main">
      <div className="mono eyebrow">LEVEL {String(level.id).padStart(2, '0')} · PROJECT</div>
      <h2 className="title">{level.name}</h2>

      {project && (
        <div className="card">
          <h3>Project brief</h3>
          <Markdown text={project.brief_md} />
          <textarea
            className="code-input mono"
            placeholder="Paste or write your Python code here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={12}
          />
          <button className="btn" onClick={handleSubmit} disabled={submitting}>
            {submitting ? 'Grading…' : 'Submit my code'}
          </button>
          {error && <p className="error">{error}</p>}
        </div>
      )}

      {result && (
        <div className="card">
          <h3>Feedback</h3>
          <div className="feedback-score">
            <span className="num mono">{result.score}</span>
            <span className="of">/ 100</span>
          </div>
          <p>{result.feedback}</p>
          <div className="tags">
            {result.strengths?.map((s, i) => (
              <span className="tag good" key={`s-${i}`}>{s}</span>
            ))}
            {result.fixes?.map((f, i) => (
              <span className="tag fix" key={`f-${i}`}>{f}</span>
            ))}
          </div>
          <p className="next-step mono">{result.next_step}</p>
          {result.passed ? (
            <p className="passed-banner">
              Passed — {result.next_level_id != null ? 'the next level is unlocked.' : "that's the last level for now."}
            </p>
          ) : (
            <p className="retry-banner">Not quite 70+ yet — revise and resubmit when ready.</p>
          )}
        </div>
      )}
    </div>
  )
}
