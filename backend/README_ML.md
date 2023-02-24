# General things
Any model that can be loaded with python can be added. Both pytorch and tensorflow can be used. We are using using a model from hugging face. Any model whose output can be convert to a text (string) can be used. We also have user confgurable option that can be set by the api. Our model has some user configurable option such as length of simplfied text. These option can be sent to the front end and are dynamic added.

# Where to look
`application_logic/simplification` is where python files that deal with machinelearnig and simplfication are located in. addtional in `restapi_simplification` the model is loaded. 

# Contributing
To added new model, first load the model in `restapi_simplfication/app.py`. 
Then using the model_interface.py you can create a new file model_name.py and extend with the interface. 

Any class you add should follow the following template:



    class T5(model_interface.ModelInterface):
        def __init__(self, options: dict = None, model_name_loaded=None, tokenizer_loaded=None, model_loaded=None):
            super().__init__()
            self.model_name = "t5"
            self.options = options
            self.model_name_loaded = model_name_loaded
            self.tokenizer_loaded = tokenizer_loaded
            self.model = model_loaded



After implement all the functions that are in the interface, add the model to the list of models in `simplification_pipline.py` along with and user configurable options. Add the name of the model to <code>\__init__\()</code> and in the Dic in <code>get_models()</code> along option(s) name, a discrption of the option(s) and the option(s) type. This will be use in the frontend to display to user. Follow the example of the T5 model.  

Then go to `restapi_simplification/requet_parser.py` and import from `apps.py`
and add the model to <code>get_simplified_text()</code>  

You have now sucessfully implemented a new model, check if it displayed on the frontend and if user can select it.

# SOME IMPORNTANT NOTES
> Note that the model name is the name of the model that is used in the api and will be use by front end. ***KEEP THE NAME THE SAME EVEREYWHERE.***

>Note if no options value are given by the user, the model should use the default options values. please look at the `T5.py` model for an example. 




