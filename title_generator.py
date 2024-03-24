import random


def getRandomTitle():
    # Open the file in read mode
    with open("title/title.txt", "r", encoding="utf8") as file:
        # Read all lines into a list
        titles = file.readlines()
    # Select a random line from the list
    random_title = random.choice(titles).replace("\n", "")
    random_number = random.randint(1, 9999)
    final_title = random_title + " #" + str(random_number)
    return final_title


if __name__ == "__main__":
    print(getRandomTitle())
