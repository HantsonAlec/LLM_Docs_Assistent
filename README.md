# LLM_docs_assistant
This LLM docs assistant PoC uses small open source models and will be running on a raspberry Pi.<br>
The model will be able to answer questions based on the *provided vector store*. Since this runs on a raspberry Pi, memory capabilities are limited.

## Setup

- Hardware: Raspberry Pi 4. With 4GB of RAM
- LLM: Llama3.2 - 1b version
- Vector store: pinecone dimension 896


### Step 1: Installing ollama and the LLM on the raspberry Pi
Connect via ssh, and enter ```curl https://ollama.ai/install.sh | sh```<br>
Run your favorite small LLM with ```ollama run llama3.2:1b```

### Step 2: Get the code on the raspberry Pi
1. In order to get the code repo on the raspberry pi. Install git ```sudo apt install git```<br>
2. Install pip by running ```sudo apt-get install python3-pip```
3. clone the repo ```git clone https://github.com/HantsonAlec/LLM_Docs_Assistent.git```
4. Create virtual venv ```python3 -m venv LLM_Docs_Assistent/venv.``` and activate ```source venv./bin/activate```
5. cd into the LLM_Docs_Assistent folder
6. Install required packages ```pip install -r requirements.txt```

### Step 2: Run the streamlit app
1. Create a .env file(```nano .env```) in the main folder with the following values: 
```
PINECONE_API_KEY=
INDEX_NAME = 
INDEX_HOST =
```
2. ```streamlit run src/main.py``` following the network URL you can access the streamlit app.


You can now enjoy this small PoC app and ask your own questions!

