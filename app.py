from flask import Flask, jsonify, request
import tagAnalysis  # tagAnalysis.py 파일을 임포트

app = Flask(__name__)

@app.route('/categorize', methods=['POST'])
def categorize_tags():
    # JSON으로 받은 데이터에서 'tags' 값을 추출
    data = request.json
    tags = data.get('tags', [])

    # 받은 태그 데이터 출력 (디버깅용)
    print(f"받은 태그들: {tags}")
    
    # 각 태그를 카테고리로 분류
    categorized_hashtags = {}
    for tag in tags:
        category = tagAnalysis.categorize_new_tag_with_embeddings(tag, tagAnalysis.category_embeddings)
        if category not in categorized_hashtags:
            categorized_hashtags[category] = []
        categorized_hashtags[category].append(tag)

    # 분류된 결과 출력 (디버깅용)
    print(f"분류된 결과: {categorized_hashtags}")

    # 결과 반환
    # 결과를 JSON으로 반환 (명시적으로 UTF-8 설정)
    response = jsonify(categorized_hashtags)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True)