import { motion } from 'framer-motion'
import { ArrowRight, Sparkles, TrendingUp, Shield } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { GlassCard } from '../components/GlassCard'
import { analytics } from '../lib/analytics'

export default function Home() {
  const navigate = useNavigate()

  const handleStartQuiz = () => {
    analytics.startedQuiz()
    navigate('/quiz')
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-electricblue/10 via-transparent to-transparent" />

        <div className="max-w-6xl mx-auto relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center space-y-8"
          >
            {/* Logo/Brand */}
            <div className="inline-block">
              <span className="text-electricblue text-sm font-medium tracking-wider uppercase">
                Introducing
              </span>
              <h1 className="text-6xl md:text-7xl font-display font-bold mt-2 bg-gradient-to-r from-electricblue to-neonmint bg-clip-text text-transparent">
                Life After AI
              </h1>
            </div>

            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              Predict which jobs AI will automate, simulate your{' '}
              <span className="text-neonmint font-semibold">AI Dividend</span>, and plan your future
              in the AI economy.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
              <Button size="lg" onClick={handleStartQuiz} className="group text-lg">
                Start the 3-Minute Test
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button size="lg" variant="outline" onClick={() => navigate('/learn')}>
                Learn More
              </Button>
            </div>

            <p className="text-sm text-gray-500">
              Join 10,000+ people planning their AI-era future
            </p>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-display font-bold text-center mb-12">
            Your Complete AI Future Plan
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <GlassCard>
              <div className="flex flex-col items-center text-center space-y-4">
                <div className="p-4 rounded-full bg-electricblue/20">
                  <Sparkles className="w-8 h-8 text-electricblue" />
                </div>
                <h3 className="text-xl font-display font-semibold">Automation Prediction</h3>
                <p className="text-gray-400">
                  Get personalized risk assessment and timeline for your occupation based on latest
                  AI research.
                </p>
              </div>
            </GlassCard>

            <GlassCard>
              <div className="flex flex-col items-center text-center space-y-4">
                <div className="p-4 rounded-full bg-neonmint/20">
                  <TrendingUp className="w-8 h-8 text-neonmint" />
                </div>
                <h3 className="text-xl font-display font-semibold">AIDE Dividend Simulator</h3>
                <p className="text-gray-400">
                  See your potential universal income from automation surplus over 5, 10, and 20
                  years.
                </p>
              </div>
            </GlassCard>

            <GlassCard>
              <div className="flex flex-col items-center text-center space-y-4">
                <div className="p-4 rounded-full bg-purple-500/20">
                  <Shield className="w-8 h-8 text-purple-400" />
                </div>
                <h3 className="text-xl font-display font-semibold">Personal Action Plan</h3>
                <p className="text-gray-400">
                  Get 3 custom career tracks with skills, resources, and affiliate course
                  recommendations.
                </p>
              </div>
            </GlassCard>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <GlassCard className="bg-gradient-to-r from-electricblue/10 to-neonmint/10">
            <div className="text-center space-y-6">
              <h2 className="text-3xl md:text-4xl font-display font-bold">
                Ready to Plan Your Future?
              </h2>
              <p className="text-xl text-gray-300">
                Take the quiz now and get your personalized AI-era roadmap in 3 minutes.
              </p>
              <Button size="lg" onClick={handleStartQuiz} className="text-lg">
                Start Your Assessment
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-4">
        <div className="max-w-6xl mx-auto text-center text-gray-500 space-y-4">
          <p>© 2024 Life After AI. Illustrative projections, not financial advice.</p>
          <div className="flex gap-6 justify-center text-sm">
            <a href="/legal/privacy" className="hover:text-electricblue">
              Privacy
            </a>
            <a href="/legal/terms" className="hover:text-electricblue">
              Terms
            </a>
            <a href="/premium" className="hover:text-electricblue">
              Premium
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}
