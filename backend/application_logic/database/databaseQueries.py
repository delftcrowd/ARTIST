import datetime
import os
import traceback

from bson import ObjectId
from pymongo import MongoClient
from pymongo import errors

MONGODB_URL_FULL = os.environ.get("MONGODB_URL_FULL")
if MONGODB_URL_FULL is None:
    raise Exception(
        "Database info not found. Please check the config file or the environment variables."
    )

# Connect to the database
# url format: mongodb+srv://<USER>:<PASS>@YOUR_MONGODB_INSTANCEretryWrites=true&w=majorit
client = MongoClient(MONGODB_URL_FULL)

# Required keys for inserting suggestion
required_keys_suggestion = {
    "unsimplified_text",
    "simplified_by_model",
    "simplified_by_user",
    "model_info",
}

# Required keys for inserting feedback
required_keys_feedback = {
    "unsimplified_text",
    "simplified_by_model",
    "simplified_by_user",
    "model_info",
}

not_required_keys = {
    "rating_simplification",
    "difficult_sentences_original",
    "difficult_sentences_revised",
    "rating_sentences",
    "metric_options",
    "comments",
    "difficult_sentences_simplified",
}


def get_database_status():
    try:
        client.server_info()
        return "Online."
    except errors.ServerSelectionTimeoutError as err:
        print(str(err))
        return "Offline. Contact server administrator."


def add_to_db(data: dict) -> bool:
    """
    add_to_db adds an entry to the database. The entry must be a dictionary with the following keys
    """
    try:
        if get_database_status():
            myclient = client
            mydb = myclient["artist_suggestions_database"]
            mycol = mydb["suggestions"]
            mycol.insert_one(data)
        return True
    except Exception as e:
        raise e


def get_all_entries_from_db():
    """
    getAllEntriesFromDB returns all Entries from the database

    :return: List of all the entries in the database, or none in case there was an error
    """
    try:
        if get_database_status():
            myclient = client
            mydb = myclient["artist_suggestions_database"]
            mycol = mydb["suggestions"]
        return mycol.find()
    except Exception as e:
        print(
            "Error occured while trying to get all Entries from DB. Call stack has been printed to stderr."
        )
        print(e)
        traceback.print_stack()
        raise e


def insert_suggestion_into_db(suggestion: dict) -> bool:
    """Description
    :type suggestion:dict:
    :param suggestion:dict:

    :raises: Exceptions for incorrect format for input

    :rtype: bool:

    :format of suggestions:{
    "unsimplified_text" :           STRING "<text>",
    "simplified_by_model":          STRING "<text>",
    "simplified_by_user":           STRING "<text>",
    "model_info" :                  DICTIONARY {
                                        "model_name":       STRING "<model_name>",
                                        "options":          LIST [
                                                            DICIONARY {
                                                                "option_name":          STRING "<option_name>",
                                                                "option_type":          STRING "<option_type>",
                                                                "option_value":         STRING "<option_value>"
                                                                },
                                                            ]
                                    },

    "type":                             STRING "<type>", (automatically generated)
    "Datetime":                         DATE <date> (automatically generated)
    }
    """

    # Check if the suggestion has the required keys
    for key in required_keys_suggestion:
        if key not in suggestion:
            raise Exception(f"Missing {key} parameter in suggestion dictionary.")

    # Check if the suggestion has the correct types
    for key in suggestion:
        if key in required_keys_suggestion and key != "model_info":
            if type(suggestion[key]) != str:
                raise Exception(f"{key} is not a string.")

    # Check if the model_info is the correct type
    if type(suggestion["model_info"]) != dict:
        raise Exception("model_info is not a dictionary.")

    # Check if the model_info has the correct keys
    has_model_name = False
    for i in suggestion["model_info"]:
        # Check if model_name is a string
        if i == "model_name":
            if type(suggestion["model_info"][i]) != str:
                raise Exception(f"{i} is not a string.")
            else:
                has_model_name = True

        # Check if model_info -> options is a list
        elif i == "options" and suggestion["model_info"][i] != None:
            if type(suggestion["model_info"][i]) != list:
                raise Exception(f"{i} is not a list.")

            # Check if options is a list of dict and value in dic are strings
            for j in suggestion["model_info"][i]:
                if type(j) != dict:
                    raise Exception(f"model_info -> options{j} is not a dictionary.")
                # Check if parameter are a string
                for k in j:
                    if type(j[k]) != str and k != "option_value":
                        raise Exception(
                            f"model_info -> options -> {j} ->{k} is not a string."
                        )

    # Check if model_name is present
    if not has_model_name:
        raise Exception("Field 'model_name' not present inside 'model_info'")

    keys = suggestion.keys()
    all_pos = required_keys_suggestion
    if len(set(keys).difference(set(all_pos))) > 0:
        raise Exception("Feedback contains keys not recognised: ", set(keys).difference(set(all_pos)))

    suggestion["type"] = "suggestion"
    suggestion["Datetime"] = datetime.datetime.now()

    return add_to_db(suggestion)


def insert_feedback_into_db(feedback: dict) -> bool:
    """Description
    :type feedback:dict:
    :param feedback:dict:

    :raises: Exceptions for incorrect format for input

    :rtype: bool:

    :correct format for input
    {
    "unsimplified_text" :           STRING "<text>",
    "simplified_by_model":          STRING "<text>",
    "simplified_by_user":           STRING "<text>",
    "rating_simplification":        INTEGER <rating>, between 0 and 5
    "comments":                     STRING "<comments>"
    "model_info" :                  DICTIONARY {
                                        "model_name":       STRING "<model_name>",
                                        "options":          LIST [
                                                            DICIONARY {
                                                                "option_name":          STRING "<option_name>",
                                                                "option_type":          STRING "<option_type>",
                                                                "option_value":         STRING "<option_value>"
                                                                },
                                                            ]
                                    },
    "difficult_sentences_original": LIST ["sentence1", "sentence2"] //Sentences need to be WITHOUT the ending character ('.', '?', '!') #TODO:  implement this
    "difficult_sentences_revised":  LIST ["sentence1", "sentence2"] //Sentences need to be WITHOUT the ending character ('.', '?', '!') #TODO:  implement this
    "rating_sentences":             INTEGER <rating>,
    "metric_options":               DICIONARY {
                                        "metric_name":      "STRING <metric_name>"
                                    }
    }
    """
    # check if all required keys are present
    for key in required_keys_feedback:
        if key not in feedback:
            raise Exception(
                f"Missing {key} parameter in feedback dictionary or it is None."
            )
    # check if all keys are of the correct type
    for key in feedback:
        if key in required_keys_feedback and key != "model_info":
            if type(feedback[key]) != str:
                raise Exception(f"{key} is not a string.")

    # check if rating_simplification exists and is of the correct type
    if "rating_simplification" in feedback:
        if type(feedback["rating_simplification"]) != int:
            raise Exception("rating_simplification must be an integer")
        if (
            feedback["rating_simplification"] < 0
            or feedback["rating_simplification"] > 5
        ):
            raise Exception(
                "Field rating_simplification must be an integer between 0 and 5."
            )
    # check if comments exists and is of the correct type

    if "comments" in feedback and feedback["comments"] != None:
        if type(feedback["comments"]) != str:
            raise Exception("Field comments must be a string.")

    # check if model_info is of the correct type
    if type(feedback["model_info"]) != dict:
        raise Exception("Field model_info is not a dictionary.")

    # check if model_info has the correct keys and if they are of the correct type
    has_name = False
    for i in feedback["model_info"]:
        # check if model_name is of the correct type
        if i == "model_name":
            if type(feedback["model_info"][i]) != str:
                raise Exception(f"{i} is not a string.")
            else:
                has_name = True
        # check if options is of the correct type
        if i == "options" and feedback["model_info"][i] != None:
            # check if options is a list
            if type(feedback["model_info"][i]) != list:
                raise Exception(f"{i} is not a list.")

            # check if each option is a list of dictionaries and if the dictionaries have the correct keys and if they are of the correct type
            for j in feedback["model_info"][i]:
                if type(j) != dict:
                    raise Exception(f"model_info -> options{j} is not a dictionary.")
                for k in j:
                    if type(j[k]) != str and k != "option_value":
                        raise Exception(
                            f"model_info -> options -> {j} -> {k} is not a string."
                        )
    # difficulty sentences original are present and are of the correct type
    if (
        "difficult_sentences_original" in feedback
        and feedback["difficult_sentences_original"] != None
    ):
        if type(feedback["difficult_sentences_original"]) != list:
            raise Exception("difficult_sentences_original must be a list.")
        for i in feedback["difficult_sentences_original"]:
            if type(i) != str:
                raise Exception(
                    "difficult_sentences_original must be a list of strings."
                )
        # tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        # for sentence in feedback["difficult_sentences_original"]:
        #    if sentence not in '\n-----\n'.join(tokenizer.tokenize(feedback["unsimplified_text"])):
        #        raise Exception ("Sentence '" + str(sentence) + "' could not be find in unsimplified text.")

    # difficulty sentences revised are present and are of the correct type
    if (
        "difficult_sentences_revised" in feedback
        and feedback["difficult_sentences_revised"] != None
    ):
        if type(feedback["difficult_sentences_revised"]) != list:
            raise Exception("difficult_sentences_revised must be a list.")
        for i in feedback["difficult_sentences_revised"]:
            if type(i) != str:
                raise Exception(
                    "difficult_sentences_revised must be a list of strings."
                )

    # check if rating_sentences exists and is of the correct type
    if "rating_sentences" in feedback and feedback["rating_sentences"] != None:
        if type(feedback["rating_sentences"]) != int:
            raise Exception("rating_sentences must be an integer")
        if feedback["rating_sentences"] < 0 or feedback["rating_sentences"] > 5:
            raise Exception("rating_sentences must be an integer between 0 and 5.")

    # check if metric_options exists and is of the correct type
    if "metric_options" in feedback and feedback["metric_options"] != None:
        if type(feedback["metric_options"]) != dict:
            raise Exception("metric_options must be a dictionary.")
        for i in feedback["metric_options"]:
            if type(feedback["metric_options"][i]) != str:
                raise Exception(f"{i} is not a string.")

    if not has_name:
        raise Exception("model_info must have a field model_name.")

    keys = feedback.keys()
    all_pos = required_keys_feedback.union(not_required_keys)
    if len(set(keys).difference(set(all_pos))) > 0:
        raise Exception("Feedback contains keys not recognised: ", set(keys).difference(set(all_pos)))

    feedback["type"] = "feedback"
    feedback["Datetime"] = datetime.datetime.now()

    return add_to_db(feedback)


def remove_from_db(ids: list):
    """
    removeFromDb removes entries from the database given the specific ids. Prints the number of entries deleted.
    If it is given a nonexistent id, it will print that 0 entries have been deleted.
    This method should be used with caution, as loss of data is a great risk!

    :param ids:                 List of ids to be deleted from the database
    :return:                    The string "success" or the specified error message
    """
    try:
        if get_database_status():
            myclient = client
            mydb = myclient["artist_suggestions_database"]
            mycol = mydb["suggestions"]

            count = 0
            if type(ids) == str:  # Work also if someone gave only a string as input
                result = mycol.delete_one({"_id": ObjectId(ids)})
                count = count + result.deleted_count

            else:  # The normal way of functioning
                for id in ids:
                    if type(id) != str:
                        raise Exception("Id: " + str(id) + " is not a string!")

                    try:
                        result = mycol.delete_one({"_id": ObjectId(id)})
                        count = count + result.deleted_count
                    except Exception as e:
                        print("Error deleting entry with id " + id)
                        print(e)
                        traceback.print_stack()

            print("successfully deleted " + str(count) + " entries from the database.")
            return "success"

    except Exception as e:
        stre = "Exception occured while trying to remove ids from the database."
        raise Exception(stre)
