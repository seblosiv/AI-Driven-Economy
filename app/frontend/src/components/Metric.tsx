/**
 * Metric display component with optional delta.
 */
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { cn } from '@/lib/utils'

interface MetricProps {
  label: string
  value: string | number
  delta?: number
  deltaLabel?: string
  icon?: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}

export function Metric({ label, value, delta, deltaLabel, icon, size = 'md' }: MetricProps) {
  const sizes = {
    sm: 'text-2xl',
    md: 'text-4xl',
    lg: 'text-5xl',
  }

  const getDeltaColor = (delta: number) => {
    if (delta > 0) return 'text-neonmint'
    if (delta < 0) return 'text-red-400'
    return 'text-gray-400'
  }

  const getDeltaIcon = (delta: number) => {
    if (delta > 0) return <TrendingUp className="w-4 h-4" />
    if (delta < 0) return <TrendingDown className="w-4 h-4" />
    return <Minus className="w-4 h-4" />
  }

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2 text-sm text-gray-400">
        {icon}
        <span>{label}</span>
      </div>

      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5, type: 'spring' }}
        className={cn('font-display font-bold', sizes[size])}
      >
        {value}
      </motion.div>

      {delta !== undefined && (
        <div className={cn('flex items-center gap-1 text-sm font-medium', getDeltaColor(delta))}>
          {getDeltaIcon(delta)}
          <span>{Math.abs(delta)}%</span>
          {deltaLabel && <span className="text-gray-500">{deltaLabel}</span>}
        </div>
      )}
    </div>
  )
}
