# Créer des outils IA avec les Skills & Sub-agents de Claude Code

## Workshop pour l'équipe de développement Generix

**Durée :** 90 minutes (pratique)
**Application :** `docgen` -- Générateur de documentation CLI

> NARRATION : Bienvenue au workshop. Aujourd'hui, nous allons construire et étendre un générateur de documentation propulsé par l'IA. Vous apprendrez à créer des skills réutilisables, à configurer des sub-agents spécialisés et à les orchestrer ensemble. Ce sont des patterns que vous pouvez appliquer à n'importe quel projet.

---

## Ce que nous allons apprendre

1. **Structurer des fichiers SKILL.md** pour des workflows IA prévisibles
2. **Créer des sub-agents** avec des skills spécifiques et des permissions contrôlées
3. **Déclencher, tester et orchestrer** des sub-agents ensemble

> NARRATION : À la fin de ce workshop, vous aurez une expérience pratique avec ces trois points. Nous ferons trois exercices guidés où vous construirez tout vous-même. Les concepts s'appliquent à n'importe quel projet -- pas seulement à cette application de démonstration.

---

## L'application : `docgen`

**Ce qu'elle fait :** CLI qui génère de la documentation pour du code source en utilisant un LLM

**Commandes :**

- `docgen generate <file>` -- Générer la documentation d'un fichier source
- `docgen list` -- Afficher tous les fichiers documentés
- `docgen check <file>` -- Vérifier si la documentation est encore à jour

**Stack technique :** Python, Typer, Rich, OpenAI SDK, stockage JSON

> NARRATION : Notre application de démonstration est un générateur de documentation. Vous le pointez vers un fichier source, il lit le code, l'envoie à un LLM et produit une documentation en markdown. Il peut aussi lister ce qui a été documenté et vérifier si la documentation est encore exacte quand le code change.

---

## Vue d'ensemble de l'architecture

```
main.py
  |
  v
commands/__init__.py
  |
  +-- generate.py
  +-- list.py
  +-- check.py
  +-- update.py
  |
  +-- llm.py        (OpenAI SDK)
  +-- storage.py    (persistance JSON)
  +-- display.py    (sortie terminal Rich)
```

> NARRATION : L'architecture suit une séparation claire des responsabilités. Le point d'entrée dirige vers les fichiers de commandes individuels. Chaque commande utilise trois modules partagés : llm.py pour les appels LLM, storage.py pour la persistance et display.py pour la sortie terminal. C'est le même pattern que vous retrouverez dans beaucoup d'applications CLI.

---

## CLAUDE.md : Le contexte de votre projet

**Ce que contient CLAUDE.md :**

- Stack technique et dépendances
- Carte de l'architecture
- Modèles de données et schémas
- Commandes de développement (`run`, `test`, `lint`)
- Règles et conventions

**Point clé :** Toujours chargé dans chaque conversation -- c'est le cerveau de votre projet.

> NARRATION : CLAUDE.md est un fichier spécial que Claude Code lit au début de chaque conversation. Il donne à Claude le contexte de votre projet -- la stack technique, l'architecture, le flux de données et les règles. Voyez-le comme la documentation que Claude a toujours en tête. Regardons le nôtre.

---

## Démo live : Utilisation de l'application

```bash
# Générer la documentation d'un fichier
docgen generate src/docgen/models.py
# --> crée docs/models.md

# Lister tous les fichiers documentés
docgen list
# --> affiche un tableau des fichiers documentés

# Vérifier si la documentation est encore exacte
docgen check src/docgen/models.py
# --> rapporte le statut d'exactitude
```

> NARRATION : Voyons l'application en action. D'abord je génère la documentation pour notre fichier models -- regardez l'appel LLM se produire. Maintenant listons ce que nous avons documenté. Et enfin, vérifions si la documentation est encore exacte. Chacune de ces commandes suit le même pattern : valider l'entrée, appeler le LLM si nécessaire, mettre à jour le stockage, afficher les résultats.

---

## Qu'est-ce que les Skills ?

- **Skills = jeux d'instructions réutilisables** pour des workflows spécifiques
- Stockés dans `.claude/skills/<nom>/SKILL.md`
- **Chargés à la demande** -- PAS toujours dans le contexte
- Voyez-les comme des **"playbooks"** pour des tâches spécifiques

> NARRATION : Les skills sont des fichiers markdown qui définissent comment Claude doit gérer des tâches spécifiques. Contrairement à CLAUDE.md qui est toujours chargé, les skills sont chargés à la demande -- uniquement quand la tâche correspond. Cela garde votre contexte propre. Vous ne chargez que les instructions dont vous avez besoin, quand vous en avez besoin.

---

## Skills vs CLAUDE.md

| | **CLAUDE.md** | **Skills** |
|---|---|---|
| **Chargement** | Toujours | À la demande |
| **Portée** | Contexte projet global | Workflows spécifiques à une tâche |
| **Répond à** | "Qu'est-ce que ce projet ?" | "Comment je fais cette tâche spécifique ?" |

> NARRATION : Voici la distinction clé. CLAUDE.md répond à "qu'est-ce que ce projet ?" -- il est toujours là. Les skills répondent à "comment je fais cette tâche spécifique ?" -- ils ne sont chargés que quand c'est pertinent. Si une convention s'applique à chaque conversation, mettez-la dans CLAUDE.md. Si c'est un workflow spécifique, faites-en un skill.

---

## Anatomie d'un fichier SKILL.md

```
1. Nom & Description          --> Quand déclencher
2. Workflow                    --> Instructions étape par étape
3. Exemples de code            --> Patterns CORRECT vs INCORRECT
4. Conventions & Checklist     --> Validation finale
```

**Flux :** Déclenchement --> Workflow --> Validation

> NARRATION : Chaque skill suit cette structure. La description indique à Claude quand l'utiliser. Le workflow donne des instructions étape par étape. Les exemples de code montrent exactement quels patterns suivre -- les bons comme les mauvais exemples. Et la checklist s'assure que rien n'est oublié. Regardons un vrai exemple.

---

## Méthodologie : Créer un Skill

1. **Identifier** la tâche répétitive
2. **Définir** les conditions de déclenchement
3. **Écrire** le workflow étape par étape
4. **Ajouter des exemples de code** avec les patterns CORRECT / INCORRECT
5. **Ajouter une checklist de conventions**
6. **Tester** en demandant à Claude de l'utiliser

> NARRATION : C'est la méthodologie que vous suivrez dans l'exercice 1. Commencez par identifier quelle tâche vous codifiez. Puis définissez quand Claude doit utiliser ce skill. Écrivez le workflow. Ajoutez des exemples de code concrets -- Claude fonctionne très bien quand vous lui montrez exactement le pattern que vous voulez. Ajoutez une checklist. Et enfin, testez-le. Ce processus fonctionne pour n'importe quel skill.

---

## Parcours détaillé : Skill `generating-documentation`

**Fichier :** `.claude/skills/generating-documentation/SKILL.md`

**Points clés :**

- Utilisation du module LLM (correct vs incorrect)
- Pattern de prompt engineering
- Conventions de gestion d'erreurs
- Flux de mise à jour du stockage
- Checklist de conventions

> NARRATION : Ouvrons notre skill pré-construit et parcourons-le. Remarquez à quel point les exemples de code sont spécifiques -- nous montrons exactement comment appeler le module LLM et exactement ce qu'il ne faut PAS faire. Nous définissons le pattern de prompt engineering. Nous spécifions la gestion d'erreurs. Et nous avons une checklist à la fin. C'est ce niveau de détail qui rend les skills efficaces.

---

## Exercice 1 : Créer un Skill

### Créer le skill `reviewing-documentation`

**Durée :** 10-12 minutes

- **Template :** `exercises/exercise-1-template-SKILL.md`
- **Bonne référence :** `generate.py` (suit toutes les conventions)
- **Mauvaise référence :** `update.py` (enfreint les conventions -- votre skill devrait détecter ces problèmes)

> NARRATION : À votre tour. Vous allez créer un skill pour la revue de qualité du code. J'ai fourni un template avec la structure -- vous devez remplir le contenu. Regardez generate.py comme la référence de ce que le bon code doit être, et update.py pour tout ce que votre skill doit détecter. Suivez le guide de l'exercice étape par étape.

---

## Pourquoi des Sub-agents ?

**Problème :** L'agent principal fait tout --> remplit la fenêtre de contexte, devient lent

**Solution :** Déléguer à des sub-agents spécialisés

```
Agent Principal
  |
  +-- dispatche --> doc-reviewer   --> résultats en retour
  +-- dispatche --> doc-generator  --> résultats en retour
```

> NARRATION : Jusqu'ici, nous avons travaillé avec l'agent principal qui fait tout. Mais pour les projets plus importants, cela remplit vite la fenêtre de contexte. Les sub-agents résolvent ce problème -- ce sont des travailleurs spécialisés qui fonctionnent dans leur propre contexte. L'agent principal les dispatche, ils font leur travail et renvoient les résultats. Beaucoup plus efficace.

---

## Sub-agents : Concepts clés

1. Les sub-agents **n'héritent PAS** des skills du parent
2. Vous devez **assigner explicitement** les skills
3. Vous **contrôlez quels outils** chaque agent reçoit
4. Le SKILL.md entier est **chargé quand l'agent est dispatché**

> NARRATION : Point critique -- les sub-agents ne reçoivent pas automatiquement les skills du parent. Vous devez être explicite. Pareil pour les outils -- vous choisissez exactement quels outils chaque agent peut utiliser. Quand un agent est dispatché, ses skills assignés sont entièrement chargés dans son contexte. Cela vous donne un contrôle précis sur ce que chaque agent peut faire.

---

## Principe du moindre privilège

| **doc-reviewer** | **doc-generator** |
|---|---|
| Read, Glob, Grep | Read, Write, Edit, Bash, Glob, Grep |
| "Peut regarder, ne peut pas toucher" | "Peut regarder ET modifier" |

**Point clé :** Ne donnez à chaque agent que les permissions dont il a besoin.

> NARRATION : C'est le principe du moindre privilège appliqué aux agents IA. Notre reviewer ne peut que lire les fichiers -- il rapporte les problèmes mais ne peut rien modifier. Notre generator peut lire ET écrire -- il doit créer des fichiers de documentation. Aucun agent n'a plus de pouvoir que nécessaire. C'est une bonne pratique pour tout système, IA ou non.

---

## Créer un agent : `/agents`

**Étapes :**

1. `/agents` --> Create new --> Project
2. Choisir **Manual configuration**
3. Configurer chaque champ :
   - **name** -- Identifiant de l'agent
   - **prompt** -- Personnalité et rôle
   - **description** -- Quand le dispatcher
   - **tools** -- Capacités autorisées
   - **model** -- Quel modèle Claude
   - **color** -- Couleur d'affichage dans le terminal
   - **skills** -- Fichiers SKILL.md assignés

> NARRATION : Créer un agent est simple. Utilisez la commande /agents, choisissez manual configuration pour voir chaque champ. Vous définirez un nom, écrirez un prompt qui définit la personnalité de l'agent, choisirez les outils et assignerez les skills. Laissez-moi vous montrer le processus.

---

## Prompt de l'agent vs Skill

| | **Prompt** | **Skill** |
|---|---|---|
| **Objectif** | Personnalité et rôle de l'agent | Workflow et conventions spécifiques |
| **Portée** | Générique, réutilisable | Détaillé, spécifique à une tâche |
| **Définit** | QUI est l'agent | COMMENT il fait les tâches |

**Ensemble = Comportement puissant et prévisible**

> NARRATION : Voyez le prompt comme la personnalité de l'agent -- il définit QUI est l'agent. Le skill définit COMMENT il fait des tâches spécifiques. Le prompt peut être assez générique pour être réutilisé entre projets. Le skill fournit les conventions spécifiques au projet. Ensemble, ils vous donnent un comportement prévisible et de haute qualité.

---

## Exercice 2 : Créer des Sub-agents

### Créer deux sub-agents avec des permissions différentes

**Durée :** 10-12 minutes

| Agent | Tools | Skill |
|---|---|---|
| `doc-reviewer` | Read, Glob, Grep | `reviewing-documentation` |
| `doc-generator` | Read, Write, Edit, Bash, Glob, Grep | `generating-documentation` |

> NARRATION : C'est l'heure de l'exercice 2. Vous allez créer les deux sub-agents en utilisant la commande /agents. Faites bien attention aux outils que vous donnez à chacun. Le reviewer reçoit des outils en lecture seule. Le generator reçoit des outils en lecture-écriture. N'oubliez pas d'ajouter le champ skills après avoir créé chaque agent. Suivez le guide de l'exercice.

---

## Déclencher des Sub-agents

**Comment déclencher :** Demandez naturellement !

```
"Use the doc-reviewer to review update.py"
```

1. Claude dispatche l'agent avec ses skills et outils
2. L'agent travaille dans son propre contexte
3. Renvoie les résultats à l'agent principal

> NARRATION : Déclencher un sub-agent est aussi simple que de demander. Dites "use the doc-reviewer to review update.py" et Claude le dispatche. L'agent fonctionne dans sa propre fenêtre de contexte avec ses skills assignés chargés. Quand c'est fini, les résultats reviennent à l'agent principal. Le langage naturel est tout ce dont vous avez besoin.

---

## Démo : Revue de la mauvaise commande

**Commande :** "Use the doc-reviewer to review update.py"

**Problèmes attendus :**

- Pas d'annotations de type
- `print()` au lieu du module `display`
- Mauvais codes de sortie
- Pas de validation des entrées
- Appels LLM en ligne (n'utilise pas `llm.py`)
- Manipulation directe du stockage (n'utilise pas `storage.py`)
- Docstring manquant

> NARRATION : Voyons le reviewer en action. Je vais lui demander de revoir notre commande update.py intentionnellement mauvaise. Regardez le sub-agent être dispatché... et voici le rapport. Il a trouvé tous les problèmes -- pas d'annotations de type, utilisation de print au lieu de display, mauvais codes de sortie. C'est exactement ce que notre skill lui a dit de vérifier.

---

## Démo : Correction basée sur la revue

**Flux :** L'agent principal lit le résultat de la revue --> applique les corrections

**Avant / Après :**

- `print()` --> `display.info()`, `display.error()`
- Pas de types --> Annotations de type complètes
- `sys.exit(1)` --> `raise typer.Exit(code=1)`
- LLM en ligne --> `llm.generate_documentation()`
- JSON brut --> `storage.save_entry()`

> NARRATION : Maintenant l'agent principal prend le rapport du reviewer et corrige chaque problème. Regardez comment il ajoute les annotations de type, remplace print par les méthodes display, corrige les codes de sortie, ajoute la validation. L'agent principal n'a pas besoin du skill de revue chargé -- il utilise simplement le résultat.

---

## Démo : Génération de documentation

**Commande :** "Use the doc-generator to generate docs for storage.py"

**Ce qui se passe :**

1. L'agent lit `src/docgen/storage.py`
2. Appelle le LLM via le module `llm.py`
3. Écrit `docs/storage.md`
4. Met à jour l'entrée de stockage
5. Vérification : `docgen list` montre la nouvelle entrée

> NARRATION : Utilisons maintenant notre generator. Je lui demande de documenter storage.py. L'agent lit le fichier, appelle le LLM via notre module llm.py, écrit le markdown dans docs/storage.md et met à jour l'entrée de stockage. Vérifions avec docgen list -- le voilà.

---

## Exercice 3 : Déclencher et tester

### Mettez vos agents au travail !

**Durée :** 10-12 minutes

1. Revoir `update.py` avec `doc-reviewer`
2. Corriger les problèmes avec l'agent principal
3. Générer la documentation avec `doc-generator`
4. Vérifier avec `docgen list`

**Bonus :** Ajouter une commande `summarize` et exécuter les deux agents dessus

> NARRATION : Dernier exercice. Vous allez déclencher les deux agents vous-même. Commencez par faire revoir update.py par le reviewer. Puis corrigez les problèmes. Ensuite générez la documentation pour un fichier. Et vérifiez que tout fonctionne avec docgen list. Si vous finissez en avance, essayez le bonus -- ajoutez une nouvelle commande et exécutez les deux agents dessus.

---

## Ce que nous avons construit

- Une **application CLI** fonctionnelle avec intégration LLM
- **2 skills :** génération et revue de documentation
- **2 sub-agents :** generator (lecture-écriture) et reviewer (lecture seule)
- Un workflow complet **revue --> correction --> génération**

> NARRATION : Récapitulons ce que nous avons construit aujourd'hui. Une vraie application CLI qui appelle un LLM. Deux skills qui codifient nos workflows. Deux sub-agents avec des permissions différentes. Et nous avons vu comment les orchestrer -- revoir le code, corriger les problèmes, générer la documentation. Ces patterns fonctionnent à l'échelle de n'importe quel projet.

---

## Points clés à retenir

1. **Skills** = workflows prévisibles pour des tâches spécifiques
2. **Sub-agents** = travailleurs spécialisés avec des permissions contrôlées
3. **CLAUDE.md** = contexte projet, toujours disponible
4. **Le principe du moindre privilège** s'applique aussi aux agents IA

> NARRATION : Quatre choses à retenir. Les skills vous donnent des workflows prévisibles. Les sub-agents vous donnent des travailleurs spécialisés avec des permissions contrôlées. CLAUDE.md est le contexte toujours actif de votre projet. Et tout comme pour le contrôle d'accès humain, ne donnez aux agents IA que les permissions dont ils ont besoin. Ces principes fonctionnent pour n'importe quel projet.

---

## Prochaines étapes

**Créez des skills pour VOS projets Generix :**

- Skill de déploiement
- Skill de revue de code
- Skill de testing

**Partagez avec votre équipe :**

- Niveau projet : `.claude/skills/` dans votre repo
- Niveau utilisateur : `~/.claude/skills/` pour vos workflows personnels

**Ressources :** Documentation Claude Code, commandes `/skills` et `/agents`

> NARRATION : Et après ? Ramenez ces patterns dans vos propres projets. Réfléchissez aux workflows que vous répétez -- ce sont des candidats pour des skills. Partagez les skills avec votre équipe via le dossier .claude du projet. Expérimentez avec les sub-agents pour différents rôles. Les commandes /skills et /agents sont vos points de départ. Merci !
