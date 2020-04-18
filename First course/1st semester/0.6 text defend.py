import re
s1 = "So if you're asking me I want you to know"
s2 = "When my time comes"
s3 = "Forget the wrong that I've done"
s4 = "Help me leave behind some reasons to be missed"
s5 = "And don't resent me"
s6 = "And when you're feeling empty"
s7 = "Keep me in your memory"
s8 = "Leave out all the rest."
Text = [s1, s2, s3, s4, s5, s6, s7, s8]
text = []
for i in range(len(Text)):
   text.append(list(Text[i].split( )))
pattern = re.compile(r'(.)\1')
for i in range(len(text)):
    for j in range(len(text[i])):
        if pattern.findall(text[i][j]):
            print(text[i][j])
