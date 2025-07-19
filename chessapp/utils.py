# chessapp/utils.py

def fen_to_dict(fen_string):
    piece_to_html = {
        'K': '&#9812;', 'Q': '&#9813;', 'R': '&#9814;', 'B': '&#9815;',
        'N': '&#9816;', 'P': '&#9817;', 'k': '&#9818;', 'q': '&#9819;',
        'r': '&#9820;', 'b': '&#9821;', 'n': '&#9822;', 'p': '&#9823;',
    }

    position_part = fen_string.split(' ')[0]
    ranks = position_part.split('/')
    rows_list = []

    for rank_index, rank_str in enumerate(ranks):
        rank_number = 8 - rank_index  # Rank numbers 8 to 1
        rank_dict = {}
        file_index = 0  # Files 'a' to 'h'

        for c in rank_str:
            if c.isdigit():
                for _ in range(int(c)):
                    file_letter = chr(ord('a') + file_index)
                    position = f"{file_letter}{rank_number}"
                    rank_dict[position] = '&nbsp;'
                    file_index += 1
            else:
                file_letter = chr(ord('a') + file_index)
                position = f"{file_letter}{rank_number}"
                rank_dict[position] = piece_to_html.get(c, '&nbsp;')
                file_index += 1

        rows_list.append(rank_dict)

    return rows_list
