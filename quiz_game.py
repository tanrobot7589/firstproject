import requests

class QuizGame:
    def __init__(self):
        self.api_url = 'https://opentdb.com/api.php'
        self.score = 0

    def fetch_questions(self, topic, difficulty):
        params = {
            'amount': 5,
            'category': topic,
            'difficulty': difficulty,
            'type': 'multiple'
        }
        response = requests.get(self.api_url, params=params)
        return response.json()['results']

    def ask_questions(self, questions):
        for question in questions:
            print(question['question'])
            choices = question['incorrect_answers'] + [question['correct_answer']]
            for i, choice in enumerate(choices):
                print(f"{i + 1}: {choice}")
            answer = int(input('Select the correct answer (1-4): ')) - 1
            if choices[answer] == question['correct_answer']:
                print('Correct!')
                self.score += 1
            else:
                print('Wrong!')
                self.score -= 0.25

    def display_score(self):
        print(f'Final Score: {self.score}')

    def start_game(self):
        age = int(input('Enter your age: '))
        topic = input('Select a topic (9 for General Knowledge, 18 for Science: Computers, etc.): ')
        difficulty = input('Choose difficulty (easy, medium, hard): ')
        questions = self.fetch_questions(topic, difficulty)
        self.ask_questions(questions)
        self.display_score()

if __name__ == '__main__':
    game = QuizGame()
    game.start_game()