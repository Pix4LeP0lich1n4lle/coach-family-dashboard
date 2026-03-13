# 🎯 Espaces Coaching Personnalisés

Système d'accès sécurisé pour les espaces coaching individuels de chaque participant.

## 🔐 Architecture

```
coaching/
├── index.html                    # Page d'authentification (landing page)
├── tokens.json                   # Tokens de sécurité (git-ignored en production)
├── dashboards/
│   ├── joseph.html              # Dashboard personnel Joseph
│   ├── marie.html               # Dashboard personnel Marie
│   ├── alex.html                # Dashboard personnel Alex
│   ├── chantal.html             # Dashboard personnel Chantal
│   └── danielle.html            # Dashboard personnel Danielle
└── README.md                     # Ce fichier
```

## 🔑 Tokens d'Accès

Chaque participant a un **token secret unique** pour accéder à son espace:

```json
{
  "joseph": "joseph_coach_secret_x7k2m9n",
  "marie": "marie_coach_secret_q4b8r1p",
  "alex": "alex_coach_secret_w9d3f5t",
  "chantal": "chantal_coach_secret_h7j2l8v",
  "danielle": "danielle_coach_secret_z6c4m1x"
}
```

## 📱 Flux d'Accès

### Pour un participant:
1. Reçoit un **lien unique** par email: `https://github.io/coaching/?token=joseph_coach_secret_x7k2m9n`
2. Arrive sur la page d'authentification (`index.html`)
3. Entre son token (ou clique sur le lien précomplété)
4. JavaScript valide le token
5. Redirige vers son dashboard personnel (`dashboards/joseph.html`)
6. Session stockée en `sessionStorage` (navigateur local uniquement)

### Sécurité:
- ✅ Token en URL = facile à partager par email (lien unique)
- ✅ `sessionStorage` = persiste pendant la session mais pas entre navigateurs
- ✅ Pas de compte externe (GitHub, etc.) requis
- ✅ Page d'authentification = landing (pas indexée par défaut)

## 🧪 Test avec Joseph

### Lien d'accès pour Joseph:
```
https://[repo].github.io/coaching/?token=joseph_coach_secret_x7k2m9n
```

### Ou:
1. Accéder à: `https://[repo].github.io/coaching/`
2. Entrer le token: `joseph_coach_secret_x7k2m9n`
3. Cliquer "Accéder à mon espace"

### Dashboard Joseph contient:
- 📊 **Vue d'ensemble** — Stats S06-S09, archétype, moments clés
- 📈 **Progression** — Courbe d'évolution semaine par semaine
- 🎯 **Objectifs S10** — Plan personnalisé (1-2 objectifs/jour max)
- 📝 **Entrées journelles** — Toutes les 9 entrées avec timeline
- 💡 **Plan coaching** — Stratégie S10+, forces, points d'attention

## 🔄 Déploiement

### Étape 1: Ajouter au repo GitHub
```bash
cd /home/chakra/ai-lab/PROJECTS/Coach_Suivies/coach_agents/github/

# Si pas encore initialisé:
git init
git add coaching/
git commit -m "feat: add personalized coaching spaces with Joseph test"
git push origin main
```

### Étape 2: Activer GitHub Pages (si nécessaire)
- Aller sur Settings → Pages
- Source: main branch
- Deploy from `/github/coaching/` (si structuré ainsi)

### Étape 3: Récupérer les URLs
```
Landing (auth): https://[owner].github.io/coaching/
Joseph dashboard: https://[owner].github.io/coaching/?token=joseph_coach_secret_x7k2m9n
```

## 🛠️ Modifications Futures

### Pour ajouter un nouveau participant:
1. **Créer le dashboard HTML** — Copier `dashboards/joseph.html` → `dashboards/{nom}.html`
2. **Adapter le contenu** — Remplacer données Joseph par celles du participant
3. **Ajouter token** — Ajouter entrée à `tokens.json`
4. **Générer lien** — Créer URL avec le token

### Pour améliorer la sécurité:
- Stocker `tokens.json` en `git-ignore` + gérer les tokens en variables d'environnement
- Utiliser JWT tokens (optionnel, plus complexe)
- Ajouter encryption au niveau client (optionnel)

## 📊 Contenu du Dashboard Joseph

### Données Sources:
- `../evolution_summary_S01_S10.json` — Stats S06-S09
- `../progression/joseph/EVOLUTION_S01_S10.md` — Rapport détaillé
- `../progression/joseph/raw_data.json` — Entrées brutes

### Sections:
1. **Vue d'ensemble** — Statistiques + moments clés
2. **Progression** — Tableau semaine-par-semaine + phases
3. **Objectifs S10** — Plan coaching personnalisé
4. **Entrées journelles** — Timeline des 9 entrées avec citations
5. **Plan coaching** — Stratégie détaillée S10+

## 🔗 Intégration avec Coach Dashboard

### Option 1: Lien depuis le dashboard familial
Ajouter un lien "🔐 Mon espace personnel" sur la carte Joseph qui redirige vers:
```html
<a href="./coaching/?token=joseph_coach_secret_x7k2m9n">
  🔐 Mon espace personnel
</a>
```

### Option 2: Repo séparé
Garder `coaching/` dans un repo privé ou semi-privé si les tokens doivent rester secrets.

## 📝 Notes de Test

Pour tester Joseph:
1. Cloner/accéder à la structure locale
2. Ouvrir `index.html` dans le navigateur
3. Copier-coller le token: `joseph_coach_secret_x7k2m9n`
4. Vérifier que le dashboard charge correctement

## 🚀 Prochaines Étapes

- [ ] Tester complètement avec Joseph
- [ ] Créer dashboards pour Marie, Alex, Chantal, Danielle
- [ ] Valider sécurité (pas de données sensibles exposées)
- [ ] Mettre à jour les tokens en variables d'env si en production
- [ ] Ajouter lien depuis coach-family-dashboard (optionnel)
- [ ] Auto-synchronisation hebdomadaire des données (optionnel)

---

**Créé:** 13 mars 2026 | **Status:** ✅ Prêt pour test avec Joseph
