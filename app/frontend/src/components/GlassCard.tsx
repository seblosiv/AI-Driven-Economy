/**
 * Premium glassmorphism card component.
 */
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface GlassCardProps {
  children: React.ReactNode
  className?: string
  hover?: boolean
  animate?: boolean
}

export function GlassCard({ children, className, hover = true, animate = true }: GlassCardProps) {
  const Component = animate ? motion.div : 'div'

  return (
    <Component
      initial={animate ? { opacity: 0, y: 20 } : undefined}
      animate={animate ? { opacity: 1, y: 0 } : undefined}
      transition={{ duration: 0.5 }}
      className={cn(
        'glass rounded-2xl p-6 shadow-2xl',
        hover && 'hover:-translate-y-1 hover:shadow-electricblue/10 hover:ring-1 hover:ring-electricblue/30',
        'transition-all duration-300',
        className
      )}
    >
      {children}
    </Component>
  )
}
