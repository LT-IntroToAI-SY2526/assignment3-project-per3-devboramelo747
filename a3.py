# Important variables:
#     movie_db: list of 4-tuples (imported from movies.py)
#     pa_list: list of pattern-action pairs (queries)
#       pattern - strings with % and _ (not consecutive)
#       action  - return list of strings

# THINGS TO ASK THE MOVIE CHAT BOT:
# what movies were made in _ (must be date, because we don't have location)
# what movies were made between _ and _
# what movies were made before _
# what movies were made after _
# who directed %
# who was the director of %
# what movies were directed by %
# who acted in %
# when was % made
# in what movies did % appear
# bye

#  Include the movie database, named movie_db
from movies import movie_db
from match import match
from typing import List, Tuple, Callable, Any

# The projection functions, that give us access to certain parts of a "movie" (a tuple)
def get_title(movie: Tuple[str, str, int, List[str], str]) -> str:
    return movie[0]


def get_director(movie: Tuple[str, str, int, List[str], str]) -> str:
    return movie[1]


def get_year(movie: Tuple[str, str, int, List[str], str]) -> int:
    return movie[2]


def get_actors(movie: Tuple[str, str, int, List[str], str]) -> List[str]:
    return movie[3]

def get_genre(movie: Tuple[str, str, int, List[str], str]) -> List[str]:
    return movie[4]


# Below are a set of actions. Each takes a list argument and returns a list of answers
# according to the action and the argument. It is important that each function returns a
# list of the answer(s) and not just the answer itself.


def title_by_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    result = []

    for movie in movie_db:
        if get_year(movie) == year:
            result.append(get_title(movie))
    
    return result


def title_by_year_range(matches: List[str]) -> List[str]:
    result = []
    starting_year = int(matches[0])
    ending_year = int(matches[1])

    for movie in movie_db:
        movie_year = get_year(movie)
        if starting_year <= movie_year <= ending_year:
            result.append(get_title(movie))
    
    return result


def title_before_year(matches: List[str]) -> List[str]:
    result = []
    year = int(matches[0])

    for movie in movie_db:
        movie_year = get_year(movie)
        if movie_year < year:
            result.append(get_title(movie))
    
    return result


def title_after_year(matches: List[str]) -> List[str]:
    result = []
    year = int(matches[0])

    for movie in movie_db:
        movie_year = get_year(movie)
        if year < movie_year:
            result.append(get_title(movie))
    
    return result


def director_by_title(matches: List[str]) -> List[str]:
    title = matches[0]
    result = []

    for movie in movie_db:
        if get_title(movie) == title:
            result.append(get_director(movie))
    
    return result


def title_by_director(matches: List[str]) -> List[str]:

    result = []
    director = matches[0]

    for movie in movie_db:
        if get_director(movie) == director:
            result.append(get_title(movie))
    
    return result


def actors_by_title(matches: List[str]) -> List[str]:
    result = []
    title = (matches[0])

    for movie in movie_db:
        if get_title(movie) == title:
            result = (get_actors(movie))
            break

    return result


def year_by_title(matches: List[str]) -> List[int]:
    result = []
    title = matches[0]

    for movie in movie_db:
        if get_title(movie) == title:
            result.append(get_year(movie))


    return result


def title_by_actor(matches: List[str]) -> List[str]:
    result = []
    actor_name = matches[0]

    for movie in movie_db:
        actors = get_actors(movie)

        for actor in actors:
            if actor_name in actor:
                result.append(get_title(movie))
                break
    
    
    return result

def actors_by_director(matches: List[str]) -> List[str]:
    result = []
    director = matches[0]

    for movie in movie_db:
        if get_director == director:
            result = get_actors(movie)
            break
     
    return result

def genre_by_title(matches: List[str]) -> List[str]:
    result = []
    title = matches[0]

    for movie in movie_db:
        if get_title == title:
            result.append.get_genre(movie)
    
    return result

def title_by_genre(matches: List[str]) -> List[str]:
    result = []
    genre = matches[0]

    for movie in movie_db:
        if get_genre == genre:
            result.append.get_title(movie)


# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# The pattern-action list for the natural language query system A list of tuples of
# pattern and action It must be declared here, after all of the function definitions
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what movies were made in _"), title_by_year),
    (str.split("what movies were made between _ and _"), title_by_year_range),
    (str.split("what movies were made before _"), title_before_year),
    (str.split("what movies were made after _"), title_after_year),
    # note there are two valid patterns here two different ways to ask for the director
    # of a movie
    (str.split("who directed %"), director_by_title),
    (str.split("who was the director of %"), director_by_title),
    (str.split("what movies were directed by %"), title_by_director),
    (str.split("who acted in %"), actors_by_title),
    (str.split("when was % made"), year_by_title),
    (str.split("in what movies did % appear"), title_by_actor),
    (str.split("who acted in movies directed by %"), actors_by_director),
    (str.split("what genre is %"), genre_by_title),
    (str.split("what movies are in the % genre"), title_by_genre),
    (["bye"], bye_action),
    









    (str.split("in what year was % made"), year_by_title),
    (str.split("what was the year when % was made"), year_by_title),
    (str.split("In what annum was the cinematic production of % brought to fruition and subsequently released for public consumption?"), year_by_title),
]
def search_pa_list(src: List[str]) -> List[str]:
    for pat, act in pa_list:
        print(f"pattern: {pat}, source: {src}, action {act}")
        mat = match(pat, src)
        print(f"match: {mat}")

        if mat is not None:
            ans = act(mat)
            print(f"answer: {ans}")
            return ans if ans else ["No answers"]
    
    return["I don't understand"]


def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully.
    """
    print("Welcome to the movie database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nSo long!\n")

def beast_search(matches: List[str]) -> List[str]:
    result = []
    beast = matches[0]

    for movie in movie_db:
        if get_director == beast:
            result = get_actors(movie)
            break
    
    return result 