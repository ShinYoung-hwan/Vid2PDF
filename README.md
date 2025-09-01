# Vid2PDF

**Vid2PDF**는 동영상 파일에서 장면 전환을 감지하여, 각 장면의 대표 이미지를 추출하고 이를 PDF로 변환하는 Python 기반 도구입니다.  
알고리즘 및 PDF 생성 방식을 모듈화하여, 다양한 추출/생성 방식을 쉽게 확장할 수 있습니다.

---

## 주요 기능

- 동영상(.mp4 등)에서 장면 전환 자동 감지
- 각 장면의 대표 이미지 추출
- 추출된 이미지를 PDF로 변환
- 추출/생성 알고리즘을 모듈화하여 손쉽게 교체 및 확장 가능

---

## 폴더 구조

```
Vid2PDF/
├── main.py                # 메인 실행 파일 (CLI)
├── scene_extractors/      # 장면 추출 알고리즘 모듈
│   ├── base.py            # 추상 SceneExtractor 클래스
│   └── contentSceneExtractor.py  # ContentDetector 기반 구현
├── pdf_generators/        # PDF 생성 모듈
│   ├── base.py            # 추상 PDFGenerator 클래스
│   └── img2pdf_gen.py     # img2pdf 기반 구현
├── videos/                # 입력 동영상 파일 폴더
├── pdfs/                  # 생성된 PDF 저장 폴더
└── README.md
```

---

## 설치

```bash
pip install "scenedetect[opencv]" img2pdf
```

---

## 사용법

```bash
python main.py -i videos/your_video.mp4
```

- `-i, --input`: 입력 동영상 파일 경로 (필수)
- `-o, --output`: 출력 PDF 파일 경로 (생략 시 `pdfs/`)
- `-t, --threshold`: 장면 감지 민감도 (기본값: 27.0, 낮을수록 민감)

예시:
```bash
python main.py -i videos/sample.mp4 -o pdfs/result.pdf -t 20.0
```

---

## 확장성

- **장면 추출 알고리즘 추가**: `scene_extractors/`에 새로운 클래스를 추가하고, `base.py`의 `SceneExtractor`를 상속받아 구현
- **PDF 생성 방식 추가**: `pdf_generators/`에 새로운 클래스를 추가하고, `base.py`의 `PDFGenerator`를 상속받아 구현
- `main.py`에서 원하는 구현체를 import하여 사용

---

## 예시

```bash
python main.py -i videos/startup_01-01.mp4
python main.py -i videos/foo.mp4 -o result.pdf -t 18.5
```

---

## 기여 및 참고

- PySceneDetect, img2pdf 등 오픈소스 라이브러리 사용
- 추가 알고리즘/기능 기여 환영

---

**문의/이슈**: GitHub Issue 등록