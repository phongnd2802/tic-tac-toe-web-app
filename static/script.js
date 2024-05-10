const statusDisplay = document.querySelector('.game--status');

let gameActive = true;
let currentPlayer = "X";
let gameState = {}
let moves = []
let utility = 0
let apiResponseReceived = true;


function initialGame(){
    for(let i = 0; i < 3; i++){
        for(let j=0; j < 3; j++){
            const key = `${i},${j}`;
            const move = [i, j];
            moves.push(move);
            gameState[key] = "";
        }
    }
}


const drawMessage = () => `Game ended in a draw!`;
const currentPlayerTurn = () => `It's ${currentPlayer}'s turn`;

statusDisplay.innerHTML = currentPlayerTurn();



function handlePlayerChange() {
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    statusDisplay.innerHTML = currentPlayerTurn();
}

function handleCellPlayed(clickedCell, clickedCellIndex) {
    gameState[clickedCellIndex] = currentPlayer;
    clickedCell.innerHTML = currentPlayer;
}

function handleCheckGame(result){
    if(result === 0 || moves.length === 0){
        statusDisplay.innerHTML = "Draw!";
        gameActive = false;
    }else if(result === 1){
        statusDisplay.innerHTML = "X wins!";
        gameActive = false;
    }else if(result === -1){
        statusDisplay.innerHTML = "O wins!";
        gameActive = false;
    }
}

function arraysEqual(arr1, arr2){
    if(arr1.length !== arr2.length) return false;

    for(let i = 0; i < arr1.length; i++){
        if(arr1[i] !== arr2[i]) return false;
    }
    return true;
}

function handleCellClick(clickedCellEvent) {
    if(!apiResponseReceived){
        return;
    }
    const clickedCell = clickedCellEvent.target;
    const clickedCellIndex = clickedCell.getAttribute('data-cell-index');
    
    if(gameState[clickedCellIndex] !== "" || !gameActive)
        return;

    if(currentPlayer === "X"){
        handleCellPlayed(clickedCell, clickedCellIndex);

        const move = clickedCellIndex.split(",").map(coord => parseInt(coord));
        moves = moves.filter(item => !arraysEqual(item, move));
        handlePlayerChange();
    }
    apiResponseReceived = false;
    fetch('http://127.0.0.1:5000/api/move', {
    method: 'POST',
    'headers': {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        player: currentPlayer,
        utility: utility,
        board: gameState,
        moves: moves
    })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if(data.move === null){
            const result = parseInt(data.result);
            handleCheckGame(result);
            return;
        }
        const aiMove = data.move.join(',');
        moves = data.moves;
        utility = parseInt(data.utility);
        gameState[aiMove] = currentPlayer;
        const aiMoveCell = document.querySelector(`[data-cell-index="${aiMove}"]`);
        handleCellPlayed(aiMoveCell, aiMove);
        apiResponseReceived = true;
        handlePlayerChange();
        const result = parseInt(data.result);
        handleCheckGame(result);
    })
    .catch(error => {
        console.log("Error: ",error);;
    });
}

initialGame()
document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('click', handleCellClick));