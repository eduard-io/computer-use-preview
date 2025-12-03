# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import os

from agent import BrowserAgent
from computers import BrowserbaseComputer, PlaywrightComputer


PLAYWRIGHT_SCREEN_SIZE = (1440, 900)
MOBILE_SCREEN_SIZE = (390, 844)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the browser agent with a query.")
    parser.add_argument(
        "query",
        type=str,
        nargs="?",
        default=None,
        help="The query for the browser agent to execute (can be a string or a file path).",
    )
    parser.add_argument(
        "--query",
        type=str,
        dest="query_flag",
        default=None,
        help="The query for the browser agent to execute (can be a string or a file path). Alternative to positional argument.",
    )

    parser.add_argument(
        "--env",
        type=str,
        choices=("playwright", "browserbase"),
        default="playwright",
        help="The computer use environment to use.",
    )
    parser.add_argument(
        "--initial_url",
        type=str,
        default="https://www.google.com",
        help="The inital URL loaded for the computer.",
    )
    parser.add_argument(
        "--highlight_mouse",
        action="store_true",
        default=False,
        help="If possible, highlight the location of the mouse.",
    )
    parser.add_argument(
        "--model",
        default='gemini-2.5-computer-use-preview-10-2025',
        help="Set which main model to use.",
    )
    parser.add_argument(
        "--save_screenshots",
        action="store_true",
        default=False,
        help="Save screenshots locally to a 'screenshots' directory.",
    )
    parser.add_argument(
        "--mobile",
        action="store_true",
        default=False,
        help="Enable mobile device emulation (mobile resolution and behavior).",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        default=False,
        help="Output only the final agent reasoning message in a clean, pipeable format.",
    )
    args = parser.parse_args()

    # Determine query source (positional or --query flag)
    query_value = args.query_flag if args.query_flag is not None else args.query

    # Ensure at least one query source is provided
    if query_value is None:
        parser.error("Query is required. Provide it as a positional argument or use --query flag.")

    # Check if query is a file path and read it, otherwise use as string
    if os.path.isfile(query_value):
        with open(query_value, "r", encoding="utf-8") as f:
            query = f.read().strip()
    else:
        query = query_value

    screen_size = MOBILE_SCREEN_SIZE if args.mobile else PLAYWRIGHT_SCREEN_SIZE
    
    if args.env == "playwright":
        env = PlaywrightComputer(
            screen_size=screen_size,
            initial_url=args.initial_url,
            highlight_mouse=args.highlight_mouse,
            mobile=args.mobile,
            print_mode=args.print,
        )
    elif args.env == "browserbase":
        env = BrowserbaseComputer(
            screen_size=screen_size,
            initial_url=args.initial_url,
            mobile=args.mobile,
            print_mode=args.print,
        )
    else:
        raise ValueError("Unknown environment: ", args.env)

    with env as browser_computer:
        agent = BrowserAgent(
            browser_computer=browser_computer,
            query=query,
            model_name=args.model,
            save_screenshots=args.save_screenshots,
            verbose=not args.print,
            print_mode=args.print,
        )
        agent.agent_loop()
        if args.print:
            print(agent.final_reasoning or "")
    return 0


if __name__ == "__main__":
    main()
