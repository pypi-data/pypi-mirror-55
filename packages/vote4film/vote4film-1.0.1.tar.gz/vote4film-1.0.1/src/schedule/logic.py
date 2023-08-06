from operator import attrgetter

from calender.models import Event, Register
from films.models import Film


def get_schedule():
    """Return a list of (Event, Film) based on votes and the register."""
    event = Event.objects.future_events().first()
    if not event:
        return (None, None)

    film = preferred_film(event)
    return (event, film)


def preferred_film(event):
    """Return the preferred film for the given event."""
    present_users = set(
        register.user for register in Register.objects.present_for(event)
    )
    absent_users = set(register.user for register in Register.objects.absent_for(event))
    films = films_by_score(present_users, absent_users)
    return films[0]


def films_by_score(present_users, absent_users):
    films = (
        Film.objects.potentially_watchable()
        .prefetch_related("vote_set")
        .prefetch_related("vote_set__user")
    )
    if not films:
        return [None]

    score_films(films, present_users, absent_users)
    # TODO: Then sort by when added
    return sorted(films, key=attrgetter("_schedule_score"), reverse=True)


def score_films(films, present_users, absent_users):
    for film in films:
        score_film(film, present_users, absent_users)


def score_film(film, present_users, absent_users):
    film._schedule_score = 0
    for vote in film.vote_set.all():
        score = vote.choice
        if vote.user in present_users:
            film._schedule_score += score
        elif vote.user in absent_users:
            film._schedule_score -= score
