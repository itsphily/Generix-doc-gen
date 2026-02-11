# Exercice 3 : Déclencher et tester les Sub-agents

**Durée :** 10-12 minutes
**Objectif :** Déclencher les deux sub-agents, observer leur comportement et expérimenter le workflow complet revue-correction-génération.

---

## Contexte

Vous avez construit les éléments : un skill qui définit les standards de revue (exercice 1) et deux sub-agents avec des permissions définies (exercice 2). Maintenant vous allez les mettre au travail.

Dans cet exercice, vous allez :
1. Dispatcher le `doc-reviewer` pour trouver les problèmes dans `update.py`
2. Demander à l'agent principal de corriger les problèmes
3. Dispatcher le `doc-generator` pour créer de la documentation
4. Vérifier les résultats via le CLI `docgen`

C'est le workflow qui donne toute leur valeur aux sub-agents : des agents spécialisés gèrent des tâches spécialisées dans leur propre fenêtre de contexte, pendant que l'agent principal reste concentré sur le développement et l'orchestration.

---

## Étape 1 : Déclencher le doc-reviewer

### 1a. Dispatcher le reviewer

Dans Claude Code, tapez le prompt suivant :

```
Use the doc-reviewer to review the update.py command
```

### 1b. Observer ce qui se passe

Observez attentivement l'interface Claude Code. Vous devriez voir :

1. L'agent principal reconnaît que c'est une tâche pour le sub-agent `doc-reviewer`
2. Le sub-agent est dispatché — remarquez qu'il se charge dans son propre contexte
3. Le skill `reviewing-documentation` est chargé automatiquement
4. Le sub-agent lit `update.py`, puis lit les fichiers de référence (`display.py`, `constants.py`, `llm.py`, `generate.py`)
5. Il vérifie `update.py` par rapport à chaque élément de la conventions checklist
6. Il produit un rapport structuré

### 1c. Lire le résultat de la revue

Le reviewer devrait trouver plusieurs problèmes dans `update.py`. Attendez-vous à des résultats comme :

| Sévérité | Description | Localisation |
|----------|-------------|--------------|
| Critical | Pas d'annotations de type — les paramètres utilisent des types bruts sans `Annotated` | Signature de la fonction |
| Critical | Utilise `print()` au lieu du module `display` | Plusieurs lignes |
| Critical | Utilise des nombres magiques comme codes de sortie au lieu de constantes nommées | `raise typer.Exit(1)` |
| Critical | Pas de validation des entrées — les chemins de fichiers ne sont pas vérifiés avant utilisation | Début de la fonction |
| Critical | Appels LLM en ligne — importe OpenAI directement au lieu d'utiliser le module `llm` | Section imports et corps de la fonction |
| Critical | Manipulation directe de JSON au lieu d'utiliser le module `storage` | Section I/O fichiers |
| Warning  | Docstring manquant sur la fonction de commande | Définition de la fonction |
| Warning  | Pas de gestion d'erreurs / blocs try-except | Toute la fonction |

> **Observation clé :** Remarquez que le reviewer a trouvé tous ces problèmes mais n'a PAS tenté d'en corriger aucun. Il ne peut pas — il n'a que les tools Read, Glob et Grep. C'est le principe du moindre privilège en action. Le reviewer rapporte ; le développeur (ou l'agent principal) décide quoi corriger.

---

## Étape 2 : Corriger les problèmes

### 2a. Demander à l'agent principal de corriger

Maintenant demandez à l'agent principal (pas au sub-agent) de corriger les problèmes :

```
Fix the issues found by the reviewer in update.py
```

### 2b. Observer le processus de correction

Observez comment l'agent principal gère cela :

1. Il lit le résultat de la revue du sub-agent
2. Il lit `update.py` pour comprendre l'état actuel
3. Il lit `generate.py` comme référence pour les patterns corrects
4. Il applique les corrections une par une :
   - Ajoute des annotations de type `Annotated` avec du texte d'aide
   - Remplace les appels `print()` par `display.success()`, `display.error()`, etc.
   - Remplace les codes de sortie magiques par des constantes nommées de `constants.py`
   - Ajoute la validation des entrées en début de fonction
   - Remplace les appels OpenAI en ligne par `llm.generate_documentation()`
   - Remplace la manipulation directe de JSON par `storage.add_entry()`
   - Ajoute un docstring
   - Enveloppe la logique dans des blocs try-except

### 2c. Vérifier les corrections

Après que l'agent principal a terminé, vous pouvez optionnellement relancer le reviewer pour confirmer :

```
Use the doc-reviewer to review update.py again
```

La revue devrait maintenant revenir propre, ou avec seulement des avertissements mineurs.

> **Observation clé :** L'agent principal a utilisé son ensemble complet de tools (Read, Write, Edit) pour appliquer les corrections. Le reviewer n'aurait pas pu le faire seul. Cette séparation crée un point de contrôle naturel : d'abord la revue, puis la décision de ce qu'il faut corriger.

---

## Étape 3 : Déclencher le doc-generator

### 3a. Dispatcher le generator

Tapez le prompt suivant dans Claude Code :

```
Use the doc-generator to generate documentation for storage.py
```

### 3b. Observer ce qui se passe

Le sub-agent `doc-generator` va :

1. Se charger dans son propre contexte avec le skill `generating-documentation`
2. Lire `storage.py` pour comprendre l'API du module, ses fonctions et son objectif
3. Utiliser le module `llm` pour générer une documentation markdown complète
4. Écrire le résultat dans `docs/storage.md`
5. Mettre à jour l'index de stockage pour que `docgen list` connaisse la nouvelle documentation

### 3c. Vérifier le résultat

Après que le generator a terminé, vérifiez que la documentation a été créée :

```bash
cat docs/storage.md
```

La documentation devrait inclure :
- Vue d'ensemble et objectif du module
- Signatures de fonctions avec descriptions des paramètres
- Documentation des valeurs de retour
- Exemples d'utilisation
- Notes ou mises en garde importantes

> **Observation clé :** Le generator a les tools Write, Edit et Bash parce qu'il doit créer des fichiers et potentiellement exécuter des commandes. Le reviewer n'a pas ces tools. Chaque agent a exactement les permissions que son travail requiert.

---

## Étape 4 : Vérifier avec l'application

Exécutez le CLI `docgen` pour confirmer que tout est enregistré :

```bash
uv run docgen list
```

Vous devriez voir `storage.md` (ou `storage.py`) listé comme module documenté. Cela confirme que le generator a non seulement créé le fichier de documentation mais aussi mis à jour correctement l'index de stockage.

> **Astuce :** Si l'entrée n'apparaît pas, le generator n'a peut-être pas appelé `storage.add_entry()`. Vous pouvez demander à l'agent principal de vérifier et corriger cela.

---

## Étape 5 (Bonus) : Workflow complet

Si vous avez du temps restant, essayez le workflow complet développement-revue-documentation :

### 5a. Créer une nouvelle commande

Demandez à l'agent principal :

```
Add a new "summarize" command to docgen that takes a docs/ directory and produces a summary of all documented modules
```

L'agent principal va créer un nouveau fichier de commande (ex. `summarize.py`), l'enregistrer auprès du CLI et implémenter la logique.

### 5b. Revoir la nouvelle commande

Dispatchez le reviewer :

```
Use the doc-reviewer to review the summarize command
```

Comme l'agent principal a écrit la commande en connaissant les conventions du projet (il a lu `generate.py` et le skill tout au long de cette session), la revue devrait revenir relativement propre. Mais il peut encore y avoir des problèmes — c'est normal et utile.

### 5c. Documenter la nouvelle commande

Dispatchez le generator :

```
Use the doc-generator to generate documentation for summarize.py
```

### 5d. Vérification finale

```bash
uv run docgen list
```

Vous devriez maintenant voir la commande summarize documentée aux côtés des autres modules.

---

## Ce que vous avez appris

### Le pattern Sub-agent

```
Agent Principal (orchestrateur)
  |
  |-- dispatche --> doc-reviewer (lecture seule, rapporte les problèmes)
  |                    |-- charge le skill : reviewing-documentation
  |                    |-- tools : Read, Glob, Grep
  |
  |-- lit le résultat de la revue, applique les corrections
  |
  |-- dispatche --> doc-generator (lecture-écriture, crée la documentation)
                       |-- charge le skill : generating-documentation
                       |-- tools : Read, Write, Edit, Bash, Glob, Grep
```

### Pourquoi c'est mieux qu'un seul agent qui fait tout

1. **Efficacité de la fenêtre de contexte.** Chaque sub-agent a sa propre fenêtre de contexte. Le contexte de l'agent principal n'est pas consommé par la checklist détaillée de revue ou les prompts de génération de documentation. C'est important dans les sessions longues où l'espace de contexte est précieux.

2. **Cohérence grâce aux skills.** Le reviewer vérifie toujours la même checklist, à chaque fois, sans oublier d'éléments. Un humain ou un agent généraliste pourrait sauter des vérifications quand il est fatigué ou distrait. Le skill rend la revue déterministe et exhaustive.

3. **Sécurité grâce aux permissions.** Le reviewer ne peut physiquement pas modifier le code. Ce n'est pas une suggestion ni une instruction dans le prompt — il n'a littéralement pas le tool Write. C'est une garantie plus forte que de dire à un agent "please don't modify files."

4. **Composabilité.** Vous pouvez réutiliser ces agents dans différents workflows. Besoin de revoir toutes les commandes avant une release ? Bouclez le reviewer sur chaque fichier. Besoin de regénérer toute la documentation après un refactoring ? Bouclez le generator. Les agents sont des briques de construction.

5. **Auditabilité.** Le résultat de chaque sub-agent est un artefact discret et lisible. Vous pouvez revoir ce que le reviewer a trouvé, vérifier ce que le generator a écrit et tracer chaque décision. C'est beaucoup plus difficile quand tout se passe dans une seule longue conversation.

---

## Critères de réussite

Vous avez terminé cet exercice quand :
- [ ] Vous avez déclenché le `doc-reviewer` et reçu un rapport structuré des problèmes dans `update.py`
- [ ] L'agent principal a corrigé les problèmes en se basant sur le résultat de la revue
- [ ] Vous avez déclenché le `doc-generator` et `docs/storage.md` a été créé
- [ ] `uv run docgen list` affiche le module nouvellement documenté
- [ ] Vous pouvez expliquer pourquoi les sub-agents sont plus efficaces qu'un seul agent pour des tâches spécialisées
