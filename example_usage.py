from leetcode_scraper import LeetCodeScraper
import json
import time

def print_problem_details(problem_data):
    """Print formatted problem details"""
    if not problem_data:
        print("No problem data available")
        return
    
    print("="*80)
    print(f"TITLE: {problem_data.get('title')}")
    print(f"DIFFICULTY: {problem_data.get('difficulty')}")
    print("-"*80)
    print("DESCRIPTION:")
    print(problem_data.get('description', 'No description available'))
    print("-"*80)
    
    # Print examples
    print("EXAMPLES:")
    for example in problem_data.get('examples', []):
        print(f"Example {example.get('example_num')}:")
        print(example.get('example_text'))
        print()
    
    # Print constraints
    print("CONSTRAINTS:")
    for constraint in problem_data.get('constraints', []):
        print(f"- {constraint}")
    
    # Print follow-ups if available
    follow_ups = problem_data.get('follow_ups', [])
    if follow_ups:
        print("-"*80)
        print("FOLLOW-UPS:")
        for follow_up in follow_ups:
            print(f"- {follow_up}")
    
    # Print hints if available
    hints = problem_data.get('hints', [])
    if hints:
        print("-"*80)
        print("HINTS:")
        for i, hint in enumerate(hints, 1):
            print(f"Hint {i}: {hint}")
    
    print("="*80)

if __name__ == "__main__":
    scraper = LeetCodeScraper()
    
    # Example 1: Scrape a single problem
    print("Scraping 'set-matrix-zeroes' problem...")
    problem_data = scraper.scrape_problem("set-matrix-zeroes")
    print_problem_details(problem_data)
    
    # Example 2: Get a list of problems and scrape the first 3
    print("\nGetting list of problems...")
    problem_list = scraper.scrape_problem_list(limit=3)
    
    print(f"Found {len(problem_list)} problems:")
    for i, problem in enumerate(problem_list, 1):
        print(f"{i}. {problem['title']} (Difficulty: {'Easy' if problem['difficulty'] == 1 else 'Medium' if problem['difficulty'] == 2 else 'Hard'})")
    
    # Uncomment to scrape all problems in the list
    """
    print("\nScraping all problems in the list...")
    for problem in problem_list:
        print(f"Scraping {problem['title']}...")
        scraper.scrape_problem(problem['slug'])
        time.sleep(2)  # Add delay between requests
    """
