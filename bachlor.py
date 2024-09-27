import os.path
import sys

from gpt4all import GPT4All
from timeit import default_timer as timer
from fehlerkorrektur1 import fehlerkorrektur
from fehlerkorrektur2 import fehlerkorrektur_transformation
from schemaMatching2 import schema_matching2
from entityMatching2 import entity_matching2
import test_file_writer


def gpt4all():
    model_names = [
        'orca-mini-3b-gguf2-q4_0.gguf',  # model_name_0
        'mistral-7b-instruct-v0.2.Q4_0.gguf',  # model_name_1
        'mixtral-8x7b-instruct-v0.1.Q3_K_M.gguf',  # model_name_2 (nur Server)
        'qwen2-7b-instruct-q4_0.gguf',  # model_name_3
        'Qwen2.5-7B-Instruct-Q6_K.gguf',  # model_name_4
        'Phi-3.1-mini-4k-instruct-Q6_K.gguf',  # model_name_5
        'Meta-Llama-3-8B-Instruct.Q4_0.gguf',  # model_name_6
        'Meta-Llama-3.1-8B-Instruct.Q4_0.gguf',  # model_name_7
        'Meta-Llama-3.1-8B-Instruct-Q6_K.gguf',  # model_name_8
        'Mistral-7B-Instruct-v0.3-Q6_K.gguf',  # model_name_9 (Server)
        'Qwen2.5-14B-Instruct-IQ3_M.gguf',     # model_name_10 (Server)
        'Qwen2.5-7B-Instruct-Q6_K_L.gguf',     # model_name_11 (Server)
        'Phi-3.5-mini-instruct-Q6_K.gguf',     # model_name_12 (Server)
        'Meta-Llama-3.1-8B-Instruct-Q6_K.gguf',  # model_name_13 (Server)
        'gemma-2-9b-it-Q5_K_M.gguf'            # model_name_14 (Server)

    ]
    model_name = model_names[10]

    try:
        model_number = int(sys.argv[1])
        if model_number >= 0:
            model_name = model_names[model_number]
    except (ValueError, IndexError) as e:
        prompts = []
    print(model_name)

    path = os.path.join(os.path.dirname(__file__), "models")
    print(path)
    try:
        print(GPT4All.list_gpus())
    except ValueError as e:
        prompts = []

    prompts = []
    responses = []
    sample_solutions = []

    try:
        model = GPT4All(model_name=model_name, model_path=path, allow_download=False, device='cuda')  # 'cuda' 'gpu'
        device = model.device
    except ValueError as e:
        print(e)
        device = None
    if device is None:
        model = GPT4All(model_name=model_name, model_path=path, allow_download=False)
        device = 'CPU'
    print(device)

    start_time = timer()

    value_correction_error_reference_data(model, prompts, responses, sample_solutions)
    value_correction_error_transformation(model, prompts, responses, sample_solutions)
    schema_matching(model, prompts, responses, sample_solutions)
    entity_matching(model, prompts, responses, sample_solutions)

    test_time = round(timer() - start_time, 2)
    print(test_time)

    test_file_writer.test_file_writer(device, model_name, test_time, prompts, responses, sample_solutions)


def value_correction_error_reference_data(model, prompts, responses, sample_solutions):
    obj = fehlerkorrektur()
    result = 0
    for i in range(0, 40):
        prompt = ("You are a data cleaning machine that returns a correction, which is a single expression.\n"
                  "If you do not find a correction, you return the token<NULL>.\n"
                  "You always follow the example."
                  f"{obj.example_president[0]},<Error>,{obj.example_end[0]}\n"
                  f"correction:{obj.example_start[0]}\n"
                  f"{obj.example_president[1]},<Error>,{obj.example_end[0]}\n"
                  f"correction:{obj.example_start[1]}\n"
                  f"{obj.example_president[2]},<Error>,{obj.example_end[0]}\n"
                  f"correction:{obj.example_start[2]}\n"
                  f"{obj.example_president[3]},<Error>,{obj.example_end[0]}\n"
                  f"correction:{obj.example_start[3]}\n"
                  f"{obj.example_president[4]},<Error>,{obj.example_end[0]}\n"
                  f"correction:{obj.example_start[4]}\n"
                  f"{obj.data_president[i]},<Error>,{obj.data_end[i]}"
                  "correction:")
        response = model.generate(prompt, max_tokens=5, temp=0.2)
        print(f"{obj.data_president[i]},<{obj.data_start[i]}>,{obj.data_end[i]}")
        print(response)
        text = response
        if obj.data_start[i] in text:
            print("ja")
            result = result + 1
        else:
            print("nein")
        prompts.append(prompt)
        responses.append(response)
        sample_solutions.append(f"{obj.data_start[i]}\n{result} von {i + 1} richtig")


def value_correction_error_transformation(model, prompts, responses, sample_solutions):
    obj = fehlerkorrektur_transformation()
    result = 0
    for i in range(0, 100):
        prompt = ("You are a data cleaning machine that detects patterns to return a correction.\n"
                  "If you do not find a correction, you return the token<NULL>.\n"
                  "You always follow the example."
                  f"{obj.example[0]}\n"
                  f"correction:{obj.example_solution[0]}\n"
                  f"{obj.example[1]}\n"
                  f"correction:{obj.example_solution[1]}\n"
                  f"{obj.example[2]}\n"
                  f"correction:{obj.example_solution[2]}\n"
                  f"{obj.example[3]}\n"
                  f"correction:{obj.example_solution[3]}\n"
                  f"{obj.example[4]}\n"
                  f"correction:{obj.example_solution[4]}\n"
                  f"{obj.example[5]}\n"
                  f"correction:{obj.example_solution[5]}\n"
                  f"{obj.example[6]}\n"
                  f"correction:{obj.example_solution[6]}\n"
                  f"{obj.example[7]}\n"
                  f"correction:{obj.example_solution[7]}\n"
                  f"{obj.example[8]}\n"
                  f"correction:{obj.example_solution[8]}\n"
                  f"{obj.example[9]}\n"
                  f"correction:{obj.example_solution[9]}\n"
                  f"{obj.data[i]}"
                  "correction:")
        response = model.generate(prompt, max_tokens=15, temp=0.2)
        print(obj.data[i])
        print(response)
        text = response
        if obj.data_solution[i] in text:
            print("ja")
            result = result + 1
        else:
            print("nein")
        prompts.append(prompt)
        responses.append(response)
        sample_solutions.append(f"{obj.data_solution[i]}\n{result} von {i + 1} richtig")


def schema_matching(model, prompts, responses, sample_solutions):
    obj = schema_matching2()
    result = 0
    true_positive = 0
    false_positive = 0
    false_negative = 0
    for i in range(0, 50):
        prompt = ("You are a data schema matching machine that check if two columns match.\n"
                  "Respond only with <yes> if they match, or <no> if they do not.\n"
                  "You always follow the example."
                  f"{obj.example_column_1[0]}|{obj.example_column_2[0]}\n"
                  f"matching:<{obj.example_solution[0]}>\n"
                  f"{obj.example_column_1[1]}|{obj.example_column_2[1]}\n"
                  f"matching:<{obj.example_solution[1]}>\n"
                  f"{obj.example_column_1[2]}|{obj.example_column_2[2]}\n"
                  f"matching:<{obj.example_solution[2]}>\n"
                  f"{obj.example_column_1[3]}|{obj.example_column_2[3]}\n"
                  f"matching:<{obj.example_solution[3]}>\n"
                  f"{obj.example_column_1[4]}|{obj.example_column_2[4]}\n"
                  f"matching:<{obj.example_solution[4]}>\n"
                  f"{obj.example_column_1[5]}|{obj.example_column_2[5]}\n"
                  f"matching:<{obj.example_solution[5]}>\n"
                  f"{obj.example_column_1[6]}|{obj.example_column_2[6]}\n"
                  f"matching:<{obj.example_solution[6]}>\n"
                  f"{obj.data_column_1[i]}|{obj.data_column_2[i]}\n"
                  f"matching:")
        response = model.generate(prompt, max_tokens=5, temp=0.2)
        response = response.split('\n')
        print(f"{obj.data_column_1[i]}|{obj.data_column_2[i]}")
        print(response)
        text = response[0]
        if obj.data_solution[i] in text:
            print("richtig")
            result = result + 1
            if obj.data_solution[i] == 'yes':
                true_positive = true_positive + 1
        else:
            print("falsch")
            if obj.data_solution[i] == 'yes':
                false_negative = false_negative + 1
            else:
                false_positive = false_positive + 1
        prompts.append(prompt)
        responses.append(response[0])
        sample_solutions.append(f"{obj.data_solution[i]}\n{result} von {i + 1} richtig\ntrue_positive = {true_positive} | false_positive = {false_positive} | false_negative = {false_negative}")
        print(f"{obj.data_solution[i]}\n{result} von {i + 1} richtig")


def entity_matching(model, prompts, responses, sample_solutions):
    obj = entity_matching2()
    result = 0
    true_positive = 0
    false_positive = 0
    false_negative = 0
    for i in range(0, 120):
        prompt = ("You are a data entity matching machine that check if two rows match.\n"
                  "Respond only with <yes> if they match, or <no> if they do not.\n"
                  "You always follow the example."
                  f"{obj.example_row_1[0]}|{obj.example_row_2[0]}\n"
                  f"matching:<{obj.example_solution[0]}>\n"
                  f"{obj.example_row_1[1]}|{obj.example_row_2[1]}\n"
                  f"matching:<{obj.example_solution[1]}>\n"
                  f"{obj.example_row_1[2]}|{obj.example_row_2[2]}\n"
                  f"matching:<{obj.example_solution[2]}>\n"
                  f"{obj.example_row_1[3]}|{obj.example_row_2[3]}\n"
                  f"matching:<{obj.example_solution[3]}>\n"
                  f"{obj.example_row_1[4]}|{obj.example_row_2[4]}\n"
                  f"matching:<{obj.example_solution[4]}>\n"
                  f"{obj.example_row_1[5]}|{obj.example_row_2[5]}\n"
                  f"matching:<{obj.example_solution[5]}>\n"
                  f"{obj.example_row_1[6]}|{obj.example_row_2[6]}\n"
                  f"matching:<{obj.example_solution[6]}>\n"
                  f"{obj.data_row_1[i]}|{obj.data_row_2[i]}\n"
                  f"matching:")
        response = model.generate(prompt, max_tokens=5, temp=0.2)
        response = response.split('\n')
        print(f"{obj.data_row_1[i]}|{obj.data_row_2[i]}")
        print(response)
        text = response[0]
        if obj.data_solution[i] in text:
            print("richtig")
            result = result + 1
            if obj.data_solution[i] == 'yes':
                true_positive = true_positive + 1
        else:
            print("falsch")
            if obj.data_solution[i] == 'yes':
                false_negative = false_negative + 1
            else:
                false_positive = false_positive + 1
        prompts.append(prompt)
        responses.append(response[0])
        sample_solutions.append(f"{obj.data_solution[i]}\n{result} von {i + 1} richtig\ntrue_positive = {true_positive} | false_positive = {false_positive} | false_negative = {false_negative}")
        print(f"{obj.data_solution[i]}\n{result} von {i + 1} richtig")


if __name__ == '__main__':
    gpt4all()

