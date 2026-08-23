// this is triggered when the window is loaded
window.onload = function() {
    console.log("Página carregada.");
    gameCreate();
};

// frontend game creation request logic
async function gameCreate() {
    try {
        // wait for the response of the open window
        const response = await fetch('http://localhost:8000/game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                width: 9,
                height: 9,
                mine_count: 10
            })
        });

        const data = await response.json();
        console.log('Game created successfully: ', data);

        window.gameId = data.id;
        window.boardData = data.board;

        renderBoard(data.board); // calls board rendering logic
    } catch(error) {
        console.error('Error creating a game:', error);
    }
}

function renderBoard (boardData) {
    const app = document.getElementById('app');
    app.innerHTML = ''; // container cleaned

    for (let y = 0; y < boardData.length; y++) {
        const line = boardData[y];
        for (let x = 0; x < line.length; x++) {
            const cell = line[x];

            const div = document.createElement('div');
            div.className = 'cell';
            
            if (cell.is_flagged) div.classList.add('flagged');
            if (cell.is_mine && cell.is_revealed) div.classList.add('mine');

            // configure display text
            div.textContent = '';
            if (cell.is_revealed) {
                div.classList.add('revealed');
                if (cell.is_mine)
                    div.textContent = '🟐';
                else if (cell.neighbor_mines)
                    div.textContent = cell.neighbor_mines;
            }
            else if (cell.is_flagged)
                div.textContent = '⚑';

            // save coordinates
            div.dataset.x = x;
            div.dataset.y = y;

            // add left click
            div.addEventListener('click', function() {
                const x = parseInt(this.dataset.x);
                const y = parseInt(this.dataset.y);
                clickCell(x, y);
            });

            // add right click (flag)
            div.addEventListener('contextmenu', function(event) {
                event.preventDefault(); // prevents menu
                const x = parseInt(this.dataset.x);
                const y = parseInt(this.dataset.y);
                flagCell(x, y);
            });

            // add cell to container
            app.appendChild(div);
        }
    }
}

// cell click logic
async function clickCell(x, y) {
    try {
        // sends the click to the backend
        const response = await fetch(`http://localhost:8000/game/${window.gameId}/click`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                x: x,
                y: y
            })
        });

        // awaits for the response (updated game json)
        const data = await response.json();

        window.boardData = data.board;
        renderBoard(data.board);

        console.log('Click response: ', data);

        // verify endgame
        if (data.state == 'lost') alert('KABOOM');
        else if (data.state == 'won') alert('YOU WIN');
    } catch (error) {
        console.error('An error has occurred while trying to click: ', error);
    }
}

async function flagCell(x, y) {
    try {
        const response = await fetch(`http://localhost:8000/game/${window.gameId}/flag`, {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({
                x: x,
                y: y
            })
        });

        const data = await response.json();
        console.log('Flag response: ', data);

        window.boardData = data.board;
        renderBoard(data.board);
    } catch (error) {
        console.error('An error has occurred while trying to flag: ', error);
    }
}