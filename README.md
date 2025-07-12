# Coghedrin

A custom Red-DiscordBot cog with fun commands, API integrations, and event listeners.

## Features
- Fun commands: ping, roll, dice, rock-paper-scissors, weather, timeofday, when, measure, secret, roulette, slots, coinflip, decide, balding
- API call example and event listener
- Uses environment variables for secrets
- Modular and maintainable code
- Command cooldowns for anti-spam
- Unit tests for utility functions

## Getting Started

### Prerequisites
- Python 3.8+
- Red-DiscordBot (https://docs.discord.red/en/stable/)
- `discord.py` and `requests` libraries

### Installation
1. Clone this repo or copy the `coghedrin` folder to your RedBot cogs directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your `.env` file with any required secrets (see below)
4. Load the cog in RedBot:
   ```
   [p]load coghedrin
   ```

### Environment Variables
- `SAMPLE_API` - URL for the sample API call
- `WEATHER_API` - URL for weather data
- `DAYNIGHT_API` - URL for day/night data

## Usage Examples
- `[p]pinghedrin` - Pong!
- `[p]roll` - Roll 1-100
- `[p]dice` - Roll 1-6
- `[p]rps @user` - Rock-paper-scissors
- `[p]apicall` - Call the sample API
- `[p]weather` - Get current weather
- `[p]timeofday` - Get current time of day
- `[p]when day` - Time until day
- `[p]measure` - Random measurement
- `[p]secret` - Secret DM
- `[p]roulette` - Russian roulette
- `[p]slots` - Slot machine
- `[p]coinflip even` - Coin flip
- `[p]decide` - Yes/no
- `[p]balding` - Balding percent

## Testing
- Run unit tests with pytest:
  ```bash
  pytest test/
  ```

## Troubleshooting
- Ensure all required environment variables are set in `.env`
- Check bot permissions and privacy settings for DM commands
- Use `[p]help` for command usage

## Security
- Never commit your `.env` or secrets
- All user input is validated
- Command cooldowns prevent spam

## Contributing
See `CONTRIBUTING.md` for guidelines.

## License
MIT
