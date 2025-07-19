from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .utils import fen_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import chess
import json
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from .models import GameRequest, ChessGame

def signup_view(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('home')
    else:
        signup_form = UserCreationForm()
    return render(request, 'signup.html', {'form': signup_form})


@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    Session.objects.filter(session_key=request.session.session_key).delete()
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('sessionid')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
def home(request):
    
    c_game = ChessGame.objects.filter(marked=False, player1=request.user).first() or ChessGame.objects.filter(marked=False, player2=request.user).first()

    if c_game:
       
        return redirect('game_page', game_id=c_game.id)
  
    active_users = get_logged_in_users().exclude(id=request.user.id)
    player1_games = ChessGame.objects.filter(player1=request.user, p1_visible=True)
    player2_games = ChessGame.objects.filter(player2=request.user, p2_visible=True)
    games = list(player1_games) + list(player2_games)

    games_moves = []
    for game in games:
        user_moves = game.get_user_moves(request.user)
        opponent = game.player1 if game.player2 == request.user else game.player2
        is_winner = game.winner == request.user
        is_loser = game.loser == request.user

        games_moves.append({
            'game': game,
            'opponent': opponent,
            'user_moves': user_moves,
            'is_winner': is_winner,
            'is_loser': is_loser,
        })

    context = {
        'active_users': active_users,
        'games_with_moves': games_moves,
    }
    
    return render(request, 'home.html', context)


@csrf_exempt
@login_required
def challenge(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            opponent_id = data.get('opponent_id')

            if not opponent_id:
                return JsonResponse({'error': 'opponent_id is required.'}, status=400)

            opponent = User.objects.get(id=opponent_id)
           
            if ongoing_game_present(request.user) or ongoing_game_present(opponent):
                return JsonResponse({'status': 'error', 'message': 'One or both players are already in an ongoing game.'}, status=400)
          
            GameRequest.objects.create(sender=request.user, receiver=opponent)

            return JsonResponse({'status': 'success', 'message': 'Challenge sent!'})
        
        except (json.JSONDecodeError, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid opponent.'}, status=400)


def ongoing_game_present(user):
    return ChessGame.objects.filter(marked=False,player1=user).exists() or ChessGame.objects.filter(marked=False,player2=user
    ).exists()



@login_required
def pending_challenges_view(request):
    challenges = GameRequest.objects.filter(receiver=request.user, marked=False)
    data = [{'id': c.id, 'sender': c.sender.username} for c in challenges]
    return JsonResponse({'pending_challenges': data})


def is_valid_fen(fen):
    try:
        board = chess.Board(fen)  
        return True
    except ValueError:
        return False


@csrf_exempt
@login_required
def accept_challenge_view(request, challenge_id):
    challenge_status = get_object_or_404(GameRequest, id=challenge_id, receiver=request.user)
    board = chess.Board()  
    initial_FEN = board.fen()
   
    if not is_valid_fen(initial_FEN):
        return JsonResponse({'status': 'error', 'message': 'Invalid intial FEN.'})
    
    game = ChessGame.objects.create(player1=challenge_status.sender,player2=challenge_status.receiver,fen=initial_FEN
    )
    
    challenge_status.marked = True
    challenge_status.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Game started!',
        'board': fen_to_dict(game.fen),
        'game_id': game.id,
        'redirect_url': '/'
    })


@csrf_exempt
@login_required
def decline_challenge_view(request, challenge_id):
    challenge = get_object_or_404(GameRequest, id=challenge_id, receiver=request.user)
    challenge.marked = True
    challenge.save()
    return JsonResponse({'status': 'success', 'message': 'Challenge declined!'})

def get_logged_in_users():
    active_sessions = Session.objects.filter(expire_date__gte=now())
    user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]
    return User.objects.filter(id__in=user_ids, is_active=True).distinct()

def active_users_view(request):
    users = get_logged_in_users().exclude(id=request.user.id)
    data = {'active_users': [{'id': user.id, 'username': user.username} for user in users]}
    return JsonResponse(data)

@csrf_exempt
@login_required
def game_state(request, game_id):
    game = get_object_or_404(ChessGame, id=game_id)

    board_dict = fen_to_dict(game.fen)
    fen_parts = game.fen.split()  

    if len(fen_parts) > 1:  
        turn = fen_parts[1]  
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid FEN format'})

    player_color = (
        'White' if game.player1 == request.user else 
        'Black' if game.player2 == request.user else 
        'Spectator'
    )
    
    return JsonResponse({
        'status': 'success',
        'board': board_dict,
        'game_id': game.id,
        'turn': turn,
        'player_color': player_color
    })


@csrf_exempt
@login_required
def process_view(request, game_id):
    game = get_object_or_404(ChessGame, id=game_id)
    move = json.loads(request.body).get('move')
    board = chess.Board(game.fen)         
    current_turn = 'White' if board.turn == chess.WHITE else 'Black'
        
    if (current_turn == 'White' and game.player1 != request.user) or \
       (current_turn == 'Black' and game.player2 != request.user):
        return JsonResponse({'status': 'error', 'message': 'Not your turn to play.'})

    if chess.Move.from_uci(move) in board.legal_moves:
        board.push(chess.Move.from_uci(move))  
        new_fen = board.fen()  

        if not is_valid_fen(new_fen):
            return JsonResponse({'status': 'error', 'message': 'Invalid FEN generated after move.'})

        game.fen = new_fen  
        game.last_move = move
                
        if game.player1 == request.user:
            game.num_moves_player1 += 1
        elif game.player2 == request.user:
            game.num_moves_player2 += 1
        game.save()

        if board.is_checkmate():
            winner = game.player1 if board.turn == chess.BLACK else game.player2
            loser = game.player2 if winner == game.player1 else game.player1
            game.winner = winner
            game.loser = loser
            game.marked = True  
            game.save()
            return JsonResponse({
                'status': 'success',
                'checkmate': True,
                'winner': winner.username,
                'redirect_url': '/'
            })
        elif board.is_stalemate():
            game.marked = True  
            game.save()
            return JsonResponse({
                'status': 'success',
                'stalemate': True,
                'redirect_url': '/'
            })

        return JsonResponse({
            'status': 'success',
            'board': fen_to_dict(game.fen),
            'turn': game.fen.split()[1] 
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid move'})


@csrf_exempt
@login_required
def ongoing_game(request):
    try:
        game = ChessGame.objects.filter(
            marked=False, player1=request.user
        ).first() or ChessGame.objects.filter(
            marked=False, player2=request.user
        ).first()

        if game:
            if not is_valid_fen(game.fen):
                return JsonResponse({'status': 'error', 'message': 'Invalid FEN format in ongoing game.'})

            board_dict = fen_to_dict(game.fen)
            turn = game.fen.split()[1]

            if game.marked: 
                outcome = "win" if game.winner == request.user else "loss"
                return JsonResponse({
                    'status': 'game_over',
                    'outcome': outcome,
                    'winner': game.winner.username,
                })

            return JsonResponse({
                'status': 'success',
                'game_id': game.id,
                'board': board_dict,
                'turn': turn,
                'player_color': 'White' if game.player1 == request.user else 'Black'
            })
        else:
            return JsonResponse({'status': 'no_active_game'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@csrf_exempt
@login_required
def resign_game_view(request, game_id):
    game = get_object_or_404(ChessGame, id=game_id)

    if game.player1 == request.user:
        winner = game.player2
        loser = game.player1
    elif game.player2 == request.user:
        winner = game.player1
        loser = game.player2
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not a participant in this game.'})

    game.marked = True  
    game.winner = winner
    game.loser = loser
    game.outcome = 'win'  
    game.save()

    return JsonResponse({'status': 'success', 'message': f'{loser.username} resigned. {winner.username} wins.','redirect_url': '/'})


@login_required
def game_page(request, game_id):
    game = get_object_or_404(ChessGame, id=game_id)
    
    player_color = 'White' if game.player1 == request.user else 'Black'
    turn = 'White' if game.fen.split()[1] == 'w' else 'Black'
    context = {'game': game,'player_color': player_color,'turn': turn,
    }
    return render(request, 'game.html', context)

@csrf_exempt
@login_required
def history(request):
    games = ChessGame.objects.filter(player1=request.user) | ChessGame.objects.filter(player2=request.user)
    games = games.order_by('-id')  
    return render(request, 'home.html', {'games': games})

@csrf_exempt
@login_required
def edit_journal(request, game_id):
    c_game = get_object_or_404(
        ChessGame, 
        Q(player1=request.user) | Q(player2=request.user), 
        id=game_id
    )
 
    if c_game.player1 == request.user:
        journal_entry = c_game.p1_journal_entry
    else:
        journal_entry = c_game.p2_journal_entry

    if request.method == 'POST':
        description = request.POST.get('description', '')
        entry = request.POST.get('entry', '')
        
        journal_entry = {'description': description, 'entry': entry}

        if c_game.player1 == request.user:
            c_game.p1_journal_entry = journal_entry
        else:
            c_game.p2_journal_entry = journal_entry

        c_game.save()
        return redirect('home')

    context = {'game': c_game, 'journal_entry': journal_entry}
    return render(request, 'edit_game.html', context)

@csrf_exempt
@login_required
def delete_journal(request, game_id):
    if request.method == 'POST':
        c_game = get_object_or_404(ChessGame, id=game_id)
        
        if c_game.player1 == request.user:
            c_game.p1_visible = False
        elif c_game.player2 == request.user:
            c_game.p2_visible = False
        else:
            return JsonResponse({'status': 'error', 'message': 'Not permitted to delete this game.'})

        c_game.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


def chesshistory_view(request):
    return render(request, 'history.html')

def rules_view(request):
    return render(request, 'rules.html')

def about_view(request):
    return render(request, 'about.html')







