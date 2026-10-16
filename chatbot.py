
def get_chatbot_response(message):
    message = message.lower()

    if "registration fee" in message or "pay money" in message:
        return (
            "Be careful! Unexpected recruitment fees can be a warning sign. "
            "Verify the company through its official website."
        )

    elif "fake job" in message or "job scam" in message:
        return (
            "Warning signs include payment requests, unrealistic salary "
            "promises, and pressure to act quickly. Verify the employer."
        )

    elif "verify company" in message or "real company" in message:
        return (
            "Visit the company's official website, check its careers page, "
            "and contact the company using verified contact details."
        )

    elif "internship" in message:
        return (
            "Check the internship description, company details, selection "
            "process, and offer letter. Be cautious of requests for money."
        )

    elif "hello" in message or "hi" in message:
        return (
            "Hello! Welcome to FakeJobDetector Chatbot. "
            "Ask me about fake jobs, internships, or company verification."
        )

    else:
        return (
            "I can help with fake job warning signs, registration fees, "
            "internships, and company verification. Please ask about one "
            "of these topics."
        )
