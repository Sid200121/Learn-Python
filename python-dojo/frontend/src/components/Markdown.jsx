// Minimal markdown renderer — just enough for our lesson/brief content:
// fenced code blocks, **bold**, `inline code`, and "- " bullet lists.
// Avoids pulling in a full markdown dependency for a handful of patterns.

function renderInline(text, keyPrefix) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return parts.map((part, i) => {
    const key = `${keyPrefix}-${i}`
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={key}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={key}>{part.slice(1, -1)}</code>
    }
    return <span key={key}>{part}</span>
  })
}

export default function Markdown({ text }) {
  const blocks = []
  const lines = text.trim().split('\n')
  let i = 0
  let listBuffer = []

  const flushList = () => {
    if (listBuffer.length) {
      blocks.push(
        <ul key={`list-${blocks.length}`}>
          {listBuffer.map((item, idx) => (
            <li key={idx}>{renderInline(item, `li-${blocks.length}-${idx}`)}</li>
          ))}
        </ul>
      )
      listBuffer = []
    }
  }

  while (i < lines.length) {
    const line = lines[i]

    if (line.trim().startsWith('```')) {
      flushList()
      const codeLines = []
      i++
      while (i < lines.length && !lines[i].trim().startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      blocks.push(
        <pre key={`code-${blocks.length}`}>
          <code>{codeLines.join('\n')}</code>
        </pre>
      )
      i++
      continue
    }

    if (line.trim().startsWith('- ')) {
      listBuffer.push(line.trim().slice(2))
      i++
      continue
    }

    flushList()
    if (line.trim() === '') {
      i++
      continue
    }
    blocks.push(<p key={`p-${blocks.length}`}>{renderInline(line, `p-${blocks.length}`)}</p>)
    i++
  }
  flushList()

  return <div className="markdown">{blocks}</div>
}
