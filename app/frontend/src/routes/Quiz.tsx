import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, ArrowLeft } from 'lucide-react'
import { Button } from '../components/ui/button'
import { GlassCard } from '../components/GlassCard'
import { apiClient } from '../lib/api'
import { analytics } from '../lib/analytics'
import { toast } from 'sonner'

export default function Quiz() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [formData, setFormData] = useState({
    country: 'US',
    age_range: '25-34',
    current_job_title: '',
    current_salary: 0,
    skills: [] as string[],
    creative_interests: [] as string[],
    risk_tolerance: 'medium',
    time_horizon: 10,
    learning_hours_per_week: 5,
  })

  const handleSubmit = async () => {
    try {
      const result = await apiClient.submitQuiz(formData)
      analytics.finishedQuiz(formData.current_job_title)

      // Store quiz ID and navigate to results
      sessionStorage.setItem('quizId', result.quiz_id)
      sessionStorage.setItem('quizData', JSON.stringify(formData))
      navigate('/results')
    } catch (error) {
      toast.error('Failed to submit quiz. Please try again.')
    }
  }

  const steps = [
    {
      title: 'About You',
      component: (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Current Job Title</label>
            <input
              type="text"
              value={formData.current_job_title}
              onChange={(e) =>
                setFormData({ ...formData, current_job_title: e.target.value })
              }
              className="w-full px-4 py-3 rounded-xl glass text-offwhite placeholder-gray-500 focus:ring-2 focus:ring-electricblue outline-none"
              placeholder="e.g., Software Developer"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Current Salary (USD)</label>
            <input
              type="number"
              value={formData.current_salary || ''}
              onChange={(e) =>
                setFormData({ ...formData, current_salary: Number(e.target.value) })
              }
              className="w-full px-4 py-3 rounded-xl glass text-offwhite placeholder-gray-500 focus:ring-2 focus:ring-electricblue outline-none"
              placeholder="70000"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Age Range</label>
            <select
              value={formData.age_range}
              onChange={(e) => setFormData({ ...formData, age_range: e.target.value })}
              className="w-full px-4 py-3 rounded-xl glass text-offwhite focus:ring-2 focus:ring-electricblue outline-none"
            >
              <option value="18-24">18-24</option>
              <option value="25-34">25-34</option>
              <option value="35-44">35-44</option>
              <option value="45-54">45-54</option>
              <option value="55+">55+</option>
            </select>
          </div>
        </div>
      ),
    },
    {
      title: 'Your Skills',
      component: (
        <div className="space-y-6">
          <p className="text-gray-400">
            Select your top skills (we'll use these for your plan):
          </p>
          {[
            'Programming',
            'Data Analysis',
            'Design',
            'Writing',
            'Marketing',
            'Sales',
            'Teaching',
            'Management',
          ].map((skill) => (
            <label key={skill} className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.skills.includes(skill)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setFormData({ ...formData, skills: [...formData.skills, skill] })
                  } else {
                    setFormData({
                      ...formData,
                      skills: formData.skills.filter((s) => s !== skill),
                    })
                  }
                }}
                className="w-5 h-5 rounded border-gray-600 text-electricblue focus:ring-electricblue"
              />
              <span>{skill}</span>
            </label>
          ))}
        </div>
      ),
    },
    {
      title: 'Planning Preferences',
      component: (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">
              Time Horizon (years to plan for)
            </label>
            <input
              type="range"
              min="5"
              max="20"
              step="5"
              value={formData.time_horizon}
              onChange={(e) =>
                setFormData({ ...formData, time_horizon: Number(e.target.value) })
              }
              className="w-full"
            />
            <div className="text-center text-2xl font-bold text-electricblue mt-2">
              {formData.time_horizon} years
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Learning Time Available (hours/week)
            </label>
            <input
              type="range"
              min="0"
              max="20"
              step="1"
              value={formData.learning_hours_per_week}
              onChange={(e) =>
                setFormData({ ...formData, learning_hours_per_week: Number(e.target.value) })
              }
              className="w-full"
            />
            <div className="text-center text-2xl font-bold text-neonmint mt-2">
              {formData.learning_hours_per_week} hours/week
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Risk Tolerance</label>
            <div className="grid grid-cols-3 gap-3">
              {['low', 'medium', 'high'].map((level) => (
                <button
                  key={level}
                  onClick={() => setFormData({ ...formData, risk_tolerance: level })}
                  className={`px-4 py-3 rounded-xl glass capitalize ${
                    formData.risk_tolerance === level
                      ? 'ring-2 ring-electricblue bg-electricblue/20'
                      : ''
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>
        </div>
      ),
    },
  ]

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-display font-bold mb-4">
            <span className="bg-gradient-to-r from-electricblue to-neonmint bg-clip-text text-transparent">
              Life After AI
            </span>
          </h1>
          <p className="text-gray-400">Step {step + 1} of {steps.length}</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-electricblue to-neonmint"
              initial={{ width: 0 }}
              animate={{ width: `${((step + 1) / steps.length) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Quiz Content */}
        <GlassCard className="mb-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <h2 className="text-2xl font-display font-bold mb-6">{steps[step].title}</h2>
              {steps[step].component}
            </motion.div>
          </AnimatePresence>
        </GlassCard>

        {/* Navigation */}
        <div className="flex justify-between">
          <Button
            variant="ghost"
            onClick={() => setStep(Math.max(0, step - 1))}
            disabled={step === 0}
          >
            <ArrowLeft className="mr-2 w-4 h-4" />
            Back
          </Button>

          {step < steps.length - 1 ? (
            <Button onClick={() => setStep(step + 1)}>
              Next
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          ) : (
            <Button onClick={handleSubmit}>Submit & See Results</Button>
          )}
        </div>
      </div>
    </div>
  )
}
