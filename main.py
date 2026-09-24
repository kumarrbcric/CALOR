import flet as ft
import requests

def fetch_weather_data(lat=10.7867, lon=79.1378):
    """
    Fetches real-time weather & heat metrics from Open-Meteo API.
    Default coordinates set to Thanjavur / SASTRA campus region.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature&timezone=auto"
    )
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json().get("current", {})
            return {
                "temp": data.get("temperature_2m", "N/A"),
                "humidity": data.get("relative_humidity_2m", "N/A"),
                "apparent_temp": data.get("apparent_temperature", "N/A"),
            }
    except Exception as e:
        print(f"Error fetching weather: {e}")
    
    return {"temp": "N/A", "humidity": "N/A", "apparent_temp": "N/A"}

def main(page: ft.Page):
    page.title = "CalorPulse - Heat Risk Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI Elements
    title_text = ft.Text("CalorPulse", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_400)
    subtitle_text = ft.Text("Real-Time Heat Risk & Weather Alert", size=14, color=ft.colors.GREY_400)
    
    temp_card = ft.Text("Temperature: -- °C", size=20, weight=ft.FontWeight.W_500)
    apparent_temp_card = ft.Text("Feels Like: -- °C", size=20, weight=ft.FontWeight.W_500, color=ft.colors.RED_300)
    humidity_card = ft.Text("Humidity: -- %", size=18, color=ft.colors.BLUE_200)

    status_indicator = ft.Text("Status: Initializing...", size=16, color=ft.colors.AMBER_300)

    def refresh_weather(e=None):
        status_indicator.value = "Status: Fetching live weather data..."
        page.update()

        weather = fetch_weather_data()
        
        temp_card.value = f"Temperature: {weather['temp']} °C"
        apparent_temp_card.value = f"Feels Like: {weather['apparent_temp']} °C"
        humidity_card.value = f"Humidity: {weather['humidity']} %"
        
        # Simple heat risk assessment based on apparent temperature
        if isinstance(weather['apparent_temp'], (int, float)):
            if weather['apparent_temp'] > 40:
                status_indicator.value = "Alert: Extreme Heat Risk!"
                status_indicator.color = ft.colors.RED_500
            elif weather['apparent_temp'] > 35:
                status_indicator.value = "Warning: High Heat Risk"
                status_indicator.color = ft.colors.ORANGE_400
            else:
                status_indicator.value = "Status: Normal Conditions"
                status_indicator.color = ft.colors.GREEN_400
        else:
            status_indicator.value = "Status: Data Updated"
            status_indicator.color = ft.colors.BLUE_300
            
        page.update()

    refresh_button = ft.ElevatedButton(
        text="Refresh Weather",
        icon=ft.icons.REFRESH,
        on_click=refresh_weather,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.ORANGE_800)
    )

    # Layout Container
    page.add(
        ft.Column(
            controls=[
                title_text,
                subtitle_text,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            temp_card,
                            apparent_temp_card,
                            humidity_card,
                            ft.Divider(height=10, color=ft.colors.GREY_700),
                            status_indicator,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                    border_radius=12,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    alignment=ft.alignment.center,
                ),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                refresh_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    )

    # Fetch initial weather data on load
    refresh_weather()

if __name__ == "__main__":
    # Calling flet.app directly avoids the 'module flet has no attribute app' issue on mobile
    ft.app(target=main)
