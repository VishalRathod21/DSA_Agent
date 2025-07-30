PROBLEM_CATEGORIES = {
    'Arrays & Hashing': [
        'Two Sum',
        'Contains Duplicate',
        'Valid Anagram',
        'Group Anagrams',
        'Top K Frequent Elements'
    ],
    'Two Pointers': [
        'Valid Palindrome',
        'Two Sum II - Input Array Is Sorted',
        '3Sum',
        'Container With Most Water'
    ],
    'Sliding Window': [
        'Best Time to Buy and Sell Stock',
        'Longest Substring Without Repeating Characters',
        'Longest Repeating Character Replacement',
        'Permutation in String'
    ],
    'Stack': [
        'Valid Parentheses',
        'Min Stack',
        'Evaluate Reverse Polish Notation',
        'Generate Parentheses'
    ],
    'Binary Search': [
        'Binary Search',
        'Search a 2D Matrix',
        'Find Minimum in Rotated Sorted Array',
        'Search in Rotated Sorted Array'
    ],
    'Linked List': [
        'Reverse Linked List',
        'Merge Two Sorted Lists',
        'Linked List Cycle',
        'Merge k Sorted Lists'
    ],
    'Trees': [
        'Invert Binary Tree',
        'Maximum Depth of Binary Tree',
        'Same Tree',
        'Binary Tree Level Order Traversal'
    ],
    'Graphs': [
        'Number of Islands',
        'Clone Graph',
        'Course Schedule',
        'Pacific Atlantic Water Flow'
    ],
    'Dynamic Programming': [
        'Climbing Stairs',
        'House Robber',
        'Longest Increasing Subsequence',
        'Word Break'
    ],
    'Backtracking': [
        'Subsets',
        'Combination Sum',
        'Permutations',
        'N-Queens'
    ]
}

def get_problem_template(problem_name):
    """Return a template for the given problem name"""
    templates = {
        'Two Sum': {
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'example': 'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]',
            'constraints': [
                '2 <= nums.length <= 10^4',
                '-10^9 <= nums[i] <= 10^9',
                '-10^9 <= target <= 10^9',
                'Only one valid answer exists.'
            ]
        },
        'Reverse Linked List': {
            'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
            'example': 'Input: head = [1,2,3,4,5]\nOutput: [5,4,3,2,1]',
            'constraints': [
                'The number of nodes in the list is in the range [0, 5000]',
                '-5000 <= Node.val <= 5000'
            ]
        },
        'Default': {
            'description': 'Enter your DSA problem statement here...',
            'example': 'Example input/output will be displayed here',
            'constraints': ['Constraints will be listed here']
        }
    }
    
    return templates.get(problem_name, templates['Default'])
