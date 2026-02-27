QUERY_100_REPOS = """
query {
  search(
    query: "stars:>10000 sort:stars-desc",
    type: REPOSITORY,
    first: 100
  ) {
    nodes {
      ... on Repository {
        nameWithOwner
      }
    }
  }
}
"""