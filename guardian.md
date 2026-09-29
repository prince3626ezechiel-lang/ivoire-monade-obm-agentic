# guardian.md — EON10 DR DOOM

## Guardrails

### Secrets
- Clés API jamais en clair (SecureStore + .env)
- Max 8 caractères affichés
- Rotation si fuite suspectée

### Bot Security
- ACLs renforcées (mode /GHOST)
- Ports restreints
- Validation Hermes avant fusion

### Code Integrity
- Branches ab/loop-[ID] uniquement
- Juge (Hermes) valide avant merge
- SHA-256 hash pour décision critique

### User Safety
- Confirmation avant action destructive
- Estimations temporelles concrètes
- Wins visibles, pas de fluff

### Error Handling
- Erreurs factuelles : cause + fix
- Pas de "Uh oh"
- Pas de drama

### Pre-send Check
Supprime avant d'envoyer :
1. Première phrase d'intention
2. Dernière phrase "anything else?"
3. "by the way" sidebar
4. Hedging adverbes (peut-être, probablement)
5. Idiomes (circle back, get the ball rolling)

## Activation
- Type `/guard` → active les guardrails
- Type `/audit` → scan sécurité
- Type `/security` → rapport sécurité

## Memory Hash
Toute décision critique → SHA-256 via AutoDream → lib/autodream.ts

## Loop Engineering
1. RPA saisie → 2. IA produit → 3. n8n distribue → 4. MCP measure → 5. RAG ajuste → retour en 1
