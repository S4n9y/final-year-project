async function fetchPrices() {
      const tableBody = document.getElementById("market-data");
      tableBody.innerHTML = `<tr><td colspan="5">Fetching latest prices...</td></tr>`;

      try {
        // Example static data (replace with live API later)
        const data = [
          { crop: "Wheat", market: "Pune", min: 1900, max: 2100, modal: 2000 },
          { crop: "Rice", market: "Nagpur", min: 1800, max: 2050, modal: 1950 },
          { crop: "Soybean", market: "Nashik", min: 3400, max: 3600, modal: 3500 },
          { crop: "Maize", market: "Aurangabad", min: 1600, max: 1800, modal: 1700 }
        ];

        tableBody.innerHTML = data.map(item => `
          <tr>
            <td>${item.crop}</td>
            <td>${item.market}</td>
            <td>${item.min}</td>
            <td>${item.max}</td>
            <td>${item.modal}</td>
          </tr>
        `).join('');
      } catch (error) {
        tableBody.innerHTML = `<tr><td colspan="5">Failed to load data. Try again later.</td></tr>`;
        console.error(error);
      }
    }

    // Load prices on page load
    window.onload = fetchPrices;