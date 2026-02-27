
QUERY_100_REPOS = """
{
  search(query: "stars:>10000 sort:stars-desc", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        pullRequests(states: MERGED) {
          totalCount
        }
        releases {
          totalCount
        }
        updatedAt
        primaryLanguage {
          name
        }
        issues {
          totalCount
        }
        closedIssues: issues(states: CLOSED) {
          totalCount
        }
      }
    }
  }
}
"""