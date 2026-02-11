# Exercice 2 : Créer des Sub-agents avec des Skills et des Tools

**Durée :** 10-12 minutes
**Objectif :** Créer deux sub-agents — `doc-reviewer` et `doc-generator` — chacun avec des permissions soigneusement définies et des skills attachés.

---

## Contexte

Les sub-agents sont des instances spécialisées de Claude que l'agent principal peut dispatcher pour gérer des tâches ciblées. Chaque sub-agent possède :
- Un **prompt** définissant son rôle et son comportement
- Un **ensemble de tools** qu'il est autorisé à utiliser (principe du moindre privilège)
- Des **skills** qui lui donnent des connaissances spécifiques au domaine
- Sa **propre fenêtre de contexte**, pour ne pas consommer celle de l'agent principal

Le principe de conception clé ici est le **moindre privilège** : chaque agent ne reçoit que les tools dont il a besoin, rien de plus. Un reviewer qui peut modifier du code est dangereux. Un generator qui ne peut pas écrire de fichiers est inutile. Bien définir les permissions des tools est ce qui rend les sub-agents sûrs et efficaces.

---

## Étape 1 : Comprendre le modèle de permissions

Avant de créer les agents, comprenez POURQUOI les tools diffèrent :

| Agent | Objectif | Peut lire | Peut écrire | Peut exécuter des commandes |
|-------|----------|-----------|-------------|----------------------------|
| `doc-reviewer` | Revoir la qualité du code | Oui | **Non** | **Non** |
| `doc-generator` | Générer la documentation | Oui | Oui | Oui |

**Pourquoi le reviewer ne peut pas écrire :**
- Le travail d'un reviewer est de rapporter les problèmes, pas de les corriger
- Si le reviewer pouvait modifier des fichiers, il pourrait silencieusement "corriger" des choses sans que le développeur le sache
- Séparation des responsabilités : l'agent principal décide quoi corriger en fonction du résultat de la revue
- Cela reflète la revue de code réelle — les reviewers commentent, les auteurs corrigent

**Pourquoi le generator a besoin de l'accès en écriture :**
- Il doit créer de nouveaux fichiers markdown dans `docs/`
- Il doit mettre à jour l'index de stockage via le module `storage`
- Il peut avoir besoin d'exécuter des commandes shell (ex. `uv run docgen list` pour vérifier les résultats)

---

## Étape 2 : Créer l'agent `doc-reviewer`

### 2a. Ouvrir l'interface de création d'agents

1. Ouvrez Claude Code dans le répertoire du projet `docgen`
2. Tapez `/agents`
3. Sélectionnez **"Create new agent"**
4. Sélectionnez **"Project"** (pour que l'agent soit stocké dans `.claude/agents/`)
5. Sélectionnez **"Manual configuration"**

### 2b. Configurer l'agent

Remplissez les champs suivants :

**Name :**
```
doc-reviewer
```

**Prompt** (copiez et collez exactement) :
```
You are a code and documentation reviewer ensuring high quality standards.
When invoked, review CLI command files and generated documentation for code quality, convention adherence, input validation, and documentation accuracy.
Output: Issues table with severity, description, suggested fix. Summary with counts. Specific code fixes for critical issues.
```

**Description :**
```
Reviews code and documentation quality. Use when the user asks to review, audit, or check quality.
```

**Tools :** Sélectionnez UNIQUEMENT les trois tools suivants, et désélectionnez tout le reste :
- Read
- Glob
- Grep

**Model :** Inherit from parent

**Color :** Purple

### 2c. Sauvegarder et ajouter le Skill

Après la sauvegarde, Claude Code crée le fichier `.claude/agents/doc-reviewer.md`. Ouvrez ce fichier et ajoutez la section skills en bas :

```yaml
skills:
  - reviewing-documentation
```

Cela lie le skill que vous avez créé dans l'exercice 1 à cet agent. Quand l'agent principal dispatche `doc-reviewer`, il chargera automatiquement le skill `reviewing-documentation` dans le contexte du sub-agent.

> **Astuce :** La section `skills` doit être au niveau racine du frontmatter du fichier agent, ou ajoutée comme métadonnée selon le format utilisé par Claude Code. Ouvrez le fichier après la sauvegarde pour voir sa structure et ajoutez la référence skills au bon endroit.

---

## Étape 3 : Créer l'agent `doc-generator`

### 3a. Ouvrir à nouveau l'interface de création d'agents

1. Dans Claude Code, tapez `/agents`
2. Sélectionnez **"Create new agent"**
3. Sélectionnez **"Project"**
4. Sélectionnez **"Manual configuration"**

### 3b. Configurer l'agent

**Name :**
```
doc-generator
```

**Prompt** (copiez et collez exactement) :
```
You are a documentation generator that reads source code and produces comprehensive markdown documentation.
When invoked, read target source files, use llm.py to generate docs, write to docs/ directory, update storage.
Output: What files were documented, where docs were saved, any issues encountered.
```

**Description :**
```
Generates and updates documentation. Use when asked to generate, write, or update docs.
```

**Tools :** Sélectionnez les six tools suivants :
- Read
- Write
- Edit
- Bash
- Glob
- Grep

**Model :** Inherit from parent

**Color :** Yellow

### 3c. Sauvegarder et ajouter le Skill

Après la sauvegarde, ouvrez `.claude/agents/doc-generator.md` et ajoutez :

```yaml
skills:
  - generating-documentation
```

> **Note :** Le skill `generating-documentation` n'existe peut-être pas encore s'il ne faisait pas partie des matériaux pré-construits. Ce n'est pas grave — l'agent fonctionnera quand même, et le skill pourra être ajouté plus tard. L'important est que le fichier agent le référence pour qu'il soit chargé quand le skill deviendra disponible.

---

## Étape 4 : Vérifier les deux agents

Vérifiez que les deux fichiers agents existent dans le répertoire `.claude/agents/` :

```bash
ls -la .claude/agents/
```

Vous devriez voir :
```
doc-reviewer.md
doc-generator.md
```

Ouvrez chaque fichier et vérifiez :
- Le prompt correspond à ce que vous avez saisi
- La liste des tools est correcte (3 tools pour le reviewer, 6 pour le generator)
- La référence skills est présente

### Checklist de vérification rapide

Pour `doc-reviewer.md` :
- [ ] Le prompt mentionne "reviewer" et "quality standards"
- [ ] Seuls Read, Glob, Grep sont listés comme tools
- [ ] Skills référence `reviewing-documentation`
- [ ] La couleur est purple

Pour `doc-generator.md` :
- [ ] Le prompt mentionne "documentation generator" et "write to docs/"
- [ ] Read, Write, Edit, Bash, Glob, Grep sont listés comme tools
- [ ] Skills référence `generating-documentation`
- [ ] La couleur est yellow

---

## Étape 5 : Recharger Claude Code

Fermez et rouvrez Claude Code pour qu'il détecte les nouveaux agents.

Après la réouverture, tapez `/agents` pour voir la liste. `doc-reviewer` et `doc-generator` devraient tous deux apparaître.

> **Astuce :** Si un agent n'apparaît pas, vérifiez :
> - Le fichier est dans `.claude/agents/` (pas `.claude/skills/` ou un autre répertoire)
> - Le nom de fichier se termine par `.md`
> - Le fichier est du markdown valide avec un frontmatter correct

---

## Pourquoi c'est important

La séparation que vous venez de créer est une version miniature de la conception des systèmes IA en production :

1. **Le moindre privilège prévient les accidents.** Le reviewer ne peut pas accidentellement écraser un fichier. Le generator ne peut pas accidentellement supprimer du code. Chaque agent ne peut faire que ce pour quoi il est conçu.

2. **Un contexte spécialisé est plus efficace.** Au lieu d'un agent qui essaie d'être expert en tout, chaque sub-agent ne charge que les connaissances (skills) dont il a besoin. Cela signifie moins de bruit dans la fenêtre de contexte et des résultats plus ciblés et précis.

3. **L'agent principal orchestre.** Votre session principale Claude Code agit comme le "manager" — elle décide quand dispatcher chaque sub-agent, lit leur résultat et agit en conséquence. Cela reflète la façon dont un tech lead délègue les revues de code et les tâches de documentation à des spécialistes.

4. **Les skills rendent les agents cohérents.** Sans le skill, le reviewer utiliserait ses connaissances générales pour revoir le code. Avec le skill, il vérifie par rapport aux conventions spécifiques de VOTRE projet. C'est la différence entre une revue générique et une revue utile.

---

## Critères de réussite

Vous avez terminé cet exercice quand :
- [ ] `.claude/agents/doc-reviewer.md` existe avec le bon prompt, 3 tools (Read, Glob, Grep) et le skill `reviewing-documentation`
- [ ] `.claude/agents/doc-generator.md` existe avec le bon prompt, 6 tools (Read, Write, Edit, Bash, Glob, Grep) et le skill `generating-documentation`
- [ ] Les deux agents apparaissent quand vous exécutez `/agents` dans Claude Code
- [ ] Vous pouvez expliquer pourquoi le reviewer a moins de tools que le generator
