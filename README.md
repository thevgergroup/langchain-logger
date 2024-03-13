# Langchain Logger 
- [Langchain Logger](#langchain-logger)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Tips](#tips)
    - [CrewAI](#crewai)
    - [Viewing in a browser](#viewing-in-a-browser)
    - [Local Dev](#local-dev)


The genesis for this project was the need to see and display what was actually occurring during a langchain invoke or run method.
There is a cloud service LangSmith appears to capture the internals transactions or Chain of Thought of an invoke or run
but what if you wanted to capture that within your application, maybe show to your end user the internal processing of a request.

Right now you would have to take the result of the invoke and display the COT after processing. 
However you can capture it in real time, and also display the contents.

## Installation 

```
pip install langchain-logger
```


## Usage

Begin by creating a logger, file loggers work well as you can tail them in real time across workers and threads.
This is a standard stream logger

```python

from langchain_openai import OpenAI

from langchain_logger.callback import ChainOfThoughtCallbackHandler
import logging

# Set up logging for the example
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create the Chain of Thought callback handler
cot= ChainOfThoughtCallbackHandler(logger=logger)


# Create a new OpenAI instance
llm = OpenAI(callbacks=[cot])
```


Any using this LLM will now have the chain of though streamed through the logger

A full example is in [example.py](blob/main/example.py)



## Tips

### CrewAI
This works with any layer above langchain that you have access to the LLM
and looks really impressive when you have multiple calls or iterations occurring 

For example CrewAI 

e.g.

```python
from crewai import Agent
....
cot= ChainOfThoughtCallbackHandler(logger=logger)
llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7, callbacks=[cot])

researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  llm=llm
)
```

### Viewing in a browser

A lot of python implementations are single server or shared file system deployments
So it can make sense to log to a file and tail that log to a browser.
We suggest taking a look at the [flask-log-viewer](https://github.com/thevgergroup/flask-log-viewer) to see how you can do that.

We've included a simple log file method to pair with the Chain of Though logger
Start with installing flask and flask-log-viewer
```sh
pip install flask flask-log-viewer
```

create your flask app and add the flask-log-viewer blueprint

```python
from langchain_logger.logger import configure_logger
import uuid

random_log = f"tmp/log_{uuid.uuid4()}.txt"
logger = configure_logger(log_filename=random_log, max_bytes=1024, backup_count=1, max_age_days=3, formatter=None)

cot= ChainOfThoughtCallbackHandler(logger=logger)
llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7, callbacks=[cot])

log_directory = "tmp/logs" #Directory logs are stored in
app = Flask(__name__)

log_viewer = log_viewer_blueprint(base_path=log_directory, allowed_directories=[log_directory])

app.register_blueprint(log_viewer, url_prefix='/logs')
```

Now going to http://localhost:5000/logs/stream/xxxxxx where xxxxx is the random_log file name will now stream the log for you!



### Local Dev

If using local dev with the example, we tend to use poetry for python management

```sh
poetry install -G dev
```

This will install langchain_openai as it's an optional dependency that we used in the example