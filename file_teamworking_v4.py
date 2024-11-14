import os
import shutil
import pyautogui

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sort_files_by_extension_and_category(source_dir):
    # 파일을 문서, 이미지, 음악 등의 큰 카테고리로 분류
    categories = {
        '문서': ['txt', 'hwp', 'pdf', 'docx'],
        '이미지': ['jpg', 'jpeg', 'png', 'gif'],
        '음악': ['mp3', 'wav', 'flac'],
        '비디오': ['mp4', 'avi', 'mkv'],
        '압축파일': ['zip', 'rar', '7z']
    }

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            ext = filename.split('.')[-1].lower()
            moved = False
            for category, exts in categories.items():
                if ext in exts:
                    category_folder = os.path.join(source_dir, category)
                    create_directory(category_folder)
                    shutil.move(file_path, os.path.join(category_folder, filename))
                    moved = True
                    break
            # 확장자가 해당 카테고리에 없으면 그냥 두기
            if not moved:
                unknown_folder = os.path.join(source_dir, '기타')
                create_directory(unknown_folder)
                shutil.move(file_path, os.path.join(unknown_folder, filename))

def get_keyword_input():
    # pyautogui로 키워드 입력받기
    keywords_input = pyautogui.prompt('세부 키워드를 쉼표로 구분하여 입력하세요 (예: 중요, 계약서, 초안):',title = "스마트 파일 정리 시스템")
    keywords = keywords_input.split(',')
    return [keyword.strip() for keyword in keywords]  # 입력된 키워드 리스트 반환

def sort_files_by_keyword(source_dir, keywords):
    # 키워드를 기준으로 파일을 세부 분류
    for category_folder in os.listdir(source_dir):
        category_folder_path = os.path.join(source_dir, category_folder)
        if os.path.isdir(category_folder_path):
            for filename in os.listdir(category_folder_path):
                file_path = os.path.join(category_folder_path, filename)
                if os.path.isfile(file_path):
                    for keyword in keywords:
                        if keyword.lower() in filename.lower():
                            keyword_folder = os.path.join(category_folder_path, keyword)
                            create_directory(keyword_folder)
                            shutil.move(file_path, os.path.join(keyword_folder, filename))
                            break  # 첫 번째 매칭되는 키워드로만 분류

# 메인 실행
def main():
    source_dir = r"C:\Users\didsu\OneDrive\바탕 화면"  # 정리할 파일 경로
    user_input = pyautogui.confirm("파일을 분류하시겠습니까?", buttons=["예", "아니오"],title ="스마트 파일 정리 시스템")
    
    if user_input == "예":
        sort_files_by_extension_and_category(source_dir)  # 확장자별로 대분류
        keywords = get_keyword_input()  # 세부 키워드 입력받기
        sort_files_by_keyword(source_dir, keywords)  # 키워드로 세부 분류
        pyautogui.alert("파일 정리가 완료되었습니다!")
    else:
        pyautogui.alert("파일 정리를 취소했습니다.")

# 실행
main()
