import random

def shuffle_answers(correct_answer, wrong_answers):
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)
    return all_answers

def process_questions(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    question_mapping = {}

    with open(output_file, 'w') as f_out:
        for line in lines:
            parts = line.strip().split(';')
            number, question, correct_answer, *wrong_answers = parts
            shuffled_answers = shuffle_answers(correct_answer, wrong_answers)
            f_out.write(f"{number}. {question}\n")
            f_out.write(f"A. {shuffled_answers[0]}\n")
            f_out.write(f"B. {shuffled_answers[1]}\n")
            f_out.write(f"C. {shuffled_answers[2]}\n")
            f_out.write(f"D. {shuffled_answers[3]}\n")
            f_out.write(f"\n")
            question_mapping[number] = ['A', 'B', 'C', 'D'][shuffled_answers.index(correct_answer)]

    return question_mapping


def answer_questions(input_file, output_file, answer_file, question_mapping):
    with open(output_file, 'r', encoding='utf-8') as f_out:
        questions = f_out.readlines()

    with open(answer_file, 'w', encoding='utf-8') as f_ans:
        for i in range(0, len(questions), 6):
            for j in range(i, i+6):
                print(questions[j].strip())
            user_answer = input("Your answer (A/B/C/D): ").upper()

            while user_answer not in ['A', 'B', 'C', 'D']:
                print("Invalid input. Please enter A, B, C, or D.")
                user_answer = input("Your answer (A/B/C/D): ").upper()

            question_number = questions[i].split('.')[0]
            f_ans.write(f"{question_number};{user_answer}\n")

def check_answers(answer_file, question_mapping):

    with open(answer_file, 'r') as f_ans:
        user_answers = f_ans.readlines()

    count = 0
    for user_ans in user_answers:
        number, letter = user_ans.strip().split(';')
        correct_answer = question_mapping[number]

        if letter != correct_answer:
            print(f"Question {number}: Correct answer is {correct_answer}, but you chose {letter}")
        else:
            print(f"Question {number}: Your answer {letter} is correct!")
            count += 1

    procenty = (count / 120.0) * 100.0
    print("{:.2f}%".format(procenty))
    if procenty < 75.00:
        print("Nie zdales egzaminu 🙁")
    else:
        print("Egzamin zdany 🙂")

question_mapping = process_questions('baza.txt', 'test.txt')
print("Test file 'test.txt' has been generated. Finish answering and then run the script again.")

# Answer the questions interactively one at a time
answer_questions('baza.txt', 'test.txt', 'answer.txt', question_mapping)

# Check the answers
check_answers('answer.txt', question_mapping)