# TODO: as we are stopping at RET, we might not get all the code (label after ret)
import os
from binascii import hexlify
from queue import Queue

from pyChatGPT import ChatGPT

session_token = ""

# Get the current selection
if currentSelection is None:
    raise ValueError("No selection")

# FunctionManager instance
functionManager = currentProgram.getFunctionManager()

# Minimum address of selection
min_addr = currentSelection.getMinAddress()
# Maximum address of selection
max_addr = currentSelection.getMaxAddress()

# get asm listing
listing = currentProgram.getListing()

# Get the instruction at the selection address
code = listing.getInstructions(min_addr, True)

# Contains the discovered functions in the form of a list of tuples (function name, function address)
found_functions = set()
q = Queue()
output = ""


def handle_refs(line, refs):
    out = ""
    if len(refs) > 0:
        for ref in refs:
            data_at_ref = listing.getDataAt(ref.getToAddress())
            if line.getMnemonicString() == "CALL":
                funcName = functionManager.getFunctionAt(ref.getToAddress()).getName()
                if (funcName, ref.getToAddress()) not in found_functions:
                    found_functions.add((funcName, ref.getToAddress()))
                    q.put((funcName, ref.getToAddress()))
                out += "[0x{} : {}]\n".format(ref.getToAddress(), funcName)
            elif data_at_ref is not None and "RDI" not in line.toString():
                # big workaround as this Python 3 script is not able to handle the bytes
                # object returned by the getBytes() method
                # so we have to convert it to a string and then to a bytes object again
                tmp = [x & 0xFF for x in line.getBytes()]
                in_hex = hexlify(bytes(tmp)).decode("utf-8")
                out += ("[0x{} : {:16} {}]\n".format(data_at_ref.getAddress(), in_hex,
                                                        data_at_ref.toString().replace("ds ", "")))
    return out


def format_line(line):
    out = ""
    # big workaround as this Python 3 script is not able to handle the bytes
    # object returned by the getBytes() method
    # so we have to convert it to a string and then to a bytes object again
    tmp = [x & 0xFF for x in line.getBytes()]
    in_hex = hexlify(bytes(tmp)).decode("utf-8")
    out += "0x{} : {:16} {}\n".format(line.getAddress(), in_hex, line.toString())
    refs = line.getReferencesFrom()
    out += handle_refs(line, refs)
    return out


while code.hasNext():
    instr = code.next()
    output += format_line(instr)

    # Stop at the end of the selection
    if instr.getAddress() >= max_addr:
        break

# Define end of listing
output += "----------------------------------------\n"

# Print the discovered functions
while not q.empty():
    func = q.get()
    # Get the code of the function at address
    func_code = listing.getInstructions(func[1], True)
    # Print the function name
    output += "::{}::\n".format(func[0])
    try:
        # Assume there's only 1 function with that name
        func1 = getGlobalFunctions(func[0])[0]
    except:
        # If there's no function  or the function is from an external library, skip it
        output += "No body\n"
        continue

    # Get the body of the function
    addrSet = func1.getBody()
    # Get the code of the function
    lines = listing.getCodeUnits(func[1], True)

    # iterate over the code units
    for line in lines:
        output += format_line(line)

        # If the line is a RET instruction, break
        if line.getMnemonicString() == "RET":
            break

print(output)

# ChatGPT stuff
api = ChatGPT(session_token=session_token)
gpt_msg = "After this message I will post the output of a disassembled binary by Ghidra." \
          "The first column contains the address, the second column the hex representation and the third" \
          "column the assembly code. When an instruction references an address, the function name or data" \
          "can be found in the next line with the corresponding address, between square brackets." \
          "The code of most referenced functions can be found after the line with many dashes. the name of the" \
          "function is between colons, followed by the asm code in the following lines. If there is no code," \
          "'No body' will be the line under the function name. This is mostly the case for standard" \
          "library functions. Can you tell me what this snippet does? Please answer very verbosely and" \
          "be as specific as possible."

resp = api.send_message(gpt_msg)
# We do not want the "I'm sorry, but I am unable to view the code snippet you have provided" message, so we skip that
# print to null
print(resp['message'], file=open(os.devnull, 'w'))
resp = api.send_message(output)
print(resp['message'])