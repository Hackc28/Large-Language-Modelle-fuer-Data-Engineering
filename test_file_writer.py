import os.path
from datetime import datetime


def test_file_writer(device, model_name, test_time, prompts, responses, sample_solutions):

    time = datetime.now()
    datum_zeit_str = time.strftime("%m-%d_%H-%M-%S")

    text1 = [
        'Tests von llms:\n',
        'benutzte Hardware: ' + device + '\n',
        'benutztes Model: ' + model_name + '\n',
        '\n'
    ]

    text2 = ''
    for i in range(len(prompts)):
        text2 = text2 + '\nPromt' + str(i) + ':\n'
        text2 = text2 + prompts[i] + '\n'
        text2 = text2 + '\nResponse' + str(i) + ':\n'
        text2 = text2 + responses[i] + '\n'
        text2 = text2 + '\nSample Solution' + str(i) + ':\n'
        text2 = text2 + sample_solutions[i] + '\n'

    text3 = [
        '\n',
        'Alle Tests abgeschlossen\n',
        'Dauer: ' + str(test_time) + 's'
    ]
    path = os.path.join(os.path.dirname(__file__), "tests")
    with open(path + '/test_' + datum_zeit_str + '.txt', 'w', encoding='utf-8') as file:
        file.writelines(text1)
        file.writelines(text2)
        file.writelines(text3)

