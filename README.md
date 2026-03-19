CS 575 Repository

Michael A. Goodrich  
Brigham Young University  

---

### Quick Start

1. Clone the repo in VS Code.
2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\\Scripts\\activate  # Windows PowerShell
```

3. Install dependencies for development (pytest, mypy):

```bash
pip install -e ".[dev]"
```

4. Install `graphviz` (needed by `pydot` for plotting):

```bash
# macOS
brew install graphviz
# Windows (PowerShell)
winget install -e --id Graphviz.Graphviz
```

This installs the `graphviz` python module globally on your computer, in contrast to the other python modules that are installed only within the virtual environment. If you are using Windows (PowerShell), you'll probably need to update the path inside VSCode so that it can find the `graphviz` module. Use an AI assistant for instructions on how to update the path.

5. Select the Python interpreter in VS Code: Command Palette → `Python: Select Interpreter` → pick `.venv`.

---

### Base vs ML Dependencies

- Base dependencies (NumPy, Pandas, NetworkX, Matplotlib, SciPy, pydot, ipykernel) install automatically.
- ML extras (installed later when needed): PyTorch, Torch Geometric, Gensim, and scikit-learn.

Install ML extras when we reach those topics:

```bash
pip install -e ".[ml]"
```

Note: Torch Geometric wheels depend on your installed PyTorch version. If you hit issues, install `torch` first, then `torch-geometric`. CPU-only builds are fine for this course.

---

### Running Tests

- Configure tests: Command Palette → `Python: Configure Tests` → `pytest` → choose `tests`.
- Or run from terminal:

```bash
pytest tests
```

---

### Branch Workflow

This repository has two main branches:

- **`master`** (student-facing): The primary branch for students. This is the branch you should work from and pull updates from throughout the semester. The instructor will periodically merge stable, tested changes here.

- **`instructor-branch`**: A staging branch used by the instructor for development and testing. **Students should ignore this branch.** Changes are tested here before being merged to `master`.

**Student update pattern** (use this to stay current):

```bash
git switch master
git pull origin master
```

**Instructor release pattern**:

```bash
git switch instructor-branch
# develop and commit changes
git push origin instructor-branch
git switch master
git merge instructor-branch
git push origin master
```

Keep releases small and frequent so students can pull cleanly; resolve conflicts on `instructor-branch` before merging to `master`.

---

### Project Structure

```
.
├── src/
│   ├── network_utilities.py
│   ├── plotting_utilities.py
│   └── plotting_utilities_for_movie_database.py
├── tests/
│   └── test_graph_construction/
│       ├── test_vertex_edge_sets.py
│       ├── test_adjacency_list.py
│       └── test_adjacency_matrix.py
│   └── test_homework_1/     # ignore this folder for now
├── notebooks/
│   └── sequence_of_Jupyter_notebook_tutorials.ipynb
├── data/           # large datasets (ignored)
├── pyproject.toml
├── README.md
└── .gitignore
```
- `src/network_utilities.py`: graph creation and validation utilities.
- `src/plotting_utilities.py`: graph plotting helpers (show_* functions).
- `src/plotting_utilities_for_movie_database.py`: plotting helpers used by the movie knowledge graph notebook.
- `notebooks`: Jupyter notebooks for demos and assignments.
- `tests/test_graph_construction/`: pytest-based tests for graph construction utilities.
- `data`: tracked folder with `.gitkeep`; contents are ignored by Git.

---

### Notes and Tips

- Avoid `pygraphviz` on macOS; use `pydot` with `graphviz` installed.
- If you're using conda, deactivate it before activating `.venv`.
- To deactivate the virtual environment: `deactivate`.

See [pyproject.toml](pyproject.toml) for dependency details and extras.