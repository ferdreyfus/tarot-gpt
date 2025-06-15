import random, time
from ai import call_gpt

# Code in Place 2025 - Final Project, by Fernando Dreyfus.
# Tarot-GPT, script that shuffles a tarot deck for different divination structures, to then be interpreted by chatGPT.

# define global variables, deck, definitions, and list of questions.
original_deck = [
    # Major Arcana
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World",

    # Minor Arcana - Wands
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands",
    "Five of Wands", "Six of Wands", "Seven of Wands", "Eight of Wands",
    "Nine of Wands", "Ten of Wands", "Page of Wands", "Knight of Wands",
    "Queen of Wands", "King of Wands",

    # Minor Arcana - Cups
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups",
    "Five of Cups", "Six of Cups", "Seven of Cups", "Eight of Cups",
    "Nine of Cups", "Ten of Cups", "Page of Cups", "Knight of Cups",
    "Queen of Cups", "King of Cups",

    # Minor Arcana - Swords
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords",
    "Five of Swords", "Six of Swords", "Seven of Swords", "Eight of Swords",
    "Nine of Swords", "Ten of Swords", "Page of Swords", "Knight of Swords",
    "Queen of Swords", "King of Swords",
    
    # Minor Arcana - Pentacles
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles",
    "Five of Pentacles", "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles",
    "Nine of Pentacles", "Ten of Pentacles", "Page of Pentacles", "Knight of Pentacles",
    "Queen of Pentacles", "King of Pentacles"
    ]

asker_questions_list = [
    # questions to process personality into randomness, without taking in any PERSONALLY IDENTIFIABLE INFORMATION
    "What's your favorite smell in the world?",
    "What kind of music do you usually listen to when you're relaxing?",
    "Do you prefer sunrise or sunset?",
    "What’s your favorite way to spend a rainy day?",
    "Which season do you feel most like yourself in?",
    "What’s a small thing that instantly makes your day better?",
    "Do you like cities, forests, mountains, or beaches the most?",
    "What’s your comfort food when you’re feeling down?",
    "Is there a movie or book that really stuck with you?",
    "What’s your favorite sound (like waves, rain, birds, etc.)?",
    "If you could learn any skill instantly, what would it be?",
    "What’s a scent that brings back a strong memory?",
    "Are you more of a night owl or an early bird?",
    "What color do you think matches your personality?",
    "Do you collect anything or wish you did?",
    "What’s something you always enjoy talking about?",
    "If you could live in any fictional world, which would it be?",
    "Do you prefer silence, background noise, or music when working?",
    "What kind of weather makes you feel happiest?",
    "What’s a hobby or activity you lose track of time doing?"
    ]

tarot_definition_dictionary = {
    # Major Arcana
    "The Fool": "A leap of faith, beginnings, and spontaneous adventure.",
    "The Magician": "Manifestation and using your resources to create change.",
    "The High Priestess": "Intuition, secrets, and the unconscious mind.",
    "The Empress": "Fertility, abundance, and nurturing energy.",
    "The Emperor": "Authority, structure, and leadership.",
    "The Hierophant": "Tradition, spiritual guidance, and conformity.",
    "The Lovers": "Love, alignment, and choices in relationships.",
    "The Chariot": "Willpower, victory, and determination.",
    "Strength": "Inner strength, courage, and compassion.",
    "The Hermit": "Introspection, solitude, and inner guidance.",
    "Wheel of Fortune": "Cycles, fate, and unexpected change.",
    "Justice": "Fairness, truth, and law or karma.",
    "The Hanged Man": "Letting go, surrender, and seeing from a new perspective.",
    "Death": "Endings, transformation, and new beginnings.",
    "Temperance": "Balance, harmony, and moderation.",
    "The Devil": "Addiction, materialism, and feeling trapped.",
    "The Tower": "Sudden upheaval, revelation, and disruption.",
    "The Star": "Hope, inspiration, and spiritual renewal.",
    "The Moon": "Illusion, fear, and the subconscious.",
    "The Sun": "Joy, success, and vitality.",
    "Judgement": "Awakening, reckoning, and life purpose.",
    "The World": "Completion, fulfillment, and achievement.",

    # Minor Arcana - Wands
    "Ace of Wands": "New inspiration, creative spark, and potential.",
    "Two of Wands": "Planning, progress, and looking ahead.",
    "Three of Wands": "Expansion, foresight, and waiting for results.",
    "Four of Wands": "Celebration, harmony, and homecoming.",
    "Five of Wands": "Conflict, competition, and tension.",
    "Six of Wands": "Victory, recognition, and success.",
    "Seven of Wands": "Defensiveness, perseverance, and standing your ground.",
    "Eight of Wands": "Speed, progress, and rapid movement.",
    "Nine of Wands": "Resilience, persistence, and guarding your territory.",
    "Ten of Wands": "Burden, stress, and being overworked.",
    "Page of Wands": "Enthusiasm, discovery, and exploration.",
    "Knight of Wands": "Passion, adventure, and impulsive energy.",
    "Queen of Wands": "Confidence, independence, and charisma.",
    "King of Wands": "Leadership, vision, and boldness.",

    # Minor Arcana - Cups
    "Ace of Cups": "New emotions, love, and spiritual beginnings.",
    "Two of Cups": "Partnership, connection, and mutual attraction.",
    "Three of Cups": "Friendship, celebration, and community.",
    "Four of Cups": "Apathy, contemplation, and reevaluation.",
    "Five of Cups": "Regret, loss, and focusing on the negative.",
    "Six of Cups": "Nostalgia, childhood, and past memories.",
    "Seven of Cups": "Choices, illusion, and wishful thinking.",
    "Eight of Cups": "Walking away, withdrawal, and seeking deeper meaning.",
    "Nine of Cups": "Contentment, satisfaction, and emotional fulfillment.",
    "Ten of Cups": "Harmony, family, and lasting happiness.",
    "Page of Cups": "Creative beginnings, messages of love, and sensitivity.",
    "Knight of Cups": "Romantic pursuit, charm, and idealism.",
    "Queen of Cups": "Compassion, intuition, and emotional depth.",
    "King of Cups": "Emotional balance, wisdom, and diplomacy.",

    # Minor Arcana - Swords
    "Ace of Swords": "Clarity, truth, and a breakthrough.",
    "Two of Swords": "Stalemate, difficult choices, and indecision.",
    "Three of Swords": "Heartbreak, grief, and emotional pain.",
    "Four of Swords": "Rest, recovery, and contemplation.",
    "Five of Swords": "Conflict, betrayal, and hollow victory.",
    "Six of Swords": "Transition, moving on, and rite of passage.",
    "Seven of Swords": "Deception, strategy, and acting alone.",
    "Eight of Swords": "Restriction, feeling trapped, and self-limitation.",
    "Nine of Swords": "Anxiety, nightmares, and inner turmoil.",
    "Ten of Swords": "Betrayal, painful endings, and rock bottom.",
    "Page of Swords": "Curiosity, vigilance, and mental energy.",
    "Knight of Swords": "Ambition, action, and recklessness.",
    "Queen of Swords": "Truth, independence, and clear thinking.",
    "King of Swords": "Authority, intellect, and ethical leadership.",

    # Minor Arcana - Pentacles
    "Ace of Pentacles": "New opportunities, prosperity, and manifestation.",
    "Two of Pentacles": "Balance, adaptability, and time management.",
    "Three of Pentacles": "Teamwork, skill, and building something worthwhile.",
    "Four of Pentacles": "Control, stability, and possessiveness.",
    "Five of Pentacles": "Hardship, loss, and financial insecurity.",
    "Six of Pentacles": "Generosity, giving and receiving, and support.",
    "Seven of Pentacles": "Patience, assessment, and long-term view.",
    "Eight of Pentacles": "Mastery, diligence, and skill development.",
    "Nine of Pentacles": "Self-sufficiency, luxury, and refinement.",
    "Ten of Pentacles": "Legacy, family, and long-term success.",
    "Page of Pentacles": "Ambition, planning, and new ventures.",
    "Knight of Pentacles": "Responsibility, routine, and productivity.",
    "Queen of Pentacles": "Practicality, nurturing, and material comfort.",
    "King of Pentacles": "Abundance, leadership, and financial security."
}

copy_deck = original_deck # to use a different list and reload the basic deck when needed.

def main():
    # Program prints intro, then asks user semi personal info, hashes into a number, user selects type of reading,
    # then draws the respective cards and passes the hash, type of reading, and cards drawn into a gpt query for a reading.    
    # Randomize the questions asked.
    random.shuffle(asker_questions_list)

    # Welcome intro Lines - turn into the "print_intro function"
    print_intro()   

    # Ask user about themselves, set the hashed answers into a variable.
    # Define Variable that defines uniqueness - TODO add another random number multiplication to ensure true randomness after inputs. 
    uniqueness = get_user_info() # asks user about themselves, hash, then use that number as seed for uniqueness
    uniqueness = uniqueness * random.random()  # multiply the above value times another random.random() value. this is to prevent repetition in results with same input.

    # Select type of reading
    reading_choice_str = define_reading_type()
            
    # Retrieve user consultation
    print("\nExcellent! \n")
    time.sleep(1)
    print("Now clear your mind... \n")
    time.sleep(1)
    user_query = input("Visualize your question, and type it here: ") #Take the user's question.

    # Set randomness seed to a variable
    random.seed(uniqueness) # sets seed
    # draws the card
    card_set = draw_cards(reading_choice_str,uniqueness,user_query) # outputs a list the cards drawn in order by index of read type.

    # passes info to ChatGPT to tell user fortune, then prints it.
    user_fortune = tell_fortune(card_set,reading_choice_str)
    print(user_fortune)

    time.sleep(2)
    goodbye_message = "\nTake the above with a grain of salt, but do use the reading as a mirror to self analyze and decide what is best, what's true, and what are blessings for you. Love and light!"
    print(goodbye_message)

def define_reading_type():
    # Choose type of reading - put into a function.
    print("\nWhat kind of reading would your like to have?: \n")    
    print("1. single card read - meditation")
    print("2. five card read - divination")
    print("3. Celtic Cross 11 card read - full in depth\n")

    reading_choice_str = input("Please select a reading type: 1, 2, or 3: ")

    while reading_choice_str not in ["1", "2", "3"]:
        print("Invalid choice.")
        reading_choice_str = input("Please select a reading type: 1, 2, or 3: ")

    return reading_choice_str

def print_intro():
    # Just a header print function 
    print("----- Tarot-GPT -----")
    print("Welcome to Tarot-GPT!, my Code in Place final project.\n")
    time.sleep(2)
    input("If you wish to ask the oracle anything about your future, press ENTER (or send any message, if in whatsapp) : ")

def draw_cards(reading_type,uniqueness,user_query): 
    # set uniqueness as seed for random, then shuffle the deck, then flow into the selected reading.
    random.seed(uniqueness)
    random.shuffle(copy_deck)
    
    if reading_type == "1":
        print("\nYou have chosen a single card meditation. \n")
        time.sleep(1)
    
        print("please, clear your mind, and focus on the question you previously asked:\n")
        time.sleep(1)
        
        print("*** "+ user_query + " ***\n")
        
        time.sleep(1)
        
        card_1 = copy_deck.pop()
        card_read_list = [card_1]

        # Show results for single card read, and the definition
        print("Your drawn card for meditation is: " + card_1)
        card_explainer_1 = tarot_definition_dictionary[card_1]
        print()
        print("Focus on the following: This card represents: " + card_explainer_1 + "\n")
        
        return card_read_list

    elif reading_type == "2":
        print("\nYou have chosen a 5 card read meditation. \n")
        time.sleep(2)
        print("please, clear your mind, and focus on the question you previously asked: \n")
        time.sleep(1)
        print("*** "+ user_query + " ***\n")
        time.sleep(4)

        # Draw the cards into variables
        card_1 = copy_deck.pop()
        card_2 = copy_deck.pop()
        card_3 = copy_deck.pop()
        card_4 = copy_deck.pop()
        card_5 = copy_deck.pop()

        # Pull definition of cards into variables
        card_explainer_1 = tarot_definition_dictionary[card_1]
        card_explainer_2 = tarot_definition_dictionary[card_2]
        card_explainer_3 = tarot_definition_dictionary[card_3]
        card_explainer_4 = tarot_definition_dictionary[card_4]
        card_explainer_5 = tarot_definition_dictionary[card_5]

        print("Your first drawn card, signifying the Current situation is: " + card_1 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_1 + "\n")
        time.sleep(4)
        print("Your second drawn card, signifying your response to the question asked is: " + card_2 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_2 + "\n")
        time.sleep(4)
        print("Your third drawn card, signifying what's holding you back regarding the question is: " + card_3 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_3 + "\n")
        time.sleep(4)
        print("Your fourth drawn card, signifying what you should do, is: " + card_4 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_4 + "\n")
        time.sleep(4)
        print("Your fifth drawn card, signifying what the outcome, if actioned is: " + card_5 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_5 + "\n")

        card_read_list =[]
        card_read_list.append(card_1)
        card_read_list.append(card_2)
        card_read_list.append(card_3)
        card_read_list.append(card_4)
        card_read_list.append(card_5)

        # return card list    
        return card_read_list

    elif reading_type == "3":
        print("You have chosen an 11 card complete read meditation.")
        time.sleep(2)
        print("please, clear your mind, and focus on the question you previously asked: \n")
        time.sleep(1)
        print("*** "+ user_query + " ***")
        time.sleep(4)

        # Draw the cards into variables
        card_1 = copy_deck.pop()
        card_2 = copy_deck.pop()
        card_3 = copy_deck.pop()
        card_4 = copy_deck.pop()
        card_5 = copy_deck.pop()
        card_6 = copy_deck.pop()
        card_7 = copy_deck.pop()
        card_8 = copy_deck.pop()
        card_9 = copy_deck.pop()
        card_10 = copy_deck.pop()
        card_11 = copy_deck.pop()

        # Pull definition of cards into variables
        card_explainer_1 = tarot_definition_dictionary[card_1]
        card_explainer_2 = tarot_definition_dictionary[card_2]
        card_explainer_3 = tarot_definition_dictionary[card_3]
        card_explainer_4 = tarot_definition_dictionary[card_4]
        card_explainer_5 = tarot_definition_dictionary[card_5]                
        card_explainer_6 = tarot_definition_dictionary[card_6]
        card_explainer_7 = tarot_definition_dictionary[card_7]
        card_explainer_8 = tarot_definition_dictionary[card_8]
        card_explainer_9 = tarot_definition_dictionary[card_9]
        card_explainer_10 = tarot_definition_dictionary[card_10]
        card_explainer_11 = tarot_definition_dictionary[card_11]


## 1. 'This covers it', card 3. 'This crosses it', card 4. Past influences, card 5. Near Future, card 6. Conscious Goal/Best Outcome, card 7. Unconscious influence / root, 8. You/your attitude, card 9. External influences, card 10. Hopes & Fears, card 11. Outcome 

        # Print out the cards, then their explanations from the list and dictionary respectively. - TODO fix the prints 
        print("Your first drawn card, is the Significator of the read: " + card_1 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_1 + "\n")
        time.sleep(4)

        print("Second drawn card, signifies, 'This covers it', the main influence of your question: " + card_2 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_2 + "\n")
        time.sleep(4)
        
        print("Your third drawn card, signifying obstacles, or 'this crosses it': " + card_3 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_3 + "\n")
        time.sleep(4)
        
        print("Your fourth drawn card, signifies past influences on your question: " + card_4 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_4 + "\n")
        time.sleep(4)
        
        print("Your fifth drawn card, represents the near future: " + card_5 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_5 + "\n")
        time.sleep(4)

        print("Your sixth card represents your conscious goal, or best outcome: " + card_6 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_6 + "\n")
        time.sleep(4)

        print("Your seventh card, represents your unconscious influence, or root of the issue:" + card_7 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_7 + "\n")
        time.sleep(4)

        print("Your eight card, represents you and your attitudes: " + card_8 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_8 + "\n")
        time.sleep(4)

        print("Your ninth card, represents external influences: " + card_9 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_9 + "\n")
        time.sleep(4)

        print("Your tenth card are your hopes and fears: " + card_10 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_10 + "\n")
        time.sleep(4)

        print("Your eleventh card signifies what the outcome is if things continue: " + card_11 + "\n")
        time.sleep(1)
        print("This card represents: " + card_explainer_11 + "\n")
        time.sleep(4)

        card_read_list =[]
        card_read_list.append(card_1)
        card_read_list.append(card_2)
        card_read_list.append(card_3)
        card_read_list.append(card_4)
        card_read_list.append(card_5)
        card_read_list.append(card_6)
        card_read_list.append(card_7)
        card_read_list.append(card_8)
        card_read_list.append(card_9)
        card_read_list.append(card_10)
        card_read_list.append(card_11)

        # return the list of 11 cards
        return card_read_list

def tell_fortune(card_set,reading_choice_str): 
    # This Function takes in the value of type of reading chosen, and the list of cards, then queries chatGPT for a reading.

    if reading_choice_str == "1":
        one_card_query = call_gpt(f"provide a single card tarot reading, using rider waite deck, single card meditation, for the following card: {card_set}, limit the answer to 800 characters, and do not give an intro in the response, just print the answer block. Also give a 4 sentence summary of the read at the end.")
        return one_card_query
    elif reading_choice_str == "2":
        five_card_query = call_gpt(f"provide a five card, rider waite deck read for the following list of cards: {card_set}, for the list of cards, interpret them the following way: card 1. Current situation, card 2. Your response, card 3. What's holding you back , card 4. What you should do, card 5. Outcome if actioned. limit the answer to 800 characters, and do not give an intro in the response, just print the answer block. Also give a 4 sentence summary of the read at the end.")
        return five_card_query
    elif reading_choice_str == "3":
        eleven_card_query = call_gpt(f"provide a eleven card, rider waite deck read for the following list of cards: {card_set}, for the list of cards, interpret them the following way: card 1. Significator, card 2. 'This covers it', card 3. 'This crosses it', card 4. Past influences, card 5. Near Future, card 6. Conscious Goal/Best Outcome, card 7. Unconscious influence / root, 8. You/your attitude, card 9. External influences, card 10. Hopes & Fears, card 11. Outcome if things continue. limit the answer to 800 characters, and do not give an intro in the response, just print the answer block. Also give a 4 sentence summary of the read at the end. ")
        return eleven_card_query

def get_user_info():
    # This function selects 3 random questions from the list above, to then hash into a single value for randomness for card pull and return it.
    
    print("\nBreathe in, breathe out, and feel your body and the air around it... \n")
    time.sleep(5)
    print("In order to add a bit of your essence to this mystical consultation, please answer the following questions about yourself. \n")
    time.sleep(2)
    question_1 = asker_questions_list.pop()
    question_2 = asker_questions_list.pop()
    question_3 = asker_questions_list.pop()

    answer_1 = hash(input(question_1 + " : "))
    answer_2 = hash(input(question_2 + " : "))
    answer_3 = hash(input(question_3 + " : "))

    hashed_value = answer_1 + answer_2 + answer_3
    return hashed_value

if __name__ == "__main__":
    main()
