input = ""
for line in open("mother.speech.txt"):
    input += line
input = input.strip()
input2 = ""
for char in input:
    if char != "W":
        input2 += char
utterances_original = input.split("U")
utterances2 = input2.split("U")

freq = {}
trans = {}
for utt in utterances2:
    sylls = [x for x in utt.split("S") if x]
    if sylls:
        last_syl = ""
        for s in sylls:
            if s not in freq:
                freq[s] = 0
            freq[s] += 1
            if last_syl:
                add = last_syl + "\t" + s
                if add not in trans:
                    trans[add] = 0
                trans[add] += 1
            last_syl = s

tps = {k: trans[k] / freq[k.split("\t")[0]] for k in trans}

total = 0
ahhh = 0
for utt in utterances2:
    sylls = [x for x in utt.split("S") if x]
    if sylls:
        tps_temp = []
        last_syl = ""
        for s in sylls:
            if last_syl:
                lookup = last_syl + "\t" + s
                tps_temp.append(tps[lookup])
            last_syl = s
        print(tps_temp, len(tps_temp))
        # print(sylls, len(sylls))
        output = sylls[0] + "S"
        if len(tps_temp) > 1:
            # if tps_temp[0] < tps_temp[1]:
            #     output += "W"
            output += sylls[1] + "S"
            i: int = 1
            while i < len(tps_temp) - 1:
                if tps_temp[i] < tps_temp[i - 1] and tps_temp[i] < tps_temp[i + 1]:
                    output += "W"
                output += sylls[i + 1] + "S"
                i += 1
            if tps_temp[len(tps_temp) - 1] < tps_temp[len(tps_temp) - 2]:
                output += "W"
            output += sylls[len(sylls) - 1] + "S"
            # output += sylls[i]+"S"+ sylls[len(sylls)-1] + "S"
        output += "W"

        # print("ONE", output.split("W"))
        # print("TWO", utterances_original[total].split("W"))
        right = [x for x in utterances_original[total].split("W") if x]
        other = [x for x in output.split("W") if x]
        correct = [x for x in other if x in right]
        print(right)
        print(other)
        ahhh += len(correct) / len(other)

    total += 1

print(ahhh / total)
