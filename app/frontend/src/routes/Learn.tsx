import { motion } from 'framer-motion'
import { ExternalLink, BookOpen, Video, Code } from 'lucide-react'
import { GlassCard } from '../components/GlassCard'
import { Button } from '../components/ui/button'

export default function Learn() {
  const tracks = [
    {
      title: 'AI Literacy Fundamentals',
      category: 'Foundation',
      duration: '4 weeks',
      icon: <BookOpen className="w-6 h-6" />,
      description: 'Understanding AI capabilities, limitations, and impact',
      affiliate: 'https://coursera.org',
    },
    {
      title: 'Creative Skills for AI Era',
      category: 'Creative',
      duration: '6 weeks',
      icon: <Video className="w-6 h-6" />,
      description: 'Develop automation-resistant creative capabilities',
      affiliate: 'https://udemy.com',
    },
    {
      title: 'Human-AI Collaboration',
      category: 'Technology',
      duration: '8 weeks',
      icon: <Code className="w-6 h-6" />,
      description: 'Master working with AI tools and copilots',
      affiliate: 'https://linkedin.com/learning',
    },
  ]

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
            Learning{' '}
            <span className="bg-gradient-to-r from-electricblue to-neonmint bg-clip-text text-transparent">
              Paths
            </span>
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Curated courses and resources to future-proof your career
          </p>
        </motion.div>

        {/* Tracks Grid */}
        <div className="grid md:grid-cols-3 gap-6">
          {tracks.map((track, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <GlassCard className="h-full flex flex-col">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-xl bg-electricblue/20 text-electricblue">
                    {track.icon}
                  </div>
                  <div>
                    <span className="text-xs text-gray-400 uppercase tracking-wider">
                      {track.category}
                    </span>
                    <p className="text-sm text-gray-500">{track.duration}</p>
                  </div>
                </div>

                <h3 className="text-xl font-display font-bold mb-3">{track.title}</h3>
                <p className="text-gray-400 mb-6 flex-grow">{track.description}</p>

                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => window.open(track.affiliate, '_blank')}
                >
                  View Course
                  <ExternalLink className="ml-2 w-4 h-4" />
                </Button>
              </GlassCard>
            </motion.div>
          ))}
        </div>

        {/* Info Note */}
        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Courses open in partner platforms. Life After AI may earn affiliate commissions.
          </p>
        </div>
      </div>
    </div>
  )
}
