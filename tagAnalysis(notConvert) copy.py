from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch

# 1. 임베딩 모델 로드
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# 2. 기존 카테고리들 (태그) - 태그를 벡터로 변환
categories = {
    '여행' :['여행', '여행지', '캠핑', '관광지', '트레일러', 'travel', 'vacation', 'holiday', 'backpacking', 'naturetrip', '여행지추천', '여행사진', '휴가', '여행스타그램', '여행블로그', '여행정보', '여행준비', '여행계획', '모험', '배낭여행', '탐방', '여행코스', '해외여행', '국내여행', '자전거여행', '동남아여행', '유럽여행', '미국여행', '일본여행', '커플여행', '가족여행', '친구와여행', '혼자여행', '여행상품', '여행팁', '여행지도', '여행추천', '힐링여행', '해변여행', '자연여행', '산책로', '액티브여행', '배낭여행자', '여행예산', '여행숙소', '여행지추천', '해외여행준비', '여행경비', '여행준비물', '휴양지', '자연경관', '여행일정', '전통문화', '여행하기', '여행용품', '여행기념품', '국제여행', '국내여행지', '여행강좌', '여행장소', '여행용카메라', '여행할인', '여행액세서리', '여행이벤트', '여행특가', '여행가이드', '문화탐방', '휴가철여행', '여행동기', '여행비용', '기차여행', '여행기록', '명소', '맛집탐방', '세계여행', '해외여행지', '안전여행', '배낭여행자', '여행물품', '여행추천지', '해변휴양지', '유적지여행', '미니멀여행', '모험여행', '휴양리조트', '글램핑', '여행사진촬영', '여행패키지', '해양활동', '트레킹', '등산여행', '드라이브여행', '숙박추천', '여행경험', '현지문화', '유명여행지', '자유여행'],
    
    '카페' :['카페', '커피', '카페추천', 'coffee', 'caferecommendation', '커피숍', '카페스타그램', '카페인', '커피맛집', 'latte', 'espresso', 'americano', 'mocha', 'tea', '카페문화',  '브런치카페', '커피타임', '여유로운카페', '커피빈', '스타벅스', '카페리스트', '맛있는커피', '카페모카', '라떼아트', '카페분위기', '카페투어', '인스타카페', '고급커피', '핸드드립', '에스프레소', '블렌딩커피', '카페라떼', '달콤한커피', '커피사랑', '테이크아웃', '커피숍추천', '소박한카페', '북카페', '수제커피', '커피홀릭', '편안한카페', '카페음악', '카페테라스', '감성카페', '미니멀카페', '조용한카페', '유명카페', '카페인중독', '핸드드립커피', '카페용품', '브루잉', '커피홀', '카페데이트', '카페포스터', '커피문화', '조용한커피숍', '이색카페', '커피토크', '커피러버', '가게카페', '커피원두', '커피매니아', '커피전문점', '간단한브런치', '아침커피', '로스팅커피', '커피선물', '오후커피', '카페추천리스트', '라떼문화', '카페음료', '모던카페', '빈티지카페', '카페여행', '아이스커피', '카페인조절', '비건커피', '핸드드립카페', '스페셜티커피', '싱글오리진', '음악과커피', '바리스타', '여행카페', '창작카페', '휴식카페', '카페인충전', '음악카페', '케이크와커피', '아메리카노', '커피핸드메이드','coldbrew'],

    '디저트': ['디저트', '빵', 'bread', '케이크', 'cake', '쿠키', 'cookie', '마카롱', 'macaron', '초콜릿', 'chocolate', '타르트', 'tart', '파이', 'pie', '푸딩', 'pudding', '젤라토', 'gelato', '아이스크림', 'icecream', '스콘', 'scone', '에클레어', 'eclair', '무스', 'mousse', '크루아상', 'croissant', '도넛', 'donut', '크레이프', 'crepe', '마들렌', 'madeleine', '브라우니', 'brownie', '와플', 'waffle', '팬케이크', 'pancake', '롤케이크', 'rollcake', '빙수', 'bingsu', '쉬폰케이크', 'chiffoncake', '디저트카페', 'dessertcafe', '디저트메뉴', 'dessertmenu', '디저트추천', 'dessertrecommendation', '디저트샵', 'dessertshop', '디저트레시피', 'dessertrecipe', '홈베이킹', 'homebaking', '수제디저트', 'handmadedessert', '디저트타임', 'desserttime', '디저트러버', 'dessertlover', '디저트여행', 'desserttravel', '비건디저트', 'vegandessert', '로우디저트', 'rawdessert', '오가닉디저트', 'organicdessert', '글루텐프리', 'glutenfree', '디저트음료', 'dessertdrink', '차와디저트', 'teaanddessert', '커피와디저트', 'coffeeanddessert', '디저트선물', 'dessertgift', '디저트배달', 'dessertdelivery', '디저트코스', 'dessertcourse', '디저트도시락', 'dessertlunchbox', '디저트아이디어', 'dessertidea', '디저트디자인', 'dessertdesign', '디저트창작', 'dessertcreation', '디저트아트', 'dessertart', '미니디저트', 'minidessert', '디저트플레이트', 'dessertplate', '디저트와인', 'dessertwine', '초콜릿케이크', 'chocolatecake', '체리파이', 'cherrypie', '크림브륄레', 'cremebrulee', '치즈케이크', 'cheesecake', '디저트레스토랑', 'dessertrestaurant', '디저트공방', 'dessertworkshop', '디저트샵추천', 'dessertshoprecommendation', '디저트스타그램', 'dessertstagram', '핸드메이드디저트', 'handmadedessert', '디저트사진', 'dessertphoto', '디저트스타일', 'dessertstyle', '프렌치디저트', 'frenchdessert', '이탈리안디저트', 'italiandessert'],

    '식당' :['식당', '점심식사', '아침식사', '저녁식사', '레스토랑', '식사', 'restaurant', 'lunch', 'breakfast', 'dinner', 'brunch', '뷔페', 'buffet', '음식점', 'foodplace', '맛집', 'gourmet', '한식', 'koreanfood', '중식', 'chinesefood', '일식', 'japanesefood', '양식', 'westernfood', '세계음식', 'globalcuisine', '퓨전음식', 'fusionfood', '길거리음식', 'streetfood', '패스트푸드', 'fastfood', '디너코스', 'dinnercourse', '점심특선', 'lunchspecial', '테이크아웃', 'takeout', '예약식당', 'reservationrestaurant', '미슐랭', 'michelin', '로컬맛집', 'localrestaurant', '카운터다이닝', 'counterdining', '가성비맛집', 'affordablefood', '캐주얼다이닝', 'casualdining', '파인다이닝', 'finedining', '포차', 'pub', '치킨집', 'chickenplace', '족발집', 'pigfeetrestaurant', '곱창집', 'intestinerestaurant', '전통음식점', 'traditionalrestaurant', '일품요리', 'signaturedish', '특별식사', 'specialmeal', '식당추천', 'restaurantrecommendation', '식사메뉴', 'mealmenu', '식사시간', 'mealtime', '식당예약', 'restaurantreservation', '개인식당', 'privaterestaurant', '체인점', 'chainrestaurant', '테마식당', 'themerestaurant', '로맨틱식당', 'romanticrestaurant', '가족식사', 'familymeal', '데이트코스', 'datedining', '푸드트럭', 'foodtruck', '푸드코트', 'foodcourt', '채식식당', 'vegetarianrestaurant', '비건식당', 'veganrestaurant', '할랄식당', 'halalrestaurant', '해산물식당', 'seafoodrestaurant', '스테이크하우스', 'steakhouse', '이탈리안레스토랑', 'italianrestaurant', '프렌치레스토랑', 'frenchrestaurant', '아시안음식점', 'asianrestaurant', '지중해음식', 'mediterraneanfood', '인도음식점', 'indianrestaurant', '태국음식점', 'thaifoodrestaurant', '베트남음식점', 'vietnamesefood', '메뉴추천', 'menurecommendation', '다양한음식', 'diversefood', '음식문화', 'foodculture', '현지음식', 'localcuisine', '외식', 'diningout', '출장요리', 'catering'],

    '운동' :['운동', '헬스', '피트니스', '오운완', '헬스장', 'PT', '운동추천', '운동스타그램', '운동일지', '운동기록', 'workout', 'fitness', 'gym', 'healthclub', 'personaltraining', '스트레칭', 'stretching', '요가', 'yoga', '필라테스', 'pilates', '러닝', 'running', '조깅', 'jogging', '사이클링', 'cycling', '스피닝', 'spinning', '웨이트트레이닝', 'weighttraining', '크로스핏', 'crossfit', '근력운동', 'strengthtraining', '유산소운동', 'cardio', '홈트', 'homeworkout', 'bodyweighttraining', '운동루틴', '운동계획', '운동습관', '운동의효과', '다이어트운동', 'dietexercise', '체중감량', 'weightloss', '건강관리', 'healthmanagement', '운동팁', '운동방법', '운동전후', '운동복', '운동화', '운동용품', '운동보충제', '운동장비', '트레이닝', 'training', '근육운동', 'muscletraining', '복부운동', 'coreworkout', '팔운동', 'armworkout', '하체운동', 'legworkout', '상체운동', 'upperbodyworkout', '유연성운동', 'flexibility', '체육', 'physicaleducation', '팀스포츠', 'teamsports', '축구', 'soccer', '농구', 'basketball', '배구', 'volleyball', '야구', 'baseball', '스포츠', 'sports', '테니스', 'tennis', '배드민턴', 'badminton', '골프', 'golf', '스케이트보드', 'skateboarding', '서핑', 'surfing', '수영', 'swimming', '클라이밍', 'climbing', '암벽등반', 'rockclimbing', '스키', 'skiing', '스노우보드', 'snowboarding', '트레킹', 'trekking', '하이킹', 'hiking', '태권도', 'taekwondo', '복싱', 'boxing', '무에타이', 'muaythai', '마라톤', 'marathon', '운동동기', 'fitnessmotivation', '운동챌린지', 'exercisechallenge', '운동성과', '운동목표'],

    '자연' : ['산', '강', '자연', '자연경관', '트래킹', '등산', '하이킹', 'hiking', '트레킹', 'trekking', '숲', 'forest', '해변', 'beach', '바다', 'sea', '호수', 'lake', '강변', 'riverside', '계곡', 'valley', '자연탐방', 'natureexploration', '야생', 'wildlife', '초원', 'meadow', '사막', 'desert', '빙하', 'glacier', '자연보호', 'natureconservation', '생태계', 'ecosystem', '자연의소리', 'soundsofnature', '숲속산책', 'forestwalk', '자연속에서', 'innature', '산림욕', 'forestbathing', '자연관찰', 'natureobservation', '일출', 'sunrise', '일몰', 'sunset', '지구', 'earth', '환경', 'environment', '자연사진', 'naturephotography', '야생화', 'wildflowers', '국립공원', 'nationalpark', '생태공원', 'ecopark', '수목원', 'arboretum', '산책로', 'walkingtrail', '고원', 'plateau', '바위산', 'rockymountain', '모래사장', 'sandybeach', '해양생물', 'marinebiology', '동굴', 'cave', '화산', 'volcano', '자연명소', 'naturalscenery', '정상', 'peak', '들판', 'field', '풍경', 'landscape', '언덕', 'hill', '자연의경이로움', 'wondersofnature', '자연에서의휴식', 'relaxationinnature', '고요한자연', 'calmnature', '야생동물관찰', 'wildlifewatching', '야외활동', 'outdooractivities', '자연모험', 'natureadventure', '하천', 'stream', '폭포', 'waterfall', '바위', 'rocks', '알프스', 'alps', '사파리', 'safari', '자연재해', 'naturaldisaster', '숲속캠핑', 'forestcamping', '맑은공기', 'freshair', '자연스러운빛', 'naturallight', '초록풍경', 'greenlandscape', '산속풍경', 'mountainview', '열대우림', 'rainforest', '황야', 'wilderness', '자연에감사', 'gratitudeinnature', '평화로운풍경', 'peacefullandscape', '자연에서의삶', 'lifeinnature'],

    '교육' : ['교육', '학원', '독서실', 'study', '학원추천', '공부', 'studytime', '학습', 'learning', '교과서', 'textbook', '자기계발', 'selfdevelopment', '온라인강의', 'onlineclass', '교육자료', 'educationalresources', '교육정보', 'educationinfo', '학교', 'school', '대학', 'university', '입시', 'admissions', '학과', 'department', '학습방법', 'studymethods', '학원비', 'tuition', '방과후수업', 'afterschool', '유아교육', 'earlyeducation', '초등교육', 'elementaryeducation', '중등교육', 'secondaryeducation', '고등교육', 'highereducation', '특수교육', 'specialeducation', '학습도구', 'learningtools', '학생', 'student', '교수', 'professor', '수업', 'lecture', '공부방', 'studyroom', '스터디그룹', 'studygroup', '교육환경', 'educationenvironment', '교육기관', 'educationalinstitution', '교재', 'teachingmaterials', '공부법', 'studyhabits', '교육비', 'educationcost', '공부자극', 'studyinspiration', '강의', 'lecturevideos', '과외', 'tutoring', '전문교육', 'professionaltraining', '인문학', 'humanities', '자연과학', 'naturalsciences', '수학', 'mathematics', '과학', 'science', '영어', 'english', '역사', 'history', '교육연수', 'educationtraining', '창의교육', 'creativeeducation', '토론수업', 'discussionclass', '교육과정', 'curriculum', '교육정책', 'educationpolicy', '학문', 'academics', '교육컨설팅', 'educationconsulting', '이러닝', 'elearning', '학생복지', 'studentwelfare', '모바일교육', 'mobileeducation', '교육기술', 'educationaltechnology', '홈스쿨링', 'homeschooling', '코딩교육', 'codingeducation', '진로교육', 'careereducation', '평생교육', 'lifelonglearning', '학습성과', 'learningoutcomes', '교육프로그램', 'educationalprogram', '학습목표', 'learninggoals', '기초교육', 'basiceducation', '교육행사', 'educationevent', '인성교육', 'charactereducation', '리더십교육', 'leadershiptraining', '교육과학', 'educationalsciences', '학습코칭', 'learningcoaching', '디지털교육', 'digitaleducation'],

    '문화' : ['영화', 'movie', '문화', '도서관', '게임', 'game', '노래', '음악', 'music', '콘서트', 'concert', '뮤지컬', 'musical', '전시회', 'exhibition', '박물관', 'museum', '문화유산', 'culturalheritage', '공연', 'performance', '오페라', 'opera', '연극', 'theater', '예술', 'art', '댄스', 'dance', '미술', 'fineart', '갤러리', 'gallery', '사진전', 'photographyexhibition', '영화제', 'filmfestival', '독서', 'reading', '문학', 'literature', '시', 'poetry', '소설', 'novel', '연주회', 'recital', '공공문화', 'publicculture', '문화센터', 'culturecenter', '인문학', 'humanities', '스트리트컬처', 'streetculture', '힙합', 'hiphop', '팝', 'popmusic', '클래식', 'classicalmusic', '국악', 'traditionalmusic', '민속', 'folklore', '영상', 'visualarts', '문화체험', 'culturalexperience', '세계문화', 'worldculture', '문화축제', 'culturalfestival', '문화교류', 'culturalexchange', '창작', 'creativearts', '디자인', 'design', '공예', 'craft', '보컬', 'vocal', '밴드', 'band', '음악회', 'concert', '창작곡', 'originalmusic', '애니메이션', 'animation', '만화', 'comics', '그래픽노블', 'graphicnovel', '스트리밍', 'streaming', '문화상품', 'culturalgoods', '문화관광', 'culturaltourism', '영상미디어', 'videomedia', '언어문화', 'languageculture', '전통문화', 'traditionalculture', '문화자원', 'culturalresources', '문화산업', 'culturalindustry', '문화재', 'culturalproperty', '국제영화제', 'internationalfilmfestival', '문화활동', 'culturalactivities', '창의문화', 'creativeculture', '문화보존', 'culturalpreservation', '문화연구', 'culturalstudies', '현대예술', 'contemporaryart', '서예', 'calligraphy', '민속놀이', 'traditionalgames', '연극제', 'theaterfestival', '무용', 'ballet', '모바일게임', 'mobilegame'],

    '디지털' :['it', '디지털', '컴퓨터', '아두이노', '라즈베리파이', 'Window', '디지털노마드', 'IT기술', 'tech', '소프트웨어', 'software', '하드웨어', 'hardware', '프로그래밍', 'programming', '코딩', 'coding', '알고리즘', 'algorithm', '자바', 'java', '파이썬', 'python', 'C언어', 'C', '자바스크립트', 'javascript', 'HTML', 'CSS', 'React', 'Vue', 'Angular', '데이터베이스', 'database', 'SQL', 'MySQL', 'NoSQL', 'MongoDB', 'AI', '인공지능', 'machinelearning', '딥러닝', 'deeplearning', '머신러닝', 'ArtificialIntelligence', '클라우드', 'cloud', 'AWS', 'Azure', '구글클라우드', 'GoogleCloud', '컨테이너', 'Docker', '쿠버네티스', 'Kubernetes', '블록체인', 'blockchain', '비트코인', 'bitcoin', '암호화폐', 'cryptocurrency', 'Ethereum', 'NFT', '웹개발', 'webdevelopment', '모바일앱', 'mobileapp', 'iOS', '안드로이드', 'Android', '게임개발', 'gamedevelopment', '유니티', 'Unity', '언리얼', 'UnrealEngine', '리눅스', 'Linux', '윈도우', 'Windows', '네트워크', 'networking', '사이버보안', 'cybersecurity', '해킹', 'hacking', 'VPN', '백엔드', 'backend', '프론트엔드', 'frontend', '풀스택', 'fullstack', 'API', 'RESTAPI', 'GraphQL', '웹서비스', 'webservices', '디지털트랜스포메이션', 'digitaltransformation', '디지털마케팅', 'digitalmarketing', 'SEO', '검색엔진최적화', 'UI/UX', '사용자인터페이스', '웹디자인', 'webdesign', '모바일디자인', 'mobiledesign', '소셜미디어', 'socialmedia', '디지털컨텐츠', 'digitalcontent', '온라인커머스', 'ecommerce', '핀테크', 'fintech', '스타트업', 'startup', '스마트홈', 'smarthome', '웨어러블', 'wearables', '증강현실', 'augmentedreality', '가상현실', 'virtualreality', 'VR', 'AR', 'IoT', '사물인터넷', '5G', '클라우드컴퓨팅', 'cloudcomputing', '디지털기기', 'digitaldevices'],

    '건강': ['건강', '병원', '다이어트', '영양', '식이요법', '건강식', '헬스케어', '영양제', '건강검진', '스트레스','건강관리', '건강정보', '면역력', '건강한삶', '체중감량', '웰빙', '건강팁', '비타민', '생활습관', '심리건강','영양소', '식단', '단백질', '채식', '비건', '식사요법', '음식', '영양가', '저염식', '저칼로리','유산균', '건강주스', '건강차', '식사일지', '불규칙한식사', '식사습관', '음주', '흡연', '가공식품', '수면','숙면', '피로회복', '수면건강', '불면증', '수면시간', '명상', '마음건강', '정신건강', '정신과', '스트레스관리','호르몬', '면역체계', '장건강', '소화', '장내미생물', '간건강', '체온', '면역력강화', '건강한식사', '근육량','체형관리', '피부건강', '아토피', '피부염', '피부관리', '비타민C', '콜라겐', '뼈건강', '관절', '골다공증','치매', '건강증진', '건강습관', '암', '심혈관질환', '당뇨', '고혈압', '고지혈증', '약물치료', '건강보험','응급처치', '건강식품', '건강검진주기', '건강체크', '피트니스센터', '건강앱', '심리상담', '스트레스해소','자기개발', '긍정적인생각', '행복한삶', '건강정보사이트', '건강한라이프스타일'],

    '패션' :['패션', '바지', '상의', '옷가게', '셔츠', '드레스', '청바지', '아우터', '재킷', '코트', '스타일','패션스타그램', '패션아이템', '패션디자인', '코디', '옷', '의류', '패션쇼', '패션브랜드', '스트리트패션','패션디자이너', '신발', '가방', '액세서리', '모자', '시계', '목걸이', '귀걸이', '패션매거진', '패션블로그','패션트렌드', '클래식패션', '캐주얼패션', '스트릿패션', '패션피플', '패션아이디어', '봄패션', '여름패션','가을패션', '겨울패션', '패셔니스타', '고급패션', '컨템포러리패션', '유행', '트렌드', '빈티지패션', '디자이너브랜드','아디다스', '나이키', '스타벅스패션', '패션매장', '패션쇼핑', '뷰티패션', '패션가방', '명품패션', '온라인패션','패션쇼핑몰', '맞춤형패션', '한정판패션', '어반패션', '파리패션', '뉴욕패션', '서울패션', '패션컬렉션', '패션전시회','스타일링', '핫한패션', '세련된패션', '자주색패션', '패션센스', '고급스러운패션', '디지털패션', '스포츠패션', '여성패션','남성패션', '패션취향', '모던패션', '미니멀패션', '옷스타그램', '패션아이템추천', '패션기획', '데일리패션', '트렌디한패션','스웨터', '티셔츠', '패션코디', '스타일북', '패션사이트', '온라인패션쇼핑', '스포츠웨어', '패션잡지', '패션디렉터','fashion', 'streetstyle', 'streetfashion', 'fashionista', 'trend', 'vintagefashion', 'luxuryfashion', 'fashionstore','stylish', 'fashionblog', 'fashiontrend', 'casualstyle', 'highendfashion', 'stylishoutfits', 'fashionshow', 'fashionista','designerwear', 'clothingstore', 'fashionstyle', 'fallfashion', 'winterfashion', 'summerfashion', 'springfashion', 'urbanfashion']
}

# 3. 기존 카테고리 태그들을 벡터화 (벡터화 후 numpy로 변환)
category_embeddings = {}
for category, tags in categories.items():
    embeddings = model.encode(tags, convert_to_tensor=True)
    category_embeddings[category] = embeddings.numpy()  # numpy로 변환하여 저장

# 4. 벡터화된 데이터를 파일로 저장
for category, embeddings in category_embeddings.items():
    np.save(f'{category}_embeddings.npy', embeddings)  # 카테고리 이름으로 파일 저장


# 5. 새로운 태그들
new_hashtags = [
    '디저트'
]





# 5. 새로운 태그 분류 (임베딩 모델 기반)
def categorize_new_tag_with_embeddings(new_tag, category_embeddings, threshold=0.9):
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

# 6. 새로운 태그들을 카테고리로 분류
categorized_hashtags = {}
for new_tag in new_hashtags:
    category = categorize_new_tag_with_embeddings(new_tag, category_embeddings)
    if category not in categorized_hashtags:
        categorized_hashtags[category] = []
    categorized_hashtags[category].append(new_tag)

# 7. 결과 출력
for category, tags in categorized_hashtags.items():
    print(f"{category} 그룹: {tags}")
