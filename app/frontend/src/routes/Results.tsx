import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Share2, Download, Sparkles } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Button } from '../components/ui/button'
import { GlassCard } from '../components/GlassCard'
import { Metric } from '../components/Metric'
import { RibbonCTA } from '../components/RibbonCTA'
import { apiClient, AutomationPrediction, DividendProjection } from '../lib/api'
import { formatCurrency } from '../lib/utils'
import { analytics } from '../lib/analytics'
import { toast } from 'sonner'

export default function Results() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [automation, setAutomation] = useState<AutomationPrediction | null>(null)
  const [dividend, setDividend] = useState<DividendProjection | null>(null)

  useEffect(() => {
    loadResults()
  }, [])

  const loadResults = async () => {
    try {
      const quizData = sessionStorage.getItem('quizData')
      if (!quizData) {
        navigate('/quiz')
        return
      }

      const data = JSON.parse(quizData)

      // Search for occupation
      const occupations = await apiClient.searchOccupations(data.current_job_title)
      if (!occupations.length) {
        toast.error('Could not find occupation. Using default.')
        return
      }

      const occupation = occupations[0]

      // Get automation prediction
      const automationResult = await apiClient.predictAutomation(occupation.id)
      setAutomation(automationResult)

      // Get dividend projection
      const dividendResult = await apiClient.simulateDividend({
        sector: occupation.sector,
        automation_score: automationResult.automation_score,
        base_salary: data.current_salary || occupation.median_salary,
        country: data.country,
        contribution_hours_weekly: data.learning_hours_per_week,
      })
      setDividend(dividendResult)

      setLoading(false)
    } catch (error) {
      console.error('Failed to load results:', error)
      toast.error('Failed to load results')
      setLoading(false)
    }
  }

  const handleShare = () => {
    analytics.shareClick('twitter')
    toast.success('Share feature coming soon!')
  }

  const handleUpgrade = () => {
    analytics.upgradeClick('results')
    navigate('/premium')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-electricblue border-t-transparent mx-auto mb-4" />
          <p className="text-gray-400">Analyzing your future...</p>
        </div>
      </div>
    )
  }

  if (!automation || !dividend) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-400">No results found.</p>
          <Button onClick={() => navigate('/quiz')} className="mt-4">
            Take Quiz
          </Button>
        </div>
      </div>
    )
  }

  const bandColor = {
    Low: 'text-neonmint',
    Medium: 'text-yellow-400',
    High: 'text-red-400',
  }[automation.band] || 'text-gray-400'

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-display font-bold mb-4">
            Your AI Future Report
          </h1>
          <p className="text-gray-400 text-lg">
            Personalized insights and action plan for the AI economy
          </p>
        </motion.div>

        {/* Key Metrics */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <GlassCard>
            <Metric
              label="Automation Risk"
              value={automation.band}
              icon={<Sparkles className="w-4 h-4" />}
            />
            <p className={`mt-4 font-medium ${bandColor}`}>
              {automation.eta_years} years until substantial impact
            </p>
          </GlassCard>

          <GlassCard>
            <Metric
              label="10-Year AIDE Projection"
              value={formatCurrency(dividend.year_10)}
              icon={<Sparkles className="w-4 h-4" />}
            />
            <p className="mt-4 text-sm text-gray-400">
              {dividend.percentage_of_current_salary_y10.toFixed(0)}% of current salary
            </p>
          </GlassCard>

          <GlassCard>
            <Metric
              label="Confidence Score"
              value={`${(automation.confidence * 100).toFixed(0)}%`}
              icon={<Sparkles className="w-4 h-4" />}
            />
            <p className="mt-4 text-sm text-gray-400">Based on current AI research</p>
          </GlassCard>
        </div>

        {/* Automation Explanation */}
        <GlassCard className="mb-8">
          <h3 className="text-xl font-display font-bold mb-4">Automation Analysis</h3>
          <p className="text-gray-300 leading-relaxed mb-6">{automation.explanation}</p>

          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Key Factors</h4>
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(automation.drivers).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm capitalize">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <span className={value > 0 ? 'text-red-400' : 'text-neonmint'}>
                    {value > 0 ? '+' : ''}
                    {(value * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </GlassCard>

        {/* Dividend Chart */}
        <GlassCard className="mb-8">
          <h3 className="text-xl font-display font-bold mb-6">AIDE Dividend Projection</h3>

          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dividend.series}>
              <defs>
                <linearGradient id="dividendGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#64FBD2" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#64FBD2" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="year" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px',
                }}
              />
              <Area
                type="monotone"
                dataKey="user_dividend"
                stroke="#64FBD2"
                fill="url(#dividendGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>

          <p className="text-sm text-gray-400 mt-4">{dividend.explanation}</p>
        </GlassCard>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Button variant="outline" onClick={handleShare} className="flex-1">
            <Share2 className="mr-2 w-4 h-4" />
            Share Results
          </Button>
          <Button variant="ghost" disabled className="flex-1">
            <Download className="mr-2 w-4 h-4" />
            Download PDF (Pro)
          </Button>
        </div>

        {/* Upgrade CTA */}
        <RibbonCTA
          title="Unlock Your Full Plan"
          description="Get 3 personalized career tracks, advanced simulator, and PDF reports with Premium"
          buttonText="Upgrade to Pro"
          onClick={handleUpgrade}
        />
      </div>
    </div>
  )
}
