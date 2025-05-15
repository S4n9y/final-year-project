 function predictYield() {
      const crop = document.getElementById('crop').value;
      let area = parseFloat(document.getElementById('area').value);
const unit = document.getElementById('unit').value;

// Convert to hectares if unit is in acres
if (unit === 'acre') {
  area *= 0.4047;
}

      const region = document.getElementById('region').value;
      const resultDiv = document.getElementById('result');

      if (!area || !region) {
        resultDiv.textContent = "Please fill all fields correctly.";
        return;
      }

      const baseYieldPerHectare = {
        wheat: 3.2,
        rice: 4.5,
        maize: 2.8,
        soybean: 2.1,
        cotton: 1.5,
        sugarcane: 75.0,
        turmeric: 6.5,
        sorghum: 2.0,
        chickpeas: 1.8,
        corn: 3.0,
        banana: 30.0
      };

      const predictedYield = (baseYieldPerHectare[crop] * area).toFixed(2);

      resultDiv.textContent = `Estimated Yield for ${document.getElementById("crop").selectedOptions[0].text}: ${predictedYield} tonnes`;
    }