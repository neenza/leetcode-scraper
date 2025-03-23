# LeetCode Scraper

A Python tool to scrape problem details from LeetCode and save them in JSON format.

## Features

- Scrape LeetCode problems by slug (URL name)
- Extract problem title, description, examples, and constraints
- Extract hints, follow-ups, and solutions when available
- Save data in structured JSON format
- Get a list of available problems with filtering options

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Scrape a Specific Problem

```python
from leetcode_scraper import LeetCodeScraper

scraper = LeetCodeScraper()
problem_data = scraper.scrape_problem("two-sum")
print(problem_data)
```

### Scrape Multiple Problems

```python
scraper = LeetCodeScraper()
problem_list = scraper.scrape_problem_list(limit=5)  # Get 5 problems

for problem in problem_list:
    print(f"Scraping: {problem['title']}")
    scraper.scrape_problem(problem['slug'])
    time.sleep(2)  # Add delay between requests
```

## Output Format

The scraper saves each problem as a JSON file with the following structure:

```json
{
  "title": "Two Sum",
  "problem_id": "1",
  "frontend_id": "1",
  "difficulty": "Easy",
  "problem_slug": "two-sum",
  "topics": ["Array", "Hash Table"],
  "description": "Given an array of integers nums and an integer target...",
  "examples": [
    {
      "example_num": 1,
      "example_text": "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]"
    }
  ],
  "constraints": [
    "2 <= nums.length <= 10^4",
    "-10^9 <= nums[i] <= 10^9",
    "-10^9 <= target <= 10^9"
  ],
  "follow_ups": [
    "Follow-up: Can you come up with an algorithm that is less than O(n²) time complexity?"
  ],
  "hints": [
    "A really brute force way would be to search for all possible pairs of numbers but that would be too slow.",
    "Try to use the fact that the array is sorted and use two pointers to speed up the search."
  ],
  "code_snippets": {
    "python": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        "
  }
}
```

## Notes

- Be respectful of LeetCode's servers and avoid making too many requests in a short period
- The tool adds a delay between requests to avoid being rate-limited
