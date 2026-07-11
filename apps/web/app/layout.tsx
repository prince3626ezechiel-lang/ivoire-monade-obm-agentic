import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'IVOIRE MONADE -- OBM Agentic',
  description: "CRM, support client, Odoo, Shopify agentic pour l'Afrique"
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        {children}
      </body>
    </html>
  )
}
