let cellCount = 0;

function addCodeCell() {
    const cellsDiv = document.getElementById('codeCells');
    const newCell = document.createElement('div');
    newCell.className = 'code-cell';
    newCell.innerHTML = `
        <label for="cell_${cellCount}">Code Cell ${cellCount + 1}:</label>
        <textarea name="cell_${cellCount}" id="cell_${cellCount}" 
                  placeholder="Enter Python code here..." required></textarea>
        <button type="button" class="remove-cell" 
                onclick="removeCodeCell(this.parentElement)">Remove Cell</button>
    `;
    cellsDiv.appendChild(newCell);
    cellCount++;
}

function removeCodeCell(cell) {
    cell.remove();
    // Renumber remaining cells
    const cells = document.getElementsByClassName('code-cell');
    for (let i = 0; i < cells.length; i++) {
        const label = cells[i].getElementsByTagName('label')[0];
        label.textContent = `Code Cell ${i + 1}:`;
    }
}

// Add first cell when page loads
document.addEventListener('DOMContentLoaded', function() {
    addCodeCell();
});