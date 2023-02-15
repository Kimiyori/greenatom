LAUNCH_QUERY = """
query Query {
  launches {
    id
    details
    mission_id
    mission_name
    rocket {
      rocket {
        id
        description
        name
      }
    }
  }
}
  """
