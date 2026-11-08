import json
import os
import sys

STATE_FILE = "state.json"


class Quiz:
    """개별 퀴즈의 정보를 담고 출력 및 채점을 담당하는 클래스"""

    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

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


def safe_input_str(prompt: str) -> str:
    """공백 제거 및 Ctrl+C / EOF 대응 안전 문자열 입력 함수"""
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                print("⚠️ 빈 입력은 허용되지 않습니다. 내용을 입력해 주세요.")
                continue
            return val
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 프로그램이 사용자에 의해 중단되었습니다. 안전하게 종료합니다.")
            sys.exit(0)


def safe_input_int(prompt: str, min_val: int, max_val: int) -> int:
    """공백 제거, 문자 입력 방어, 범위 검증, Ctrl+C 대응 안전 정수 입력 함수"""
    while True:
        try:
            raw_input = input(prompt).strip()
            if not raw_input:
                print(f"⚠️ 빈 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력해 주세요.")
                continue

            val = int(raw_input)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력해 주세요.")
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력해 주세요.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 프로그램이 사용자에 의해 중단되었습니다. 안전하게 종료합니다.")
            sys.exit(0)


def save_state(quizzes: list[Quiz], best_score: int) -> bool:
    """퀴즈 목록과 최고 점수를 state.json에 UTF-8 인코딩으로 저장합니다."""
    try:
        data = {
            "quizzes": [q.to_dict() for q in quizzes],
            "best_score": best_score
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {e}")
        return False


def load_state() -> tuple[list[Quiz], int]:
    """state.json에서 데이터를 불러오며, 누락/손상 시 기본 데이터로 자동 복구합니다."""
    if not os.path.exists(STATE_FILE):
        default_quizzes = get_default_quizzes()
        save_state(default_quizzes, 0)
        return default_quizzes, 0

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]
        best_score = data.get("best_score", 0)

        if not quizzes:
            quizzes = get_default_quizzes()
            save_state(quizzes, best_score)

        return quizzes, best_score
    except (json.JSONDecodeError, KeyError, Exception):
        print("\n⚠️ state.json 데이터 파일이 손상되었습니다.")
        print("🔧 기본 퀴즈 데이터로 안전하게 복구(초기화)합니다.\n")
        default_quizzes = get_default_quizzes()
        save_state(default_quizzes, 0)
        return default_quizzes, 0


# ==========================================
# [QuizGame 클래스 (과제 요구사항 2, 6, 10 충족)]
# ==========================================
class QuizGame:
    """퀴즈 게임 전체 흐름과 메뉴, 데이터 상태를 관리하는 컨트롤러 클래스"""

    def __init__(self):
        self.quizzes, self.best_score = load_state()

    def show_menu(self) -> None:
        """과제 명세서 표준 메인 메뉴를 출력합니다."""
        print("\n" + "=" * 40)
        print(" 🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print(" 1. 퀴즈 풀기")
        print(" 2. 퀴즈 추가")
        print(" 3. 퀴즈 목록")
        print(" 4. 점수 확인")
        print(" 5. 종료")
        print("=" * 40)

    def play_quiz(self) -> None:
        """과제 요구사항 6: 저장된 퀴즈 순차 출제, 채점 및 최고 점수 갱신"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해 주세요.")
            return

        total_questions = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total_questions}문제)")
        print("-" * 40)

        correct_count = 0

        for idx, quiz in enumerate(self.quizzes, start=1):
            quiz.display(q_num=idx)
            user_ans = safe_input_int("\n정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_ans):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다! (정답: {quiz.answer}번 {correct_choice})")
            print("-" * 40)

        # 결과 점수 계산 (100점 만점 기준 환산)
        score = int((correct_count / total_questions) * 100)

        print("\n" + "=" * 40)
        print(f"🏆 결과: {total_questions}문제 중 {correct_count}문제 정답! ({score}점)")

        if score > self.best_score:
            self.best_score = score
            save_state(self.quizzes, self.best_score)
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def add_quiz(self) -> None:
        """과제 요구사항 7: 새로운 퀴즈 등록 및 state.json 영구 저장"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = safe_input_str("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = safe_input_str(f"선택지 {i}: ")
            choices.append(choice)

        answer = safe_input_int("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        save_state(self.quizzes, self.best_score)

        print("\n✅ 퀴즈가 추가되었습니다! (state.json 파일에 자동 저장 완료)")

    def show_quizzes(self) -> None:
        """과제 요구사항 8: 저장된 퀴즈 목록 전체 출력"""
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f" [{idx}] {quiz.question}")
        print("-" * 40)

    def show_score(self) -> None:
        """과제 요구사항 9: 최고 점수 확인 및 미플레이 예외 처리"""
        print("\n" + "=" * 40)
        if self.best_score == 0:
            print("🏆 최고 점수: 0점 (아직 퀴즈를 풀지 않았거나 정답이 없습니다.)")
            print("👉 1번 메뉴를 눌러 첫 퀴즈에 도전해 보세요!")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")
        print("=" * 40)

    def run(self) -> None:
        """메인 이벤트 루프를 실행합니다."""
        print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

        while True:
            self.show_menu()
            choice = safe_input_int("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                # 종료 시 데이터 저장 후 안전 종료
                save_state(self.quizzes, self.best_score)
                print("\n💾 데이터가 안전하게 저장되었습니다.")
                print("👋 퀴즈 게임을 종료합니다. 감사합니다!\n")
                break


if __name__ == "__main__":
    game = QuizGame()
    game.run()
