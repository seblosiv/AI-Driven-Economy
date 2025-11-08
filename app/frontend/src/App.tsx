import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'sonner'
import Home from './routes/Home'
import Quiz from './routes/Quiz'
import Results from './routes/Results'
import Premium from './routes/Premium'
import Learn from './routes/Learn'

function App() {
  return (
    <div className="min-h-screen bg-charcoal">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/results" element={<Results />} />
        <Route path="/premium" element={<Premium />} />
        <Route path="/learn" element={<Learn />} />
      </Routes>
      <Toaster position="top-center" theme="dark" />
    </div>
  )
}

export default App
