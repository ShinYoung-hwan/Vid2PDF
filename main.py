import os
import argparse
import tempfile
import shutil
import logging
from scene_extractors.content_scene_extractor import ContentSceneExtractor
from pdf_generators.img2pdf_gen import Img2PDFGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SceneDetectToPDF')

def parse_args():
    parser = argparse.ArgumentParser(
        description="동영상에서 장면 전환을 감지하여 PDF로 변환하는 스크립트"
    )
    parser.add_argument(
        '-i', '--input', 
        type=str, 
        required=True, 
        help="입력 동영상 파일 경로"
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        default="pdfs/",
        help="출력 PDF 폴더 경로. 지정하지 않으면 'pdfs/' 폴더에 저장됩니다."
    )
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=27.0,
        help=f"장면 전환 감지 민감도(임계값). 낮을수록 민감합니다. (기본값: 27.0)"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    # 입력 파일 존재 여부 확인
    if not os.path.exists(args.input):
        logger.error(f"입력 파일 '{args.input}'을 찾을 수 없습니다.")
        return

    # 출력 폴더 경로 설정 및 생성
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    # 입력 파일명 기반 출력 PDF 경로 생성
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    output_pdf = os.path.join(output_dir, f"{base_name}_summary.pdf")

    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()

    # SceneExtractor, PDFGenerator 인스턴스 생성
    scene_extractor = ContentSceneExtractor(threshold=args.threshold)
    pdf_generator = Img2PDFGenerator()

    try:
        logger.info(f"'{os.path.basename(args.input)}' 파일에서 장면 전환을 감지하는 중... (시간이 걸릴 수 있습니다)")
        # 1단계: 장면 감지 및 이미지 추출
        image_paths = scene_extractor.extract_scenes(args.input, temp_dir)
        if not image_paths:
            logger.warning("동영상에서 어떠한 장면 전환도 감지되지 않았습니다.")
        else:
            logger.info(f"{len(image_paths)}개의 장면을 감지했습니다. 이미지를 추출합니다.")
            # 2단계: 이미지들을 PDF로 변환
            pdf_generator.generate(image_paths, output_pdf)
            logger.info(f"PDF 파일이 성공적으로 생성되었습니다: {output_pdf} 🎉")
    except Exception as e:
        logger.error(f"처리 중 오류 발생: {e}")
    finally:
        # 3단계: 임시 파일 정리
        logger.info("임시 파일을 정리합니다.")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
