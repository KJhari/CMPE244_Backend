import openai, json, os, time, logging

workdir = os.path.abspath(os.path.dirname(__file__))
print(workdir)
api_key_file = os.path.join(workdir, "API_Key.json")  # Construct the full file path

try:
    with open(api_key_file, "r") as f:
        keyDict = json.load(f)
    # Now you can use the API key from keyDict
    api_key = keyDict["HL"]
    print("API Key loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file was not found at {api_key_file}.")
except json.JSONDecodeError:
    print(f"Error: There was an issue decoding the JSON file at {api_key_file}.")
except KeyError:
    print("Error: The key 'HL' was not found in the JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

MODEL = "gpt-3.5-turbo"
API_KEY = keyDict.get("HL")
openai.api_key = API_KEY


def configure_logging():
    logging.basicConfig(filename=workdir + 'output.log', level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s')
    return logging.getLogger()


def upload_file(file_name):
    # Note: For a 400KB train_file, it takes about 1 minute to upload.
    file_upload = openai.File.create(file=open(file_name, "rb"), purpose="fine-tune")
    logger.info(f"Uploaded file with id: {file_upload.id}")

    while True:
        logger.info("Waiting for file to process...")
        file_handle = openai.File.retrieve(id=file_upload.id)

        if len(file_handle) and file_handle.status == "processed":
            logger.info("File processed")
            break
        time.sleep(60)

    return file_upload


if __name__ == '__main__':
    # Configure logger
    logger = configure_logging()

    file_name = workdir + "\gpt_flattend_prompts.jsonl"
    uploaded_file = upload_file(file_name)

    logger.info(uploaded_file)
    job = openai.FineTuningJob.create(training_file=uploaded_file.id, model=MODEL)
    logger.info(f"Job created with id: {job.id}")

    # Note: If you forget the job id, you can use the following code to list all the models fine-tuned.
    # result = openai.FineTuningJob.list(limit=10)
    # print(result)