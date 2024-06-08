import pandas as pd #pandas 라이브러리를 import

class LevenshteinChatBot:   #챗봇 초기화하고 질문과 답변 데이터를 로드
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath): #CSV 파일에서 질문과 답변을 로드합니다.
        data = pd.read_csv(filepath) #CSV 파일 읽기
        questions = data['Q'].tolist() #질문 리스트로 변환
        answers = data['A'].tolist() #답변 리스트로 변환
        return questions, answers #질문과 답변 반환

    def levenshtein_distance(self, a, b): #레벤슈타인 거리 계산하기       
        if a == b: 
            return 0  # 두 문자열이 같으면 거리 0
        a_len = len(a)  # 첫 번째 문자열의 길이
        b_len = len(b)  # 두 번째 문자열의 길이
        if a == "": 
            return b_len  # 첫 번째 문자열이 빈 문자열이면 두 번째 문자열의 길이 반환
        if b == "": 
            return a_len  # 두 번째 문자열이 빈 문자열이면 첫 번째 문자열의 길이 반환
        
        #2차원 표 준비
        matrix = [[0 for j in range(b_len + 1)] for i in range(a_len + 1)]
        for i in range(a_len + 1):
            matrix[i][0] = i #첫 번째 열 초기화
        for j in range(b_len + 1):
            matrix[0][j] = j  #첫 번째 행 초기화
        
        #표를 채워서 레벤슈타인 거리 계산
        for i in range(1, a_len + 1):
            ac = a[i - 1] #첫 번째 문자열의 현재 문자
            for j in range(1, b_len + 1):
                bc = b[j - 1] #두 번째 문자열의 현재 문자
                cost = 0 if (ac == bc) else 1 #비용계산, 셋 중 최소 비용을 선택하여 matrix 갱신
                matrix[i][j] = min([
                    matrix[i - 1][j] + 1,  # 문자 제거
                    matrix[i][j - 1] + 1,  # 문자 삽입
                    matrix[i - 1][j - 1] + cost  # 문자 교체
                ])
        return matrix[a_len][b_len] #두 문자열의 레벤슈타인 거리 반환

    def find_best_answer(self, input_sentence): #입력 문장과 가장 유사한 질문을 찾아 해당 답변을 반환
        distances = [self.levenshtein_distance(input_sentence, question) for question in self.questions]
        best_match_index = distances.index(min(distances))  #가장 작은 거리의 인덱스를 찾음
        return self.answers[best_match_index] #해당 인덱스의 답변 반환

# CSV 파일 경로
filepath = 'ChatbotData.csv'

# 레벤슈타인 거리 기반 챗봇 인스턴스를 생성
chatbot = LevenshteinChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        print('챗봇을 종료합니다.')
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
    
    