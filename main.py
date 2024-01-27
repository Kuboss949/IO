import random
import linecache
import PySimpleGUI as sg

def create_layout(num, question, answers):
    layout = [
        [sg.Text(f'Pytanie {num}: {question}', key='-TEXT-')],
    ]

    # Dynamically generate radio buttons for answers
    for i, answer in enumerate(answers):
        layout.append([sg.Radio(answer, group_id='answer', key=f'answer{i}')])

    layout.append([sg.Button('Sprawdź odpowiedź'), sg.Button('Dalej')])

    return layout


def get_next_question():
    with open('ioiofull.txt') as f:
        num_lines = sum(1 for _ in f)

    # Losuj numer linii
    line_num = random.randint(1, num_lines)

    # Odczytaj linię o wylosowanym numerze
    line = linecache.getline('ioiofull.txt', line_num)

    # Podziel linię na części
    parts = line.strip().split(';')

    # Wyodrębnij numer pytania, pytanie i odpowiedzi
    num = parts[0]
    question = parts[1]
    answers = parts[2:]
    correct = answers[0]

    # Wylosuj kolejność odpowiedzi
    random.shuffle(answers)

    return num, question, answers, correct

# Inicjalizacja pierwszego pytania
num, question, answers, correct = get_next_question()

# Utwórz elementy GUI
layout = [
    [sg.Text(f'Pytanie {num}: {question}', key='-TEXT-')],
]

# Znajdź indeks poprawnej odpowiedzi przed wymieszaniem
correct_answer_index = answers.index(answers[0])

# Dynamically generate radio buttons for answers
for i, answer in enumerate(answers):
    layout.append([sg.Radio(answer, group_id='answer', key=answer)])

layout.append([sg.Button('Sprawdź odpowiedź'), sg.Button('Dalej')])

# Utwórz okno GUI
window = sg.Window('Quiz', layout)

# Pętla główna
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Sprawdź odpowiedź':
        # Sprawdź, czy odpowiedź jest poprawna
        selected_answer_key = next((k for k, v in values.items() if v), None)
        if selected_answer_key is None:
            sg.popup('Proszę wybrać odpowiedź!')
        elif selected_answer_key == correct:
            sg.popup('Odpowiedź jest poprawna!')
        else:
            sg.popup(f'Odpowiedź jest niepoprawna. Poprawna odpowiedź to: {correct}')

    if event == 'Dalej':
        # Inicjalizacja kolejnego pytania
        num, question, answers, correct = get_next_question()

        # Znajdź indeks poprawnej odpowiedzi przed wymieszaniem
        new_layout = create_layout(num, question, answers)

        # Zaktualizuj layout okna
        window.Layout(new_layout)

# Zamknij okno po zakończeniu pętli
window.close()

