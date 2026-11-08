class Quiz:
    """개별 퀴즈의 정보를 담고 출력 및 채점을 담당하는 클래스"""

    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question      # 문제 내용 (str)
        self.choices = choices        # 4지선다 보기 리스트 (list[str])
        self.answer = answer          # 정답 번호 1~4 (int)

    def display(self, q_num: int | None = None) -> None:
        """문제와 4지선다 보기를 화면에 출력합니다."""
        if q_num is not None:
            print(f"\n[문제 {q_num}] {self.question}")
        else:
            print(f"\n[문제] {self.question}")

        for idx, choice in enumerate(self.choices, start=1):
            print(f" {idx}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 입력한 번호가 정답과 일치하는지 확인합니다."""
        return user_answer == self.answer

    def to_dict(self) -> dict:
        """JSON 파일 저장을 위해 Quiz 객체를 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """JSON에서 읽어온 딕셔너리를 Quiz 객체로 복원합니다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )


def get_default_quizzes() -> list[Quiz]:
    """과제 필수 요구사항: 기본 퀴즈 5문항 생성 (주제: 영화 상식)"""
    return [
        Quiz(
            question="마블 시네마틱 유니버스(MCU)에서 타노스가 모은 인피니티 스톤의 총 개수는?",
            choices=["4개", "5개", "6개", "7개"],
            answer=3
        ),
        Quiz(
            question="2020년 아카데미 시상식에서 4관왕을 달성한 영화 '기생충'의 감독은?",
            choices=["박찬욱", "봉준호", "이창동", "김지운"],
            answer=2
        ),
        Quiz(
            question="영화 '인터스텔라'에서 주인공 쿠퍼 일행이 탑승한 주요 우주선의 이름은?",
            choices=["인듀어런스호", "밀레니엄 팔콘", "엔터프라이즈호", "디스커버리호"],
            answer=1
        ),
        Quiz(
            question="영화 '어바웃 타임'에서 가문의 남자들이 대대로 물려받은 특별한 능력은?",
            choices=["순간이동", "시간 여행 (시간 되돌리기)", "마음 읽기 (독심술)", "투명인간 변신"],
            answer=2
        ),
        Quiz(
            question="영화 '아바타' 시리즈에서 판도라 행성에 살아가는 푸른 피부의 원주민 종족 이름은?",
            choices=["나비(Na'vi)족", "벌칸족", "클링온족", "아스가르드족"],
            answer=1
        )
    ]


if __name__ == "__main__":
    # [단독 기능 테스트]
    print("=== Quiz 클래스 동작 테스트 ===")
    sample_quizzes = get_default_quizzes()
    first_quiz = sample_quizzes[0]

    first_quiz.display(q_num=1)

    print("\n--- 채점 테스트 ---")
    print(f"3번(6개) 선택 시 정답 여부: {first_quiz.is_correct(3)} (예상: True)")
    print(f"1번(4개) 선택 시 정답 여부: {first_quiz.is_correct(1)} (예상: False)")
    print("=== 테스트 종료 ===")
