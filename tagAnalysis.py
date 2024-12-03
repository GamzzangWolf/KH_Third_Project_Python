from sentence_transformers import SentenceTransformer, util
import numpy as np
import os
import time

# 실행 시간 측정 시작
start_time = time.perf_counter()

# 1. 임베딩 모델 로드
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
# model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

# 2. 파일 경로 설정 (임베딩 파일이 저장된 경로)
save_dir = './embedding_files'

# 3. 기존 카테고리 태그들이 저장된 임베딩 파일을 불러오기
category_embeddings = {}
categories = ['건강','교육','디저트','디지털','문화','식당','여행','운동','자연','카페','패션']

for category in categories:
    file_path = os.path.join(save_dir, f'{category}_embeddings.npy')
    category_embeddings[category] = np.load(file_path)  # 저장된 벡터 불러오기

# 4. 새로운 태그 분류 (임베딩 모델 기반)/ 함수정의
def categorize_new_tag_with_embeddings(new_tag, category_embeddings, threshold=0.8):
    # 새로운 태그를 벡터로 변환
    new_tag_embedding = model.encode(new_tag, convert_to_tensor=True)

    # 카테고리별 유사도 계산
    category_scores = {}
    for category, embeddings in category_embeddings.items():
        # 기존 태그들과의 유사도 계산 (최대 유사도 점수 사용)
        similarities = util.pytorch_cos_sim(new_tag_embedding, embeddings)
        category_scores[category] = similarities.max().item()

    # 가장 유사한 카테고리와 점수 반환
    best_category = max(category_scores, key=category_scores.get)
    best_score = category_scores[best_category]

    # 유사도가 임계값(threshold) 미만이면 '기타'로 분류
    if best_score < threshold:
        return '기타'
    return best_category

# # 6. 새로운 태그들을 카테고리로 분류
# categorized_hashtags = {}
# for new_tag in new_hashtags:
#     category = categorize_new_tag_with_embeddings(new_tag, category_embeddings)
#     if category not in categorized_hashtags:
#         categorized_hashtags[category] = []
#     categorized_hashtags[category].append(new_tag)

# # 7. 결과 출력
# for category, tags in categorized_hashtags.items():
#     print(f"{category} 그룹: {tags}")

# 실행 시간 측정 종료
end_time = time.perf_counter()

# 실행 시간 출력
execution_time = end_time - start_time
print(f"실행 시간: {execution_time:.4f}초")