import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_report_docx(output_path):
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Assignment 01: Git-Based Collaboration for an ML Project")
    run.font.name = 'Arial'
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = RGBColor(31, 78, 121)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s_run = sub.add_run("Final Collaboration & MLOps Reproducibility Report")
    s_run.font.name = 'Arial'
    s_run.font.size = Pt(14)
    s_run.font.italic = True
    s_run.font.color.rgb = RGBColor(89, 89, 89)

    doc.add_paragraph() # Spacer

    # Section 1: Team & Project Overview
    h1 = doc.add_heading("1. Team Overview & Repository Details", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Repository URL: ").bold = True
    p.add_run("https://github.com/taaibausman/TaZ-dragons-ml-collab\n")
    p.add_run("Team Name: ").bold = True
    p.add_run("TaZ-dragons\n")
    p.add_run("Selected Dataset: ").bold = True
    p.add_run("Titanic Survival Prediction Dataset (UCI / Kaggle tabular dataset)")

    # Team Table
    table = doc.add_table(rows=3, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Member Name", "GitHub Handle", "Assigned Role", "Primary Responsibilities"]
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1F4E79")
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True

    members = [
        ("Zaneeha Afzal", "@zaneehaafzal", "Data & Platform Co-Owner", "DVC data tracking, dataset updates, pre-commit hooks, data checks, notebook pairing"),
        ("Taaiba Usman", "@taaibausman", "Model & Platform Co-Owner", "Training pipeline, hyperparameter configs, GitHub Actions CI, release candidate & tags")
    ]

    for row_idx, data in enumerate(members, start=1):
        row_cells = table.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            if row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F2F2F2")

    doc.add_paragraph()

    # Helper function for Screenshot Placeholders
    def add_screenshot_placeholder(box_title, instruction_text):
        p_box = doc.add_paragraph()
        p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_box = doc.add_table(rows=1, cols=1)
        table_box.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table_box.rows[0].cells[0]
        cell.width = Inches(6.0)
        set_cell_background(cell, "F9FBFD")
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"📷 SCREENSHOT PLACEHOLDER: {box_title}\n\n")
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(31, 78, 121)

        r2 = p.add_run(f"[ PASTE SCREENSHOT HERE ]\n\n{instruction_text}")
        r2.font.italic = True
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(120, 120, 120)
        doc.add_paragraph()

    # Phase 1
    doc.add_heading("2. Phase 1: Team and Repository Setup", level=2)
    p = doc.add_paragraph("Formed a 2-person team ('TaZ-dragons'), created the repository 'TaZ-dragons-ml-collab', configured Git user identities, assigned split platform co-owner roles, and configured branch protection rules on GitHub.")
    add_screenshot_placeholder("Phase 1: GitHub Repository & Collaborators Setup", "Paste screenshot of GitHub repository page showing branches (main, staging, dev) and team collaborators.")

    # Phase 2
    doc.add_heading("3. Phase 2: Project Scaffolding & Initial Import", level=2)
    p = doc.add_paragraph("Established Cookiecutter Data Science layout (configs/, data/, models/, notebooks/, src/, tests/, .github/). Pinned dependencies in requirements.txt & pyproject.toml. Created strict .gitignore excluding datasets and binary models from Git history.")
    add_screenshot_placeholder("Phase 2: Initial Git Commit Log on main", "Paste screenshot of terminal output showing 'git log --oneline main' with initial scaffold commits.")

    # Phase 3
    doc.add_heading("4. Phase 3: Guard Rails (Pre-commit Hooks & Secret Scanning)", level=2)
    p = doc.add_paragraph("Configured .pre-commit-config.yaml with ruff, nbstripout, check-added-large-files (1MB limit), and detect-secrets. Verified that pre-commit intercepts and blocks 2MB files and fake API keys.")
    add_screenshot_placeholder("Phase 3: Pre-Commit Intercepting & Blocking 2MB File", "Paste screenshot of terminal output showing pre-commit blocking 'large_test.bin (2048 KB) exceeds 1000 KB'.")

    # Phase 4
    doc.add_heading("5. Phase 4: Data Versioning with DVC", level=2)
    p = doc.add_paragraph("Initialized DVC, tracked raw dataset 'data/raw/titanic.csv' using DVC pointer 'titanic.csv.dvc', configured local cache remote storage, and opened PR data/initial-dataset -> dev.")
    add_screenshot_placeholder("Phase 4: DVC Tracking Pointer (.dvc) in Git", "Paste screenshot of File Explorer or GitHub PR showing data/raw/titanic.csv.dvc pointer file.")

    # Phase 5
    doc.add_heading("6. Phase 5: Notebooks Done Right", level=2)
    p = doc.add_paragraph("Created exploratory notebook 'notebooks/01-eda.ipynb' paired with Jupytext ('notebooks/01-eda.py'). Extracted reusable feature function 'compute_family_size' into 'src/features.py' with unit test in 'tests/test_features.py'. Enforced nbstripout to strip cell outputs.")
    add_screenshot_placeholder("Phase 5: Clean Jupytext Paired Notebook Diff", "Paste screenshot of GitHub PR diff for 01-eda.ipynb showing clean stripped cell outputs.")

    # Phase 6
    doc.add_heading("7. Phase 6: Reproducible Pipeline", level=2)
    p = doc.add_paragraph("Constructed 3-stage DVC DAG (prepare -> train -> evaluate) defined in dvc.yaml. Centralized seeds (42) and hyperparameters in params.yaml. Executed 'dvc repro' to generate dvc.lock and baseline metrics.json.")
    
    # Baseline Metrics Table
    doc.add_paragraph("Baseline Pipeline Metrics (metrics.json):").runs[0].font.bold = True
    m_table = doc.add_table(rows=2, cols=5)
    m_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_headers = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]
    for i, h in enumerate(m_headers):
        m_table.rows[0].cells[i].text = h
        set_cell_background(m_table.rows[0].cells[i], "1F4E79")
        m_table.rows[0].cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        m_table.rows[0].cells[i].paragraphs[0].runs[0].font.bold = True
    
    vals = ["0.7672", "0.5660", "0.4412", "0.4959", "0.7794"]
    for i, v in enumerate(vals):
        m_table.rows[1].cells[i].text = v
        set_cell_background(m_table.rows[1].cells[i], "F2F2F2")

    doc.add_paragraph()
    add_screenshot_placeholder("Phase 6: Terminal Output of 'dvc repro' Execution", "Paste screenshot of terminal output showing dvc repro running prepare, train, evaluate stages.")

    # Phase 7
    doc.add_heading("8. Phase 7: Experiments & Multi-Member Collaboration", level=2)
    p = doc.add_paragraph("Executed hyperparameter tuning experiments across branches (exp/zaneeha-n-estimators). Compared metrics via 'dvc exp show'. Retained exp/zaneeha-n-estimators as an abandoned experiment branch to document experiment drift. Simulated and resolved a real merge conflict in params.yaml via git rebase dev.")

    # Exp Table
    exp_table = doc.add_table(rows=5, cols=6)
    exp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    e_hdrs = ["Run Name", "Branch", "n_estimators", "Accuracy", "F1 Score", "Status / Result"]
    for i, h in enumerate(e_hdrs):
        exp_table.rows[0].cells[i].text = h
        set_cell_background(exp_table.rows[0].cells[i], "1F4E79")
        exp_table.rows[0].cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        exp_table.rows[0].cells[i].paragraphs[0].runs[0].font.bold = True

    exp_data = [
        ("Baseline", "dev", "100", "0.7672", "0.4874", "Baseline"),
        ("piano-flux", "exp/zaneeha-n-estimators", "50", "0.7634", "0.4918", "Winner (Best F1 & ROC AUC)"),
        ("sheen-jive", "exp/zaneeha-n-estimators", "150", "0.7672", "0.4874", "Evaluated"),
        ("minus-taro", "exp/zaneeha-n-estimators", "250", "0.7672", "0.4874", "Evaluated")
    ]
    for r_idx, row in enumerate(exp_data, start=1):
        for c_idx, val in enumerate(row):
            exp_table.rows[r_idx].cells[c_idx].text = val
            if r_idx % 2 == 1:
                set_cell_background(exp_table.rows[r_idx].cells[c_idx], "F2F2F2")

    doc.add_paragraph()
    add_screenshot_placeholder("Phase 7: 'dvc exp show' Experiment Comparison Table", "Paste screenshot of terminal output showing dvc exp show table.")
    add_screenshot_placeholder("Phase 7: Git Merge Conflict Resolution in params.yaml", "Paste screenshot of GitHub PR or terminal showing Git merge conflict resolved after git rebase dev.")

    # Phase 8
    doc.add_heading("9. Phase 8: Continuous Integration (GitHub Actions)", level=2)
    p = doc.add_paragraph("Added GitHub Actions CI workflow in .github/workflows/ci.yml running on PRs into dev, staging, and main. Automated Ruff linting, Pytest unit tests, Data schema/null checks, and Smoke Training.")
    add_screenshot_placeholder("Phase 8: Failing CI Check (Deliberately Broken Test)", "Paste screenshot of GitHub PR showing red cross 'All checks have failed' blocking PR merge.")
    add_screenshot_placeholder("Phase 8: Passing CI Check Workflow", "Paste screenshot of GitHub Actions tab showing green checkmark 'MLOps CI Pipeline passed'.")

    # Phase 9
    doc.add_heading("10. Phase 9: Production Release & Tagging", level=2)
    p = doc.add_paragraph("Promoted dev -> staging -> main. Performed independent reproducibility verification with 'dvc pull && dvc repro' yielding identical metrics. Tagged production model release 'model-v1.0' on main.")

    # Reproducibility Table
    repro_table = doc.add_table(rows=7, cols=2)
    repro_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    repro_table.rows[0].cells[0].text = "Metric / Artifact Parameter"
    repro_table.rows[0].cells[1].text = "Empirical Value"
    set_cell_background(repro_table.rows[0].cells[0], "1F4E79")
    set_cell_background(repro_table.rows[0].cells[1], "1F4E79")
    repro_table.rows[0].cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    repro_table.rows[0].cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    r_items = [
        ("Release Tag", "model-v1.0"),
        ("Production Commit SHA", "5faae18"),
        ("Data DVC Hash", "74cc1e4c4e7e30ec8a49abf227f5099c"),
        ("Random Seed", "42"),
        ("Final Accuracy", "0.7672"),
        ("Final F1 Score", "0.4959")
    ]
    for r_idx, (k, v) in enumerate(r_items, start=1):
        repro_table.rows[r_idx].cells[0].text = k
        repro_table.rows[r_idx].cells[1].text = v
        if r_idx % 2 == 1:
            set_cell_background(repro_table.rows[r_idx].cells[0], "F2F2F2")
            set_cell_background(repro_table.rows[r_idx].cells[1], "F2F2F2")

    doc.add_paragraph()
    add_screenshot_placeholder("Phase 9: Production Release Tag 'model-v1.0' on GitHub", "Paste screenshot of GitHub Releases/Tags page showing tag model-v1.0.")

    # Retrospective & Contributions
    doc.add_heading("11. Retrospective & Member Contributions", level=1)
    
    doc.add_heading("Team Retrospective", level=2)
    doc.add_paragraph("1. What Broke: Initial pre-commit execution encountered Windows AppLocker policy restrictions on virtual environment binary scripts, which was resolved by invoking modules via 'python -m dvc'. Concurrent hyperparameter tuning on params.yaml required manual merge conflict resolution via git rebase dev.\n2. What We Standardized: Strict Conventional Commits standard across all branches, 3-stage DVC pipeline DAG, and mandatory GitHub Actions CI checks on all pull requests.")

    doc.add_heading("Individual Member Contributions", level=2)
    p_z = doc.add_paragraph()
    p_z.add_run("Zaneeha Afzal (Data & Platform Co-Owner): ").bold = True
    p_z.add_run("Configured pre-commit hooks, set up initial DVC dataset versioning, created Jupytext paired EDA notebook, conducted hyperparameter experiment runs on n_estimators, performed conflict resolution via git rebase, and verified independent end-to-end pipeline reproducibility.")

    p_t = doc.add_paragraph()
    p_t.add_run("Taaiba Usman (Model & Platform Co-Owner): ").bold = True
    p_t.add_run("Designed model training pipeline, structured hyperparameter configurations, built GitHub Actions CI workflow (ci.yml), executed hyperparameter tuning experiments on max_depth, managed release candidates, and created production tag model-v1.0.")

    # Save document
    doc.save(output_path)
    print(f"Successfully generated report Word document at: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.getcwd(), "Assignment01_Git_Based_Collaboration_Report.docx")
    create_report_docx(out_file)
