import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './style.css'

const api = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '') ?? ''

function App() {
  const [health, setHealth] = useState('Não verificado')
  const [database, setDatabase] = useState('Não verificado')
  const [read, setRead] = useState('Não verificado')
  const [write, setWrite] = useState('Não executado')
  const [token, setToken] = useState('')
  const [busy, setBusy] = useState(false)

  async function request(path: string, init?: RequestInit) {
    const response = await fetch(`${api}${path}`, { ...init, cache: 'no-store' })
    if (!response.ok) throw new Error(`Serviço indisponível ou acesso negado (${response.status})`)
    return response.json()
  }

  async function check() {
    setBusy(true)
    try {
      const result = await request('/health')
      setHealth(result.status === 'ok' ? 'API conectada' : 'Resposta inesperada')
    } catch (error) { setHealth((error as Error).message) }
    try {
      const result = await request('/db')
      setDatabase(result.connected ? 'Banco conectado' : 'Banco indisponível')
    } catch (error) { setDatabase((error as Error).message) }
    try {
      const result = await request('/records/demo')
      setRead(`demo: ${result.value}`)
    } catch (error) { setRead((error as Error).message) }
    setBusy(false)
  }

  async function testWrite() {
    setBusy(true)
    try {
      const result = await request('/records', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ key: 'demo', value: 'Dado sintético da PoC' }),
      })
      setWrite(`${result.key}: ${result.value}`)
      setToken('')
    } catch (error) { setWrite((error as Error).message) }
    setBusy(false)
  }

  return <main>
    <p className="eyebrow">Fase 00 · Prova de conceito</p>
    <h1>Tickr</h1>
    <p>Validação de hospedagem, API e persistência com dados sintéticos. Nenhuma funcionalidade financeira está ativa.</p>
    <button disabled={busy} onClick={check}>Verificar conectividade</button>
    <section aria-live="polite">
      <p><strong>API:</strong> {health}</p>
      <p><strong>PostgreSQL:</strong> {database}</p>
      <p><strong>Leitura:</strong> {read}</p>
      <p><strong>Escrita:</strong> {write}</p>
    </section>
    <label htmlFor="token">Token temporário da PoC para escrita</label>
    <input id="token" type="password" autoComplete="off" value={token} onChange={event => setToken(event.target.value)} />
    <button disabled={busy || !token} onClick={testWrite}>Gravar registro sintético</button>
    <p className="note">Use somente um token de teste. Ele permanece no navegador até a página ser fechada ou após a escrita.</p>
  </main>
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>)
