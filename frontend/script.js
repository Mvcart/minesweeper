default_width = 9;
default_height = 9;
default_mine_count = 10;

// this is triggered when the window is loaded
window.onload = function() {
    console.log("Página carregada.");
    renderMenu();
};

function renderMenu() {
    updateMessage('Preparing your game...', 'yellow');

    // Cria inputs com valores padrão
    addInput('parameters', 'width', default_width, 'number', 'Width:')
    addInput('parameters', 'height', default_height, 'number', 'Height:')
    addInput('parameters', 'nmines', default_mine_count, 'number', 'Number of mines:')
    addButton('buttons', 'rebootButton', 'reboot?');

    // Adiciona evento onchange que chama newGame()
    newGame(); // chama gameCreate com valores atuais
}

async function newGame() {
    updateMessage('Preparing your game...', 'yellow');
    const width = parseInt(document.getElementById('width').value);
    const height = parseInt(document.getElementById('height').value);
    const mine_count = parseInt(document.getElementById('nmines').value);
    await gameCreate(width, height, mine_count);
    updateMessage('Playing...', 'yellow');
}

function updateMessage(text, type) {
    div_message = document.getElementById('message');
    div_message.textContent = text;
    div_message.className = type;
}

function addInput(parentId, elementId, value, type, text_message) {
    const parent = document.getElementById(parentId);

    const newInput = document.createElement('input');

    parent.appendChild(document.createTextNode(text_message));

    newInput.type = type;
    newInput.id = elementId;
    newInput.value = value;
    parent.appendChild(newInput);
    newInput.addEventListener('change', newGame);
}

function addButton(parentId, elementId, value) {
    const container = document.getElementById(parentId);

    const newButton = document.createElement('button');

    newButton.id = elementId;
    newButton.textContent = value;
    container.appendChild(newButton);
    newButton.addEventListener('click', newGame);
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

function createCellElement(app, cell) {
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
    div_cell.dataset.x = cell.x;
    div_cell.dataset.y = cell.y;

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

function renderBoard (boardData) {
    const app = document.getElementById('app');
    app.innerHTML = ''; // container cleaned

    const cols = boardData[0] ? boardData[0].length : 9;
    app.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
    
    for (let y = 0; y < boardData.length; y++) {
        const line = boardData[y];
        for (let x = 0; x < line.length; x++) {
            const cell = line[x];
            createCellElement(app, cell);
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
        
        if (data.state == 'lost') updateMessage('KABOOM', 'red');
        else if (data.state == 'won') updateMessage('YOU WIN', 'green');
        
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