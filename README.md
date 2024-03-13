# Langchain Logger 


The genesis for this project was the need to see and display what was actually occurring during a langchain invoke or run method.
There is a cloud service LangSmith appears to capture the internals transactions or Chain of Thought of an invoke or run
but what if you wanted to capture that within your application, maybe show to your end user the internal processing of a request.

Right now you would have to take the result of the invoke and display the COT after processing. 
However you can capture it in real time.

## Installation 

```
pip install langchain-logger
```


## Usage
I suggest pairing this with the [flask-log-viewer](https://github.com/thevgergroup/flask-log-viewer)

Begin by creating a logger, file loggers work well as you can tail them in real time across workers and threads.

