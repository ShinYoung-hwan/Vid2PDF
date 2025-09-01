# main.py
#
# 이 스크립트는 동영상 파일을 입력받아 장면 전환을 감지하고,
# 각 장면의 시작 프레임을 캡처하여 하나의 PDF 파일로 합칩니다.
#
# 사전 설치가 필요한 라이브러리:
# pip install "scenedetect[opencv]" img2pdf
#
# 실행 방법:
# python main.py -i [동영상_파일_경로]
# 예시: python main.py -i my_video.mp4
#
# 선택 옵션:
# -o [출력_PDF_파일_경로]: 출력될 PDF 파일의 경로를 지정합니다. (기본값: [입력_파일_이름].pdf)
# -t [임계값]: 장면 전환 감지 민감도를 설정합니다. 값이 낮을수록 더 민감하게 반응합니다. (기본값: 27.0)

import os
import argparse
import tempfile
import shutil
import logging
from typing import List

# PySceneDetect 라이브러리 임포트
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images

# img2pdf 라이브러리 임포트
import img2pdf

# 로깅 설정 (PySceneDetect의 상세 메시지 출력 방지)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SceneDetectToPDF')

def find_scenes_and_extract_images(video_path: str, threshold: float, temp_dir: str) -> List[str]:
    """동영상에서 장면을 감지하고 대표 이미지를 임시 폴더에 저장합니다."""
    try:
        video = open_video(video_path)
        scene_manager = SceneManager()
        
        # 콘텐츠 기반 감지기 추가 (임계값 설정)
        scene_manager.add_detector(ContentDetector(threshold=threshold))
        
        logger.info(f"'{os.path.basename(video_path)}' 파일에서 장면 전환을 감지하는 중... (시간이 걸릴 수 있습니다)")
        
        # 장면 감지 실행
        scene_manager.detect_scenes(video=video)
        
        # 감지된 장면 목록 가져오기
        scene_list = scene_manager.get_scene_list()
        
        if not scene_list:
            logger.warning("동영상에서 어떠한 장면 전환도 감지되지 않았습니다.")
            return []
            
        logger.info(f"{len(scene_list)}개의 장면을 감지했습니다. 이미지를 추출합니다.")
        
        # 감지된 장면의 시작 프레임을 이미지로 저장
        save_images(
            scene_list=scene_list,
            video=video,
            num_images=1,  # 각 장면 당 1개의 이미지만 저장
            output_dir=temp_dir,
            image_name_template='$SCENE_NUMBER' # 파일명을 숫자로 지정하여 정렬 용이
        )
        
        # 저장된 이미지 파일 목록을 정렬하여 반환
        image_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]
        image_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
        
        return image_files

    except Exception as e:
        logger.error(f"장면 감지 중 오류 발생: {e}")
        return []

def create_pdf_from_images(image_files: List[str], output_pdf_path: str):
    """이미지 파일 목록을 받아 하나의 PDF 파일로 변환합니다."""
    if not image_files:
        logger.warning("PDF로 변환할 이미지가 없습니다.")
        return

    logger.info(f"{len(image_files)}개의 이미지를 '{output_pdf_path}' 파일로 변환합니다.")
    try:
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_files))
        logger.info("PDF 파일이 성공적으로 생성되었습니다. 🎉")
    except Exception as e:
        logger.error(f"PDF 생성 중 오류 발생: {e}")

def main():
    """메인 실행 함수: 인자 파싱 및 전체 프로세스 조율."""
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
        help="출력 PDF 파일 경로. 지정하지 않으면 입력 파일 이름으로 자동 생성됩니다."
    )
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=27.0,
        help="장면 전환 감지 민감도(임계값). 낮을수록 민감합니다. (기본값: 27.0)"
    )
    
    args = parser.parse_args()

    # 입력 파일 존재 여부 확인
    if not os.path.exists(args.input):
        logger.error(f"입력 파일 '{args.input}'을 찾을 수 없습니다.")
        return

    # 출력 파일 경로 설정
    output_pdf = args.output
    if not output_pdf:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_pdf = f"{base_name}_summary.pdf"

    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1단계: 장면 감지 및 이미지 추출
        image_paths = find_scenes_and_extract_images(args.input, args.threshold, temp_dir)
        
        # 2단계: 이미지들을 PDF로 변환
        if image_paths:
            create_pdf_from_images(image_paths, output_pdf)
            
    finally:
        # 3단계: 임시 디렉토리 및 파일 정리
        logger.info("임시 파일을 정리합니다.")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()