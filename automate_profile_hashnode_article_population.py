import requests


# Hashnode API endpoint
url = "https://gql.hashnode.com"

# GraphQL query
query = """
query Publication(
    $id: ObjectId="6714bcb54bcdc5c7d9980730"
  ) {
    publication(
      id: $id
    ) {
      posts(first:3) {
        edges {
          node {
            title,
            brief,
            slug,
            url
          }
        }
      }
    } 
  }
"""

response = requests.post(url, json={"query": query})
data = response.json()
posts = data['data']['publication']['posts']['edges']


md_content = ""
for idx, post in enumerate(posts, start =1):
    md_content += (f"{idx}. [{post['node']['title']}]({post['node']['url']})\n")
print(md_content)


start_marker = "<!-- BEGIN HASHNODE ARTICLES -->"
end_marker = "<!-- END HASHNODE ARTICLES -->"

with open("README.md", "r") as readme:
    content = readme.read()
print(content)

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)


if start_idx != -1 and end_idx != -1:
    print("start/end indexes found")
    # Update the content between the markers
    updated_content = (
        content[:start_idx + len(start_marker)]  # Content before the start marker
        + "\n" + md_content.strip() + "\n"      # New content
        + content[end_idx:]                      # Content after the end marker
    )
else:
    # If markers are not found, append the new section at the end
    updated_content = content + f"\n{start_marker}\n{md_content.strip()}\n{end_marker}\n"
print(updated_content)

with open("README.md", "w") as readme:
    readme.write(updated_content)
    print("README.md has been updated.")
    print(md_content)
