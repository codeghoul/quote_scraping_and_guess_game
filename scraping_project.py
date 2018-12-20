import requests
from bs4 import BeautifulSoup
from csv import DictReader
from random import choice
from time import sleep

BASE_URL = "http://quotes.toscrape.com"


def read_quotes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quote_list):
    flag = True
    while flag:
        remaining_guess = 4
        quote_dict = choice(quote_list)
        quote, author, href = quote_dict['text'], quote_dict['author'], quote_dict['bio-link']
        print("Here's a quote: \n")
        print(quote + '\n')
        guess = ''
        while guess.lower() != author.lower() and remaining_guess:
            guess = input(f"Who said this? Guesses remaining: {remaining_guess}. ")
            if guess.lower() == author.lower():
                print("Congratulations!! You got it right!! \n")
                break
            remaining_guess -= 1
            print_hint(author, href, remaining_guess)
        flag = True if input(
            "Press 'yes' to play again: ").lower() == 'yes' else False


def print_hint(author, href, remaining_guess):
    if remaining_guess == 3:
        html = requests.get(f"{BASE_URL}{href}").text
        soup = BeautifulSoup(html, 'html.parser')
        birth_date = soup.find(class_='author-born-date').get_text()
        birth_place = soup.find(
            class_='author-born-location').get_text()
        print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
    elif remaining_guess == 2:
        hint = author.split()[0][0]
        print(f"Here's a hint: The author's first name starts with a {hint}.")
    elif remaining_guess == 1:
        hint = author.split()[-1][0]
        print(f"Here's a hint: The author's last name starts with a {hint}.")
    else:
        print(f"Oops! You ran out of guesses. The answer was {author}.\n")

if __name__ == '__main__':
    quotes = read_quotes("quotes.csv")
    start_game(quotes)
