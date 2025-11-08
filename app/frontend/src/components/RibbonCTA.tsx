/**
 * Prominent ribbon-style CTA component.
 */
import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'
import { Button } from './ui/button'

interface RibbonCTAProps {
  title: string
  description: string
  buttonText: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
}

export function RibbonCTA({
  title,
  description,
  buttonText,
  onClick,
  variant = 'primary',
}: RibbonCTAProps) {
  const bgGradient =
    variant === 'primary'
      ? 'bg-gradient-to-r from-electricblue/20 to-neonmint/20'
      : 'bg-gradient-to-r from-purple-500/20 to-pink-500/20'

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`glass-strong rounded-2xl p-8 ${bgGradient}`}
    >
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex-1">
          <h3 className="text-2xl font-display font-bold mb-2">{title}</h3>
          <p className="text-gray-300">{description}</p>
        </div>

        <Button size="lg" onClick={onClick} className="group">
          {buttonText}
          <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </Button>
      </div>
    </motion.div>
  )
}
