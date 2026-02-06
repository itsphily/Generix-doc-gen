import typer
import json
import hashlib
from pathlib import Path

app = typer.Typer()


@app.command()
def update(source_file, output_dir="docs"):
    # no docstring

    # BAD: using print() instead of display methods
    print("Updating docs for " + source_file)

    path = Path(source_file)

    # BAD: no input validation -- no check if file exists
    source_code = path.read_text()

    # BAD: inline LLM call instead of using llm.py module
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate docs."},
            {"role": "user", "content": source_code},
        ],
    )
    docs = response.choices[0].message.content

    # BAD: no error handling around file operations
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    doc_path = output_path / (path.stem + ".md")
    doc_path.write_text(docs)

    # BAD: directly manipulating storage instead of using storage module
    from docgen.storage import STORAGE_PATH, _ensure_storage_exists
    _ensure_storage_exists()
    data = json.loads(STORAGE_PATH.read_text())
    found = False
    for entry in data["entries"]:
        if entry["source_file"] == source_file:
            entry["status"] = "current"
            entry["source_hash"] = hashlib.sha256(source_code.encode()).hexdigest()
            found = True
    if not found:
        data["entries"].append({
            "source_file": source_file,
            "doc_file": str(doc_path),
            "status": "current",
            "generated_at": "unknown",
            "source_hash": hashlib.sha256(source_code.encode()).hexdigest(),
        })
    STORAGE_PATH.write_text(json.dumps(data))

    # BAD: wrong exit code (using 1 for success)
    print("Done!")
    raise typer.Exit(1)
