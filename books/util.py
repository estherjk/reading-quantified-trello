"""
Helper functions that parse desired information from Trello cards (aka books).
"""

def get_created_action(card):
    """
    Return the date when a card was created.
    """
    if not card.actions:
        return

    for action in card.actions:
        if action['type'] == 'createCard':
            return action


def get_date_created_in_list(card, list_name):
    """
    Return the date a card was created in the specified list.
    """
    created_action = get_created_action(card)

    if not created_action:
        return

    if created_action['data']['list']['name'] == list_name:
        return created_action['date']


def get_list_change_date(card, list_before_name, list_after_name):
    """
    Return the date of when a list changed from the specified before & after lists.
    """
    if not card.actions:
        return

    for action in card.actions:
        if all(key in action['data'] for key in ['listBefore', 'listAfter']):
            if action['data']['listBefore']['name'] == list_before_name and action['data']['listAfter']['name'] == list_after_name:
                return action['date']


def get_date_started(card):
    """
    Return the date when a book (card) was started, i.e. moved to or created in the 'Reading' list.
    """
    return get_date_created_in_list(card, 'Reading') or \
        get_list_change_date(card, 'To Read', 'Reading') or \
        get_list_change_date(card, 'Backlog', 'Reading')


def get_date_finished(card):
    """
    Return the date when a book (card) was finished, i.e. moved from the 'Reading' to the 'Finished' list.
    """
    return get_list_change_date(card, 'Reading', 'Finished')


def remove_cover_attachment_previews(cover_attachment):
    """
    Remove the previews element from cover_attachment. It contains a lot of data. Then, return.
    """

    del cover_attachment["previews"]

    return cover_attachment