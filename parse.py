# Helper functions that parse desired information from Trello cards (aka books)

def get_created_action(card):
    """
    Return the date when a card was created.
    """
    if not card.actions:
        return

    for action in card.actions:
        if action['type'] == 'createCard':
            return action


def get_list_change_date(card, list_before, list_after):
    """
    Return the date of when a list change occurred.
    """
    if not card.actions:
        return

    for action in card.actions:
        if action['data']['listBefore']['name'] == list_before and action['data']['listAfter']['name'] == list_after:
            return action['date']


def get_date_started(card):
    """
    Return the date when a book (card) was started, i.e. moved to or created in the 'Reading' list
    """
    # Check if the card was created in the Reading list
    created_action = get_created_action(card)
    date_started = None
    if created_action['data']['list']['name'] == 'Reading':
        date_started = created_action['date']

    return date_started or \
        get_list_change_date(card, 'To Read', 'Reading') or \
        get_list_change_date(card, 'Backlog', 'Reading')


def get_date_finished(card):
    """
    Return the date when a book (card) was finished, i.e. moved from the 'Reading' to the 'Finished' list
    """
    return get_list_change_date(card, 'Reading', 'Finished')
