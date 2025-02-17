import html
import logging
import os
import pickle
import re
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text):
    try:
        text = html.unescape(text)
        text = text.replace('"', "")
        text = text.replace('“', "")
        text = text.replace('|', "")
        text = text.replace('~', "")
        text = re.sub('<[^<]+?>', '', text)
        text = re.sub(' +', ' ', text)

        return text
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}".format(stacktrace))

        raise e

def load_pickle(file_path, file_name):
    try:
        path = "{}.pkl".format(os.path.join(file_path, file_name))

        logger.info("Reading files from {}".format(path))

        with open(path, 'rb') as pickle_file:
            data = pickle.load(pickle_file)
        pickle_file.close()

        return data
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}".format(stacktrace))

        raise e

def tokenize_sequence(tokenizer, max_seq_length, data):
    try:
        input_ids = []
        input_masks = []
        input_segments = []

        bert_input = tokenizer.encode_plus(
            data,
            add_special_tokens=True,
            max_length=max_seq_length,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_token_type_ids=True
        )

        input_ids.append(bert_input['input_ids'])
        input_masks.append(bert_input['attention_mask'])
        input_segments.append(bert_input['token_type_ids'])

        return bert_input['input_ids'], bert_input['attention_mask'], bert_input['token_type_ids']
    except Exception as e:
        stacktrace = traceback.format_exc()

        logger.error("{}".format(stacktrace))
        print("{}".format(stacktrace))

        raise e