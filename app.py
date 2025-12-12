import streamlit as st
from PIL import Image

# 아스키 문자와 설정
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65 # 폰트 세로 비율 보정
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def convert_image_to_ascii(image, new_width=100):
    new_image_data = pixels_to_ascii(grayify(resize_image(image, new_width)))
    
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))
    return ascii_image

# --- 웹페이지 UI (Streamlit) ---
st.set_page_config(page_title="이미지 -> 아스키 변환기", layout="wide")
st.title("🖼️ 나만의 아스키 아트 변환기")
st.write("이미지를 업로드하면 텍스트로 바꿔줍니다!")

# 사이드바 설정
st.sidebar.header("설정")
new_width = st.sidebar.slider("해상도 (너비 문자 수)", min_value=30, max_value=300, value=100)

# 파일 업로드
uploaded_file = st.file_uploader("이미지를 선택하세요 (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. 원본 이미지 보여주기
    image = Image.open(uploaded_file)
    st.image(image, caption="원본 이미지", use_column_width=True)
    
    # 2. 변환 실행
    if st.button("변환하기"):
        try:
            ascii_art = convert_image_to_ascii(image, new_width)
            
            # 3. 결과 보여주기
            st.subheader("결과물 (복사 가능)")
            # st.code를 쓰면 텍스트가 깨지지 않고 복사 버튼도 생깁니다.
            st.code(ascii_art, language="text")
            
            # 4. 텍스트 파일 다운로드 버튼
            st.download_button(
                label="텍스트 파일로 다운로드",
                data=ascii_art,
                file_name="ascii_art.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")
