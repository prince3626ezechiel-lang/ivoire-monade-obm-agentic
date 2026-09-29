# EON10 Secrets — DR DOOM Stack

Bot Telegram + App React Native pour SaaS-MCP, AAAIAA MCP, RAG MCP.

## Fichiers

| Fichier | Description |
|---------|-------------|
| eon10_bot.py | Bot original (menu grid, compte, depot) |
| eon10_autoclaw.py | Bot autoclaw — jev + gpt6 via Explabs |
| saas_mcp_claw.py | Claw autonome avec jev |
| src/app/index.tsx | App React Native (secrets + QCM maieutique) |
| SOUL.md | Identite DR DOOM |
| agents.md | Definitions agents |
| memo.json | Memoire loop |
| guardian.md | Guardrails |

## Bulk Loop Engine



## Lancement

### Bot classique
python eon10_bot.py

### Bot autoclaw (jev + gpt6)
EXPLABS_API_KEY=xpl_08b9a0678b55f04281447e9a993e538ffe1394c1 python eon10_autoclaw.py

### App React Native
cd EON10Secrets && npx expo start

## Variables denvironnement

EON10_BOT_TOKEN=8680913270:AAERwtVz1xpVz8xACgCZpWTeYmeNTqxZdn4
EON10_ADMIN_CHAT_ID=6499054466
EXPLABS_API_KEY=xpl_08b9a0678b55f04281447e9a993e538ffe1394c1

## Commands Bot

/start | Creer compte
/utiliser | Activer autoclaw
/render | Lancer spot Blender
/jobs | Status rendus
/stop | Desactiver autoclaw
/parrain | Lien parrainage
/signal | Signaux marche
/bug | Signalement

## Autoclaw

- jev-latest : raisonnement TypeSafe (systemone endpoint)
- gpt-6-luna : contenu chat (chat completions endpoint)
- Blender : rendu spots motion design
- Loop : decide -> genere -> rend -> boucle

## Modeles Explabs

type-safe/jev-latest | Raisonnement | ~/usr/bin/bash.000000042
openai/gpt-6-luna | Contenu | /usr/bin/bash.0000001 prompt
anthropic/claude-haiku-4.5 | Backup | —
