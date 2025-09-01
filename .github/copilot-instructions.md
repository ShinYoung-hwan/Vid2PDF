
# Copilot Instructions for Vid2PDF

## Project Overview
- **Vid2PDF** is a modular Python CLI tool that converts videos into summary PDFs by detecting scene changes and extracting keyframes.
- The codebase is organized for extensibility: scene extraction and PDF generation are pluggable via dedicated modules.

## Architecture & Key Files
- `main.py`: CLI entry point. Handles argument parsing, workflow orchestration, and delegates to extractor/generator modules.
- `scene_extractors/`: Scene extraction algorithms. Each extractor implements the `SceneExtractor` interface (`base.py`).
    - Example: `content_scene_extractor.py` (default, uses PySceneDetect's ContentDetector)
- `pdf_generators/`: PDF generation backends. Each generator implements the `PDFGenerator` interface (`base.py`).
    - Example: `img2pdf_gen.py` (default, uses img2pdf)
- `videos/`: Input video files (e.g., `.mp4`).
- `pdfs/`: Output PDFs are saved here by default.
- `README.md`: Usage, structure, and extension documentation.

## Developer Workflow
1. **Install dependencies**:
   ```bash
   pip install "scenedetect[opencv]" img2pdf
   ```
2. **Run the CLI**:
   ```bash
   python main.py -i videos/example.mp4
   # Optional: -o pdfs/output.pdf  # Output folder or file
   # Optional: -t 20.0             # Scene detection threshold
   ```
3. **Output**: PDF named `[input_basename]_summary.pdf` in `pdfs/` by default.

## Extensibility Patterns
- **Scene Extraction**: Add a new extractor in `scene_extractors/`, subclassing `SceneExtractor`. Register/import in `main.py` to use.
- **PDF Generation**: Add a new generator in `pdf_generators/`, subclassing `PDFGenerator`. Register/import in `main.py` to use.
- All processing is local; no external APIs or services are called.

## Conventions & Patterns
- Logging: Uses Python logging at INFO level for progress and errors.
- CLI options and defaults are documented in `main.py` (Korean comments).
- Output PDF naming: `[input_basename]_summary.pdf` in `pdfs/` unless otherwise specified.
- Temporary files are managed in a temp directory and always cleaned up.
- No test suite or CI/CD as of this writing.

## Examples
- Convert a video:
  ```bash
  python main.py -i videos/startup_01-01.mp4
  ```
- Custom output and threshold:
  ```bash
  python main.py -i videos/foo.mp4 -o pdfs -t 18.5
  ```

## Quick Reference
- **Dependencies**: `scenedetect[opencv]`, `img2pdf`
- **Entrypoint**: `main.py`
- **Input**: `.mp4` files in `videos/`
- **Output**: PDF in `pdfs/`

---
If you add new features or change workflows, update this file to keep AI agents productive.
