console.log("active_users.js loaded");

let ismoveprog = false;
let pollingActive = false;
let actGameid = null;

setInterval(() => {
    if (!pollingActive) {
        pollingActive = true;
       modifyActivePlayers();
        fetchingPendChallenges();
        checkingongoingGame();
        pollingActive = false;
    }
}, 2000);

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded");
   modifyActivePlayers();
});


function modifyActivePlayers() {
    fetch('/active-users/')
        .then(response => response.json())
        .then(data => {
            const activePlayersList = document.getElementById('active-players');
            activePlayersList.innerHTML = '';

            if (data.active_users.length > 0) {
                data.active_users.forEach(user => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                    listItem.innerHTML = `
                        ${user.username}
                        <button class="btn btn-sm btn-primary" onclick="sendChallenge(${user.id})">Challenge</button>
                    `;
                    activePlayersList.appendChild(listItem);
                });
            } else {
                activePlayersList.innerHTML = '<li class="list-group-item">No active players available.</li>';
            }
        })
        .catch(error => console.error('Error fetching active users:', error));
}

function checkingongoingGame() {
    if (ismoveprog) return;

    fetch('/ongoing-game/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.game_id) {
                actGameid = data.game_id;
                if (window.location.pathname === '/') {
                    window.location.href = `/game/${actGameid}/`;
                }
                renderChessboard(data.board, actGameid, data.turn, data.player_color);
            } else if (data.status === 'no_active_game') {
                document.getElementById('chessboard-container').innerHTML = '<p>No active game.</p>';
                window.location.href = '/';
            } else if (data.status === 'game_over') {
                const outcomeMessage = `Game Over! ${data.winner} wins.`;
                const alertElement = document.getElementById('gameOutcomeAlert');
                document.getElementById('gameOutcomeMessage').innerText = outcomeMessage;
                alertElement.style.display = 'block';
                window.location.href = '/';
            }
        })
        .catch(error => console.error('Error checking for ongoing game:', error));
}


function fetchingPendChallenges() {
    fetch('/pending-challenges/')
        .then(response => response.json())
        .then(data => {
            const gameInfo = document.getElementById('game-info');
            gameInfo.innerHTML = '';

            if (data.pending_challenges.length > 0) {
                data.pending_challenges.forEach(challenge => {
                    const div = document.createElement('div');
                    div.innerHTML = `
                        <p>${challenge.sender} has challenged you!</p>
                        <button class="btn btn-success" onclick="accptchallenge(${challenge.id})">Accept</button>
                        <button class="btn btn-danger" onclick="dclchallenge(${challenge.id})">Decline</button>
                    `;
                    gameInfo.appendChild(div);
                });
            } else {
                gameInfo.innerHTML = '<p>No new challenges.</p>';
            }
        })
        .catch(error => console.error('Error fetching challenges:', error));
}


function renderChessboard(board, gameId, turn, playerColor) {
    const chessboardContainer = document.getElementById('chessboard-container');

    if (ismoveprog) return;

    chessboardContainer.innerHTML = '';

    let timestamp = new Date().getTime();

    let tableHtml = `<table class="table-bordered" data-timestamp="${timestamp}"><tbody>`;
    const colLabels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    board.forEach((row, rowIndex) => {
        tableHtml += `<tr><th>${8 - rowIndex}</th>`;
        Object.entries(row).forEach(([cellLabel, piece]) => {
            tableHtml += `
                <td id="${cellLabel}" style="width: 75px; height: 75px; font-size: 60px;
                    text-align: center; vertical-align: middle;">
                    ${piece || ''}
                </td>`;
        });
        tableHtml += '</tr>';
    });

    tableHtml += '<tr><th></th>';
    colLabels.forEach(label => {
        tableHtml += `<th>${label}</th>`;
    });
    tableHtml += '</tr></tbody></table>';

    const playerInfoHtml = `
        <div id="player-info" class="text-center mt-3">
            <p>You are playing as <strong>${playerColor}</strong>.</p>
            <p>It's <strong>${turn === 'w' ? 'White' : 'Black'}</strong>'s turn to move.</p>
        </div>
    `;

    chessboardContainer.innerHTML = playerInfoHtml + tableHtml;

    const isPlayerTurn = (turn === 'w' && playerColor === 'White') ||
        (turn === 'b' && playerColor === 'Black');

    chessboardContainer.innerHTML += `
        <form id="moveForm" class="d-flex justify-content-center align-items-center gap-2 mt-3">
            <input type="text" id="uciInput" class="form-control w-50" 
                   placeholder="Enter move (e.g., e2e4)" required ${!isPlayerTurn ? 'disabled' : ''}>
            <button type="submit" class="btn btn-primary" ${!isPlayerTurn ? 'disabled' : ''}>Move</button>
            <button type="button" id="resignButton" class="btn btn-danger">Resign</button>
        </form>
    `;


    const moveForm = document.getElementById('moveForm');
    moveForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const uciMove = document.getElementById('uciInput').value.trim();
        if (uciMove.length === 4) {
            makeMove(gameId, uciMove);
        } else {
            alert("Invalid move! Please enter a valid UCI move (e.g., e2e4).");
        }
    });

    const resignButton = document.getElementById('resignButton');
    resignButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to resign?')) {
            resginChessgame(gameId);
        }
    });

    moveForm.addEventListener('focusin', () => (ismoveprog = true));
    moveForm.addEventListener('focusout', () => (ismoveprog = false));
}



function resginChessgame(gameId) {
    fetch(`/resign-game/${gameId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('You have resigned from the game.');
                window.location.href = data.redirect_url;

            } else {
                alert(data.message || 'Failed to resign.');
            }
        })
        .catch(error => console.error('Error resigning game:', error));
}

function makeMove(gameId, move) {
    ismoveprog = true;

    applymovetouserint(move.slice(0, 2), move.slice(2));

    fetch(`/make-move/${gameId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move: move })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.checkmate) {
                    alert(`Checkmate! ${data.winner} wins.`);
                    window.location.href = data.redirect_url;
                } else if (data.stalemate) {
                    alert("The game is a draw by stalemate.");
                    window.location.href = data.redirect_url;
                } else {

                    renderChessboard(data.board, gameId, data.turn, data.player_color);
                }
            } else {
                alert(data.message || 'Invalid move');
                fetchGameState(gameId);
            }
        })
        .catch(error => {
            console.error('Error making move:', error);
            fetchGameState(gameId);
        })
        .finally(() => {
            ismoveprog = false;
        });
}


function applymovetouserint(src, dest) {
    const srcCell = document.getElementById(src);
    const destCell = document.getElementById(dest);

    if (srcCell && destCell) {
        destCell.innerHTML = srcCell.innerHTML;
        srcCell.innerHTML = '';
    }
}



function sendChallenge(opponentId) {
    fetch('/challenge/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ opponent_id: opponentId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Challenge sent successfully!');
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error('Error sending challenge:', error));
}


function accptchallenge(challengeId) {
    fetch(`/accept-challenge/${challengeId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                actGameid = data.game_id;
                window.location.href = data.redirect_url;
                renderChessboard(data.board, data.game_id, data.turn, data.player_color);
            } else {
                alert('Failed to start the game.');
            }
        })
        .catch(error => console.error('Error accepting challenge:', error));
}


function dclchallenge(challengeId) {
    fetch(`/decline-challenge/${challengeId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchingPendChallenges();
        })
        .catch(error => console.error('Error declining challenge:', error));
}


let gameIdToDelete = null;

document.getElementById('deleteModal').addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    gameIdToDelete = button.getAttribute('data-game-id');
});


document.getElementById('confirmDelete').addEventListener('click', function () {
    fetch(`/delete-game/${gameIdToDelete}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            } else {
                alert('Failed to delete the game.');
            }
        })
        .catch(error => console.error('Error deleting game:', error));
});







