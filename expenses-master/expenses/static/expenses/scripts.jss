document.addEventListener("DOMContentLoaded", function() {
    const jsonFileSelect = document.getElementById("json_file");
    const viewExpensesButton = document.getElementById("view_expenses");
    const expensesDetailsContainer = document.querySelector(".expenses-details table");

    viewExpensesButton.addEventListener("click", function() {
        const selectedFile = jsonFileSelect.value;
        if (selectedFile) {
            fetch(`/view_expenses/?file=${selectedFile}`)
                .then(response => response.json())
                .then(data => {
                    let tableContent = "<tr><th>Date</th><th>Expense Name</th><th>Amount</th></tr>";
                    for (const entry of data) {
                        tableContent += `<tr><td>${entry.date}</td><td>${entry.expense_name}</td><td>${entry.amount}</td></tr>`;
                    }
                    expensesDetailsContainer.innerHTML = tableContent;
                });
        }
    });
});

