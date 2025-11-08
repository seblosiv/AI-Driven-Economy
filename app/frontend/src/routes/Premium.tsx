import { motion } from 'framer-motion'
import { Check, Sparkles } from 'lucide-react'
import { Button } from '../components/ui/button'
import { GlassCard } from '../components/GlassCard'
import { analytics } from '../lib/analytics'

export default function Premium() {
  const handleCheckout = (planType: 'monthly' | 'yearly') => {
    analytics.upgradeClick('premium_page')
    // In production, would integrate Stripe checkout
    alert(`Checkout for ${planType} plan (Stripe integration pending)`)
  }

  const features = [
    'Advanced dividend simulator with policy scenarios',
    'Multi-job comparison tool',
    'Download PDF reports',
    '3 detailed career transition tracks',
    'Priority access to new features',
    'Ad-free experience',
    'Weekly automation updates',
    'Access to learning resources library',
  ]

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-block px-4 py-1 rounded-full glass mb-4">
            <span className="text-neonmint text-sm font-medium">PREMIUM</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-display font-bold mb-4">
            Future Insights{' '}
            <span className="bg-gradient-to-r from-electricblue to-neonmint bg-clip-text text-transparent">
              Pro
            </span>
          </h1>

          <p className="text-xl text-gray-300">
            Get comprehensive analysis and planning tools for your AI-era future
          </p>
        </motion.div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <GlassCard className="relative">
            <div className="mb-6">
              <h3 className="text-xl font-display font-bold mb-2">Monthly</h3>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold">€7</span>
                <span className="text-gray-400">/month</span>
              </div>
            </div>

            <Button onClick={() => handleCheckout('monthly')} className="w-full mb-6">
              Start Monthly Plan
            </Button>

            <p className="text-sm text-gray-400">Billed monthly, cancel anytime</p>
          </GlassCard>

          <GlassCard className="relative ring-2 ring-electricblue">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2">
              <span className="px-4 py-1 bg-electricblue text-white text-xs font-bold rounded-full">
                BEST VALUE
              </span>
            </div>

            <div className="mb-6">
              <h3 className="text-xl font-display font-bold mb-2">Yearly</h3>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold">€49</span>
                <span className="text-gray-400">/year</span>
              </div>
              <p className="text-neonmint text-sm mt-1">Save €35 (42% off)</p>
            </div>

            <Button onClick={() => handleCheckout('yearly')} className="w-full mb-6">
              <Sparkles className="mr-2 w-4 h-4" />
              Start Yearly Plan
            </Button>

            <p className="text-sm text-gray-400">Billed annually, best value</p>
          </GlassCard>
        </div>

        {/* Features */}
        <GlassCard>
          <h3 className="text-xl font-display font-bold mb-6">Everything in Pro</h3>

          <div className="grid gap-4">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="flex items-start gap-3"
              >
                <div className="p-1 rounded-full bg-neonmint/20 mt-0.5">
                  <Check className="w-4 h-4 text-neonmint" />
                </div>
                <span className="text-gray-300">{feature}</span>
              </motion.div>
            ))}
          </div>
        </GlassCard>

        {/* FAQ */}
        <div className="mt-12 text-center">
          <p className="text-gray-500 text-sm">
            Questions? Contact us at hello@lifeafterai.com
          </p>
        </div>
      </div>
    </div>
  )
}
