def detect_intent(command):

    command = command.lower()

    # -----------------------------------
    # OPEN COMMANDS
    # -----------------------------------

    open_words = ["open", "launch", "start", "run"]

    for word in open_words:

        if command.startswith(word):

            return "open"

    # -----------------------------------
    # SYSTEM COMMANDS
    # -----------------------------------

    if "battery" in command:

        return "battery"

    elif "shutdown" in command:

        return "shutdown"

    elif "restart" in command:

        return "restart"

    elif "lock" in command:

        return "lock"

    elif "time" in command:

        return "time"
    
    elif "search google for" in command:

        return "google_search"

    elif "search youtube for" in command:

        return "youtube_search"

    elif "exit" in command:

        return "exit"

    # -----------------------------------
    # DEFAULT AI
    # -----------------------------------

    return "ai"