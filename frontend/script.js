default_width = 9;
default_height = 9;
default_mine_count = 10;

// this is triggered when the window is loaded
window.onload = function() {
    console.log("Página carregada.");
    renderMenu();
};

function renderMenu() {
    const menu = document.getElementById('menu');
    menu.innerHTML = '';
    // Cria inputs com valores padrão

    menu.appendChild(document.createTextNode("Width: "));
    const widthInput = document.createElement('input');
    widthInput.type = 'number';
    widthInput.id = 'width';
    widthInput.value = default_width;
    menu.appendChild(widthInput);

    menu.appendChild(document.createTextNode("Height: "));
    const heightInput = document.createElement('input');
    heightInput.type = 'number';
    heightInput.id = 'height';
    heightInput.value = default_height;
    menu.appendChild(heightInput);

    menu.appendChild(document.createTextNode("Number of mines: "));
    const nminesInput = document.createElement('input');
    nminesInput.type = 'number';
    nminesInput.id = 'nmines';
    nminesInput.value = default_mine_count;
    menu.appendChild(nminesInput);

    const rebootButton = document.createElement('button');
    rebootButton.textContent = 'reboot?';
    rebootButton.id = 'rebootButton'
    menu.appendChild(rebootButton)

    rebootButton.addEventListener('click', newGame);

    [widthInput, heightInput, nminesInput].forEach(input => {
        input.addEventListener('change', newGame);
    });

    // Adiciona evento onchange que chama newGame()
    newGame(); // chama gameCreate com valores atuais
}

function newGame() {
    const width = parseInt(document.getElementById('width').value);
    const height = parseInt(document.getElementById('height').value);
    const mine_count = parseInt(document.getElementById('nmines').value);
    gameCreate(width, height, mine_count);
}

// frontend game creation request logic
async function gameCreate(width, height, mine_count) {
    try {
        // wait for the response of the open window
        const response = await fetch('http://localhost:8000/game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                width: width,
                height: height,
                mine_count: mine_count
            })
        });

        const data = await response.json();
        console.log('Game created successfully.\nGame data (JSON):', data);

        window.gameId = data.id;
        window.boardData = data.board;

        renderBoard(data.board); // calls board rendering logic
    } catch(error) {
        console.error('Error creating the game:', error);
    }
}

function renderBoard (boardData) {
    const app = document.getElementById('app');
    app.innerHTML = ''; // container cleaned

    const cols = boardData[0] ? boardData[0].length : 9;
    app.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
    
    for (let y = 0; y < boardData.length; y++) {
        const line = boardData[y];
        for (let x = 0; x < line.length; x++) {
            const cell = line[x];

            const div_cell = document.createElement('div');
            div_cell.className = 'cell';
            
            if (cell.is_flagged) div_cell.classList.add('flagged');
            if (cell.is_mine && cell.is_revealed) div_cell.classList.add('mine');

            // configure display text
            div_cell.textContent = '';
            if (cell.is_revealed) {
                div_cell.classList.add('revealed');
                if (cell.is_mine)
                    div_cell.textContent = '🟐';
                else if (cell.neighbor_mines)
                    div_cell.textContent = cell.neighbor_mines;
            }
            else if (cell.is_flagged)
                div_cell.textContent = '⚑';

            // save coordinates
            div_cell.dataset.x = x;
            div_cell.dataset.y = y;

            // add left click
            div_cell.addEventListener('click', function() {
                const x = parseInt(this.dataset.x);
                const y = parseInt(this.dataset.y);
                clickCell(x, y);
            });

            // add right click (flag)
            div_cell.addEventListener('contextmenu', function(event) {
                event.preventDefault(); // prevents menu
                const x = parseInt(this.dataset.x);
                const y = parseInt(this.dataset.y);
                flagCell(x, y);
            });

            // add cell to container
            app.appendChild(div_cell);
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
        
        if (data.state == 'lost') alert('KABOOM');
        else if (data.state == 'won') alert('YOU WIN');
        
        if (data) console.log('Clicked.');
        else console.error('An unknown error has occurred while trying to click.')
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
        
        if (data) console.log('Flagged.');
        else console.error('An unknown error has occurred while trying to flag.');

        window.boardData = data.board;
        renderBoard(data.board);
    } catch (error) {
        console.error('An error has occurred while trying to flag: ', error);
    }
}