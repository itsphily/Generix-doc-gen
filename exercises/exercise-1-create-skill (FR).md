# Exercice 1 : Créer un fichier SKILL.md

**Durée :** 10-12 minutes
**Objectif :** Créer le skill `reviewing-documentation` qui apprend à Claude Code comment revoir les commandes CLI de `docgen` pour la qualité du code et le respect des conventions.

---

## Contexte

Les skills sont des fichiers d'instructions en markdown qui donnent à Claude Code des connaissances spécifiques à un domaine. Quand un skill est chargé, Claude lit le fichier SKILL.md et suit ses instructions précisément. Dans cet exercice, vous allez créer un skill qui transforme Claude en expert de la revue de code pour le projet `docgen`.

Vous utiliserez deux références tout au long de cet exercice :
- **`generate.py`** — la commande "référence" qui suit correctement toutes les conventions
- **`update.py`** — le "mauvais exemple" qui enfreint de nombreuses conventions (c'est ce que le reviewer doit détecter)

Ouvrez les deux fichiers maintenant et gardez-les visibles. Comprendre la différence entre eux est la clé pour écrire un bon skill.

---

## Étape 1 : Copier le template

Ouvrez le fichier template à `exercises/exercise-1-template-SKILL.md` et copiez-le à l'emplacement du skill :

```
.claude/skills/reviewing-documentation/SKILL.md
```

Créez l'arborescence de répertoires si elle n'existe pas.

> **Astuce :** Vous pouvez le faire depuis le terminal :
> ```bash
> mkdir -p .claude/skills/reviewing-documentation
> cp exercises/exercise-1-template-SKILL.md .claude/skills/reviewing-documentation/SKILL.md
> ```

---

## Étape 2 : Écrire la section Description

Ouvrez votre nouveau fichier `SKILL.md` et remplissez la section **Description**. Elle indique à Claude CE QUE fait le skill et QUAND il doit s'activer.

Votre description doit couvrir :
- **Ce qu'il fait :** Revoit les fichiers de commandes CLI et la documentation générée pour la qualité du code, le respect des conventions et les bonnes pratiques
- **Quand il se déclenche :** Quand l'utilisateur demande de revoir du code, vérifier la qualité, auditer une commande, valider les bonnes pratiques ou inspecter la documentation

> **Astuce :** Pensez aux différentes façons dont un utilisateur pourrait formuler une demande de revue. Incluez des expressions déclencheurs comme "review", "check", "audit", "validate", "inspect quality" et "look for issues". Plus vous incluez d'expressions, plus Claude chargera ce skill de manière fiable quand nécessaire.

Exemple de structure :
```markdown
## Description

This skill reviews `docgen` CLI command files for code quality and convention adherence.
It activates when the user asks to [lister les scénarios déclencheurs ici].

The reviewer checks against a comprehensive checklist covering type annotations,
module usage, error handling, and project conventions.
```

---

## Étape 3 : Compléter le Workflow

Remplissez la section **Workflow** avec ces 4 étapes. Chaque étape doit décrire ce que Claude fait et pourquoi.

### Étape 1 — Lire les fichiers cibles
Lire le(s) fichier(s) que l'utilisateur souhaite faire revoir. Comprendre l'objectif de la commande, ses arguments et son flux logique.

### Étape 2 — Lire les fichiers de référence
Lire les modules principaux du projet pour comprendre les patterns établis :
- `display.py` — comment la sortie doit être formatée (messages success, error, warning, info)
- `constants.py` — quels codes de sortie et constantes sont disponibles
- `llm.py` — comment les appels LLM doivent être faits
- `generate.py` — la commande de référence qui suit toutes les conventions

### Étape 3 — Vérifier par rapport à la checklist
Comparer le fichier cible avec chaque élément de la Code Quality Checklist (que vous allez écrire à l'étape suivante). Signaler chaque violation avec un niveau de sévérité.

### Étape 4 — Rapporter les résultats
Formater les résultats selon le format spécifié dans la section Output Format.

> **Astuce :** Soyez explicite sur les fichiers à lire. Claude est plus performant quand vous lui donnez des chemins de fichiers exacts plutôt que des instructions vagues comme "read the relevant files."

---

## Étape 4 : Remplir la Code Quality Checklist

C'est la section la plus importante du skill. Pour chaque catégorie, fournissez un exemple CORRECT et un exemple INCORRECT. Claude utilise ces exemples concrets pour identifier les violations.

### Catégorie 1 : Annotations de type

Tous les paramètres CLI doivent utiliser `Annotated` avec `typer.Argument` ou `typer.Option` et inclure une chaîne `help`.

**CORRECT :**
```python
def generate(
    path: Annotated[str, typer.Argument(help="Path to the source file to document")],
    output: Annotated[str, typer.Option(help="Output directory for documentation")] = "docs",
):
```

**INCORRECT :**
```python
def generate(path: str, output: str = "docs"):
```

> **Astuce :** Regardez comment `generate.py` déclare ses paramètres par rapport à `update.py`. La différence est le wrapper `Annotated` avec le texte d'aide.

---

### Catégorie 2 : Module Display

Toute sortie destinée à l'utilisateur doit passer par le module `display`, jamais par un `print()` brut.

**CORRECT :**
```python
display.success("Documentation generated successfully")
display.error("File not found")
display.warning("No changes detected")
display.info("Processing file...")
```

**INCORRECT :**
```python
print("Documentation generated successfully")
print("Error: File not found")
```

> **Astuce :** Le module `display` fournit un formatage cohérent avec des couleurs, des icônes et un style approprié. Utiliser `print()` casse la cohérence visuelle du CLI.

---

### Catégorie 3 : Codes de sortie

Tous les codes de sortie doivent utiliser des constantes nommées de `constants.py`, jamais des nombres magiques.

**CORRECT :**
```python
from docgen.constants import EXIT_SUCCESS, EXIT_INVALID_INPUT, EXIT_GENERATION_ERROR

raise typer.Exit(EXIT_INVALID_INPUT)
```

**INCORRECT :**
```python
raise typer.Exit(1)
raise typer.Exit(code=2)
```

> **Astuce :** Les codes de sortie nommés rendent le code auto-documenté. Quand vous voyez `EXIT_INVALID_INPUT`, vous savez exactement ce qui s'est passé. Quand vous voyez `1`, vous devez deviner.

---

### Catégorie 4 : Validation des entrées

Tous les arguments de chemin de fichier doivent être validés avant utilisation. Vérifiez que le chemin existe et est du type attendu (fichier vs répertoire).

**CORRECT :**
```python
path = Path(path_str)
if not path.exists():
    display.error(f"Path does not exist: {path}")
    raise typer.Exit(EXIT_INVALID_INPUT)
if not path.is_file():
    display.error(f"Path is not a file: {path}")
    raise typer.Exit(EXIT_INVALID_INPUT)
```

**INCORRECT :**
```python
# Lire directement le fichier sans vérifier s'il existe
content = Path(path_str).read_text()
```

> **Astuce :** Sans validation, l'utilisateur obtient un traceback Python brut au lieu d'un message d'erreur convivial. Regardez `generate.py` pour voir comment il valide les entrées avant de continuer.

---

### Catégorie 5 : Module LLM

Toutes les interactions LLM doivent passer par le module `llm`, jamais en important directement OpenAI ou un autre fournisseur.

**CORRECT :**
```python
from docgen.llm import generate_documentation

result = generate_documentation(source_code, context)
```

**INCORRECT :**
```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

> **Astuce :** Le module `llm` abstrait le fournisseur. Si l'équipe passe d'OpenAI à Anthropic, seul `llm.py` doit changer. Les commandes qui importent OpenAI directement ne fonctionneront plus.

---

### Catégorie 6 : Module Storage

Toutes les métadonnées de documentation doivent être gérées via le module `storage`, jamais en manipulant directement les fichiers JSON.

**CORRECT :**
```python
from docgen.storage import add_entry, get_entries

add_entry(doc_metadata)
entries = get_entries()
```

**INCORRECT :**
```python
import json

with open("docs/index.json", "r") as f:
    data = json.load(f)
data.append(new_entry)
with open("docs/index.json", "w") as f:
    json.dump(data, f)
```

> **Astuce :** La manipulation directe de JSON contourne la validation, les valeurs par défaut et toute migration de schéma future que le module `storage` gère.

---

## Étape 5 : Définir le format de sortie

Remplissez la section **Output Format**. La sortie du reviewer doit être structurée et actionnable.

### Tableau des problèmes

La sortie doit inclure un tableau markdown avec ces colonnes :

| Sévérité | Description | Localisation | Correction suggérée |
|----------|-------------|--------------|---------------------|
| Critical | Utilise `print()` au lieu du module `display` | `update.py`, ligne 23 | Remplacer `print(msg)` par `display.info(msg)` |
| Warning  | Docstring manquant sur la fonction de commande | `update.py`, ligne 10 | Ajouter un docstring décrivant l'objectif de la commande |

- **Critical** — violations qui cassent les conventions ou causent des problèmes à l'exécution
- **Warning** — problèmes de style ou bonnes pratiques manquantes qui devraient être corrigés

### Résumé

Après le tableau, inclure un résumé :
```
## Summary
- Critical issues: X
- Warnings: Y
- Total: Z

### Critical Fixes Required
[Pour chaque problème critique, montrer le changement de code spécifique nécessaire]
```

> **Astuce :** Une sortie structurée facilite l'action pour l'agent principal (ou un humain). La colonne de correction suggérée est particulièrement importante -- elle indique au développeur exactement quoi faire.

---

## Étape 6 : Compléter la Conventions Checklist

Ajoutez une section **Conventions Checklist** avec 10 éléments ou plus. Ce sont des vérifications oui/non que le reviewer parcourt pour chaque fichier.

Écrivez chaque élément comme une affirmation claire et vérifiable :

1. Tous les paramètres CLI utilisent des types `Annotated` avec `typer.Argument()` ou `typer.Option()` et incluent du texte `help`
2. Toute sortie utilisateur utilise le module `display` (`display.success()`, `display.error()`, `display.warning()`, `display.info()`)
3. Aucun appel `print()` brut n'existe dans la commande
4. Tous les codes de sortie utilisent des constantes nommées de `constants.py` (ex. `EXIT_SUCCESS`, `EXIT_INVALID_INPUT`)
5. Aucun nombre magique n'est utilisé pour les codes de sortie
6. Toutes les entrées de chemin de fichier sont validées (vérification d'existence, vérification de type) avant utilisation
7. Les messages d'erreur sont conviviaux et suggèrent les prochaines étapes
8. La fonction de commande a un docstring expliquant son objectif
9. Les interactions LLM utilisent le module `llm`, pas d'imports directs du fournisseur
10. Les opérations de stockage utilisent le module `storage`, pas de manipulation directe de JSON
11. Les imports sont organisés : bibliothèque standard, tiers, modules locaux
12. La commande suit la même structure que `generate.py` (valider, traiter, afficher, quitter)

> **Astuce :** Pensez à ce qui rend `generate.py` bon et `update.py` mauvais. Chaque différence entre ces deux fichiers est un élément potentiel de la checklist.

---

## Étape 7 : Vérifier votre Skill

Ouvrez Claude Code et exécutez la commande `/skills`. Vous devriez voir `reviewing-documentation` listé comme skill disponible.

S'il n'apparaît pas :
- Vérifiez que le fichier est exactement à `.claude/skills/reviewing-documentation/SKILL.md`
- Assurez-vous que le fichier est du markdown valide
- Fermez et rouvrez Claude Code pour recharger les skills

---

## Critères de réussite

Vous avez terminé cet exercice quand :
- [ ] Le fichier SKILL.md existe à `.claude/skills/reviewing-documentation/SKILL.md`
- [ ] La section Description explique ce que fait le skill et quand il se déclenche
- [ ] La section Workflow a 4 étapes claires
- [ ] La Code Quality Checklist a 6 catégories, chacune avec des exemples CORRECT et INCORRECT
- [ ] Le Output Format définit la structure du tableau de problèmes et le format du résumé
- [ ] La Conventions Checklist a 10+ éléments vérifiables
- [ ] Le skill apparaît quand vous exécutez `/skills` dans Claude Code
