# Copilot Instructions for Vid2PDF

## Project Overview
- **Vid2PDF** is a Python script that converts a video into a PDF by detecting scene changes and saving keyframes as PDF pages.
- The main logic is in `main.py`. There are no submodules or complex service boundaries; the script is monolithic and CLI-driven.

## Key Files & Structure
- `main.py`: Entry point. Handles argument parsing, scene detection, image extraction, and PDF creation.
- `videos/`: Place input `.mp4` files here. Output PDFs are generated in the project root by default.
- `README.md`: Brief project description.

## Core Workflow
1. **Install dependencies**:
   ```bash
   pip install "scenedetect[opencv]" img2pdf
   ```
2. **Run the script**:
   ```bash
   python main.py -i videos/example.mp4
   ```
   - Optional: `-o output.pdf` to specify output path.
   - Optional: `-t 20.0` to adjust scene detection threshold.
3. **Output**: PDF named `[input]_summary.pdf` by default, or as specified.

## Scene Detection & PDF Generation
- Uses `scenedetect` (with OpenCV) for content-based scene change detection.
- Extracts one keyframe per detected scene using `save_images`.
- Converts extracted images to PDF using `img2pdf`.
- Temporary files are managed in a temp directory and cleaned up automatically.

## Conventions & Patterns
- Logging is set to `INFO` level; errors and progress are logged to console.
- All CLI options and defaults are documented in `main.py` (in Korean).
- Output PDF naming: `[input_basename]_summary.pdf` if not specified.
- No test suite or CI/CD is present as of this writing.

## Integration & Extensibility
- No external APIs or services are called; all processing is local.
- To add new video formats, update the input handling in `main.py`.
- To change PDF layout or add metadata, modify the `create_pdf_from_images` function.

## Examples
- Convert a video:
  ```bash
  python main.py -i videos/startup_01-01.mp4
  ```
- Custom output and threshold:
  ```bash
  python main.py -i videos/foo.mp4 -o result.pdf -t 18.5
  ```

## Quick Reference
- **Dependencies**: `scenedetect[opencv]`, `img2pdf`
- **Entrypoint**: `main.py`
- **Input**: `.mp4` files in `videos/`
- **Output**: PDF in `pdfs/`

---
If you add new features or change workflows, update this file to keep AI agents productive.
