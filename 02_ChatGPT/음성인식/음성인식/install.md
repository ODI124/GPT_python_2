# 음성인식 프로그램 모듈 설치 가이드

## 필수 모듈 설치 명령어

### 1. 기본 GUI 및 오디오 모듈
```bash
# PyQt5 - GUI 프레임워크
pip install PyQt5

# PyAudio - 오디오 입출력
pip install pyaudio
```

### 2. 음성인식 모듈
```bash
# Faster Whisper - 음성인식 엔진
pip install faster-whisper
```

### 3. 번역 모듈
```bash
# Google Translate - 번역 기능
pip install googletrans==3.1.0a0
```

### 4. 딥러닝 프레임워크 (GPU 지원)
```bash
# PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 5. 추가 의존성 모듈
```bash
# 수치 계산 라이브러리
pip install numpy scipy

# 기타 유틸리티
pip install wave threading queue
```

## 전체 설치 명령어 (한번에 설치)

```bash
# 모든 필수 모듈을 한번에 설치
pip install PyQt5 pyaudio faster-whisper googletrans==3.1.0a0 numpy scipy

# CUDA 지원 PyTorch 설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 설치 확인

설치가 완료된 후 다음 명령어로 모듈들이 제대로 설치되었는지 확인할 수 있습니다:

```bash
python -c "import PyQt5; import pyaudio; import faster_whisper; import googletrans; print('모든 모듈이 성공적으로 설치되었습니다!')"
```

## 주의사항

1. **CUDA 요구사항**: GPU 가속을 위해서는 NVIDIA GPU와 CUDA가 설치되어 있어야 합니다.
2. **Python 버전**: Python 3.8 이상을 권장합니다.
3. **PyAudio 설치 문제**: Windows에서 PyAudio 설치에 문제가 있을 경우, Microsoft Visual C++ Build Tools가 필요할 수 있습니다.

## 대안 번역 모듈 (googletrans 문제 시)

만약 `googletrans`에서 문제가 발생할 경우 다음 대안을 사용할 수 있습니다:

```bash
# 대안 번역 라이브러리
pip install deep-translator
```

그리고 코드에서 다음과 같이 수정:
```python
# 기존
from googletrans import Translator

# 대안
from deep_translator import GoogleTranslator
```

## 환경 변수 설정

프로그램 실행 전 다음 환경 변수를 설정하는 것을 권장합니다:

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
```

## 프로그램 실행

모든 모듈 설치 완료 후:

```bash
python sample10.py
```

## 트러블슈팅

### 1. ModuleNotFoundError 발생 시
```bash
pip install --upgrade <모듈명>
```

### 2. CUDA 관련 오류 시
- CUDA 드라이버가 설치되어 있는지 확인
- GPU 메모리 부족 시 CPU 모드로 변경:
```python
self.model = WhisperModel("large-v3", device="cpu")
```

### 3. 번역 오류 시
- 인터넷 연결 확인
- 대안 번역 라이브러리 사용 고려

---

**설치 날짜**: 2025년 10월 25일  
**Python 버전**: 3.13.5  
**작성자**: GitHub Copilot