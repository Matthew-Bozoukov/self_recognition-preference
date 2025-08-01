import json
from datasets import load_dataset
import os
import sys

def save_to_json(dictionary, file_name, force_overwrite=True):
    # Create directory if not present
    directory = os.path.dirname(file_name)
    if directory != "" and not os.path.exists(directory):
        os.makedirs(directory)

    if not force_overwrite and os.path.exists(file_name):
        return

    with open(file_name, "w") as f:
        json.dump(dictionary, f)


def load_from_json(file_name) -> dict:
    with open(file_name, "r") as f:
        return json.load(f)


def load_data(dataset, sources, target_model, num_samples, extras=False):
    responses = {}
    for source in sources:
        responses[source] = load_from_json(
            f"summaries/{dataset}/{dataset}_train_{source}_responses{'_' + str(num_samples) if (num_samples != 1000 and source == target_model) else ''}{'_extra' if extras else ''}.json"
        )

    articles = load_from_json(f"articles/{dataset}_train_articles{'_extra' if extras else ''}.json")
    if target_model in sources:
        keys = list(responses[target_model].keys())
    else:
        raise IndexError(f"target_model is not in sources: {target_model} {sources}")
        keys = list(articles.keys())
    return responses, articles, keys



def load_cnn_dailymail_data():
    """
    cnn_train: 287113 items
    cnn_test: 11490 items
    cnn_validation: 13368 items

    article: ~781 tokens
    highlights: ~56 tokens
    id
    """
    dataset = load_dataset("cnn_dailymail", "3.0.0")

    train_data = dataset["train"]
    test_data = dataset["test"]
    validation_data = dataset["validation"]

    return train_data, test_data, validation_data


def load_xsum_data():
    """
    xsum_train: ~204045 items
    xsum_test: ~11334 items
    xsum_validation: ~11332 items

    document: ~2200 chars
    summary: ~125 chairs
    id
    """
    dataset = load_dataset("EdinburghNLP/xsum")

    train_data = dataset["train"]
    test_data = dataset["test"]
    validation_data = dataset["validation"]

    return train_data, test_data, validation_data


def write_to_jsonl_for_finetuning(
    questions, answers, system_prompt, file_name="finetuningdata.jsonl"
):
    formatted_data = ""

    for question, answer in zip(questions, answers):
        entry = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer},
            ]
        }
        formatted_data += json.dumps(entry) + "\n"

    with open(file_name, "w") as file:
        file.write(formatted_data)
