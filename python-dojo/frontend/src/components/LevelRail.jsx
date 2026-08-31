export default function LevelRail({ levels, activeLevelId, onSelect }) {
  return (
    <nav className="rail">
      <div className="rail-head">
        <div className="mono eyebrow">WORKSHOP</div>
        <h1>Your path</h1>
      </div>

      {levels.map((level) => {
        const isActive = level.id === activeLevelId
        const isLocked = level.status === 'locked'
        const isDone = level.status === 'passed'
        return (
          <button
            key={level.id}
            className={`level ${isActive ? 'active' : ''} ${isDone ? 'done' : ''} ${
              isLocked ? 'locked' : ''
            }`}
            onClick={() => !isLocked && onSelect(level.id)}
            disabled={isLocked}
          >
            <span className="dot" />
            <span className="mono num">
              LEVEL {String(level.id).padStart(2, '0')}
              {isLocked ? ' · LOCKED' : ''}
            </span>
            <span className="name">{level.name}</span>
            {level.best_score != null && (
              <span className="mono score">
                {isDone ? 'passed' : 'best'} · {level.best_score}/100
              </span>
            )}
          </button>
        )
      })}
    </nav>
  )
}
