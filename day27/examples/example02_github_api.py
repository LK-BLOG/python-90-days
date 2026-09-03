"""示例2：GitHub API 调用"""
import requests
import json

def get_user(username):
    """获取 GitHub 用户信息"""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers={
        "Accept": "application/vnd.github.v3+json"
    })
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"用户 {username} 不存在")
        return None
    else:
        print(f"请求失败: {response.status_code}")
        return None

def get_user_repos(username, page=1, per_page=10):
    """获取用户仓库列表"""
    url = f"https://api.github.com/users/{username}/repos"
    params = {
        "page": page,
        "per_page": per_page,
        "sort": "stars",
        "direction": "desc"
    }
    
    response = requests.get(url, params=params, headers={
        "Accept": "application/vnd.github.v3+json"
    })
    
    if response.status_code == 200:
        return response.json()
    return []

def search_repos(query, sort="stars", per_page=10):
    """搜索仓库"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "per_page": per_page
    }
    
    response = requests.get(url, params=params, headers={
        "Accept": "application/vnd.github.v3+json"
    })
    
    if response.status_code == 200:
        return response.json()
    return {}

if __name__ == "__main__":
    print("=== GitHub 用户信息 ===")
    user = get_user("octocat")
    if user:
        print(f"用户名: {user['login']}")
        print(f"名称: {user.get('name', 'N/A')}")
        print(f"公开仓库: {user['public_repos']}")
        print(f" followers: {user['followers']}")
    
    print("\n=== 热门仓库 ===")
    repos = get_user_repos("octocat", per_page=5)
    for repo in repos:
        print(f"  {repo['name']}: ⭐{repo['stargazers_count']}")
    
    print("\n=== 搜索 Python 仓库 ===")
    results = search_repos("python web framework", per_page=5)
    for repo in results.get("items", []):
        print(f"  {repo['full_name']}: ⭐{repo['stargazers_count']}")
