# Process Constitution — EON10 DR DOOM

## Boucle Loop Engineering
1. RPA saisie → 2. IA produit → 3. n8n distribue → 4. MCP measure → 5. RAG ajuste → retour en 1

## Étapes Reverse Engineering
1. Audit obfuscation
2. Migration OpenRouter → Explabs
3. Création bot Telegram
4. Intégration MCPs
5. Test autoclaw
6. Déploiement

## Règles
- Chaque étape doit être documentée dans 00_run_report.md
- Les exceptions vont dans 05_exceptions.md
- Les décisions dans 04_decisions.md
- Le status dans default_results.json

## Validation
- Guardian valide chaque étape avant passage à la suivante
- Juge (Hermes) vérifie l'intégrité
- Orchestrateur (DR DOOM) route vers le bon MCP
