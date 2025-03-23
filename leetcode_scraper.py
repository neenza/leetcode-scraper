import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

class LeetCodeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com/problems/'
        }
        self.base_url = 'https://leetcode.com/problems/'
        self.graphql_url = 'https://leetcode.com/graphql/'
        self.problems_dir = 'problems'
        
        # Create problems directory if it doesn't exist
        if not os.path.exists(self.problems_dir):
            os.makedirs(self.problems_dir)
    
    def scrape_problem(self, problem_slug):
        """
        Scrape a LeetCode problem by its slug using GraphQL API
        """
        print(f"Fetching problem: {problem_slug}")
        
        # GraphQL query to get problem details
        query = {
            "operationName": "questionData",
            "variables": {"titleSlug": problem_slug},
            "query": """
            query questionData($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                difficulty
                topicTags {
                  name
                }
                codeSnippets {
                  lang
                  langSlug
                  code
                }
                hints
                solution {
                  content
                }
                exampleTestcases
              }
            }
            """
        }
        
        try:
            response = requests.post(self.graphql_url, headers=self.headers, json=query)
            
            if response.status_code != 200:
                print(f"Failed to fetch problem: {problem_slug}. Status code: {response.status_code}")
                return None
            
            data = response.json()
            question = data.get('data', {}).get('question', {})
            
            if not question:
                print(f"No data found for problem: {problem_slug}")
                return None
            
            # Process the problem data
            problem_data = self._process_problem_data(question)
            
            # Save the problem data
            self._save_problem_data(problem_slug, problem_data)
            
            return problem_data
        
        except Exception as e:
            print(f"Error scraping problem {problem_slug}: {str(e)}")
            return None
    
    def _process_problem_data(self, question):
        """
        Process the GraphQL API response into a structured format
        """
        problem_data = {
            'title': question.get('title'),
            'problem_id': question.get('questionId'),
            'frontend_id': question.get('questionFrontendId'),
            'difficulty': question.get('difficulty'),
            'problem_slug': question.get('titleSlug'),
            'topics': [tag.get('name') for tag in question.get('topicTags', [])]
        }
        
        # Process content with BeautifulSoup to extract description, examples, and constraints
        content_html = question.get('content', '')
        soup = BeautifulSoup(content_html, 'html.parser')
        
        # Get description (text before the first <strong>Example</strong>)
        description = []
        current_element = soup.find()
        
        while current_element:
            if current_element.name == 'strong' and 'Example' in current_element.text:
                break
            if current_element.name == 'p':
                description.append(current_element.get_text().strip())
            current_element = current_element.next_sibling
        
        problem_data['description'] = '\n'.join([d for d in description if d])
        
        # Extract examples
        examples = []
        example_blocks = soup.find_all('pre')
        for i, example in enumerate(example_blocks, 1):
            examples.append({
                'example_num': i,
                'example_text': example.get_text().strip()
            })
        problem_data['examples'] = examples
        
        # Extract constraints
        constraints = []
        constraint_header = None
        
        for elem in soup.find_all(['p', 'strong']):
            if elem.name == 'strong' and 'Constraints' in elem.text:
                constraint_header = elem.parent
                break
        
        if constraint_header:
            constraints_list = constraint_header.find_next('ul')
            if constraints_list:
                for li in constraints_list.find_all('li'):
                    constraints.append(li.get_text().strip())
        
        problem_data['constraints'] = constraints
        
        # Extract follow-up section if it exists
        follow_ups = []
        for elem in soup.find_all(['p', 'strong']):
            if elem.name == 'strong' and 'Follow-up' in elem.text:
                follow_up_text = elem.parent.get_text().strip()
                follow_ups.append(follow_up_text)
                
                # Sometimes follow-ups are in paragraphs after the header
                next_elem = elem.parent.next_sibling
                while next_elem and next_elem.name == 'p':
                    follow_up_text = next_elem.get_text().strip()
                    if follow_up_text:
                        follow_ups.append(follow_up_text)
                    next_elem = next_elem.next_sibling
        
        problem_data['follow_ups'] = follow_ups
        
        # Extract hints from the API response
        hints = question.get('hints', [])
        problem_data['hints'] = hints
        
        # Add code snippets
        code_snippets = {}
        for snippet in question.get('codeSnippets', []):
            code_snippets[snippet.get('langSlug')] = snippet.get('code')
        
        problem_data['code_snippets'] = code_snippets
        
        # Extract solution content if available
        solution_content = question.get('solution', {}).get('content')
        if solution_content:
            solution_soup = BeautifulSoup(solution_content, 'html.parser')
            problem_data['solution'] = solution_soup.get_text(strip=True)
        
        return problem_data
    
    def _save_problem_data(self, problem_slug, problem_data):
        """
        Save the problem data to a JSON file
        """
        filename = os.path.join(self.problems_dir, f"{problem_slug}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(problem_data, f, indent=2, ensure_ascii=False)
        
        print(f"Problem data saved to {filename}")
        
    def scrape_problem_list(self, limit=10):
        """
        Scrape the list of problems from LeetCode
        """
        all_problems_url = "https://leetcode.com/api/problems/all/"
        response = requests.get(all_problems_url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch problem list. Status code: {response.status_code}")
            return []
        
        data = response.json()
        problem_list = []
        
        for problem in data.get('stat_status_pairs', [])[:limit]:
            stat = problem.get('stat', {})
            problem_info = {
                'id': stat.get('question_id'),
                'title': stat.get('question__title'),
                'slug': stat.get('question__title_slug'),
                'difficulty': problem.get('difficulty', {}).get('level')
            }
            problem_list.append(problem_info)
        
        return problem_list

if __name__ == "__main__":
    scraper = LeetCodeScraper()
    
    # Option 1: Scrape a specific problem
    # problem_data = scraper.scrape_problem("two-sum")
    # print(json.dumps(problem_data, indent=2))
    
    # Option 2: Scrape multiple problems from the list
    problem_list = scraper.scrape_problem_list(limit=5)
    
    # Add a delay between requests to avoid being blocked
    for problem in problem_list:
        print(f"Scraping problem: {problem['title']} ({problem['slug']})")
        scraper.scrape_problem(problem['slug'])
        time.sleep(2)  # Wait 2 seconds between requests
