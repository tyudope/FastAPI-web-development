# Project Description

----

We're building a 'Notes' API where users can

Create Notes


Read Notes
- Filter by tag
- Filter by minimum length
- Sort by creation date


Update Notes
- Partial updates or full updates


Delete Notes
- Return deleted note




and Include followings

1. Shared dependency -> simulated DB Object
2. parameter-level dependency -> a small limit: int = Depends(get_limit)
3. function-level dependency -> Depends(get_current_user)
