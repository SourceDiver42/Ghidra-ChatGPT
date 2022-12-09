# Ghidra-ChatGPT

## Description
This is a simple python3 script that uses the [Ghidra API](https://ghidra.re/ghidra_docs/api/) to explain highlighted code segments.
It is designed to work with the [ChatGPT](https://chat.openai.com/) model, but can be used with any model that uses the same format.

## Installation
1. Install [Ghidra](https://ghidra-sre.org/)
2. Install [Python3](https://www.python.org/downloads/)
3. Install [Ghidrathon](https://github.com/mandiant/Ghidrathon)
4. Install [pyChatGPT](https://github.com/terry3041/pyChatGPT)
    1. `pip3 install pyChatGPT`
5. Put this script in your ghidra_scripts folder
6. Replace the session_token variable with your own `__Secure-next-auth.session-token` from [ChatGPT](https://chat.openai.com/)
or replace the `api` variable with a different auth mechanism for pyChatGPT

## Usage
1. Open a program in Ghidra
2. Highlight some code
3. Run the script
4. Wait for the model to generate a response
5. Read the response from the console
6. Repeat (sometimes the model will generate a response that is not helpful or very short)

## Notes
- The model will generate a response based on the highlighted code, so it is best to highlight a
function or a block of code that is related to the function you are trying to understand.
- Sometimes the script will seem to be stuck. I have no clue why but by hitting "Cancel" once, the script will
output the response within seconds.
- Due to Jython shenanigans, I had to do some very ugly hacks to get this to work. I am not proud of this code.

## Disclaimer
This project is not affiliated with OpenAI in any way. Use at your own risk. I am not responsible for any damage caused by this project. Please read the OpenAI Terms of Service before using this project.

## Credits
- [ChatGPT](https://chat.openai.com)
- [Ghidra](https://ghidra-sre.org/)
- [Ghidrathon](https://github.com/mandiant/Ghidrathon)
- [pyChatGPT](https://github.com/terry3041/pyChatGPT)
