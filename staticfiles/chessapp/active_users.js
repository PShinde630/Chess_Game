console.log("active_users.js loaded");

let activeGameId = null; // Track the active game ID
let isMoveInProgress = false; // Track if the user is entering a move
let ongoingPolling = false; // Prevent duplicate polling

// Poll for active users, pending challenges, and game state every 2 seconds
setInterval(() => {
    if (!ongoingPolling) {
        ongoingPolling = true; // Prevent parallel polling requests
        updateActivePlayers();
        fetchPendingChallenges();
        checkForOngoingGame();
        ongoingPolling = false;
    }
}, 4000);

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded");
    updateActivePlayers(); // Initial call to fetch active players
});

// Fetch active users
function updateActivePlayers() {
    fetch('/active-users/')
        .then(response => response.json())
        .then(data => {
            const activePlayersList = document.getElementById('active-players');
            activePlayersList.innerHTML = ''; // Clear previous list

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
        .catch(error => console.error('Error fetching active players:', error));
}

// Fetch pending challenges
function fetchPendingChallenges() {
    fetch('/pending-challenges/')
        .then(response => response.json())
        .then(data => {
            const gameInfo = document.getElementById('game-info');
            gameInfo.innerHTML = ''; // Clear previous content

            if (data.pending_challenges.length > 0) {
                data.pending_challenges.forEach(challenge => {
                    const div = document.createElement('div');
                    div.innerHTML = `
                        <p>${challenge.sender} has challenged you!</p>
                        <button class="btn btn-success" onclick="acceptChallenge(${challenge.id})">Accept</button>
                        <button class="btn btn-danger" onclick="declineChallenge(${challenge.id})">Decline</button>
                    `;
                    gameInfo.appendChild(div);
                });
            } else {
                gameInfo.innerHTML = '<p>No new challenges.</p>';
            }
        })
        .catch(error => console.error('Error fetching challenges:', error));
}

// Check if the user has an ongoing game
function checkForOngoingGame() {
    fetch('/ongoing-game/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.game_id) {
                activeGameId = data.game_id; // Track the active game ID
                renderChessboard(data.board, activeGameId); // Render the board
            }
        })
        .catch(error => console.error('Error checking for ongoing game:', error));
}

function renderChessboard(board, gameId, turn, playerColor) {
    const chessboardContainer = document.getElementById('chessboard-container');
    chessboardContainer.innerHTML = ''; // Clear previous board

    // Create the chessboard
    let tableHtml = '<table><tbody>';
    const colLabels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

    board.forEach((row, rowIndex) => {
        tableHtml += `<tr><th>${8 - rowIndex}</th>`; // Row numbers
        for (let [cellLabel, piece] of Object.entries(row)) {
            tableHtml += `<td id="${cellLabel}">${piece || ''}</td>`;
        }
        tableHtml += '</tr>';
    });

    tableHtml += '<tr><th></th>'; // Column labels
    colLabels.forEach(label => (tableHtml += `<th>${label}</th>`));
    tableHtml += '</tr></tbody></table>';

    // Player info section
    const playerInfoHtml = `
        <div id="player-info" class="text-center mt-3">
            <p>You are playing as <strong>${playerColor}</strong>.</p>
            <p>It's <strong>${turn === 'w' ? 'White' : 'Black'}</strong>'s turn to move.</p>
        </div>
    `;

    chessboardContainer.innerHTML = playerInfoHtml + tableHtml;

    // Add move form
    chessboardContainer.innerHTML += `
        <form id="moveForm" class="d-flex justify-content-center align-items-center gap-2 mt-3">
            <input type="text" id="uciInput" class="form-control w-50" placeholder="Enter move (e.g., e2e4)" required>
            <button type="submit" class="btn btn-primary">Move</button>
        </form>
    `;

    // Add resign button separately
    chessboardContainer.innerHTML += `
        <form id="resignButton" class="d-flex justify-content-center align-items-center gap-2 mt-3>
            <button id="resignButton" class="btn btn-danger">Resign</button>
        </form>
    `;

    // Attach event listeners
    const moveForm = document.getElementById('moveForm');
    moveForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const uciMove = document.getElementById('uciInput').value.trim();
        makeMove(gameId, uciMove);
    });

    const resignButton = document.getElementById('resignButton');
    resignButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to resign?')) {
            resignGame(gameId);
        }
    });
}

// Function to handle resignation
function resignGame(gameId) {
    fetch(`/resign-game/${gameId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('You have resigned.');
            location.reload(); // Reload to reset the game state
        } else {
            alert(data.message || 'Failed to resign.');
        }
    })
    .catch(error => console.error('Error resigning:', error));
}


// Function to make a move
function makeMove(gameId, move) {
    fetch(`/make-move/${gameId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            renderChessboard(data.board, gameId, data.turn, data.player_color); // Sync the board
        } else {
            alert(data.message || 'Invalid move');
        }
    })
    .catch(error => console.error('Error making move:', error));
}


// Send a challenge to another player
function sendChallenge(opponentId) {
    fetch('/challenge/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ opponent_id: opponentId })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Challenge sent:', data);
        alert('Challenge sent successfully!');
    })
    .catch(error => console.error('Error sending challenge:', error));
}

// Accept a challenge and start a game
function acceptChallenge(challengeId) {
    fetch(`/accept-challenge/${challengeId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            activeGameId = data.game_id; // Track the active game ID
            renderChessboard(data.board, data.game_id); // Render the chessboard
        } else {
            alert('Failed to start the game.');
        }
    })
    .catch(error => console.error('Error accepting challenge:', error));
}

// Decline a challenge
function declineChallenge(challengeId) {
    fetch(`/decline-challenge/${challengeId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchPendingChallenges(); // Refresh pending challenges
    })
    .catch(error => console.error('Error declining challenge:', error));
}
