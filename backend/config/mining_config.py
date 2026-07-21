"""Mining configuration for Google Maps worker"""

# Browser settings
BROWSER_HEADLESS = False
BROWSER_PROFILE_PATH = "./browser_profile"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

# Timing settings (human-like delays)
SCROLL_DELAY_MS = (1500, 3000)  # Random between min and max
CLICK_DELAY_MS = (800, 1500)
PAGE_LOAD_TIMEOUT_MS = 30000
ELEMENT_TIMEOUT_MS = 10000

# Scrolling settings
MAX_SCROLL_ATTEMPTS_WITHOUT_NEW_RESULTS = 3
SCROLL_CHECK_DELAY_SECONDS = 2

# Progress update frequency
PROGRESS_UPDATE_EVERY_N_COMPANIES = 5
