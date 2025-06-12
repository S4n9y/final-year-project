    // Get form elements
    const expenseForm = document.getElementById("expenseForm");
    const expenseTable = document.getElementById("expenseTable");

    // Initialize an array to hold expense data
    let expenses = [];

    // Function to add expense
    expenseForm.addEventListener("submit", function(event) {
      event.preventDefault();
      
      const expenseType = document.getElementById("expenseType").value;
      const amount = parseFloat(document.getElementById("amount").value);
      const expenseDate = document.getElementById("expenseDate").value;

      const expense = {
        type: expenseType,
        amount: amount,
        date: expenseDate
      };

      expenses.push(expense);
      renderExpenses();
      expenseForm.reset();
    });

    // Function to render expenses in the table
    function renderExpenses() {
      // Clear the current table
      expenseTable.innerHTML = "";

      // Loop through expenses and append rows to the table
      expenses.forEach(expense => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${expense.type}</td>
          <td>${expense.amount.toFixed(2)}</td>
          <td>${expense.date}</td>
        `;
        expenseTable.appendChild(row);
      });
    }