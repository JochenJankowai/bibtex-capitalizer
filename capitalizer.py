import re
import argparse


donts = ["in", "of", "for", "a", "an", "to", "and", "or",
         "the", "on", "im", "am", "from", "its", "einer", "all"]
dos = ["2d", "3d", "4d", "lic", "mri", "dlr", "airs",
       "mipas", "cfg", "cpu", "gpu", "apu", "b2lic", "uflic"]


def substituteQuotationMarks(line):
    line = line.replace('"', "{", 1)
    line = line.replace('"', "}", 1)
    return line


def capitalize(word):
    output = ""
    if word.find('-') > 0:
        splits = word.split('-')
        output = splits[0].capitalize() + "-" + splits[1].capitalize()
    else:
        output = word.capitalize()
    return output


def capitalizeTheWordsThatShouldBeCapital(line):
    global donts
    global dos
    words = line.split()
    retLine = capitalize(words[0])

    for word in words[1:]:
        if word not in donts and word not in dos:
            word = capitalize(word)

        if word in dos:
            print(word)
            word = word.upper()
            print(word)

        retLine += " " + word

    # At this point, we would like to identify semicolons and capitalize the words after. For now we assume that only one : occurs
    if retLine.find(': ') > 0:
        splits = retLine.split(': ')
        retLine = splits[0] + ': ' + splits[1].capitalize()

    return retLine


parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str)
args = parser.parse_args()

with open(args.filename, 'r') as f:
    content = f.readlines()

newContent = []

for line in content:
    index = line.find('=')
    if index != -1:
        if line[index-1] != ' ':
            line = line[:index] + ' ' + line[index:]

    index = line.find('=')
    if index != -1:
        if line[index+1] != ' ':
            line = line[:index+1] + ' ' + line[index+1:]

    line = line.lstrip()
    line = line.rstrip()

    line = substituteQuotationMarks(line)

    tag = line.split(" ")[0]

    if tag.lower() == "title":
        line = line[line.find('{')+1:line.rfind('}')]
        line = line.replace("{", "")
        line = line.replace("}", "")
        line = capitalizeTheWordsThatShouldBeCapital(line)
        line = "Title = {" + re.sub('([A-Z]+)', r'{\1}', line) + "},\n"
    else:
        if len(line) > 3:
            if line[0].islower():
                line = line[0].upper() + line[1:]
            if line[len(line)-1] == '}' and line[len(line)-2] == '}':
                line = line[:-1] + ",\n}\n"
            if line[len(line)-1] != ',' and line[len(line)-1] != '\n':
                line = line + ",\n"

    if len(tag) > 0:
        if tag[0] != '@' and tag[0] != '}':
            line = "    " + line
        if tag[0] == '@':
            line = '\n' + line

    if len(line) > 0:
        if line[len(line)-1] != '\n':
            line = line + '\n'

    newContent.append(line)

while len(newContent[0]) < 1:
    newContent.pop(0)

newContent[0] = newContent[0][1:]

with open(args.filename, 'w') as f:
    for line in newContent:
        f.write(line)
