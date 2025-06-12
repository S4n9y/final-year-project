 async function getWeather() {
      try {
        const response = await fetch("https://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q=auto:ip&days=3");
        const data = await response.json();

        // Current Weather
        document.getElementById("location").textContent = data.location.name + ", " + data.location.region;
        document.getElementById("temp").textContent = data.current.temp_c;
        document.getElementById("humidity").textContent = data.current.humidity;
        document.getElementById("condition").textContent = data.current.condition.text;
        document.getElementById("wind").textContent = data.current.wind_kph;

        // Forecast
        const forecastContainer = document.getElementById("forecast");
        forecastContainer.innerHTML = "";

        data.forecast.forecastday.forEach(day => {
          const date = day.date;
          const condition = day.day.condition.text;
          const icon = day.day.condition.icon;
          const maxTemp = day.day.maxtemp_c;
          const minTemp = day.day.mintemp_c;

          const forecastCard = `
            <div class="col-md-3 mx-2 mb-4">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">${date}</h5>
                  <img src="${icon}" alt="${condition}" />
                  <p>${condition}</p>
                  <p>🌡️ Max: ${maxTemp} °C</p>
                  <p>🌡️ Min: ${minTemp} °C</p>
                </div>
              </div>
            </div>
          `;
          forecastContainer.innerHTML += forecastCard;
        });

      } catch (error) {
        alert("Unable to load weather data.");
        console.error(error);
      }
    }

    window.onload = getWeather;