'use client'
import { motion } from 'framer-motion'
import { Bot, Workflow, BarChart3, Shield } from 'lucide-react'

const features = [
  { title:'Agentic CRM', desc:'Pipeline, deals, suivi client auto', icon:Bot },
  { title:'Workflows Odoo', desc:'Import/ventes/pieces synchronises', icon:Workflow },
  { title:'Shopify agentic', desc:'Listings, price rules, fulfillment', icon:BarChart3 },
  { title:'Securite & Audit', desc:'Logs, preuves, conformite CI/AF', icon:Shield },
]

export default function Home() {
  return (
    <main className="max-w-6xl mx-auto px-6 py-20">
      <motion.h1 initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} className="text-4xl font-bold tracking-tight">
        IVOIRE MONADE -- OBM <span className="text-brand">Agentic</span>
      </motion.h1>
      <motion.p initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} transition={{delay:.1}} className="mt-3 text-slate-400 text-lg">
        OSS pour le marche ivoirien et africain. CRM, support client, Odoo, Shopify, Hermes skills/MCP.
      </motion.p>
      <div className="mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((f,i)=> (
          <motion.div key={f.title} initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} transition={{delay: i*0.08}} className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
            <f.icon className="h-6 w-6 text-brand" />
            <h3 className="mt-3 font-semibold">{f.title}</h3>
            <p className="mt-1 text-sm text-slate-400">{f.desc}</p>
          </motion.div>
        ))}
      </div>
      <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{delay:.35}} className="mt-10 flex gap-3">
        <a href="mailto:prince3626ezechiel@gmail.com" className="rounded-xl bg-brand px-5 py-3 font-semibold text-slate-950">Contact commercial</a>
        <a href="https://wa.me/2250788626125" className="rounded-xl border border-slate-700 px-5 py-3 font-semibold">WhatsApp</a>
      </motion.div>
    </main>
  )
}
