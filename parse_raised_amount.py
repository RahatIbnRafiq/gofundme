
f = open("main_urls.txt", "a")
# Open the file and read line by line
with open("raised_amounts_4.txt", 'r') as file:
    for line in file:
        line = line.strip()
        comma_index = line.find(',')
        url = line[:comma_index]
        # Find the index of the '$' sign
        dollar_index = line.find('$')      
        if dollar_index != -1:  # Ensure '$' is found
            # Find the index of the first English alphabet character after the dollar sign
            for i in range(dollar_index + 1, len(line)):
                if line[i].isalpha():
                    alphabet_index = i
                    break
            else:
                alphabet_index = None  # Handle cases with no alphabet found
            
            if alphabet_index:
                # Extract the raised amount
                amount = line[dollar_index + 1:alphabet_index].strip()
                amount = amount.replace('·', '').replace(',', '')
                f.write(url+","+amount+"\n")
        #     else:
        #         f.write(line+"\n")
        # else:
        #     f.write(line+"\n")


